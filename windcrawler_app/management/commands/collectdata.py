from django.core.management.base import BaseCommand, CommandError
import urllib.request, urllib.parse, urllib.error, json, ssl, datetime, time
from windcrawler_app.models import HistoricalData, Wooi

class Command(BaseCommand):
    help = 'Collects wind info from buienradar api and stores it in the db'
    
    def add_arguments(self, parser):
        parser.add_argument('spot', nargs='+', type=str)

    def handle(self, *args, **options):
        for spot in options['spot']:
            try:
                s = Wooi.objects.get(title=spot)
            except Wooi.DoesNotExist:
                raise CommandError('Spot "%s" does not exist' % spot)  
            try:
                url = "https://data.buienradar.nl/2.0/feed/json"
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                attempt = None    
                uh = urllib.request.urlopen(url, context=ctx)
                data = uh.read().decode()
                js = json.loads(data)
                for key in js['actual']['stationmeasurements']:
                        if key['regio'] == spot:
                            windsnelheid = float(round((key['windspeed']*1.943845), 1))
                            windstoten = float(round((key['windgusts']*1.943845), 1))
                            tijd = str(key['timestamp'])
                            try: # check if this datapoint has already been saved
                                d = HistoricalData.objects.get(spot=s, timestamp=tijd)
                                self.stdout.write(self.style.SUCCESS('avoiding double data...skipping'))
                            except: # if not, save it now
                                b = HistoricalData(spot=s, timestamp=tijd, gust=windstoten, wind=windsnelheid)
                                b.save()
                                self.stdout.write(self.style.SUCCESS('another run done'))
            except Exception as e:
                self.stdout.write(e)




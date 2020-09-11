import urllib.request, urllib.parse, urllib.error, json, ssl, datetime, time
from windcrawler_app.models import HistoricalData, Wooi

class CollectData():
    def collect_data(self, spot):
        self.spot = spot
        try:
            s = Wooi.objects.get(title=spot)
        except Wooi.DoesNotExist:
            print("spot does not exist in database")
            return
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
                            print("avoiding double data...skipping")
                            return "avoiding double data...skipping"
                        except: # if not, save it now
                            b = HistoricalData(spot=s, timestamp=tijd, gust=windstoten, wind=windsnelheid)
                            b.save()
                            print(f"data of {spot} saved")
                            return "another run done"
        except Exception as e:
            return e
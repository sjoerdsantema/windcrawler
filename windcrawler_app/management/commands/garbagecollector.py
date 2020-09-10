from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import now, localtime
from datetime import timedelta
from windcrawler_app.models import HistoricalData

class Command(BaseCommand):
    help = 'Deletes yesterdays data in order to slim down the db'
    
    def handle(self, *args, **options):
        try:
            s = HistoricalData.objects.filter()
            day_of_month_now = localtime().replace(hour=0, minute=0, second=0, microsecond=0).strftime("%d")
            for i in s:         
                delta_days = int(day_of_month_now) - int(i.created.strftime("%d"))
                if delta_days > 0:
                    HistoricalData.objects.filter(created=i.created).delete()
                    print("delete 1 row of old data")
            self.stdout.write('done')      
                
        except HistoricalData.DoesNotExist:
            self.stdout.write('nothing to delete here!')

  
        


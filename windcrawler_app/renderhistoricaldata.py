import urllib.request, urllib.parse, urllib.error, json, ssl, datetime, time
from .models import HistoricalData, Wooi

class RenderHistoricalData:
    def get_historical_data_db(self, spot):
        self.spot = spot
        try: 
            s = Wooi.objects.get(title=spot)
            try: 
                historical_data_of_spot = HistoricalData.objects.order_by('created').reverse().all().filter(spot=s)[:10]
                historical_data_wind = [ wind.wind for wind in historical_data_of_spot ]
                historical_data_gust = [ wind.gust for wind in historical_data_of_spot ]
                historical_data_timestamp = [ wind.timestamp[-8:-3] for wind in historical_data_of_spot ]
                historical_data_timestamp.reverse()
                historical_data_gust.reverse()
                historical_data_wind.reverse()
                return(historical_data_timestamp, historical_data_wind, historical_data_gust)
            except:
                return("no known data for this spot")
        except:
            return("spot is unknown")
        
        
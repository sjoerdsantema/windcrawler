from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse 
from .renderdata import Renderdata
from .renderhistoricaldata import RenderHistoricalData
from .models import Wooi, Sources, HistoricalData
from .get_api_key import GetApiKey

HOME_PAGE_MSG = getattr(settings, "HOME_PAGE_MSG", "Missing Message")

def home(request):
    spotdatalist = []
    wind_historical = RenderHistoricalData()
    renderdata = Renderdata()
    # collect the spots from the db where the prefered api matches
    locaties = Wooi.objects.filter(active=True)
    count = 0
    for locatie in locaties:
        api = str(locatie.source_api)
        handle = str(locatie.handle)
        try: # get historical datapoints from database
            historical_data_this_spot = (wind_historical.get_historical_data_db(locatie))
        except: # pass if a spot has no historical data in db
            historical_data_this_spot = "none"
        spotdatalist.append(renderdata.render(locatie, api, handle))
        spotdatalist[count]['Bron API'] = api
        spotdatalist[count]['Spot legaal'] = locatie.legal
        if locatie.nav_link:
            spotdatalist[count]['Google Maps'] = locatie.nav_link
        if locatie.historical_available:
            spotdatalist[count]['Windhistorie'] = True
        spotdatalist[count]['data'] = historical_data_this_spot
        count += 1
        
    # this shows you what settings we are on
    print(HOME_PAGE_MSG)
    # get the weatherreport from buienradar api
    weatherreport = []
    weatherreport.append(renderdata.get_weather_report("Buienradar"))
    
    return render(request, 'windcrawler_app/home.html', {"spotdatalist": spotdatalist, "weatherreport": weatherreport})

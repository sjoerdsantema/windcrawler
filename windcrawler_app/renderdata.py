import urllib.request, urllib.parse, urllib.error, json, ssl, datetime, time
from .get_api_key import GetApiKey
from .convert_data import Convertdata

class Renderdata:
    # this function collects the buienradar weather report
    def get_weather_report(self, api):
        self.api = api
        if self.api == "Buienradar":
            service_url = "https://data.buienradar.nl/2.0/feed/json"
            url = service_url
            # ignore SSL certificate errors
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            attempt = None
            try:
                uh = urllib.request.urlopen(url, context=ctx)
                data = uh.read().decode()
                js = json.loads(data)
                title = js['forecast']['weatherreport']['title'] 
                message = js['forecast']['weatherreport']['text'] 
                summary = js['forecast']['weatherreport']['summary'] 
                weatherreport = {}
                weatherreport['text'] = message
                weatherreport['title'] = title
                weatherreport['summary'] = summary
                weatherreport['source'] = api
                return weatherreport
            except:
                weatherreport = {}
                weatherreport['summary'] = "Vooruitzicht niet beschikbaar"
                return weatherreport

    # collect the data from different api's
    def render(self, spot, api, handle):
        self.api = api
        self.handle = handle
        key_object = GetApiKey()
        api_key = key_object.get_api_key(api)
        if self.api == "Meteoserver":
            self.spot = spot
            api_key = str(key_object.get_api_key("Meteoserver"))
            service_url = "https://data.meteoserver.nl/api/liveweer_synop.php?"
            parms = dict()
            parms['locatie'] = spot
            parms['key'] = api_key
            url = service_url + urllib.parse.urlencode(parms)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            attempt = None
            try:
                uh = urllib.request.urlopen(url, context=ctx)
                data = uh.read().decode()
                js = json.loads(data)

                # assign vars with data from json
                windstoten = float(js['liveweer'][0]['windstootknp'])
                windsnelheid = float(js['liveweer'][0]['windknp'])
                windrichting = js['liveweer'][0]['windr']
                windrichtinggr = js['liveweer'][0]['windrgr']
                luchttemp = js['liveweer'][0]['luchttemp']
                zononder = js['liveweer'][0]['sunder']
                zonop = js['liveweer'][0]['sup']
                bericht = js['liveweer'][0]['lkop']
                tijd = js['liveweer'][0]['time']
                verschil = round(windstoten-windsnelheid, 1)

                # create a new dictionary
                spotdata = {}
                spotdata['Locatie'] = spot
                spotdata['Handle'] = handle
                spotdata['Windrichting'] = str(windrichting+"("+windrichtinggr+"°)")
                spotdata['Windsnelheid'] = windsnelheid  
                spotdata['Windstoten'] = windstoten
                spotdata['Verschil'] = verschil
                spotdata['Temperatuur'] = luchttemp
                spotdata['Bericht'] = bericht
                spotdata['Zonsopkomst'] = zonop
                spotdata['Zonsondergang'] = zononder
                spotdata['Gemeten op'] = tijd
                return spotdata
            except:
                spotdata = {}
                spotdata['Locatie'] = spot
                spotdata['Windrichting'] = "api broken"
                spotdata['Windsnelheid'] = 0
                spotdata['Windstoten'] = 0
                return spotdata
            else:
                print("source unknown")
                return "Source is unknown"
        if self.api == "OpenWeather":
            self.spot = spot
            self.handle = handle
            api_key = str(key_object.get_api_key("OpenWeather"))
            service_url = "https://api.openweathermap.org/data/2.5/weather?"
            parms = dict()
            parms['q'] = spot
            parms['lang'] = 29
            parms['units'] = "metric"
            parms['appid'] = api_key
            url = service_url + urllib.parse.urlencode(parms)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            attempt = None
            try:
                uh = urllib.request.urlopen(url, context=ctx)
                data = uh.read().decode()
                js = json.loads(data)
                
                # assign vars with data from json
                windrichting = js['wind']['deg']
                windsnelheid = round((js['wind']['speed']*1.94385),1 )

                # openweather sometimes leaves gust info out
                if 'gust' in js['wind']:
                    windstoten = round((js['wind']['gust']*1.94385),1 )
                    verschil = round(windstoten-windsnelheid, 1)
                else: 
                    windstoten = windsnelheid
                    verschil = 0
                temperatuur = round(js['main']['temp'], 1)
                bericht = js['weather'][0]['description']
                zonsopkomst = datetime.datetime.fromtimestamp((js['sys']['sunrise'])+7200).strftime('%H:%M:%S')
                zonsondergang = datetime.datetime.fromtimestamp((js['sys']['sunset'])+7200).strftime('%H:%M:%S')
                tijd = (js['dt'])+7200
                tijd_nu = time.time()
                tijd = datetime.datetime.fromtimestamp((tijd_nu+7200)-tijd).strftime('%M')
              
                # create a new dictionary
                spotdata = {}
                spotdata['Locatie'] = spot
                spotdata['Handle'] = handle
                spotdata['Windsnelheid'] = windsnelheid
                if "gust" in js['wind']:
                    spotdata['Windstoten'] = windstoten
                    spotdata['Verschil'] = verschil
                else:
                    spotdata['Windstoten'] = windsnelheid
                    spotdata['Verschil'] = "n.a."
                spotdata['Windrichting in graden'] = windrichting

                # degrees to cardinal
                winddata = Convertdata()
                spotdata['Windrichting'] = winddata.degrees_to_cardinal(windrichting)
                #dirs = ['N', 'NNO', 'NO', 'ONO', 'O', 'OZO', 'ZO', 'ZZO', 'Z', 'ZZW', 'ZW', 'WZW', 'W', 'WNW', 'NW', 'NNW']
                #ix = round(windrichting / (360. / len(dirs)))
                #spotdata['Windrichting'] = dirs[ix % len(dirs)]


                spotdata['Temperatuur(c)'] = temperatuur
                spotdata['Bericht'] = bericht
                spotdata['Zonsopkomst'] = zonsopkomst
                spotdata['Zonsondergang'] = zonsondergang
                spotdata['Minuten sinds laatste meting'] = tijd
                return spotdata
            except:
                spotdata = {}
                spotdata['Locatie'] = spot
                spotdata['Windrichting'] = "api broken"
                spotdata['Windsnelheid'] = 0
                spotdata['Windstoten'] = 0
                return spotdata

        if self.api == "Buienradar":
            self.spot = spot
            self.handle = handle
            service_url = "https://data.buienradar.nl/2.0/feed/json"
            url = service_url
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            attempt = None
            try:
                uh = urllib.request.urlopen(url, context=ctx)
                data = uh.read().decode()
                js = json.loads(data)

                # assign vars with data from json
                for key in js['actual']['stationmeasurements']:
                    if key['regio'] == str(spot):
                        # these values are always in the json
                        windrichting = key['winddirection']
                        windsnelheid = round((key['windspeed']*1.943845), 1)
                        windsnelheidbft = key['windspeedBft']
                        meetstation = key['stationname']
                        windstoten = round((key['windgusts']*1.943845), 1)
                        verschil = windstoten-windsnelheid
                        bericht = key['weatherdescription']
                        tijd = key['timestamp']
                        windrichtinggr = key['winddirectiondegrees']
                        # these values sometimes miss in the json
                        if 'temperature' in key:
                            temperatuur = key['temperature']
                        else:
                            temperatuur = "n.a."
                        if 'precipitation' in key:
                            mm_neerslag = key['precipitation']
                        else: 
                            mm_neerslag = "n.a."
                if js['actual']['sunrise']:
                    zonsopkomst = js['actual']['sunrise']
                else: 
                    zonsopkomst = tijd
                if js['actual']['sunset']:
                    zonsondergang = js['actual']['sunset']
                else:
                    zonsondergang = tijd 
                # create a new dictionary
                spotdata = {}
                spotdata['Locatie'] = spot
                spotdata['Handle'] = handle
                spotdata['Windsnelheid'] = windsnelheid
                spotdata['Windstoten'] = windstoten
                spotdata['Verschil'] = round(verschil, 1)
                spotdata['Windrichting'] = windrichting
                spotdata['Windrichting in graden'] = windrichtinggr
                spotdata['Windsnelheid(bft)'] = windsnelheidbft
                spotdata['Temperatuur(c)'] = temperatuur
                spotdata['Neerslag(mm)'] = mm_neerslag
                spotdata['Bericht'] = bericht
                spotdata['Zonsopkomst'] = zonsopkomst[-8:-3]
                spotdata['Zonsondergang'] = zonsondergang[-8:-3]
                spotdata['Laatste meting'] = tijd[-8:-3]
                spotdata['Meetstation'] = meetstation
                return spotdata
            except Exception as e:
                spotdata = {}
                spotdata['Locatie'] = spot
                spotdata['Windrichting'] = "api broken"
                spotdata['Windsnelheid'] = 0
                spotdata['Windstoten'] = 0
                spotdata['Bericht'] = e
                return spotdata
        if self.api == "Weerlive":
            self.spot = spot
            self.handle = handle
            api_key = str(key_object.get_api_key("Weerlive"))
            service_url = "http://weerlive.nl/api/json-data-10min.php?"
            parms = dict()
            parms['locatie'] = spot
            parms['key'] = api_key
            url = service_url + urllib.parse.urlencode(parms)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            attempt = None
            try:
                uh = urllib.request.urlopen(url, context=ctx)
                data = uh.read().decode()
                js = json.loads(data)

                # assign vars with data from json
                windstoten = float(js['liveweer'][0]['windk'])
                windsnelheid = float(js['liveweer'][0]['windk'])
                windrichting = js['liveweer'][0]['windr']
                luchttemp = js['liveweer'][0]['temp']
                zononder = js['liveweer'][0]['sunder']
                zonop = js['liveweer'][0]['sup']
                bericht = js['liveweer'][0]['samenv']
                verschil = round(windstoten-windsnelheid, 1)

                # create a new dictionary
                spotdata = {}
                spotdata['Locatie'] = spot
                spotdata['Handle'] = handle
                spotdata['Windrichting'] = windrichting
                spotdata['Windsnelheid'] = windsnelheid  
                spotdata['Windstoten'] = windstoten
                spotdata['Temperatuur'] = luchttemp
                spotdata['Bericht'] = bericht
                spotdata['Zonsopkomst'] = zonop
                spotdata['Zonsondergang'] = zononder
                return spotdata
            except:
                spotdata = {}
                spotdata['Locatie'] = spot
                spotdata['Windrichting'] = "api broken"
                spotdata['Windsnelheid'] = 0
                spotdata['Windstoten'] = 0
                return spotdata
            else:
                print("source unknown")
                return "Source is unknown"
from .models import Sources

class GetApiKey:
    def get_api_key(self, source):
        self.source = source
        try:
            key = Sources.objects.get(title=source)
            api_key = key.api_key
        except:
            api_key = "no key provided"
        return(api_key)
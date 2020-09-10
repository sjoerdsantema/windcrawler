gcloud run deploy windcrawler \
--image eu.gcr.io/infinite-aura-289015/windcrawler \
--platform managed \
--region europe-west4 \
--allow-unauthenticated \
--project infinite-aura-289015 \
--service-account windcrawler@infinite-aura-289015.iam.gserviceaccount.com
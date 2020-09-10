# host -> eu.gcr.io/infinite-aura-289015/windcrawler

# without tags
docker build -t windcrawler -f Dockerfile .
docker tag windcrawler eu.gcr.io/infinite-aura-289015/windcrawler
docker push eu.gcr.io/infinite-aura-289015/windcrawler

# with tags
# docker build -t windcrawler:tagwhateveryouwant -f Dockerfile .
# docker tag windcrawler:tagwhateveryouwant eu.gcr.io/infinite-aura-289015/windcrawler
# docker push eu.gcr.io/infinite-aura-289015/windcrawler:tagwhateveryouwant

# make sure ES is up and running
import requests
res = requests.get('https://search-search-5rzyrxhwoovdpwy3jydnaj5w5u.us-east-1.es.amazonaws.com')
print(res.content)
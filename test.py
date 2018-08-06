import datetime
import requests
Index_old = 'healthevents-' + f"{datetime.datetime.now()- datetime.timedelta(days=4):%Y-%m-%d}"
print(Index_old)
res = requests.delete('https://search-healthevents-6cwtbsen4lxay46w4ed4ugwevu.eu-central-1.es.amazonaws.com/healthevents-2018-08-02')
print(res.status_code)
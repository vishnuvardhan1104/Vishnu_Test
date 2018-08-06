import boto3
import pprint
import datetime
import requests
from elasticsearch import Elasticsearch, RequestsHttpConnection


event = []


health = boto3.client('health', endpoint_url='https://health.us-east-1.amazonaws.com',  region_name='us-east-1')

health_events = health.describe_events(filter={'eventStatusCodes':['open','upcoming']})

for events in health_events['events']:
    event_arn = events['arn']
    affected_entities = health.describe_affected_entities(filter={'eventArns': [event_arn]})
    for affected_entitiyvalues in affected_entities['entities']:
        event_details = health.describe_event_details(eventArns=[event_arn])
#        event = (f"event_arn: {affected_entitiyvalues['eventArn']}",
#                      f"Effected resources: {affected_entitiyvalues['entityValue']}",
#                      f"aws_accountid: {affected_entitiyvalues['awsAccountId']}",
#                      f"aws_service: {event_details['successfulSet'][0]['event']['service']}",
#                      f"event_type: {event_details['successfulSet'][0]['event']['eventTypeCode']}",
#                      f"aws_region: {event_details['successfulSet'][0]['event']['region']}",
#                      f"start_time: {event_details['successfulSet'][0]['event']['startTime']}"
#                      f"Description: {event_details['successfulSet'][0]['eventDescription']['latestDescription']}"
#                      )
#        pprint.pprint(event)


        host = 'search-healthevents-6cwtbsen4lxay46w4ed4ugwevu.eu-central-1.es.amazonaws.com'

        es = Elasticsearch(
            hosts=[{'host': host, 'port': 443}],
#           http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )

        doc = {
                'event_arn': affected_entitiyvalues['eventArn'],
                'Effected resources': affected_entitiyvalues['entityValue'],
                'aws_accountid': affected_entitiyvalues['awsAccountId'],
                'aws_service': event_details['successfulSet'][0]['event']['service'],
                'event_type': event_details['successfulSet'][0]['event']['eventTypeCode'],
                'aws_region': event_details['successfulSet'][0]['event']['region'],
                'start_time': event_details['successfulSet'][0]['event']['startTime'],
                'Description': event_details['successfulSet'][0]['eventDescription']['latestDescription'],
                'timestamp': datetime.datetime.now(),
        }

        Index = 'healthevents-' + f"{datetime.datetime.now():%Y-%m-%d}"
#        print(es.indices.create(index=Index, ignore=400))

        res = es.index(index=Index, doc_type='healthevents', body=doc)
#        print(res['result'])

Index_old = 'healthevents-' + f"{datetime.datetime.now()- datetime.timedelta(days=4):%Y-%m-%d}"
#print(Index_old)
requests.delete('https://search-healthevents-6cwtbsen4lxay46w4ed4ugwevu.eu-central-1.es.amazonaws.com/Index_old')

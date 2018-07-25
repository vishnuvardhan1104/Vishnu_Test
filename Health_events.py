import boto3
import pprint

event = []


health = boto3.client('health', endpoint_url='https://health.us-east-1.amazonaws.com',  region_name='us-east-1')

health_events = health.describe_events(filter={'eventStatusCodes':['open','upcoming']})

for events in health_events['events']:
    event_arn = events['arn']
    affected_entities = health.describe_affected_entities(filter={'eventArns': [event_arn]})
    for affected_entitiyvalues in affected_entities['entities']:
        event_details = health.describe_event_details(eventArns=[event_arn])
        event.append((f"event_arn: {affected_entitiyvalues['eventArn']}",
                      f"Effected resources: {affected_entitiyvalues['entityValue']}",
                      f"aws_accountid: {affected_entitiyvalues['awsAccountId']}",
                      f"aws_service: {event_details['successfulSet'][0]['event']['service']}",
                      f"event_type: {event_details['successfulSet'][0]['event']['eventTypeCode']}",
                      f"aws_region: {event_details['successfulSet'][0]['event']['region']}",
                      f"start_time: {event_details['successfulSet'][0]['event']['startTime']}"))

pprint.pprint(event)


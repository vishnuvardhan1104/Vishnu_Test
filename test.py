import boto3
import pprint

health = boto3.client('health', endpoint_url='https://health.us-east-1.amazonaws.com', region_name='us-east-1')

event = []

affected_entities = health.describe_affected_entities(filter={'eventArns': [
    'arn:aws:health:global::event/IAM/AWS_IAM_OPERATIONAL_NOTIFICATION/AWS_IAM_OPERATIONAL_NOTIFICATION_ff3dd24d-f5fe-4838-bf74-4b0307aeed0e']})
for affected_entitiyvalues in affected_entities['entities']:


    event_details = health.describe_event_details(eventArns=['arn:aws:health:global::event/IAM/AWS_IAM_OPERATIONAL_NOTIFICATION/AWS_IAM_OPERATIONAL_NOTIFICATION_ff3dd24d-f5fe-4838-bf74-4b0307aeed0e'])
    event.append((f"event_arn: {affected_entitiyvalues['eventArn']}",f"Effected resources: {affected_entitiyvalues['entityValue']}",f"aws_accountid: {affected_entitiyvalues['awsAccountId']}", f"aws_service: {event_details['successfulSet'][0]['event']['service']}", f"event_type: {event_details['successfulSet'][0]['event']['eventTypeCode']}", f"aws_region: {event_details['successfulSet'][0]['event']['region']}",
                          f"start_time: {event_details['successfulSet'][0]['event']['startTime']}"))

pprint.pprint(event)




## Script to check if a private EC2 instance allows inbound SSH traffic via port 22 with no IP restrictions (0.0.0.0/0 or ::/0)
## and then print those instances with thier security groups.

# result = True
# failReason = ""
# offenders = []
# control = "7.1"
# description = "Ensure no security groups allow ingress from 0.0.0.0/0 to port 22"
# scored = True

import boto3
import pprint

ec2 = boto3.client('ec2')
resp = ec2.describe_instances()

group_instances = {}
BAD_CIDRS = ["0.0.0.0/0", "::/0"]
BAD_PORTS = [22]
IpProtocol = ['-1', 'tcp']



offenders = []


for reservation in resp['Reservations']:
    for instance in reservation['Instances']:
        if 'PublicIpAddress' in instance:
            for security_group in instance['SecurityGroups']:
                group_id = security_group['GroupId']
                if group_id not in group_instances:
                    group_instances[group_id] = []
                group_instances[group_id].append(instance['InstanceId'])

sg_resp = ec2.describe_security_groups(GroupIds=list(group_instances))


for security_group in sg_resp['SecurityGroups']:
    group_name = security_group['GroupName']
    group_id = security_group['GroupId']
    for ip_permission in security_group['IpPermissions']:
        for ip_range in ip_permission['IpRanges']:
            cidr_ip = ip_range['CidrIp']
            if 'FromPort' in ip_permission and ip_permission['FromPort'] in BAD_PORTS and ip_range['CidrIp'] in BAD_CIDRS:
                offenders.append((group_id, group_name))
                print("Below Security Groups allows inbound SSH traffic via port 22 with no IP restrictions on  EC2:")
                pprint.pprint(offenders)
            elif 'FromPort' in ip_permission and 'ToPort' in ip_permission and ip_permission['IpProtocol'] in "tcp" and 22 in range(ip_permission['FromPort'], ip_permission['ToPort']+1)  and ip_range['CidrIp'] in BAD_CIDRS:
                 offenders.append((group_id, group_name))
                 print("Below Security Groups allows inbound TCP Traffic (includes SSH traffic via port 22) with no IP restrictions on  EC2:")
                 pprint.pprint(offenders)
            elif ip_permission['IpProtocol'] in "-1" and ip_range['CidrIp'] in BAD_CIDRS:
                 offenders.append((group_id, group_name))
                 print("Below Security Groups allows inbound All Traffic (includes SSH traffic via port 22) with no IP restrictions on  EC2:")
            pprint.pprint(offenders)

#pprint.pprint(offenders)
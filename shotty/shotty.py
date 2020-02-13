import	boto3
import click
from prettytable import PrettyTable

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')
t = PrettyTable(['id', 'Instance type', 'AvailabilityZone', 'state','public_dns_name'])

def list_instances():
	for i in ec2.instances.all():
		t.add_row([
		i.id,
		i.instance_type,
		i.placement['AvailabilityZone'],
		i.state['Name'],
		i.public_dns_name])
	print(t)	



if __name__ == '__main__':
	list_instances()

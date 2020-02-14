from prettytable import PrettyTable
import boto3
import click


session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')
t = PrettyTable(['id', 'Instance type', 'AvailabilityZone',
                 'state', 'public_dns_name', 'project tag'])


def get_instances(project):
    instances = []
    if project:
        filters = [{'Name': 'tag:Project', 'Values': [project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()

    return instances


@click.group()
def instances():
    """Commands for instances """


@instances.command('start')
@click.option('--project', default=None,
              help='Only instances for project (tag Project: <name>)')
def start_instances(project):
    "Starts EC2 instances"

    instances = get_instances(project)
    for i in instances:
        if(i.state['Name'] == 'running'):
            print(i.id+" is already running, skipping.")
        elif(i.state['Name'] == 'pending'):
            print(i.id+" is starting up, skipping.")
        else:
            print("Starting up "+i.id+"...")
            i.start()


@instances.command('stop')
@click.option('--project', default=None,
              help='Only instances for project (tag Project: <name>)')
def stop_instances(project):
    "Stops EC2 instances"
    instances = get_instances(project)

    for i in instances:
        if(i.state['Name'] == 'stopped'):
            print(i.id+" is already stopped, skipping.")
        elif(i.state['Name'] == 'stopping'):
            print(i.id+" is already stopping, skipping.")
        else:
            print("Stopping "+i.id+"...")
            i.stop()


@instances.command('list')
@click.option('--project', default=None,
              help='Only instances for project (tag Project: <name>)')
def list_instances(project):
    "Lists EC2 instances"
    instances = get_instances(project)

    for i in instances:
        tags = {t['Key']: t['Value'] for t in i.tags or []}
        t.add_row([
            i.id,
            i.instance_type,
            i.placement['AvailabilityZone'],
            i.state['Name'],
            i.public_dns_name,
            tags.get('Project', '<no project tag>')])
    print(t)


if __name__ == '__main__':
    instances()

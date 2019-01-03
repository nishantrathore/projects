import boto3
import datetime
from datetime import tzinfo
from dateutil import tz
client = boto3.client('ec2',region_name='ap-south-1')
snapshots = client.describe_snapshots(OwnerIds=['117377266569'])

delete_days = 90
from_zone = tz.tzlocal()
to_zone = tz.tzutc()
ninty_days_back_date = datetime.datetime.now() - datetime.timedelta(delete_days)

current = ninty_days_back_date.replace(tzinfo=to_zone)

for snapshot in snapshots['Snapshots']:
    try:      
      if snapshot['StartTime'] < current:
          id = snapshot['SnapshotId']
          client.delete_snapshot(SnapshotId=id)
          print "deleted- {}".format(id)
    except Exception as err:
        print err, snapshot['SnapshotId']

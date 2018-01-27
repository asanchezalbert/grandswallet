from django.conf import settings
from boto3 import client


def send_sms(phone_number, message):
    conf = settings.SERVICES['messaging']

    if conf['enable']:
        aws = client('sns')

        aws.publish(
            PhoneNumber='+52{}'.format(phone_number),
            Message=message
        )

from django.conf import settings
from boto3 import client
import logging


logger = logging.getLogger(__name__)


def send_sms(phone_number, message):
    conf = settings.SERVICES['messaging']

    logger.info('SMS: {} => {}'.format(phone_number, message))

    if conf['enable']:
        aws = client('sns')

        aws.publish(
            PhoneNumber='+52{}'.format(phone_number),
            Message=message
        )

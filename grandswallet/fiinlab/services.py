import requests
import logging
from django.conf import settings


logger = logging.getLogger(__name__)


class FiinlabService:
    _access_token = None

    def __init__(self):
        self.conf = settings.SERVICES['fiinlab']

    def path(self, route):
        return '{}/{}'.format(self.conf['url'], route)

    def get_access_token(self):
        if not self._access_token:
            req = requests.post(
                self.path('createSession'),
                data={
                    'organizationID': self.conf['organization'],
                    'channel': self.conf['channel'],
                    'application': self.conf['application'],
                    'username': self.conf['username']
                })

            logger.info(
                'Fiinlab: /createSession [%s] => %s',
                req.status_code, req.text)

            res = req.json()

            if res['code'] != '00':
                raise Exception(res['message'])

            self._access_token = res['token']

        return self._access_token

    def login(self):
        req = requests.post(
            self.path('service'),
            data={
                'username': self.conf['username'],
                'password': self.conf['password'],
                'action': 'LOGIN'
            },
            headers={
                'x-access-token': self.get_access_token()
            }
        )

        logger.info(
            'Fiinlab: /service [%s] => %s',
            req.status_code, req.text)

        res = req.json()

        return res

    def transaction(self, transaction_type, payload={}):

        payload.update({
            'trans_type': transaction_type,
            'account': '00'
        })

        req = requests.post(
            self.path('esb/core/transaction'),
            data=payload,
            headers={
                'x-access-token': self.get_access_token()
            }
        )

        logger.info(
            'Fiinlab: /%s [%s] => %s',
            transaction_type, req.status_code, req.text)

        res = req.json()

        if res['code'] != '00':
            raise Exception(res['message'])

        return res['data']

    def create_n2_account(self, info={}):
        return self.transaction('COREAOS001', info)

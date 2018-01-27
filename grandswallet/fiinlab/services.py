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

    def transaction(self, transaction_type, payload={}, account='00'):

        self.login()

        payload.update({
            'trans_type': transaction_type,
            'account': account
        })

        req = requests.post(
            self.path('esb/core/transaction'),
            data=payload,
            headers={
                'x-access-token': self.get_access_token()
            }
        )

        logger.info(
            'Fiinlab: %s [%s] => %s',
            transaction_type, req.status_code, req.text)

        res = req.json()

        if res['code'] not in ('00', '06'):
            raise Exception(res['message'])

        return res['data']

    def create_n2_account(self, info={}):
        return self.transaction('COREAOS001', info)

    def balances(self, account_number):
        res = self.transaction('BENQ0002', {
            'custaccount': account_number
        }, '01')

        return map(lambda i: {
            'code': i['Code'],
            'name': i['Name'],
            'description': i['Description'],
            'amount': i['Amount']['_']
        }, res['message'])

    def transfer(self, amount, from_account_number, to_account_number, reference=''):
        return self.transaction('INTTFR0002', {
            'fromaccountnumber': from_account_number,
            'toaccountnumber': to_account_number,
            'amount': amount,
            'reference': reference
        })['transfer_result']

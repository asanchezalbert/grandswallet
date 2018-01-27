from random import choice
from string import digits
from grandswallet.messaging import send_sms
from grandswallet.fiinlab.services import FiinlabService
from base64 import b64encode


def gen_code_for_exchange():
    return ''.join(choice(digits) for i in range(12))


def gen_send_verification_code(user, entity):
    code = ''.join(choice(digits) for i in range(12))
    phone = entity.phones.first()

    user.verification_codes.create(
        code=code
    )

    send_sms(
        phone.phone_number,
        'Tu codigo de verificacion es: {}'.format(code))


def send_exchange_code(code):
    if not code.phone_number:
        return

    customer = code.account.customer

    send_sms(
        code.phone_number,
        '{} Te ha enviado ${:0,.2f}, tu código es: {}'.format(
            customer.first_name, code.amount, code.code))


def gen_n2_account(user, entity):
    s = FiinlabService()

    address = entity.addresses.first()
    document = entity.documents.first()

    account = s.create_n2_account({
        'custfname': entity.first_name,
        'custmname': entity.middle_name,
        'custlname': entity.last_name_paternal,
        'custaname': entity.last_name_maternal,
        'custdob': entity.date_of_birth.strftime('%Y-%m-%d'),
        'custuniquepopulationregistrycode': entity.person_id,
        'custgender': 1,
        'custidnumber': entity.elector_id,
        'custbirthregion': 'EM',
        'custbirthcountrycode': 'MX',
        'custcitizenshipcode': 'MX',
        'custmsisdn': entity.phones.first().phone_number,
        'custaddstreetname': address.street,
        'custaddhouseid': address.outdoor_number,
        'custaddhouseidadd': address.interior_number,
        'custadddistrictname': address.neighborhood,
        'custaddcityname': address.city,
        'custaddregioncode': 'EM',  # address.municipality,
        'custaddcountrycode': 'MX',  # address.country,
        'custaddpostalcode': address.postal_code,
        'doctype': 'ID',
        'image1': b64encode(document.document_file.read())
    })

    entity.accounts.create(
        clabe=account['clabeaccount'],
        account_number=account['newaccount'],
        business=account['businesspartnerid']
    )

    user.is_active = True
    user.save()

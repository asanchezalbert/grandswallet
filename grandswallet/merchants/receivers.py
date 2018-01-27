from grandswallet.fiinlab.services import FiinlabService
from base64 import b64encode
from random import choice
from string import digits
from grandswallet.messaging import send_sms


def on_merchant_sign_up(sender, instance, created, **kwargs):
    if not created:
        return

    code = ''.join(choice(digits) for i in range(12))
    merchant = instance.merchant
    phone = merchant.phones.first()

    instance.verification_codes.create(
        code=code
    )

    send_sms(
        phone.phone_number,
        'Tu codigo de verificacion es: {}'.format(code))


def on_merchant_active(sender, instance, created, **kwargs):
    merchant = instance.merchant
    user = merchant.user

    if not created or user.is_active:
        return

    s = FiinlabService()

    address = merchant.addresses.first()
    document = instance

    account = s.create_n2_account({
        'custfname': merchant.first_name,
        'custmname': merchant.middle_name,
        'custlname': merchant.last_name_paternal,
        'custaname': merchant.last_name_maternal,
        'custdob': merchant.date_of_birth.strftime('%Y-%m-%d'),
        'custuniquepopulationregistrycode': merchant.person_id,
        'custgender': 1,
        'custidnumber': merchant.elector_id,
        'custbirthregion': 'EM',
        'custbirthcountrycode': 'MX',
        'custcitizenshipcode': 'MX',
        'custmsisdn': merchant.phones.first().phone_number,
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

    merchant.accounts.create(
        clabe=account['clabeaccount'],
        account_number=account['newaccount'],
        business=account['businesspartnerid']
    )

    user.is_active = True
    user.save()

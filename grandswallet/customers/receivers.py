from grandswallet.fiinlab.services import FiinlabService
from base64 import base64encode


def on_customer_signup(sender, instance, created, **kwargs):
    if not created:
        return

    s = FiinlabService()

    address = instance.addresses.first()
    document = instance.documents.first()

    account = s.create_n2_account({
        'custfname': instance.first_name,
        'custmname': instance.middle_name,
        'custlname': instance.last_name_paternal,
        'custaname': instance.last_name_maternal,
        'custdob': instance.date_of_birth.strftime('%Y-%m-%d'),
        'custuniquepopulationregistrycode': instance.person_id,
        'custgender': 1,
        'custidnumber': '{:018}'.format(instance.id),
        'custbirthregion': 'EM',
        'custbirthcountrycode': 'MX',
        'custcitizenshipcode': 'MX',
        'custmsisdn': instance.phones.first().phone_number,
        'custaddstreetname': address.first(),
        'custaddhouseid': address.outdoor_number,
        'custaddhouseidadd': address.interior_number,
        'custadddistrictname': address.neighborhood,
        'custaddcityname': address.city,
        'custaddregioncode': address.municipality,
        'custaddcountrycode': address.country,
        'custaddpostalcode': address.postal_code,
        'doctype': 'ID',
        'image1': base64encode(document.document_file.read())
    })

    print(account)

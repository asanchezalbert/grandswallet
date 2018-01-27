from django.db import models
from django.utils.timezone import now
from django.db.models.signals import post_save
from grandswallet.base.models import (
    User, UserVerificationCode, UserVerified, Address, Phone, Email, Document, Account
)
from rest_framework.authtoken.models import Token
from grandswallet.base.receivers import on_user_verified
from . import receivers


class Merchant(models.Model):
    first_name = models.CharField(
        max_length=60
    )

    middle_name = models.CharField(
        max_length=60
    )

    last_name_paternal = models.CharField(
        max_length=60
    )

    last_name_maternal = models.CharField(
        max_length=60, default=''
    )

    date_of_birth = models.DateField(
    )

    tax_id = models.CharField(
        max_length=13, default=''
    )

    person_id = models.CharField(
        max_length=18, default=''
    )

    elector_id = models.CharField(
        max_length=18, default=''
    )

    created_date = models.DateTimeField(
        default=now
    )


class MerchantUser(User):
    merchant = models.OneToOneField(
        'Merchant', models.CASCADE, related_name='user'
    )


class MerchantVerificationCode(UserVerificationCode):
    user = models.ForeignKey(
        'MerchantUser', models.CASCADE, related_name='verification_codes'
    )


class MerchantVerified(UserVerified):
    user = models.OneToOneField(
        'MerchantUser', models.CASCADE, related_name='verified'
    )

    code = models.OneToOneField(
        'MerchantVerificationCode', models.CASCADE
    )


class MerchantAddress(Address):
    merchant = models.ForeignKey(
        'Merchant', models.CASCADE, related_name='addresses'
    )


class MerchantPhone(Phone):
    merchant = models.ForeignKey(
        'Merchant', models.CASCADE, related_name='phones'
    )


class MerchantEmail(Email):
    merchant = models.ForeignKey(
        'Merchant', models.CASCADE, related_name='emails'
    )


class MerchantDocument(Document):
    merchant = models.ForeignKey(
        'Merchant', models.CASCADE, related_name='documents'
    )


class MerchantAccount(Account):
    merchant = models.ForeignKey(
        'Merchant', models.CASCADE, related_name='accounts'
    )


class MerchantToken(Token):
    user = models.OneToOneField(
        'MerchantUser', models.CASCADE, related_name='token'
    )


post_save.connect(
    receivers.on_merchant_sign_up, sender=MerchantUser)

post_save.connect(
    on_user_verified, sender=MerchantVerified)

post_save.connect(
    receivers.on_merchant_active, sender=MerchantDocument)

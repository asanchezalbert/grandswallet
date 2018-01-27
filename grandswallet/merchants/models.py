from django.db import models
from django.utils.timezone import now
from grandswallet.base.models import (
    User, Address, Phone, Email, Document, Account
)
from rest_framework.authtoken.models import Token


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

    created_date = models.DateTimeField(
        default=now
    )


class MerchantUser(User):
    merchant = models.OneToOneField(
        'Merchant', models.CASCADE, related_name='user'
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
        'Merchant', models.CASCADE, related_name='token'
    )

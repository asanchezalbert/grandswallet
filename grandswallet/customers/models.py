from django.db import models
from django.utils.timezone import now
from django.db.models.signals import post_save
from grandswallet.base.models import (
    User, Address, Phone, Email, Document,
    Account, UserVerificationCode, UserVerified
)
from rest_framework.authtoken.models import Token
from grandswallet.base.receivers import on_user_verified
from . import receivers


class Customer(models.Model):
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


class CustomerUser(User):
    customer = models.OneToOneField(
        'Customer', models.CASCADE, related_name='user'
    )


class CustomerVerificationCode(UserVerificationCode):
    user = models.ForeignKey(
        'CustomerUser', models.CASCADE, related_name='verification_codes'
    )


class CustomerVerified(UserVerified):
    user = models.OneToOneField(
        'CustomerUser', models.CASCADE, related_name='verified'
    )

    code = models.OneToOneField(
        'CustomerVerificationCode', models.CASCADE
    )


class CustomerAddress(Address):
    customer = models.ForeignKey(
        'Customer', models.CASCADE, related_name='addresses'
    )


class CustomerPhone(Phone):
    customer = models.ForeignKey(
        'Customer', models.CASCADE, related_name='phones'
    )


class CustomerEmail(Email):
    customer = models.ForeignKey(
        'Customer', models.CASCADE, related_name='emails'
    )


class CustomerDocument(Document):
    customer = models.ForeignKey(
        'Customer', models.CASCADE, related_name='documents'
    )


class CustomerAccount(Account):
    customer = models.ForeignKey(
        'Customer', models.CASCADE, related_name='accounts'
    )


class CustomerToken(Token):
    user = models.OneToOneField(
        'CustomerUser', models.CASCADE, related_name='token'
    )


post_save.connect(
    receivers.on_customer_sign_up, sender=CustomerUser)

post_save.connect(
    on_user_verified, sender=CustomerVerified)

post_save.connect(
    receivers.on_customer_active, sender=CustomerDocument)

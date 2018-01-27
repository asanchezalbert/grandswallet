from django.db import models
from django.utils.timezone import now
from grandswallet.base.models import (
    User, Address, Phone, Email, Document, Account
)


class Customer(models.Model):
    name = models.CharField(
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


class CustomerUser(User):
    customer = models.OneToOneField(
        'Customer', models.CASCADE, related_name='user'
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

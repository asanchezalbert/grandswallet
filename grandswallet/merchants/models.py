from django.db import models
from django.utils.timezone import now
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator


class Merchant(models.Model):
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


class MerchantAccount(AbstractBaseUser):
    merchant = models.OneToOneField(
        'Merchant', models.CASCADE, related_name='account'
    )

    username = models.CharField(
        max_length=150, unique=True, validators=[UnicodeUsernameValidator()]
    )

    password = models.CharField(
        max_length=255, default=''
    )

    is_active = models.BooleanField(
        default=True
    )


class MerchantAddress(models.Model):
    merchant = models.ForeignKey(
        'Merchant', models.CASCADE, related_name='addresses'
    )

    street = models.CharField(
        max_length=1024
    )

    outdoor_number = models.CharField(
        max_length=12
    )

    interior_number = models.CharField(
        max_length=12, default=''
    )

    neighborhood = models.CharField(
        max_length=64
    )

    municipality = models.CharField(
        max_length=64
    )

    city = models.CharField(
        max_length=64
    )

    state = models.CharField(
        max_length=64
    )

    country = models.CharField(
        max_length=64
    )

    postal_code = models.CharField(
        max_length=5
    )

    created_date = models.DateTimeField(
        default=now
    )


class MerchantPhone(models.Model):
    merchant = models.ForeignKey(
        'Merchant', models.CASCADE, related_name='phones'
    )

    phone_number = models.CharField(
        max_length=10
    )

    created_date = models.DateTimeField(
        default=now
    )


class MerchantEmail(models.Model):
    merchant = models.ForeignKey(
        'Merchant', models.CASCADE, related_name='emails'
    )

    email_address = models.EmailField(
    )

    created_date = models.DateTimeField(
        default=now
    )

from django.db import models
from django.utils.timezone import now
from . import receivers
from django.db.models.signals import post_save


class Code(models.Model):
    account = models.ForeignKey(
        'customers.CustomerAccount', models.CASCADE, related_name='codes'
    )

    code = models.CharField(
        max_length=12
    )

    amount = models.DecimalField(
        max_digits=19, decimal_places=2
    )

    reference = models.CharField(
        max_length=255, default=''
    )

    created_date = models.DateTimeField(
        default=now
    )

    is_active = models.BooleanField(
        default=True
    )

    phone_number = models.CharField(
        max_length=10, default=''
    )


class CodeExchanged(models.Model):
    code = models.OneToOneField(
        'Code', models.CASCADE, related_name='exchanged'
    )

    created_date = models.DateTimeField(
        default=now
    )


post_save.connect(receivers.on_code_created, sender=Code)

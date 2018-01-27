from django.db import models
from django.utils.timezone import now


class Sale(models.Model):
    merchant_account = models.ForeignKey(
        'Merchant', models.CASCADE, related_name='sales'
    )

    account = models.ForeignKey(
        'CustomerAccount', models.CASCADE, related_name='purchases'
    )

    code = models.ForeignKey(
        'CustomerAccountCode', models.CASCADE, related_name='purchases'
    )

    amount = models.DecimalField(
        max_digits=19, decimal_places=2
    )

    reference = models.CharField(
        max_length=255
    )

    created_date = models.DateTimeField(
        default=now
    )

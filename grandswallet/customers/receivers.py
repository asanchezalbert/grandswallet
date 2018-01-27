from grandswallet.utils import (
    gen_send_verification_code,
    gen_n2_account
)


def on_customer_sign_up(sender, instance, created, **kwargs):
    if not created:
        return

    gen_send_verification_code(instance, instance.customer)


def on_customer_active(sender, instance, created, **kwargs):
    customer = instance.customer
    user = customer.user

    if not created or user.is_active:
        return

    gen_n2_account(user, customer)

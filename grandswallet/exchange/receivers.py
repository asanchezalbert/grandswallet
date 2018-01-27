from grandswallet.utils import (
    send_exchange_code, send_exchange_notification
)


def on_code_created(sender, instance, created, **kwargs):
    if not created:
        return

    send_exchange_code(instance)


def on_exchange_created(sender, instance, created, **kwargs):
    if not created:
        return

    code = instance.code

    code.is_active = False
    code.save()

    send_exchange_notification(instance)

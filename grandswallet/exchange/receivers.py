from grandswallet.utils import send_exchange_code


def on_code_created(sender, instance, created, **kwargs):
    if not created:
        return

    send_exchange_code(instance)

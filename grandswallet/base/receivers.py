def on_user_verified(sender, instance, created, **kwargs):
    if not created:
        return

    user = instance.user
    code = instance.code

    user.is_verified = True
    user.save()

    code.is_active = False
    code.save()

from django.conf.urls import url
from grandswallet.merchants.views import SignUpView


urlpatterns = [
    url('^merchants/signup$', SignUpView.as_view())
]

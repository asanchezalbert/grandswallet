from django.conf.urls import url
from grandswallet.merchants.views import (
    SignUpView, VerificationView, DocumentsView
)


urlpatterns = [
    url('^merchants/signup$', SignUpView.as_view()),
    url('^merchants/verify$', VerificationView.as_view()),
    url('^merchants/documents$', DocumentsView.as_view()),
]

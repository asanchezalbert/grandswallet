from django.conf.urls import url
from grandswallet.merchants.views import (
    SignUpView, VerificationView, DocumentsView,
    ProfileView, AccountsView
)


urlpatterns = [
    url('^signup$', SignUpView.as_view()),
    url('^verify$', VerificationView.as_view()),
    url('^documents$', DocumentsView.as_view()),
    url('^profile$', ProfileView.as_view()),
    url('^accounts$', AccountsView.as_view()),
]

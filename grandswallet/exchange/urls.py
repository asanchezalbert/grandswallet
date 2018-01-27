from django.conf.urls import url
from .views import CodeView, ExchangeView

urlpatterns = [
    url('codes$', CodeView.as_view()),
    url('$', ExchangeView.as_view())
]

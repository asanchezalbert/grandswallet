from django.conf.urls import url
from .views import CodeView

urlpatterns = [
    url('codes$', CodeView.as_view()),
]

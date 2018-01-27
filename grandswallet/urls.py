from django.conf.urls import url, include


urlpatterns = [
    url('^merchants/', include('grandswallet.merchants.urls')),
]

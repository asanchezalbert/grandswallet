from django.conf.urls import url, include


urlpatterns = [
    url('^customers/', include('grandswallet.customers.urls')),
]

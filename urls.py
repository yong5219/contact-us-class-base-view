from django.conf.urls import patterns, url
from .views import CountryAsia, ContactUsMarkAsRead, ContactUsCreate

urlpatterns = patterns(
    '',
    url(r'^countries/$', CountryAsia.as_view(), name='country_asia'),
    url(r'^countries/(?P<slug>[a-zA-Z0-9-]+)/$', ContactUsCreate.as_view(), name='contact_add'),
    url(r'^mark_as_read/(?P<pk>\d+)/$', ContactUsMarkAsRead.as_view(), name='contact_us_mark_as_read'),
)

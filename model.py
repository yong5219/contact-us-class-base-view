from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone

from autoslug.fields import AutoSlugField

from rainintl.models import TimeStampedModel

class ContactUs(TimeStampedModel):
    """
    Rain Contact Us Form
    """
    name = models.CharField(_("Name"), max_length=50)
    tel_no = models.CharField(_("Telephone No"), max_length=15)
    message = models.TextField(_("Message"))
    email = models.EmailField(_("Email"), max_length=255)
    to_email = models.EmailField(_("To Email"), max_length=255)
    ip_address = models.IPAddressField(_("IP address"), blank=True, null=True)
    admin_read = models.BooleanField(_("Admin read?"), default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = _("Contact us")
        verbose_name_plural = _("Contact us")

    def __str__(self):
        return "Contact from {0}".format(self.email)

    def get_absolute_url(self):
        return reverse('country_asia')

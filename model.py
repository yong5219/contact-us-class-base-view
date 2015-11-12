from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.utils import timezone

from rainintl.models import TimeStampedModel
from rainintl.emails import contacts_admin_notification, contacts_user_thank_you

from autoslug.fields import AutoSlugField


class CountryManager(models.Manager):
    """
    Shortcut to get data from manager.
    """
    def valid(self, **kwargs):
        return self.filter(is_active=True, publish_date__lte=timezone.now(), **kwargs)


class Country(TimeStampedModel):
    """
    Rain 11 Country
    """
    name = models.CharField(_("Name"), max_length=15)
    slug = AutoSlugField(
        _("Slug"), populate_from='name', editable=True, unique=True, max_length=250,
        help_text=_("Used for URLs, auto-generated from name if blank")
    )
    address = models.TextField(_("Address"), max_length=300)
    tel_no = models.CharField(_("Telephone No"), max_length=50)
    fax_no = models.CharField(_("Fax No"), max_length=25, blank=True, null=True)
    email = models.EmailField(_("Email"), max_length=255)
    ordering = models.IntegerField(_("Ordering"), default=None, blank=True, null=True)
    publish_date = models.DateTimeField(_("Publish date"))
    is_active = models.BooleanField(_("is_active"), default=True)

    objects = CountryManager()

    class Meta:
        ordering = ['ordering']
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        model = self.__class__

        # Auto calculate ordering
        if not self.ordering and self.ordering != 0:
            try:
                last = model.objects.order_by('-ordering')[0]
                self.ordering = last.ordering + 1
            except IndexError:
                # This item is first row
                self.ordering = 0

        super(model, self).save(*args, **kwargs)


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


def send_contacts_admin_notification_user_thank_you(sender, instance, created, **kwargs):
    """
    Send notification to admin and thank you to user when contact us form is submitted.
    """
    if created:
        contacts_admin_notification(instance)
        contacts_user_thank_you(instance)

models.signals.post_save.connect(send_contacts_admin_notification_user_thank_you, sender=ContactUs)

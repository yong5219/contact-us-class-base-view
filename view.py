from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
# from django.http import http

from .models import Country, ContactUs
from .forms import ContactUsForm


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class CountryAsia(ListView):

    template_name = 'contact_asia/connect-with-us-country.html'
    model = Country

    def get_context_data(self, **kwargs):
        context = super(CountryAsia, self).get_context_data(**kwargs)
        context['countries'] = Country.objects.valid()

        return context


class ContactUsCreate(SuccessMessageMixin, CreateView):

    template_name = 'contact_asia/connect-with-us.html'
    model = Country
    form_class = ContactUsForm
    success_message = 'Email sent successfully. Thank you.'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data, name=self.object.name, email=self.object.email, message=self.object.message)

    def form_valid(self, form):
        client_ip = get_client_ip(self.request)
        form.instance.ip_address = client_ip
        form.instance.to_email = self.slug.email
        return super(ContactUsCreate, self).form_valid(form)

    def dispatch(self, *args, **kwargs):
        self.slug = get_object_or_404(Country, slug=kwargs['slug'])
        return super(ContactUsCreate, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactUsCreate, self).get_context_data(**kwargs)
        context['country'] = self.slug
        return context


class ContactUsMarkAsRead(DetailView):

    queryset = ContactUs.objects.all()

    def get_object(self):
        # Call the superclass
        object = super(ContactUsMarkAsRead, self).get_object()
        # mark the contact as read after admin click the link from email.
        object.admin_read = True
        object.save()
        # Return the object
        return object

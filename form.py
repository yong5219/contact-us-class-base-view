from django import forms
from django.utils.translation import ugettext as _

from contacts.models import ContactUs


class ContactUsForm(forms.ModelForm):
    name = forms.CharField(label=_("Your Name"), widget=forms.TextInput(attrs=dict({'class': 'form-control'})), required=True, )
    email = forms.EmailField(label=_("Email Address"), widget=forms.TextInput(attrs=dict({'class': 'form-control'})), required=True)
    tel_no = forms.CharField(label=_("Phone Number"), widget=forms.TextInput(attrs=dict({'class': 'form-control'})), required=True, )
    message = forms.CharField(label=_("Message"), widget=forms.Textarea(attrs={'rows': '4', 'class': 'form-control'}))

    class Meta:
        model = ContactUs
        exclude = ('ip_address', 'admin_read', 'to_email')

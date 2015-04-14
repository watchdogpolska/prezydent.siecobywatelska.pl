from django import forms
from django.core.mail import mail_managers
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Contact


class ContactForm(forms.Form):
    personsList = forms.ModelChoiceField(required=True, label=_("Contact person"),
                                         queryset=Contact.objects.all())
    topic = forms.CharField(required=True, max_length=150,
        label=_("Topic of messages"))
    body = forms.CharField(required=True, widget=forms.Textarea(),  label=_("Content"))
    email = forms.EmailField(required=True, label=_("E-mail"))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_action = reverse('contact:form')
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit', css_class="btn-lg btn-block"))

    def get_text(self):
        return "%(body)s \n\nE-mail: %(email)s" % self.cleaned_data

    def send(self):
        mail_managers(self.cleaned_data['topic'], self.get_text())

from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from website.models import Contact
from django.views import View
from accounts.models import User
# Create your views here.


class IndexView(TemplateView):
    template_name = "Website/index.html"

class AboutView(TemplateView):
    template_name = "Website/about.html"

class ContactView(TemplateView):
    template_name = "Website/contact.html"


class SendContact(CreateView):
    model= Contact
    fields=["first_name", "last_name", "subject", "description", "phone_number"]
    template_name="Website/contact.html"
    success_url='/'

    
    def form_valid(self, form):
        form.instance.email = self.request.user
        return super().form_valid(form)

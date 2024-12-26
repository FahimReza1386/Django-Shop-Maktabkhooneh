from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class IndexView(TemplateView):
    template_name = "Website/index.html"

class AboutView(TemplateView):
    template_name = "Website/about.html"

class ContactView(TemplateView):
    template_name = "Website/contact.html"

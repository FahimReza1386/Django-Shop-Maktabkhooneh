from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, UpdateView
from website.models import Contact, NewsletterSubscriber
from django.contrib import messages
from shop.models import FavoritesProductModel
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


class AddUserToNewLatter(CreateView):
    model=NewsletterSubscriber
    fields=["email"]
    success_url="/"
    template_name="Website/index.html"


    def form_valid(self, form):
        
        if form.instance.email == self.request.user.email:
            return super().form_valid(form)
        else:
            messages.error(self.request, "سلام ! متاسفانه این ایمیل با ایمیل شما برابر نیست ..")
            return redirect("/")
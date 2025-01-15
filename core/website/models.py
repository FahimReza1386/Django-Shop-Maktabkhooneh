from django.db import models
from accounts.validators import validate_iranian_phone_number

# Create your models here.

class Contact(models.Model):
    first_name= models.CharField(max_length=50)
    last_name= models.CharField(max_length=100)
    email= models.ForeignKey("accounts.User", on_delete=models.CASCADE,max_length=50,)
    phone_number= models.CharField(max_length=12, validators=[validate_iranian_phone_number])
    subject= models.CharField(max_length=40)
    description= models.TextField()
    is_checked=models.BooleanField(default=False)
    created_date= models.DateTimeField(auto_now_add=True)
    updated_date= models.DateTimeField(auto_now=True)

    class Meta:
        ordering=["-created_date"]
    

    def __str__(self):
        return f"{self.first_name}"
    

class NewsletterSubscriber(models.Model):
    email=models.EmailField(max_length=200,unique=True)
    subscribed_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["-subscribed_date"]

    def __str__(self):
        return f"{self.email}"
    
from . import views
from django.urls import path


app_name = "review"
urlpatterns = [
    path("submit-review/", views.SubmitReviewView.as_view(), name="submit-review"),
]
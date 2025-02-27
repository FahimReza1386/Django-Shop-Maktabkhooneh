from . import views
from django.urls import path


app_name = "review"
urlpatterns = [
    path("submit-review/", views.SubmitReviewView.as_view(), name="submit-review"),
    path("review/<int:pk>/delete", views.DeleteReviewView.as_view(), name="delete-review"),
]
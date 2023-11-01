from django.urls import path
from . import views

urlpatterns = [
    path("all_courses/", views.all_courses, name="all-courses"),
    path("premium_courses/", views.premium_courses, name="premium-courses"),
]

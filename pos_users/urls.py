from django.urls import path

from pos_users.api_v1.views import UserSignupView, UserLogin

urlpatterns = [
    path('sign-up/', UserSignupView.as_view()),
    path('sign-in/', UserLogin.as_view()),

]

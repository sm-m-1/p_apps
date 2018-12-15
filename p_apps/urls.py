"""p_apps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts.views import (
    LoginFormView,
    SignUpFormView,
    LogoutFormView,
    signup_success,
    contact_page_success,
    UserActivationView,
    ContactFormView)
from django.contrib.auth import views as auth_views
from home.views import HomePageView

from email_future.views import EmailAppFormView, email_form_success

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('admin/', admin.site.urls),

    path('contact/', ContactFormView.as_view(), name='contact_page'),
    path('contact/success', contact_page_success, name='contact_page_success'),
    # path('', EmailPageView.as_view(), name='email_page'),

    path('accounts/signup', SignUpFormView.as_view(), name='signup'),
    path('accounts/login', LoginFormView.as_view(), name='login'),
    path('accounts/logout', LogoutFormView.as_view(), name='logout'),
    path('accounts/signup/success', signup_success, name='signup_success'),
    path('accounts/signup/activate/', UserActivationView.as_view(), name='user_activate'),


    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # email app
    path('email/', EmailAppFormView.as_view(), name='email_app'),
    path('email/success', email_form_success, name='email_form_success'),

]

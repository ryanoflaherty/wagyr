"""wagyr_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),  # Home Page
    url(r'^welcome', views.welcome, name='welcome'),
    url(r'^about', views.about, name='about'),  # Home Page
    url(r'^contact', views.contact, name='contact'),  # Home Page
    url(r'^admin', admin.site.urls),   # Admin Portal
    url(r'^wagyrs', views.wagyrs, name='wagyrs'),
    url(r'^make-wagyr', views.MakeWagyr.as_view(), name='make-wagyr'),
    url(r'^search/$', views.search, name='search'),
]

# Auth
urlpatterns += [
    url(r'^accounts/login/$', views.Login.as_view(), name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    url(r'^accounts/profile', views.profile, name='profile'),
    url(r'^accounts/register/$', views.CreateUser.as_view(), name='register'),
    url(r'^accounts/register/done/$', views.user_create_done, name='register-done'),
    url(r'^accounts/password_change/$', views.PasswordChange.as_view(), name='change-password'),
    url(r'^accounts/password_change/done/$', views.password_change_done, name='change-password-done'),
]

# Payments
urlpatterns += [
    url(r'^payment_successful/$', views.PaymentView.as_view(), name='payment_successful'),
    url(r'^received_thank_you/$', views.Received_SuccessView.as_view(), name='received_thank_you'),
    url(r'^thank_you/$', views.SuccessView.as_view(), name='thank_you'),
    url(r'^receive_payment_successful/$', views.ReceivePaymentView.as_view(), name='receive_payment_successful'),
]
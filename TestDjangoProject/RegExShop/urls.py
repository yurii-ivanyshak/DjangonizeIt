"""RegExShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from shop import views
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name='home'),
    url(r'^about/', views.about, name='about'),
    url(r'^item/(&P<item_text>[^/]+)', views.item),
    url(r'^market/', views.market, name='market'),
    url(r'^contacts/', views.contacts, name='contacts'),
    url(r'^market-single/', views.market_single, name='market_single'),
]

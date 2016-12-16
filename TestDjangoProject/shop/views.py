from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from shop.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import *
import random
import string


# Create your views here.
def home(request):
    items = Item.objects.all()
    context = {
        'items': items
    }
    return render(request, 'shop/home.html', context)

def about(request):
    return render(request, 'shop/about.html')

def item(request, item_text):
    try:
        items = Item.objects.get(item_text=item_text)
    except:
        return Http404
    context = {
        'items': items
    }
    return render(request, 'shop/home.html', context)
def market_single (request):
    return render(request, 'shop/market-single.html')


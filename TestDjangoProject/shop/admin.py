from django.contrib import admin
from shop.models import *
# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name','item_price')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','category_name')


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
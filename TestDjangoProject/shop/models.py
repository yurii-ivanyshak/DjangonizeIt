from django.db import models
from datetime import *
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    category_name = models.CharField (max_length = 200, verbose_name='Category name')
    category_text = models.TextField(default='Input the description here', verbose_name='Category description')

    def __str__(self):
        return self.category_name

class Item(models.Model):
    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
    item_name = models.CharField (max_length = 200, verbose_name='Item name')
    item_price = models.IntegerField(default=0, verbose_name='Item price')
    item_image = models.CharField(max_length=255, verbose_name="Image link")
    item_text = models.TextField(default='Input the description here', verbose_name='Item description')

    category = models.ForeignKey(Category)
    def __str__(self):
        return self.item_name



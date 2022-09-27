from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image as pil_image
import uuid

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from utils.models import DateTimeMixin, HiddenDeletedMixin




class Category(MPTTModel):
    name = models.CharField(max_length=128, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    attributes = models.ManyToManyField('Attribute', through='CategoryAttribute')

    class MPTTMeta:
        order_insertion_by = ['name']
        
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    @property
    def path(self):
        path = '/' + self.name.lower() + '/'
        while self.parent:
            path = '/' + self.parent.name.lower() + path
            self = self.parent
        return path

    def __str__(self):
        return f'{self.id} - {self.name}'


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = TreeForeignKey(Category, on_delete=models.PROTECT)
    short_desc = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.id} - {self.name} - {self.category.name}'


class StockKeepingUnit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category_attributes = models.ManyToManyField('CategoryAttribute', through='SKUCategoryAttribute')
    recommended_retail_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    slug = models.SlugField(null=True, blank=True)
    in_stock = models.PositiveSmallIntegerField(default=0)
    on_sale = models.BooleanField(default=False)
    web_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, max_length=16)

    def __str__(self):
        return f'{self.id} - {self.product.name}'

class CategoryAttribute(models.Model):
    
    FILTER_CHOICES = [
    ('range', 'range'), 
    ('single', 'single'), 
    ('multi', 'multi')
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE)
    show_on_tile = models.BooleanField(default=True)
    show_in_description = models.BooleanField(default=True)
    units = models.CharField(max_length=128, blank=True, null=True)

    filter_type = models.CharField(max_length=64, choices=FILTER_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.category} - {self.attribute} ({self.units})'




class Attribute(models.Model):

    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.id} - {self.name}'


class SKUCategoryAttribute(models.Model):
    sku = models.ForeignKey('StockKeepingUnit', on_delete=models.CASCADE)
    category_attribute = models.ForeignKey('CategoryAttribute', on_delete=models.PROTECT)
    value = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.id} - {self.sku.product.name} - {self.category_attribute.attribute.name} - {self.value} - {self.category_attribute.units}'


class Image(models.Model):
    image = models.ImageField(upload_to='uploads/project_images')
    preview = models.ImageField(upload_to='uploads/project_images/previews', blank=True, null=True)
    sku = models.ForeignKey('StockKeepingUnit', on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # preview_img = pil_image.open(self.preview.path)
        # x = preview_img.width
        # y = preview_img.height
        # ratio = x/y
        # min_dimension = 360

        # if x > y:
        #     output_size = (min_dimension * ratio, min_dimension)
        # else:
        #     output_size = (min_dimension, min_dimension * ratio)
            
        # preview_img.thumbnail(output_size)
        # preview_img.save(self.preview.path)


        main_img = pil_image.open(self.image.path)
        x = main_img.width
        y = main_img.height
        ratio = x/y
        max_dimension = 1280

        if x > y:
            output_size = (max_dimension, max_dimension / ratio)
        else:
            output_size = (max_dimension / ratio, max_dimension)
        
        main_img.thumbnail(output_size)
        main_img.save(self.image.path)



class FileUpload(DateTimeMixin, models.Model):
    file = models.FileField(upload_to='product_files', 
                            validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    uploaded = models.BooleanField(default=False)


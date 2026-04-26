from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from colorfield.fields import ColorField


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)
    slug = models.SlugField(max_length=250, blank=False, null=False, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('main:product_by_category', kwargs={'slug': self.slug})

    def get_product_length(self):
        return self.products.count()



class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products')
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField(default=10)
    discount = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=10, decimal_places=1, default=4.0)
    size = models.ManyToManyField('Size', blank=True, related_name='products_by_size')
    color = models.ManyToManyField('Color', blank=True, related_name='products_by_color')
    badges = models.ManyToManyField('Budges', blank=True, related_name='products_by_bages', default='all')

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'])
        ]
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('main:product_detail', kwargs={'product_slug': self.slug})

    def get_discount_price(self):
        return self.price - (self.price * self.discount) / 100



class Size(models.Model):
    size = models.DecimalField(max_digits=10, decimal_places=1, unique=True)

    def __str__(self):
        return f"size: {self.size}"

    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'
        ordering = ['size']
        indexes = [
            models.Index(fields=['size'])
        ]




class Color(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100)
    hex_code = ColorField(max_length=7, blank=True, default='')

    def __str__(self):
        return self.name

    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'



class Budges(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Budge'
        verbose_name_plural = 'Budges'


class ProductImage(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.image.name}"

class PromoCode(models.Model):
    code = models.CharField(max_length=15)
    slug = models.SlugField(max_length=15)
    discount = models.PositiveIntegerField()

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.code)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['code']
        indexes = [models.Index(fields=['code'])]
        verbose_name = 'Code'
        verbose_name_plural = 'Codes'










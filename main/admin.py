from django.contrib import admin


from main.models import Category, Product, Size, Color, Budges, ProductImage, PromoCode

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'slug', 'discount']
    fields = ['code', 'slug', 'discount']
    prepopulated_fields = {'slug': ('code',)}

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    list_display_links = ['name']
    fields = ['name', 'slug', 'description' ,'image']
    prepopulated_fields = {'slug': ('name',)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'quantity', 'discount' ,'description', 'available', 'created_at', 'updated_at', 'brief_info']
    list_editable = ['price', 'quantity']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    actions = ['NotAv']
    inlines = [ProductImageInline]

    @admin.display(description='Brief Info')
    def brief_info(self, product: Product):
        return f"Description length is {len(product.description)}"

    @admin.action(description='Not available')
    def NotAv(self, request, queryset):
        queryset = queryset.update(available=False)
        return queryset




@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size']
    fields = ['size']
    search_fields = ['size']

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    fields = ['name', 'slug', 'hex_code']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Budges)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    fields = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}



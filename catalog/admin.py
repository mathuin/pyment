from django.contrib import admin
from catalog.models import Product, Category, ProductReview
from catalog.forms import ProductAdminForm


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    # sets values for how the admin site lists your products
    list_display = ('name', 'title', 'category', 'description', 'jars_in_stock', 'is_active', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_filter = ('is_active', 'category')
    # list_per_page = 50
    ordering = ['-created_at', 'is_active']
    search_fields = ['name', 'title', 'description', 'meta_keywords', 'meta_description']
    readonly_fields = ('created_at', 'updated_at',)
    # sets up slug to be generated from product name
    # totally lame, must do the hard way
    # prepopulated_fields = {'slug' : ('brewname', 'batchletter',)}

# registers your product model with the admin site
admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    #sets up values for how admin site lists categories
    list_display = ('name', 'bjcptag', 'count', 'is_active', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_filter = ('is_active',)
    list_per_page = 20
    ordering = ['bjcptag']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    readonly_fields = ('created_at', 'updated_at',)
    # sets up slug to be generated from category name
    prepopulated_fields = {'slug': ('name', )}

    def count(self, obj):
        return obj.products.count()
    count.short_descriptions = 'Products'

admin.site.register(Category, CategoryAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'title', 'date', 'rating', 'is_approved')
    list_per_page = 20
    list_filter = ('product', 'user', 'is_approved')
    ordering = ['date']
    search_fields = ['user', 'content', 'title']

admin.site.register(ProductReview, ProductReviewAdmin)

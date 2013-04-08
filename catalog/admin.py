from django.contrib import admin
from catalog.models import Product, Category, ProductReview
from catalog.forms import ProductAdminForm
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    # sets values for how the admin site lists your products
    list_display = ('name', 'title', 'category', 'description', 'link_jars', 'is_active', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_filter = ('is_active', 'category')
    # list_per_page = 50
    ordering = ['-created_at', 'is_active']
    search_fields = ['name', 'title', 'description', 'meta_keywords', 'meta_description']
    readonly_fields = ('created_at', 'updated_at',)
    # sets up slug to be generated from product name
    # totally lame, must do the hard way
    # prepopulated_fields = {'slug' : ('brewname', 'batchletter',)}

    def link_jars(self, obj):
        howmany = obj.jars_in_stock()
        anchor = '%s?product__id__exact=%d' % (reverse('admin:inventory_jar_changelist'), obj.pk)
        if howmany > 0:
            return mark_safe('%d (<a href="%s">list</a>)' % (howmany, anchor))
        else:
            return howmany
    link_jars.short_description = 'Jars'

# registers your product model with the admin site
admin.site.register(Product, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    #sets up values for how admin site lists categories
    list_display = ('name', 'bjcptag', 'link_products', 'is_active', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_filter = ('is_active',)
    list_per_page = 20
    ordering = ['bjcptag']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    readonly_fields = ('created_at', 'updated_at',)
    # sets up slug to be generated from category name
    prepopulated_fields = {'slug': ('name', )}

    def link_products(self, obj):
        howmany = obj.products.count()
        # FIXME: learn how to create the URL for 'the admin page for products filtering on this particular category'
        # http://localhost:8000/admin/catalog/product/?category__id__exact=1
        anchor = '%s?category__id__exact=%d' % (reverse('admin:catalog_product_changelist'), obj.pk)
        if howmany > 0:
            return mark_safe('%d (<a href="%s">list</a>)' % (howmany, anchor))
        else:
            return howmany
    link_products.short_description = 'Products'

admin.site.register(Category, CategoryAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'title', 'date', 'rating', 'is_approved')
    list_per_page = 20
    list_filter = ('product', 'user', 'is_approved')
    ordering = ['date']
    search_fields = ['user', 'content', 'title']

admin.site.register(ProductReview, ProductReviewAdmin)

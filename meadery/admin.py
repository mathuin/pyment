from django.contrib import admin
from utils.buttonadmin import ButtonAdmin
from .models import Ingredient, NewIngredientItem, NewRecipe, NewBatch, Sample, NewProduct, ProductReview
from .forms import IngredientAdminForm, NewRecipeAdminForm, NewBatchAdminForm, SampleAdminForm, NewProductAdminForm, ProductReviewForm
from meadery import create_batch_from_recipe, create_recipe_from_batch, create_product_from_batch, make_labels_from_batch
from django.core.urlresolvers import reverse
from decimal import Decimal
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect


class IngredientAdmin(admin.ModelAdmin):
    form = IngredientAdminForm
    list_display = ('name', 'is_natural', 'appellation', 'type', 'subtype', 'state', 'sg', 'sh', 'tolerance', 'cpu')
    list_display_links = ('name', )
    list_filter = ('is_natural', 'appellation', 'type')

admin.site.register(Ingredient, IngredientAdmin)


class NewIngredientItemInline(admin.StackedInline):
    model = NewIngredientItem
    extra = 0


class NewRecipeAdmin(ButtonAdmin):
    form = NewRecipeAdminForm
    list_display = ('title', 'description', 'category', 'all_natural', 'appellation', 'total_cost')
    list_display_links = ('title', )
    inlines = [NewIngredientItemInline, ]
    readonly_fields = ('category', )

    def total_cost(self, obj):
        return Decimal(sum([(item.amount * item.ingredient.cpu) for item in obj.items()])).quantize(Decimal('0.01'))

    # JMT: disabled temporarily
    def brew_sg(self, obj):
        return obj.brew_sg
    brew_sg.short_description = 'Projected OG'

    # JMT: disabled temporarily
    def final_sg(self, obj):
        if len(obj.yeast_items) > 0:
            deltasg = max([item.yeast.maxdeltasg for item in obj.items(Ingredient.TYPE_YEAST)])
        else:
            deltasg = 0
        return Decimal(obj.brew_sg - deltasg)
    final_sg.short_description = 'Projected FG'

    def create_batch(self, request, recipe=None):
        if recipe is not None:
            if create_batch_from_recipe(recipe):
                self.message_user(request, 'One batch was created!')
            else:
                self.message_user(request, 'No batch was created!')
        else:
            return None
    create_batch.short_description = 'Create batch from recipe'

    change_buttons = [create_batch]


admin.site.register(NewRecipe, NewRecipeAdmin)


class NewBatchAdmin(ButtonAdmin):
    form = NewBatchAdminForm
    # list_display = ('name', 'recipe', 'all_natural', 'appellation', 'brew_sg', 'final_sg', 'link_samples', 'firstsg', 'lastsg', 'abv', 'jars', )
    list_display = ('name', 'recipe', 'all_natural', 'appellation', 'link_samples', 'firstsg', 'lastsg', 'abv', 'jars', )
    list_display_links = ('name', )

    def link_samples(self, obj):
        howmany = obj.sample_set.count()
        anchor = '%s?batch=%d' % (reverse('admin:meadery_sample_changelist'), obj.pk)
        if howmany > 0:
            return mark_safe('%d (<a href="%s">list</a>)' % (howmany, anchor))
        else:
            return howmany
    link_samples.short_description = 'Samples'

    def firstsg(self, obj):
        # if obj.sample_set.count() > 0:
        if Sample.objects.filter(batch=obj).exists():
            return Sample.objects.filter(batch=obj).order_by('date')[0].corrsg
            # return self.sample_set.order_by('date')[0].corrsg
        else:
            return None
    firstsg.short_description = 'Actual OG'

    def lastsg(self, obj):
        # if obj.sample_set.count() > 0:
        if Sample.objects.filter(batch=obj).exists():
            return Sample.objects.filter(batch=obj).order_by('-date')[0].corrsg
            # return self.sample_set.order_by('-date')[0].corrsg
        else:
            return None
    lastsg.short_description = 'Actual FG'

    def abv(self, obj):
        return obj.abv
    abv.short_description = 'Alc. % by vol.'

    def create_recipe(self, request, batch=None):
        if batch is not None:
            if create_recipe_from_batch(batch):
                self.message_user(request, 'One recipe was created!')
            else:
                self.message_user(request, 'No recipe was created!')
        else:
            return None
    create_recipe.short_description = 'Create recipe from batch'

    def create_product(self, request, batch=None):
        if batch is not None:
            if create_product_from_batch(batch):
                self.message_user(request, 'One product was created!')
            else:
                self.message_user(request, 'No product was created!')
        else:
            return None
    create_product.short_description = 'Create product from batch'

    def add_sample(self, request, batch=None):
        if batch is not None:
            return HttpResponseRedirect('%s?batch=%d' % (reverse('admin:meadery_sample_add'), batch.pk))
        else:
            return None
    add_sample.short_description = 'Add sample'

    def make_labels(self, request, batch=None):
        if batch is not None:
            pdf = make_labels_from_batch(batch)
            if pdf is not None:
                self.message_user(request, 'Labels were made for batch {0}'.format(batch))
                filename = ''.join([batch.brewname, batch.batchletter]).lower().replace(' ', '')
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="{0}.pdf"'.format(filename)
                response.write(pdf)
                return response
            else:
                self.message_user(request, 'No labels were made!')
        else:
            return None
    make_labels.short_description = 'Make labels'

    change_buttons = [make_labels, add_sample, create_recipe, create_product]

admin.site.register(NewBatch, NewBatchAdmin)


class SampleAdmin(admin.ModelAdmin):
    form = SampleAdminForm
    list_display = ('__unicode__', 'batch', 'date', 'temp', 'sg', 'notes', )
    list_display_links = ('__unicode__', )
    list_filter = ('batch', 'date')
    ordering = ['-date', 'batch']

admin.site.register(Sample, SampleAdmin)


class NewProductAdmin(admin.ModelAdmin):
    form = NewProductAdminForm
    # sets values for how the admin site lists your products
    list_display = ('name', 'title', 'category', 'description', 'link_jars', 'is_active', 'created_at', 'updated_at',)
    list_display_links = ('name',)
    list_filter = ('is_active', 'category')
    # list_per_page = 50
    ordering = ['-created_at', 'is_active']
    search_fields = ['name', 'title', 'description', 'meta_keywords', 'meta_description']
    readonly_fields = ('created_at', 'updated_at',)

    def link_jars(self, obj):
        howmany = obj.jars_in_stock()
        anchor = '%s?product__id__exact=%d' % (reverse('admin:inventory_newjar_changelist'), obj.pk)
        if howmany > 0:
            return mark_safe('%d (<a href="%s">list</a>)' % (howmany, anchor))
        else:
            return howmany
    link_jars.short_description = 'Jars'

admin.site.register(NewProduct, NewProductAdmin)


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'title', 'date', 'rating', 'is_approved')
    list_per_page = 20
    list_filter = ('product', 'user', 'is_approved')
    ordering = ['date']
    search_fields = ['user', 'content', 'title']

admin.site.register(ProductReview, ProductReviewAdmin)

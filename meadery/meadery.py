from models import Ingredient, IngredientItem, Recipe, Batch, Sample, Product
from checkout.models import OrderItem
from cStringIO import StringIO
from labels import Sheet


def create_batch_from_recipe(recipe):
    batch = Batch()
    batch.brewname = 'CHANGEME'
    batch.batchletter = 'A'
    batch.recipe = recipe
    # First copy fields from recipe to batch.
    [setattr(batch, field.name, getattr(recipe, field.name)) for field in Recipe._meta.fields if field.name != 'id']
    batch.jars = 0
    batch.save()
    for item in IngredientItem.objects.filter(recipe=recipe):
        new_item = item
        new_item.pk = None
        new_item.recipe = batch
        new_item.save()
    return batch


def create_recipe_from_batch(batch):
    recipe = Recipe()
    # First copy fields from recipe to batch.
    [setattr(recipe, field.name, getattr(batch, field.name)) for field in Recipe._meta.fields if field.name != 'id']
    recipe.title = '%s %s Recipe' % (batch.brewname, batch.batchletter)
    recipe.save()
    # Now copy separate items.
    for item in IngredientItem.objects.filter(recipe=batch):
        new_item = item
        new_item.pk = None
        new_item.recipe = recipe
        new_item.save()
    return recipe


def create_product_from_batch(batch):
    if batch.jars > 0:
        product = Product()
        product.brewname = batch.brewname
        product.batchletter = batch.batchletter
        product.title = batch.title
        product.is_active = False
        product.description = batch.description
        firstsample = batch.sample_set.order_by('date')[0]
        lastsample = batch.sample_set.order_by('-date')[0]
        product.brewed_date = firstsample.date
        product.brewed_sg = firstsample.corrsg
        product.bottled_date = lastsample.date
        product.bottled_sg = lastsample.corrsg
        product.meta_keywords = 'bogus'
        product.meta_description = 'bogus'
        product.category = batch.category
        product.save()
        return product
    else:
        return None


try:
    from meadery_local import generate_labels
except ImportError:
    from labels import Label

    def generate_labels(batch):
        return [Label(seq, batch) for seq in xrange(batch.jars)]


def make_labels_from_batch(batch):
    # Create buffer.
    buffer = StringIO()

    # Build the label objects.
    labels = generate_labels(batch)

    # Generate label sheets.
    faux = Sheet(buffer)
    faux(labels)

    pdf = buffer.getvalue()
    buffer.close()
    return pdf

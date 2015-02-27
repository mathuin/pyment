from models import Ingredient, IngredientItem, Recipe, Batch, Sample, Product
from checkout.models import OrderItem
from cStringIO import StringIO
from labels import Sheet


def create_batch_from_recipe(recipe):
    batch = Batch()
    batch.brewname = 'CHANGEME'
    batch.batchletter = 'A'
    batch.recipe = None
    batch.event = 'Christmas'
    batch.jars = 0
    batch.save()
    batch.recipe = recipe
    # First copy fields from recipe to batch.
    for field in Recipe._meta.fields:
        if field.name != 'id' and field.name != 'pk':
            setattr(batch, field.name, getattr(recipe, field.name))
    batch.save()
    for item in IngredientItem.objects.filter(parent=recipe):
        new_item = item
        new_item.pk = None
        new_item.parent = batch
        new_item.save()
    return batch


def create_recipe_from_batch(batch):
    recipe = Recipe()
    # First copy fields from recipe to batch.
    for field in Recipe._meta.fields:
        if field.name != 'id' and field.name != 'pk':
            setattr(recipe, field.name, getattr(batch, field.name))
    recipe.title = '%s Recipe' % batch.name
    recipe.save()
    # Now copy separate items.
    for item in IngredientItem.objects.filter(parent=batch):
        new_item = item
        new_item.pk = None
        new_item.parent = recipe
        new_item.save()
    return recipe


def create_product_from_batch(batch):
    # Do not create product if product already exists!
    if Product.objects.filter(brewname=batch.brewname, batchletter=batch.batchletter).exists() or batch.sample_set.count() == 0 or batch.jars == 0:
        return None
    else:
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
        product.abv = batch.abv
        product.save()
        return product


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

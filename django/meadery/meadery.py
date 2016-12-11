from meadery.models import IngredientItem, Recipe, Batch, Product
from io import BytesIO
from itertools import chain
from meadery.labels import Sheet


def create_batch_from_recipe(recipe, brewname, batchletter, event):
    batch = Batch()
    batch.brewname = brewname
    batch.batchletter = batchletter
    batch.recipe = None
    batch.event = event
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
    from meadery.labels import Label

    def generate_labels(batch):
        return [Label(seq, batch) for seq in range(batch.jars)]


def make_labels_from_batches(batches):
    # Create buffer.
    buffer = BytesIO()

    # Build the label objects.
    if isinstance(batches, list):
        labels = list(chain.from_iterable([generate_labels(batch) for batch in batches]))
    else:
        labels = generate_labels(batches)

    # Generate label sheets.
    faux = Sheet(buffer)
    faux(labels)

    pdf = buffer.getvalue()
    buffer.close()
    return pdf

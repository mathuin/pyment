from models import Honey, Water, Flavor, Yeast, HoneyItem, CoolItem, WarmItem, FlavorItem, YeastItem, Recipe, Batch, Sample


def create_batch_from_recipe(recipe):
    batch = Batch()
    batch.brewname = 'CHANGEME'
    batch.batchletter = 'A'
    batch.recipe = recipe
    # First copy fields from recipe to batch.
    [setattr(batch, field.name, getattr(recipe, field.name)) for field in Recipe._meta.fields if field.name != 'id']
    batch.jars = 0
    batch.save()
    # Now copy separate items.
    for honey_item in recipe.honey_items:
        new_honey_item = HoneyItem()
        new_honey_item.honey = honey_item.honey
        new_honey_item.mass = honey_item.mass
        new_honey_item.recipe = batch
        new_honey_item.save()
    for warm_item in recipe.warm_items:
        new_warm_item = WarmItem()
        new_warm_item.water = warm_item.water
        new_warm_item.volume = warm_item.volume
        new_warm_item.recipe = batch
        new_warm_item.save()
    for cool_item in recipe.cool_items:
        new_cool_item = CoolItem()
        new_cool_item.water = cool_item.water
        new_cool_item.volume = cool_item.volume
        new_cool_item.recipe = batch
        new_cool_item.save()
    for flavor_item in recipe.flavor_items:
        new_flavor_item = FlavorItem()
        new_flavor_item.flavor = flavor_item.flavor
        new_flavor_item.amount = flavor_item.amount
        new_flavor_item.recipe = batch
        new_flavor_item.save()
    for yeast_item in recipe.yeast_items:
        new_yeast_item = YeastItem()
        new_yeast_item.yeast = yeast_item.yeast
        new_yeast_item.amount = yeast_item.amount
        new_yeast_item.recipe = batch
        new_yeast_item.save()
    return batch


def create_recipe_from_batch(batch):
    recipe = Recipe()
    # JMT: *looks* good...
    [setattr(recipe, field.name, getattr(batch, field.name)) for field in Recipe._meta.fields if field.name != 'id']
    recipe.title = '%s %s Recipe' % (batch.brewname, batch.batchletter)
    recipe.save()
    # Now copy separate items.
    for honey_item in batch.honey_items:
        new_honey_item = HoneyItem()
        new_honey_item.honey = honey_item.honey
        new_honey_item.mass = honey_item.mass
        new_honey_item.recipe = recipe
        new_honey_item.save()
    for warm_item in batch.warm_items:
        new_warm_item = WarmItem()
        new_warm_item.water = warm_item.water
        new_warm_item.volume = warm_item.volume
        new_warm_item.recipe = recipe
        new_warm_item.save()
    for cool_item in batch.cool_items:
        new_cool_item = CoolItem()
        new_cool_item.water = cool_item.water
        new_cool_item.volume = cool_item.volume
        new_cool_item.recipe = recipe
        new_cool_item.save()
    for flavor_item in batch.flavor_items:
        new_flavor_item = FlavorItem()
        new_flavor_item.flavor = flavor_item.flavor
        new_flavor_item.amount = flavor_item.amount
        new_flavor_item.recipe = recipe
        new_flavor_item.save()
    for yeast_item in batch.yeast_items:
        new_yeast_item = YeastItem()
        new_yeast_item.yeast = yeast_item.yeast
        new_yeast_item.amount = yeast_item.amount
        new_yeast_item.recipe = recipe
        new_yeast_item.save()
    return recipe

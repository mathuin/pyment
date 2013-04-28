from models import Honey, Water, Flavor, Yeast, Recipe, Batch, Sample


def create_batch_from_recipe(recipe):
    batch = Batch()
    batch.recipe = recipe
    # JMT: *looks* good...
    [setattr(batch, field.name, getattr(recipe, field.name)) for field in Recipe._meta.fields if field.name != 'id']
    batch.jars = 0
    batch.save()
    return batch


def create_recipe_from_batch(batch):
    recipe = Recipe()
    # JMT: *looks* good...
    [setattr(recipe, field.name, getattr(batch, field.name)) for field in Recipe._meta.fields if field.name != 'id']
    recipe.save()
    return recipe

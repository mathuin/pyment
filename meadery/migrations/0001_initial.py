# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Ingredient name', max_length=40, verbose_name=b'Ingredient Name')),
                ('is_natural', models.BooleanField(default=False, help_text=b'TRUE if the ingredient does not contain added color, artificial flavors, or synthetic substances.')),
                ('appellation', models.CharField(help_text=b'Where the ingredient was made (i.e., Oregon, California, Brazil)', max_length=20, verbose_name=b'Appellation')),
                ('type', models.IntegerField(default=1, choices=[(1, b'Sugar'), (2, b'Solvent'), (3, b'Flavor'), (4, b'Yeast')])),
                ('subtype', models.IntegerField(default=101, choices=[(b'Sugar', ((101, b'Honey'), (102, b'Malt'), (103, b'Other'))), (b'Solvent', ((201, b'Water'), (202, b'Grape Juice'), (203, b'Apple Juice'), (204, b'Fruit Juice'), (205, b'Other'))), (b'Flavor', ((301, b'Spice'), (302, b'Grape'), (303, b'Apple'), (304, b'Fruit'), (305, b'Other'))), (b'Yeast', ((401, b'Dry'), (402, b'Wet')))])),
                ('state', models.IntegerField(default=1, choices=[(1, b'Solid'), (2, b'Liquid'), (3, b'Other')])),
                ('sg', models.DecimalField(default=Decimal('1.000'), help_text=b'Specific gravity (water is 1.000, honey is usually 1.422)', verbose_name=b'Specific Gravity', max_digits=4, decimal_places=3)),
                ('sh', models.DecimalField(default=Decimal('1.00'), help_text=b'Specific heat (water is 1.00, honey is usually 0.57)', verbose_name=b'Specific Heat', max_digits=3, decimal_places=2)),
                ('tolerance', models.IntegerField(default=12, help_text=b'Maximum alcohol tolerance in percent (only for yeast)', verbose_name=b'Alcohol tolerance')),
                ('cpu', models.DecimalField(default=Decimal('1.00'), help_text=b'Cost in USD per unit (kilogram if solid, liter if liquid, other if other)', verbose_name=b'Cost Per Unit', max_digits=5, decimal_places=2)),
            ],
            options={
                'ordering': ('state',),
            },
        ),
        migrations.CreateModel(
            name='IngredientItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(help_text=b'Amount of ingredient (kilograms if solid, liters if liquid, units if other)', max_digits=5, decimal_places=3)),
                ('temp', models.IntegerField(help_text=b'Temperature of ingredient in degrees Fahrenheit')),
                ('ingredient', models.ForeignKey(to='meadery.Ingredient')),
            ],
            options={
                'ordering': ('ingredient', '-temp'),
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'Recipe title', max_length=40)),
                ('description', models.TextField(help_text=b'Description of product.')),
                ('category', models.IntegerField(default=241, choices=[(b'Traditional Mead', ((241, b'Dry Mead'), (242, b'Semi-Sweet Mead'), (243, b'Sweet Mead'))), (b'Melomel', ((251, b'Cyser'), (252, b'Pyment'), (253, b'Other Fruit Melomel'))), (b'Other Meads', ((261, b'Metheglin'), (262, b'Braggot'), (263, b'Open Category Mead'))), (b'All Meads', ((291, b'All'),))])),
            ],
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('rating', models.PositiveSmallIntegerField(default=5, choices=[(5, b'5 - Outstanding'), (4, b'4 - Excellent'), (3, b'3 - Very Good'), (2, b'2 - Good'), (1, b'1 - Fair')])),
                ('is_approved', models.BooleanField(default=True)),
                ('content', models.TextField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('temp', models.IntegerField(default=60, help_text=b'Temperature of mead in degrees Fahrenheit')),
                ('sg', models.DecimalField(default=Decimal('0.000'), help_text=b'Specific gravity of mead', max_digits=4, decimal_places=3)),
                ('notes', models.TextField(help_text=b'Tasting notes')),
            ],
            options={
                'ordering': ('date',),
            },
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('parent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='meadery.Parent')),
                ('brewname', models.CharField(help_text=b'Unique value for brew name (e.g., SIP 99)', max_length=8, verbose_name=b'Brew Name')),
                ('batchletter', models.CharField(help_text=b'Letter corresponding to batch (e.g., A)', max_length=1, verbose_name=b'Batch Letter')),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('event', models.CharField(help_text=b'Brewing event (e.g., Lughnasadh 2013, Samhain 2012, Imbolc 2011, Beltane 2010)', max_length=20, verbose_name=b'Brewing event')),
                ('jars', models.IntegerField(help_text=b'Number of jars actually produced from this batch.')),
            ],
            options={
                'ordering': ['is_active', '-created_at'],
                'abstract': False,
            },
            bases=('meadery.parent',),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('parent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='meadery.Parent')),
                ('brewname', models.CharField(help_text=b'Unique value for brew name (e.g., SIP 99)', max_length=8, verbose_name=b'Brew Name')),
                ('batchletter', models.CharField(help_text=b'Letter corresponding to batch (e.g., A)', max_length=1, verbose_name=b'Batch Letter')),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(help_text=b'Unique value for product page URL, created from brewname and batchletter.', unique=True, max_length=255, blank=True)),
                ('image', models.ImageField(upload_to=b'images/products/main', blank=True)),
                ('thumbnail', models.ImageField(upload_to=b'images/products/thumbnails', blank=True)),
                ('is_bestseller', models.BooleanField(default=False)),
                ('is_featured', models.BooleanField(default=False)),
                ('meta_keywords', models.CharField(help_text=b'Comma-delimited set of SEO keywords for meta tag', max_length=255)),
                ('meta_description', models.CharField(help_text=b'Content for description meta tag', max_length=255)),
                ('brewed_date', models.DateField()),
                ('brewed_sg', models.DecimalField(default=Decimal('0.000'), max_digits=4, decimal_places=3)),
                ('bottled_date', models.DateField()),
                ('bottled_sg', models.DecimalField(default=Decimal('0.000'), max_digits=4, decimal_places=3)),
                ('abv', models.DecimalField(default=Decimal('0.00'), max_digits=4, decimal_places=2)),
            ],
            options={
                'ordering': ['is_active', '-created_at'],
                'abstract': False,
            },
            bases=('meadery.parent',),
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('parent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='meadery.Parent')),
            ],
            bases=('meadery.parent',),
        ),
        migrations.AddField(
            model_name='ingredientitem',
            name='parent',
            field=models.ForeignKey(to='meadery.Parent'),
        ),
        migrations.AddField(
            model_name='sample',
            name='batch',
            field=models.ForeignKey(to='meadery.Batch'),
        ),
        migrations.AddField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(to='meadery.Product'),
        ),
        migrations.AddField(
            model_name='batch',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='meadery.Recipe', null=True),
        ),
    ]

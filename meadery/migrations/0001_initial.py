# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ingredient'
        db.create_table(u'meadery_ingredient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('is_natural', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('appellation', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('subtype', self.gf('django.db.models.fields.IntegerField')(default=101)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('sg', self.gf('django.db.models.fields.DecimalField')(default='1.000', max_digits=4, decimal_places=3)),
            ('sh', self.gf('django.db.models.fields.DecimalField')(default='1.00', max_digits=3, decimal_places=2)),
            ('tolerance', self.gf('django.db.models.fields.IntegerField')(default=12)),
            ('cpu', self.gf('django.db.models.fields.DecimalField')(default='1.00', max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal(u'meadery', ['Ingredient'])

        # Adding model 'IngredientItem'
        db.create_table(u'meadery_ingredientitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Parent'])),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Ingredient'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=3)),
            ('temp', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'meadery', ['IngredientItem'])

        # Adding model 'Parent'
        db.create_table(u'meadery_parent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.IntegerField')(default=241)),
        ))
        db.send_create_signal(u'meadery', ['Parent'])

        # Adding model 'Recipe'
        db.create_table(u'meadery_recipe', (
            (u'parent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['meadery.Parent'], unique=True, primary_key=True)),
        ))
        db.send_create_signal(u'meadery', ['Recipe'])

        # Adding model 'Batch'
        db.create_table(u'meadery_batch', (
            (u'parent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['meadery.Parent'], unique=True, primary_key=True)),
            ('brewname', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('batchletter', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Recipe'], null=True, on_delete=models.SET_NULL, blank=True)),
            ('event', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('jars', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'meadery', ['Batch'])

        # Adding model 'Sample'
        db.create_table(u'meadery_sample', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('batch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Batch'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('temp', self.gf('django.db.models.fields.IntegerField')(default=60)),
            ('sg', self.gf('django.db.models.fields.DecimalField')(default='0.000', max_digits=4, decimal_places=3)),
            ('notes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'meadery', ['Sample'])

        # Adding model 'Product'
        db.create_table(u'meadery_product', (
            (u'parent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['meadery.Parent'], unique=True, primary_key=True)),
            ('brewname', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('batchletter', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('is_bestseller', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('brewed_date', self.gf('django.db.models.fields.DateField')()),
            ('brewed_sg', self.gf('django.db.models.fields.DecimalField')(default='0.000', max_digits=4, decimal_places=3)),
            ('bottled_date', self.gf('django.db.models.fields.DateField')()),
            ('bottled_sg', self.gf('django.db.models.fields.DecimalField')(default='0.000', max_digits=4, decimal_places=3)),
            ('abv', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=4, decimal_places=2)),
        ))
        db.send_create_signal(u'meadery', ['Product'])

        # Adding model 'ProductReview'
        db.create_table(u'meadery_productreview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Product'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('rating', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=5)),
            ('is_approved', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'meadery', ['ProductReview'])


    def backwards(self, orm):
        # Deleting model 'Ingredient'
        db.delete_table(u'meadery_ingredient')

        # Deleting model 'IngredientItem'
        db.delete_table(u'meadery_ingredientitem')

        # Deleting model 'Parent'
        db.delete_table(u'meadery_parent')

        # Deleting model 'Recipe'
        db.delete_table(u'meadery_recipe')

        # Deleting model 'Batch'
        db.delete_table(u'meadery_batch')

        # Deleting model 'Sample'
        db.delete_table(u'meadery_sample')

        # Deleting model 'Product'
        db.delete_table(u'meadery_product')

        # Deleting model 'ProductReview'
        db.delete_table(u'meadery_productreview')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'meadery.batch': {
            'Meta': {'ordering': "['-is_active', '-created_at']", 'object_name': 'Batch'},
            'batchletter': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'brewname': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'jars': ('django.db.models.fields.IntegerField', [], {}),
            u'parent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['meadery.Parent']", 'unique': 'True', 'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Recipe']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'meadery.ingredient': {
            'Meta': {'object_name': 'Ingredient'},
            'appellation': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'cpu': ('django.db.models.fields.DecimalField', [], {'default': "'1.00'", 'max_digits': '5', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_natural': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'sg': ('django.db.models.fields.DecimalField', [], {'default': "'1.000'", 'max_digits': '4', 'decimal_places': '3'}),
            'sh': ('django.db.models.fields.DecimalField', [], {'default': "'1.00'", 'max_digits': '3', 'decimal_places': '2'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'subtype': ('django.db.models.fields.IntegerField', [], {'default': '101'}),
            'tolerance': ('django.db.models.fields.IntegerField', [], {'default': '12'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'meadery.ingredientitem': {
            'Meta': {'object_name': 'IngredientItem'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Ingredient']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Parent']"}),
            'temp': ('django.db.models.fields.IntegerField', [], {})
        },
        u'meadery.parent': {
            'Meta': {'object_name': 'Parent'},
            'category': ('django.db.models.fields.IntegerField', [], {'default': '241'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        u'meadery.product': {
            'Meta': {'ordering': "['-is_active', '-created_at']", 'object_name': 'Product'},
            'abv': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '4', 'decimal_places': '2'}),
            'batchletter': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'bottled_date': ('django.db.models.fields.DateField', [], {}),
            'bottled_sg': ('django.db.models.fields.DecimalField', [], {'default': "'0.000'", 'max_digits': '4', 'decimal_places': '3'}),
            'brewed_date': ('django.db.models.fields.DateField', [], {}),
            'brewed_sg': ('django.db.models.fields.DecimalField', [], {'default': "'0.000'", 'max_digits': '4', 'decimal_places': '3'}),
            'brewname': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_bestseller': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'parent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['meadery.Parent']", 'unique': 'True', 'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'meadery.productreview': {
            'Meta': {'object_name': 'ProductReview'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Product']"}),
            'rating': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '5'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'meadery.recipe': {
            'Meta': {'object_name': 'Recipe', '_ormbases': [u'meadery.Parent']},
            u'parent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['meadery.Parent']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'meadery.sample': {
            'Meta': {'object_name': 'Sample'},
            'batch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Batch']"}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'sg': ('django.db.models.fields.DecimalField', [], {'default': "'0.000'", 'max_digits': '4', 'decimal_places': '3'}),
            'temp': ('django.db.models.fields.IntegerField', [], {'default': '60'})
        }
    }

    complete_apps = ['meadery']
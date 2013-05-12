# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_table(u'meadery_newingredientitem', u'meadery_ingredientitem')
        db.rename_table(u'meadery_newrecipe', u'meadery_recipe')
        db.rename_table(u'meadery_newproduct', u'meadery_product')
        db.rename_table(u'meadery_newbatch', u'meadery_batch')

        # Changing field 'Sample.batch'
        db.alter_column(u'meadery_sample', 'batch_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Batch']))

        # Changing field 'ProductReview.product'
        db.alter_column(u'meadery_productreview', 'product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Product']))

    def backwards(self, orm):
        db.rename_table(u'meadery_ingredientitem', u'meadery_newingredientitem')
        db.rename_table(u'meadery_recipe', u'meadery_newrecipe')
        db.rename_table(u'meadery_product', u'meadery_newproduct')
        db.rename_table(u'meadery_batch', u'meadery_newbatch')

        # Changing field 'Sample.batch'
        db.alter_column(u'meadery_sample', 'batch_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.NewBatch']))

        # Changing field 'ProductReview.product'
        db.alter_column(u'meadery_productreview', 'product_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.NewProduct']))

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
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Recipe']", 'null': 'True', 'on_delete': 'models.SET_NULL'}),
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

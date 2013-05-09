# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'HoneyItem'
        db.delete_table(u'meadery_honeyitem')

        # Deleting model 'WarmItem'
        db.delete_table(u'meadery_warmitem')

        # Deleting model 'Yeast'
        db.delete_table(u'meadery_yeast')

        # Deleting model 'Honey'
        db.delete_table(u'meadery_honey')

        # Deleting model 'FlavorItem'
        db.delete_table(u'meadery_flavoritem')

        # Deleting model 'Flavor'
        db.delete_table(u'meadery_flavor')

        # Deleting model 'CoolItem'
        db.delete_table(u'meadery_coolitem')

        # Deleting model 'YeastItem'
        db.delete_table(u'meadery_yeastitem')

        # Deleting model 'Water'
        db.delete_table(u'meadery_water')

        # Adding model 'IngredientItem'
        db.create_table(u'meadery_ingredientitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Recipe'])),
            ('ingredient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Ingredient'])),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=3)),
            ('temp', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'meadery', ['IngredientItem'])

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


    def backwards(self, orm):
        # Adding model 'HoneyItem'
        db.create_table(u'meadery_honeyitem', (
            ('temp', self.gf('django.db.models.fields.IntegerField')()),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Recipe'])),
            ('honey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Honey'])),
            ('mass', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=3)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'meadery', ['HoneyItem'])

        # Adding model 'WarmItem'
        db.create_table(u'meadery_warmitem', (
            ('water', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Water'])),
            ('temp', self.gf('django.db.models.fields.IntegerField')()),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Recipe'])),
            ('volume', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=3)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'meadery', ['WarmItem'])

        # Adding model 'Yeast'
        db.create_table(u'meadery_yeast', (
            ('appellation', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('is_natural', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tolerance', self.gf('django.db.models.fields.IntegerField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'meadery', ['Yeast'])

        # Adding model 'Honey'
        db.create_table(u'meadery_honey', (
            ('appellation', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('is_natural', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('sg', self.gf('django.db.models.fields.DecimalField')(default='1.422', max_digits=4, decimal_places=3)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sh', self.gf('django.db.models.fields.DecimalField')(default='0.57', max_digits=3, decimal_places=2)),
        ))
        db.send_create_signal(u'meadery', ['Honey'])

        # Adding model 'FlavorItem'
        db.create_table(u'meadery_flavoritem', (
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Recipe'])),
            ('flavor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Flavor'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'meadery', ['FlavorItem'])

        # Adding model 'Flavor'
        db.create_table(u'meadery_flavor', (
            ('appellation', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('is_natural', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'meadery', ['Flavor'])

        # Adding model 'CoolItem'
        db.create_table(u'meadery_coolitem', (
            ('water', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Water'])),
            ('temp', self.gf('django.db.models.fields.IntegerField')()),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Recipe'])),
            ('volume', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=3)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'meadery', ['CoolItem'])

        # Adding model 'YeastItem'
        db.create_table(u'meadery_yeastitem', (
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Recipe'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('yeast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Yeast'])),
        ))
        db.send_create_signal(u'meadery', ['YeastItem'])

        # Adding model 'Water'
        db.create_table(u'meadery_water', (
            ('appellation', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('is_natural', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('sg', self.gf('django.db.models.fields.DecimalField')(default='1.000', max_digits=4, decimal_places=3)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sh', self.gf('django.db.models.fields.DecimalField')(default='1.00', max_digits=3, decimal_places=2)),
        ))
        db.send_create_signal(u'meadery', ['Water'])

        # Deleting model 'IngredientItem'
        db.delete_table(u'meadery_ingredientitem')

        # Deleting model 'Ingredient'
        db.delete_table(u'meadery_ingredient')


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
            'Meta': {'object_name': 'Batch', '_ormbases': [u'meadery.Recipe']},
            'batchletter': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'brewname': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'jars': ('django.db.models.fields.IntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['meadery.Recipe']"}),
            u'recipe_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['meadery.Recipe']", 'unique': 'True', 'primary_key': 'True'})
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
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Recipe']"}),
            'temp': ('django.db.models.fields.IntegerField', [], {})
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
            'category': ('django.db.models.fields.IntegerField', [], {'default': '241'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_bestseller': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meta_description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'meta_keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '255', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
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
            'Meta': {'object_name': 'Recipe'},
            'category': ('django.db.models.fields.IntegerField', [], {'default': '241'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'})
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
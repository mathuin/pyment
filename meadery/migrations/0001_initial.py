# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Honey'
        db.create_table(u'meadery_honey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('is_natural', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('appellation', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('sg', self.gf('django.db.models.fields.DecimalField')(default='1.422', max_digits=4, decimal_places=3)),
            ('sh', self.gf('django.db.models.fields.DecimalField')(default='0.57', max_digits=3, decimal_places=2)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'meadery', ['Honey'])

        # Adding model 'Water'
        db.create_table(u'meadery_water', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('is_natural', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('appellation', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('sg', self.gf('django.db.models.fields.DecimalField')(default='1.000', max_digits=4, decimal_places=3)),
            ('sh', self.gf('django.db.models.fields.DecimalField')(default='1.00', max_digits=3, decimal_places=2)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'meadery', ['Water'])

        # Adding model 'Flavor'
        db.create_table(u'meadery_flavor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('is_natural', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('appellation', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'meadery', ['Flavor'])

        # Adding model 'Yeast'
        db.create_table(u'meadery_yeast', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('is_natural', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('appellation', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tolerance', self.gf('django.db.models.fields.IntegerField')()),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal(u'meadery', ['Yeast'])

        # Adding model 'HoneyItem'
        db.create_table(u'meadery_honeyitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Recipe'])),
            ('honey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Honey'])),
            ('mass', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=3)),
            ('temp', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'meadery', ['HoneyItem'])

        # Adding model 'CoolItem'
        db.create_table(u'meadery_coolitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Recipe'])),
            ('water', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Water'])),
            ('volume', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=3)),
            ('temp', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'meadery', ['CoolItem'])

        # Adding model 'WarmItem'
        db.create_table(u'meadery_warmitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Recipe'])),
            ('water', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Water'])),
            ('volume', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=3)),
            ('temp', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'meadery', ['WarmItem'])

        # Adding model 'FlavorItem'
        db.create_table(u'meadery_flavoritem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Recipe'])),
            ('flavor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Flavor'])),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'meadery', ['FlavorItem'])

        # Adding model 'YeastItem'
        db.create_table(u'meadery_yeastitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Recipe'])),
            ('yeast', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Yeast'])),
            ('amount', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'meadery', ['YeastItem'])

        # Adding model 'Recipe'
        db.create_table(u'meadery_recipe', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.IntegerField')(default=241)),
        ))
        db.send_create_signal(u'meadery', ['Recipe'])

        # Adding model 'Batch'
        db.create_table(u'meadery_batch', (
            (u'recipe_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['meadery.Recipe'], unique=True, primary_key=True)),
            ('recipe', self.gf('django.db.models.fields.related.ForeignKey')(related_name='source', null=True, on_delete=models.SET_NULL, to=orm['meadery.Recipe'])),
            ('brewname', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('batchletter', self.gf('django.db.models.fields.CharField')(max_length=1)),
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
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('brewname', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('batchletter', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=255, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('category', self.gf('django.db.models.fields.IntegerField')(default=241)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_bestseller', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('meta_keywords', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('meta_description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
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
        # Deleting model 'Honey'
        db.delete_table(u'meadery_honey')

        # Deleting model 'Water'
        db.delete_table(u'meadery_water')

        # Deleting model 'Flavor'
        db.delete_table(u'meadery_flavor')

        # Deleting model 'Yeast'
        db.delete_table(u'meadery_yeast')

        # Deleting model 'HoneyItem'
        db.delete_table(u'meadery_honeyitem')

        # Deleting model 'CoolItem'
        db.delete_table(u'meadery_coolitem')

        # Deleting model 'WarmItem'
        db.delete_table(u'meadery_warmitem')

        # Deleting model 'FlavorItem'
        db.delete_table(u'meadery_flavoritem')

        # Deleting model 'YeastItem'
        db.delete_table(u'meadery_yeastitem')

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
            'Meta': {'object_name': 'Batch', '_ormbases': [u'meadery.Recipe']},
            'batchletter': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'brewname': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'event': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'jars': ('django.db.models.fields.IntegerField', [], {}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['meadery.Recipe']"}),
            u'recipe_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['meadery.Recipe']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'meadery.coolitem': {
            'Meta': {'object_name': 'CoolItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Recipe']"}),
            'temp': ('django.db.models.fields.IntegerField', [], {}),
            'volume': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '3'}),
            'water': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Water']"})
        },
        u'meadery.flavor': {
            'Meta': {'object_name': 'Flavor'},
            'appellation': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_natural': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        u'meadery.flavoritem': {
            'Meta': {'object_name': 'FlavorItem'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'flavor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Flavor']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Recipe']"})
        },
        u'meadery.honey': {
            'Meta': {'object_name': 'Honey'},
            'appellation': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_natural': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'sg': ('django.db.models.fields.DecimalField', [], {'default': "'1.422'", 'max_digits': '4', 'decimal_places': '3'}),
            'sh': ('django.db.models.fields.DecimalField', [], {'default': "'0.57'", 'max_digits': '3', 'decimal_places': '2'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'meadery.honeyitem': {
            'Meta': {'object_name': 'HoneyItem'},
            'honey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Honey']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mass': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '3'}),
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
        },
        u'meadery.warmitem': {
            'Meta': {'object_name': 'WarmItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Recipe']"}),
            'temp': ('django.db.models.fields.IntegerField', [], {}),
            'volume': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '3'}),
            'water': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Water']"})
        },
        u'meadery.water': {
            'Meta': {'object_name': 'Water'},
            'appellation': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_natural': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'sg': ('django.db.models.fields.DecimalField', [], {'default': "'1.000'", 'max_digits': '4', 'decimal_places': '3'}),
            'sh': ('django.db.models.fields.DecimalField', [], {'default': "'1.00'", 'max_digits': '3', 'decimal_places': '2'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'meadery.yeast': {
            'Meta': {'object_name': 'Yeast'},
            'appellation': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_natural': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'tolerance': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'meadery.yeastitem': {
            'Meta': {'object_name': 'YeastItem'},
            'amount': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'recipe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Recipe']"}),
            'yeast': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Yeast']"})
        }
    }

    complete_apps = ['meadery']
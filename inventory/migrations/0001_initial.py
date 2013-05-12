# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Warehouse'
        db.create_table(u'inventory_warehouse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('location', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Warehouse'])

        # Adding model 'Row'
        db.create_table(u'inventory_row', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('warehouse', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Warehouse'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=55, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Row'])

        # Adding unique constraint on 'Row', fields ['warehouse', 'number']
        db.create_unique(u'inventory_row', ['warehouse_id', 'number'])

        # Adding model 'Shelf'
        db.create_table(u'inventory_shelf', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('row', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Row'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=60, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Shelf'])

        # Adding unique constraint on 'Shelf', fields ['row', 'number']
        db.create_unique(u'inventory_shelf', ['row_id', 'number'])

        # Adding model 'Bin'
        db.create_table(u'inventory_bin', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('shelf', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Shelf'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=65, blank=True)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Bin'])

        # Adding unique constraint on 'Bin', fields ['shelf', 'number']
        db.create_unique(u'inventory_bin', ['shelf_id', 'number'])

        # Adding model 'Crate'
        db.create_table(u'inventory_crate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=10, blank=True)),
            ('capacity', self.gf('django.db.models.fields.IntegerField')(default=12)),
            ('bin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Bin'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Crate'])

        # Adding model 'Jar'
        db.create_table(u'inventory_jar', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Product'])),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=13, blank=True)),
            ('volume', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('crate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Crate'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Jar'])

        # Adding unique constraint on 'Jar', fields ['product', 'number']
        db.create_unique(u'inventory_jar', ['product_id', 'number'])


    def backwards(self, orm):
        # Removing unique constraint on 'Jar', fields ['product', 'number']
        db.delete_unique(u'inventory_jar', ['product_id', 'number'])

        # Removing unique constraint on 'Bin', fields ['shelf', 'number']
        db.delete_unique(u'inventory_bin', ['shelf_id', 'number'])

        # Removing unique constraint on 'Shelf', fields ['row', 'number']
        db.delete_unique(u'inventory_shelf', ['row_id', 'number'])

        # Removing unique constraint on 'Row', fields ['warehouse', 'number']
        db.delete_unique(u'inventory_row', ['warehouse_id', 'number'])

        # Deleting model 'Warehouse'
        db.delete_table(u'inventory_warehouse')

        # Deleting model 'Row'
        db.delete_table(u'inventory_row')

        # Deleting model 'Shelf'
        db.delete_table(u'inventory_shelf')

        # Deleting model 'Bin'
        db.delete_table(u'inventory_bin')

        # Deleting model 'Crate'
        db.delete_table(u'inventory_crate')

        # Deleting model 'Jar'
        db.delete_table(u'inventory_jar')


    models = {
        u'inventory.bin': {
            'Meta': {'ordering': "['shelf', 'number']", 'unique_together': "(('shelf', 'number'),)", 'object_name': 'Bin'},
            'capacity': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'shelf': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Shelf']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '65', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'inventory.crate': {
            'Meta': {'ordering': "['number']", 'object_name': 'Crate'},
            'bin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Bin']"}),
            'capacity': ('django.db.models.fields.IntegerField', [], {'default': '12'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '10', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'inventory.jar': {
            'Meta': {'ordering': "['created_at']", 'unique_together': "(('product', 'number'),)", 'object_name': 'Jar'},
            'crate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Crate']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Product']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '13', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'inventory.row': {
            'Meta': {'ordering': "['warehouse', 'number']", 'unique_together': "(('warehouse', 'number'),)", 'object_name': 'Row'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '55', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'warehouse': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Warehouse']"})
        },
        u'inventory.shelf': {
            'Meta': {'ordering': "['row', 'number']", 'unique_together': "(('row', 'number'),)", 'object_name': 'Shelf'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'row': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Row']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '60', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'inventory.warehouse': {
            'Meta': {'ordering': "['number']", 'object_name': 'Warehouse'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
        }
    }

    complete_apps = ['inventory']
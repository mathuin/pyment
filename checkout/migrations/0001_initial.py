# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Order'
        db.create_table(u'checkout_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal(u'checkout', ['Order'])

        # Adding model 'OrderItem'
        db.create_table(u'checkout_orderitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['meadery.Product'])),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkout.Order'])),
        ))
        db.send_create_signal(u'checkout', ['OrderItem'])

        # Adding model 'PickList'
        db.create_table(u'checkout_picklist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkout.Order'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'checkout', ['PickList'])

        # Adding model 'PickListItem'
        db.create_table(u'checkout_picklistitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('picklist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['checkout.PickList'])),
            ('jar', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Jar'])),
        ))
        db.send_create_signal(u'checkout', ['PickListItem'])


    def backwards(self, orm):
        # Deleting model 'Order'
        db.delete_table(u'checkout_order')

        # Deleting model 'OrderItem'
        db.delete_table(u'checkout_orderitem')

        # Deleting model 'PickList'
        db.delete_table(u'checkout_picklist')

        # Deleting model 'PickListItem'
        db.delete_table(u'checkout_picklistitem')


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
        u'checkout.order': {
            'Meta': {'object_name': 'Order'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'})
        },
        u'checkout.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkout.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['meadery.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'checkout.picklist': {
            'Meta': {'object_name': 'PickList'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkout.Order']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'checkout.picklistitem': {
            'Meta': {'object_name': 'PickListItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jar': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['inventory.Jar']"}),
            'picklist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['checkout.PickList']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        }
    }

    complete_apps = ['checkout']
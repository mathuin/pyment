# -*- coding: utf-8 -*-


from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('meadery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Submitted'), (2, b'Processed'), (3, b'Delivered'), (4, b'Cancelled')])),
                ('ip_address', models.GenericIPAddressField()),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1)),
                ('order', models.ForeignKey(to='checkout.Order', on_delete=models.CASCADE)),
                ('product', models.ForeignKey(to='meadery.Product', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='PickList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(default=1, choices=[(1, b'Submitted'), (2, b'Processed'), (4, b'Cancelled')])),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(to='checkout.Order', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='PickListItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jar', models.ForeignKey(to='inventory.Jar', on_delete=models.CASCADE)),
                ('picklist', models.ForeignKey(to='checkout.PickList', on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ['jar__crate__bin__shelf__row__warehouse__number', 'jar__crate__bin__shelf__row__number', 'jar__crate__bin__shelf__number', 'jar__crate__bin__number'],
            },
        ),
    ]

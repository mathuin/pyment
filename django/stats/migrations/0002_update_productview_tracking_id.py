# Generated by Django 2.0 on 2018-10-16 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("stats", "0001_initial")]

    operations = [migrations.AlterField(model_name="productview", name="tracking_id", field=models.CharField(default="", max_length=75))]

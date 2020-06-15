# Generated by Django 2.0 on 2018-10-16 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("inventory", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="bin", name="slug", field=models.SlugField(blank=True, help_text="Unique value for this bin page URL.", max_length=65)
        ),
        migrations.AlterField(
            model_name="row", name="slug", field=models.SlugField(blank=True, help_text="Unique value for this row page URL.", max_length=55)
        ),
        migrations.AlterField(
            model_name="shelf", name="slug", field=models.SlugField(blank=True, help_text="Unique value for this shelf page URL.", max_length=60)
        ),
        migrations.AlterField(
            model_name="warehouse", name="slug", field=models.SlugField(help_text="Unique value for warehouse page URL, created from name.", unique=True)
        ),
    ]

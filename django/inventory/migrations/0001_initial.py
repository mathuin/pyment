# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("meadery", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Bin",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("number", models.IntegerField()),
                ("slug", models.SlugField(help_text=b"Unique value for this bin page URL.", max_length=65, blank=True)),
                ("capacity", models.IntegerField(default=1)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["shelf", "number"]},
        ),
        migrations.CreateModel(
            name="Crate",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("number", models.IntegerField()),
                ("slug", models.SlugField(unique=True, max_length=10, blank=True)),
                ("capacity", models.IntegerField(default=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("bin", models.ForeignKey(to="inventory.Bin", on_delete=models.CASCADE)),
            ],
            options={"ordering": ["number"]},
        ),
        migrations.CreateModel(
            name="Jar",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("number", models.IntegerField()),
                ("slug", models.SlugField(unique=True, max_length=13, blank=True)),
                ("volume", models.IntegerField(default=1)),
                ("is_active", models.BooleanField(default=True)),
                ("is_available", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("crate", models.ForeignKey(to="inventory.Crate", on_delete=models.CASCADE)),
                ("product", models.ForeignKey(to="meadery.Product", on_delete=models.CASCADE)),
            ],
            options={"ordering": ["created_at"]},
        ),
        migrations.CreateModel(
            name="Row",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("number", models.IntegerField()),
                ("slug", models.SlugField(help_text=b"Unique value for this row page URL.", max_length=55, blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["warehouse", "number"]},
        ),
        migrations.CreateModel(
            name="Shelf",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("number", models.IntegerField()),
                ("slug", models.SlugField(help_text=b"Unique value for this shelf page URL.", max_length=60, blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("row", models.ForeignKey(to="inventory.Row", on_delete=models.CASCADE)),
            ],
            options={"ordering": ["row", "number"], "verbose_name_plural": "Shelves"},
        ),
        migrations.CreateModel(
            name="Warehouse",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("number", models.IntegerField()),
                ("slug", models.SlugField(help_text=b"Unique value for warehouse page URL, created from name.", unique=True)),
                ("location", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["number"]},
        ),
        migrations.AddField(model_name="row", name="warehouse", field=models.ForeignKey(to="inventory.Warehouse", on_delete=models.CASCADE)),
        migrations.AddField(model_name="bin", name="shelf", field=models.ForeignKey(to="inventory.Shelf", on_delete=models.CASCADE)),
        migrations.AlterUniqueTogether(name="shelf", unique_together=set([("row", "number")])),
        migrations.AlterUniqueTogether(name="row", unique_together=set([("warehouse", "number")])),
        migrations.AlterUniqueTogether(name="jar", unique_together=set([("product", "number")])),
        migrations.AlterUniqueTogether(name="bin", unique_together=set([("shelf", "number")])),
    ]

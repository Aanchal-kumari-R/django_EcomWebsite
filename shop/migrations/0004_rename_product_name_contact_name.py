# Generated by Django 5.0.7 on 2024-08-15 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='product_name',
            new_name='name',
        ),
    ]

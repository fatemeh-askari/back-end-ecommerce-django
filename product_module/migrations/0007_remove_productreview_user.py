# Generated by Django 4.2.4 on 2023-08-25 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0006_productreview_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productreview',
            name='user',
        ),
    ]

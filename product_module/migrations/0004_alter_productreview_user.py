# Generated by Django 4.2.4 on 2023-08-25 18:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0001_initial'),
        ('product_module', '0003_alter_productcomment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productreview',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account_module.user'),
        ),
    ]

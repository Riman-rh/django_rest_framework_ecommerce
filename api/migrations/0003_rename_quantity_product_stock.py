# Generated by Django 4.0.5 on 2022-06-05 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_order_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='quantity',
            new_name='stock',
        ),
    ]

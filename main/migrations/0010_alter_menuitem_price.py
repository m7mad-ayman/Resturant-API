# Generated by Django 4.2.3 on 2024-09-11 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_orderitem_menuitem_alter_orderitem_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
    ]

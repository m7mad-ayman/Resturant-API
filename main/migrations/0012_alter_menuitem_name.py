# Generated by Django 4.2.3 on 2024-09-11 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_menuitem_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='name',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]

# Generated by Django 4.0.1 on 2022-01-21 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_alter_order_created_at_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='item_default.png', upload_to='menu_images/'),
        ),
    ]

# Generated by Django 3.0.7 on 2020-09-01 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GreenApp', '0030_auto_20200901_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile',
            field=models.ImageField(blank=True, default='logo.png', null=True, upload_to='profile'),
        ),
    ]

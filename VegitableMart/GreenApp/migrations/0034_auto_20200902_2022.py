# Generated by Django 3.0.7 on 2020-09-02 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GreenApp', '0033_auto_20200901_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile',
            field=models.ImageField(blank=True, default='profile/user-profile.png', null=True, upload_to='profile'),
        ),
    ]

# Generated by Django 2.2 on 2020-11-12 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybottles', '0008_auto_20201110_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='bottle_user',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='avatar/%Y%m%d/'),
        ),
    ]

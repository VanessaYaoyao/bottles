# Generated by Django 2.2 on 2020-11-07 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybottles', '0006_bottle_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bottles',
            name='replier',
            field=models.CharField(default='', max_length=128),
        ),
    ]
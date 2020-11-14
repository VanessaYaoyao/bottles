# Generated by Django 2.2 on 2020-11-05 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mybottles', '0003_bottles_replier'),
    ]

    operations = [
        migrations.CreateModel(
            name='finders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finder', models.CharField(default='打捞起瓶子的人', max_length=128)),
                ('thebottle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mybottles.bottles')),
            ],
        ),
    ]

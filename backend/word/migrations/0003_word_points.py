# Generated by Django 4.0.4 on 2022-04-29 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('word', '0002_remove_word_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]

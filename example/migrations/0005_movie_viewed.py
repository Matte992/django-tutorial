# Generated by Django 2.2 on 2019-09-29 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('example', '0004_remove_movie_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
    ]

# Generated by Django 3.1.2 on 2020-10-22 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_author_publication'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='public',
            field=models.BooleanField(default=False, verbose_name='Опубликовать'),
        ),
    ]

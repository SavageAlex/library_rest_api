# Generated by Django 3.2.8 on 2021-10-30 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='averageRating',
            new_name='average_rating',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='publishedDate',
            new_name='published_date',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='ratingsCount',
            new_name='ratings_count',
        ),
    ]
# Generated by Django 4.2.11 on 2024-05-02 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalperformance',
            old_name='quality_rating_svg',
            new_name='quality_rating_avg',
        ),
    ]

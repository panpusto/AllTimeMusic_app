# Generated by Django 4.0.5 on 2022-07-04 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music_app', '0003_alter_musicianband_year_from_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='subject',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
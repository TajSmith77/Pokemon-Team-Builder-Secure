# Generated by Django 5.0.4 on 2024-04-26 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='held_items',
            field=models.CharField(max_length=255, null=True),
        ),
    ]

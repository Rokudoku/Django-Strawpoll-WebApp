# Generated by Django 2.0 on 2018-02-03 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_aboutsection'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutsection',
            name='display_order',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]

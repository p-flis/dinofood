# Generated by Django 2.2 on 2019-06-20 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0017_auto_20190620_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='sum_rating',
            field=models.IntegerField(default=0),
        ),
    ]

# Generated by Django 4.2.5 on 2023-11-24 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0014_remove_question_weights_question_points_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='percentile',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]

# Generated by Django 4.2.5 on 2023-11-24 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teachers', '0019_remove_grade_max_score_course_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='max_score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

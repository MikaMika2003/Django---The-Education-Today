# Generated by Django 4.2.5 on 2023-09-25 04:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_posts_snippet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='snippet',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='account.posts')),
            ],
        ),
    ]

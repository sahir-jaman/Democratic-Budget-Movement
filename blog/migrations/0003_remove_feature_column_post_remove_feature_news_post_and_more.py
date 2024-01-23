# Generated by Django 5.0.1 on 2024-01-20 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_post_description_alter_post_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feature_column',
            name='post',
        ),
        migrations.RemoveField(
            model_name='feature_news',
            name='post',
        ),
        migrations.DeleteModel(
            name='MediaCoverage',
        ),
        migrations.AddField(
            model_name='post',
            name='teaser',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('publish', 'Publish'), ('unpublish', 'Unpublish')], default='publish', max_length=20),
        ),
        migrations.DeleteModel(
            name='Feature_column',
        ),
        migrations.DeleteModel(
            name='Feature_news',
        ),
    ]

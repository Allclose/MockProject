# Generated by Django 2.2 on 2022-01-05 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0014_db_project_catch_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_project',
            name='catch',
            field=models.BooleanField(default=False),
        ),
    ]
# Generated by Django 2.2 on 2021-12-22 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0008_auto_20211222_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_project',
            name='state',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='db_mock',
            name='state',
            field=models.BooleanField(default=True),
        ),
    ]

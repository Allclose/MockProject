# Generated by Django 2.2 on 2022-02-23 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0020_auto_20220221_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='db_api',
            name='result',
        ),
        migrations.AddField(
            model_name='db_api',
            name='check',
            field=models.CharField(max_length=200, null=True),
        ),
    ]

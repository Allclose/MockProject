# Generated by Django 2.2 on 2022-02-23 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0021_auto_20220223_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='db_api',
            name='body',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='db_api',
            name='check',
            field=models.CharField(default=200, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='db_api',
            name='method',
            field=models.CharField(default='get', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='db_api',
            name='name',
            field=models.CharField(default='', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='db_api',
            name='url',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
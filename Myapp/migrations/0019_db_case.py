# Generated by Django 2.2 on 2022-01-13 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0018_db_api'),
    ]

    operations = [
        migrations.CreateModel(
            name='DB_case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.CharField(max_length=20, null=True)),
                ('name', models.CharField(max_length=200, null=True)),
                ('body', models.CharField(max_length=500, null=True)),
            ],
        ),
    ]

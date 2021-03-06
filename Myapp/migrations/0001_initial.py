# Generated by Django 2.2 on 2021-12-14 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DB_mock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('state', models.BooleanField(default=False)),
                ('project_id', models.CharField(blank=True, max_length=30, null=True)),
                ('catch_url', models.CharField(blank=True, max_length=500, null=True)),
                ('mock_response_body', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DB_project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('user', models.CharField(blank=True, max_length=30, null=True)),
                ('run_counts', models.IntegerField(default=0, max_length=30)),
                ('mock_counts', models.IntegerField(default=0, max_length=30)),
            ],
        ),
    ]

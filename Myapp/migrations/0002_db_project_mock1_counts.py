# Generated by Django 2.2 on 2021-12-14 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='db_project',
            name='mock1_counts',
            field=models.IntegerField(default=0, max_length=30),
        ),
    ]

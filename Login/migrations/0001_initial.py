# Generated by Django 2.2.7 on 2019-11-28 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('ID', models.CharField(max_length=15, primary_key=True, serialize=False, verbose_name='用户名')),
                ('password', models.CharField(max_length=15, verbose_name='密码')),
            ],
            options={
                'db_table': 'User List',
            },
        ),
    ]

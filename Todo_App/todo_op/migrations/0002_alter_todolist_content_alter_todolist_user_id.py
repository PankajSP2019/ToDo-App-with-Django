# Generated by Django 4.1.4 on 2024-02-10 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_op', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='content',
            field=models.CharField(default='', max_length=5000),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]

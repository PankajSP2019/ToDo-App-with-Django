# Generated by Django 4.1.4 on 2024-02-12 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_op', '0002_alter_todolist_content_alter_todolist_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todolist',
            name='user_id',
        ),
        migrations.AddField(
            model_name='todolist',
            name='user_name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='status',
            field=models.CharField(default='', max_length=70),
        ),
        migrations.AlterField(
            model_name='todolist',
            name='title',
            field=models.CharField(default='', max_length=5000),
        ),
    ]

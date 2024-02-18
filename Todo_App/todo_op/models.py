from django.db import models

from django.db import models


class TodoList(models.Model):
    todo_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, default="")
    title = models.CharField(max_length=5000, default="")
    content = models.CharField(max_length=5000, default="")
    status = models.CharField(max_length=70, default="")

    def __str__(self):
        return f"uid-{self.user_name}     td_id-{self.todo_id}"

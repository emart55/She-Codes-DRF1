from django.db import models
from django.contrib.auth import get_user_model

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField(max_length=200)
    is_open = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title  # Display the project title as the representation


class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200, null=True)
    anonymous = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        related_name='pledges'
    )
    is_deleted = models.BooleanField(default=False)


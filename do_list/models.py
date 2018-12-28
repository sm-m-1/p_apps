from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class Note(models.Model):
    description = models.TextField(null=False)
    due_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    created_on = models.DateTimeField(default=datetime.now)

    def get_delete_url(self):
        return reverse("note_delete", kwargs={"id": self.id})

    def get_update_url(self):
        return reverse("note_update", kwargs={"id": self.id})

    def __str__(self):
        return self.description[:50]
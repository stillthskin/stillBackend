from django.db import models

class DynamicData(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    value = models.JSONField()  # dynamic JSON data
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.id}"

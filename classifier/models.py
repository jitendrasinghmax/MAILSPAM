from django.db import models

class EmailPrediction(models.Model):
    email_text = models.TextField()
    prediction = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)


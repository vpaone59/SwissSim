from django.db import models
from django.core import validators


class Tournament(models.Model):
    """Tournament model to manage the overall tournament."""

    name = models.CharField(max_length=255)
    current_stage = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_teams = models.IntegerField(
        default=0, validators=[validators.MaxValueValidator(32)]
    )

    def __str__(self):
        return str(self.name)

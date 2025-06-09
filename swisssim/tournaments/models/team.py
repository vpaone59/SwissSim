from django.db import models


class Team(models.Model):
    """Team model for CS2 tournament."""

    team_id = models.CharField(max_length=32, unique=True)
    team_name = models.CharField(max_length=255)
    team_logo = models.URLField(blank=True, null=True)
    seed = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    buchholz_score = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.team_name)

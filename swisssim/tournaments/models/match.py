from django.db import models
from .team import Team


class Match(models.Model):
    """Match model for tournament matches."""

    STAGE_CHOICES = [
        (1, "Stage 1"),
        (2, "Stage 2"),
        (3, "Stage 3") or (4, "Playoffs"),
    ]

    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("live", "Live"),
        ("completed", "Completed"),
    ]

    stage = models.IntegerField(choices=STAGE_CHOICES)
    match_number = models.IntegerField()
    team1 = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="team1_matches"
    )
    team2 = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="team2_matches"
    )
    team1_score = models.IntegerField(default=0)
    team2_score = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="scheduled"
    )
    match_date = models.DateTimeField(blank=True, null=True)
    winner = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        related_name="match_wins",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = "Matches"

    def __str__(self):
        return f"{self.team1} vs {self.team2} - Stage {self.stage}"

from django.db import models
from .team import Team
from .tournament import Tournament


class TournamentTeam(models.Model):
    """Links teams to tournaments and tracks stage participation."""

    tournament = models.ForeignKey(
        Tournament, on_delete=models.CASCADE, related_name="tournament_teams"
    )
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="tournament_entries"
    )
    starting_stage = models.IntegerField(
        default=1, choices=[(1, "Stage 1"), (2, "Stage 2"), (3, "Stage 3")]
    )
    seed = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # You might want to track team performance within this specific tournament
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    buchholz_score = models.FloatField(default=0.0)

    class Meta:
        unique_together = ("tournament", "team")
        verbose_name = "Tournament Team"
        verbose_name_plural = "Tournament Teams"

    def __str__(self):
        return f"{self.team.team_name} in {self.tournament.name}"

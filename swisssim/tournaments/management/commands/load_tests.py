from django.core.management.base import BaseCommand
from datetime import date, timedelta
from tournaments.models import Team, Tournament
from tournaments.utils import generate_next_stage_matches


class Command(BaseCommand):
    help = "Loads test data for the CS2 tournament"

    def handle(self, *args, **kwargs):
        # Create tournament
        tournament, created = Tournament.objects.get_or_create(
            name="Test Tournament",
            defaults={
                "current_stage": 1,
                "is_active": True,
                "start_date": date.today(),
                "end_date": date.today() + timedelta(days=7),
                "number_of_teams": 32,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Tournament {'created' if created else 'already exists'}: {tournament.name}"
            )
        )

        # Create teams (32 teams)
        teams_data = [
            {"team_id": "1", "team_name": "Cloud9", "seed": 1},
            {"team_id": "2", "team_name": "FaZe Clan", "seed": 2},
            {"team_id": "3", "team_name": "Natus Vincere", "seed": 3},
            {"team_id": "4", "team_name": "Team Liquid", "seed": 4},
            {"team_id": "5", "team_name": "G2 Esports", "seed": 5},
            {"team_id": "6", "team_name": "Heroic", "seed": 6},
            {"team_id": "7", "team_name": "Astralis", "seed": 7},
            {"team_id": "8", "team_name": "Vitality", "seed": 8},
            {"team_id": "9", "team_name": "OG", "seed": 9},
            {"team_id": "10", "team_name": "Fnatic", "seed": 10},
            {"team_id": "11", "team_name": "ENCE", "seed": 11},
            {"team_id": "12", "team_name": "MOUZ", "seed": 12},
            {"team_id": "13", "team_name": "BIG", "seed": 13},
            {"team_id": "14", "team_name": "NiP", "seed": 14},
            {"team_id": "15", "team_name": "Spirit", "seed": 15},
            {"team_id": "16", "team_name": "FURIA Esports", "seed": 16},
            {"team_id": "17", "team_name": "Complexity Gaming", "seed": 17},
            {"team_id": "18", "team_name": "Evil Geniuses", "seed": 18},
            {"team_id": "19", "team_name": "Liquid Academy", "seed": 19},
            {"team_id": "20", "team_name": "Renegades", "seed": 20},
            {"team_id": "21", "team_name": "Tyloo", "seed": 21},
            {"team_id": "22", "team_name": "#Unknown Team A#", "seed": 22},
            {"team_id": "23", "team_name": "#Unknown Team B#", "seed": 23},
            {"team_id": "24", "team_name": "#Unknown Team C#", "seed": 24},
            {"team_id": "25", "team_name": "#Unknown Team D#", "seed": 25},
            {"team_id": "26", "team_name": "#Unknown Team E#", "seed": 26},
            {"team_id": "27", "team_name": "#Unknown Team F#", "seed": 27},
            {"team_id": "28", "team_name": "#Unknown Team G#", "seed": 28},
            {"team_id": "29", "team_name": "#Unknown Team H#", "seed": 29},
            {"team_id": "30", "team_name": "#Unknown Team I#", "seed": 30},
            {"team_id": "31", "team_name": "#Unknown Team J#", "seed": 31},
            {"team_id": "32", "team_name": "#Unknown Team K#", "seed": 32},
        ]

        teams_created = 0
        for team_data in teams_data:
            team, created = Team.objects.get_or_create(
                team_id=team_data["team_id"],
                defaults={
                    "team_name": team_data["team_name"],
                    "seed": team_data["seed"],
                },
            )
            if created:
                teams_created += 1

        self.stdout.write(self.style.SUCCESS(f"Created {teams_created} teams"))

        # Generate initial matches
        generate_next_stage_matches(1)
        self.stdout.write(self.style.SUCCESS("Generated initial matches for Stage 1"))

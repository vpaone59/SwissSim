from django.core.management.base import BaseCommand
from datetime import date, timedelta
from tournaments.models import Team, Tournament
from tournaments.utils import generate_next_stage_matches


class Command(BaseCommand):
    help = "Loads test data for the CS2 tournament"

    def handle(self, *args, **kwargs):
        # Create tournament
        tournament, created = Tournament.objects.get_or_create(
            name="Austin Major 2025",
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

        # Create teams using actual Austin Major 2025 teams
        teams_data = [
            # Europe (16 teams)
            {
                "team_id": "1",
                "team_name": "Team Vitality",
                "region": "Europe",
            },
            {"team_id": "2", "team_name": "MOUZ", "region": "Europe"},
            {"team_id": "3", "team_name": "Team Spirit", "region": "Europe"},
            {
                "team_id": "4",
                "team_name": "Aurora Gaming",
                "region": "Europe",
            },
            {
                "team_id": "5",
                "team_name": "Natus Vincere",
                "region": "Europe",
            },
            {"team_id": "6", "team_name": "G2 Esports", "region": "Europe"},
            {
                "team_id": "7",
                "team_name": "Team Falcons",
                "region": "Europe",
            },
            {"team_id": "8", "team_name": "FaZe Clan", "region": "Europe"},
            {"team_id": "9", "team_name": "3DMAX", "region": "Europe"},
            {
                "team_id": "10",
                "team_name": "Virtus.pro",
                "region": "Europe",
            },
            {"team_id": "11", "team_name": "HEROIC", "region": "Europe"},
            {
                "team_id": "12",
                "team_name": "OG Esports",
                "region": "Europe",
            },
            {
                "team_id": "13",
                "team_name": "Nemiga Gaming",
                "region": "Europe",
            },
            {
                "team_id": "14",
                "team_name": "BetBoom Team",
                "region": "Europe",
            },
            {"team_id": "15", "team_name": "Metizport", "region": "Europe"},
            {
                "team_id": "16",
                "team_name": "B8 Esports",
                "region": "Europe",
            },
            # Americas (11 teams)
            {
                "team_id": "17",
                "team_name": "Team Liquid",
                "region": "Americas",
            },
            {
                "team_id": "18",
                "team_name": "paiN Gaming",
                "region": "Americas",
            },
            {
                "team_id": "19",
                "team_name": "FURIA Esports",
                "region": "Americas",
            },
            {"team_id": "20", "team_name": "MIBR", "region": "Americas"},
            {"team_id": "21", "team_name": "M80", "region": "Americas"},
            {
                "team_id": "22",
                "team_name": "Imperial Esports",
                "region": "Americas",
            },
            {
                "team_id": "23",
                "team_name": "Complexity Gaming",
                "region": "Americas",
            },
            {"team_id": "24", "team_name": "Fluxo", "region": "Americas"},
            {
                "team_id": "25",
                "team_name": "Wildcard",
                "region": "Americas",
            },
            {
                "team_id": "26",
                "team_name": "NRG Esports",
                "region": "Americas",
            },
            {"team_id": "27", "team_name": "Legacy", "region": "Americas"},
            # Asia (5 teams)
            {"team_id": "28", "team_name": "The MongolZ", "region": "Asia"},
            {
                "team_id": "29",
                "team_name": "Lynn Vision Gaming",
                "region": "Asia",
            },
            {"team_id": "30", "team_name": "FlyQuest", "region": "Asia"},
            {
                "team_id": "31",
                "team_name": "Chinggis Warriors",
                "region": "Asia",
            },
            {"team_id": "32", "team_name": "TYLOO", "region": "Asia"},
        ]

        teams_created = 0
        for team_data in teams_data:
            team, created = Team.objects.get_or_create(
                team_id=team_data["team_id"],
                defaults={
                    "team_name": team_data["team_name"],
                    "region": team_data.get("region", ""),
                },
            )
            if created:
                teams_created += 1
            else:
                # Update existing team data
                team.team_name = team_data["team_name"]
                if "region" in team_data and hasattr(team, "region"):
                    team.region = team_data["region"]
                team.save()

        self.stdout.write(self.style.SUCCESS(f"Created/updated {teams_created} teams"))

        # Generate initial matches
        generate_next_stage_matches(1)
        self.stdout.write(self.style.SUCCESS("Generated initial matches for Stage 1"))

def calculate_buchholz_scores():
    """Calculate Buchholz scores for all teams."""
    from .models import Team, Match

    teams = Team.objects.all()
    for team in teams:
        # Get all opponents the team has played against
        team1_matches = Match.objects.filter(team1=team, status="completed")
        team2_matches = Match.objects.filter(team2=team, status="completed")

        opponents = []
        for match in team1_matches:
            opponents.append(match.team2)
        for match in team2_matches:
            opponents.append(match.team1)

        # Calculate Buchholz score (sum of opponents' wins)
        buchholz_score = sum(opponent.wins for opponent in opponents)

        # Update team's Buchholz score
        team.buchholz_score = buchholz_score
        team.save()


def generate_next_stage_matches(stage):
    """Generate matches for the next stage based on Swiss system rules."""
    from .models import Team, Match, Tournament
    from django.db.models import Q

    tournament = Tournament.objects.filter(is_active=True).first()
    if not tournament:
        return

    # Calculate Buchholz scores
    calculate_buchholz_scores()

    # Get teams ordered by wins and Buchholz score
    teams = list(Team.objects.all().order_by("-wins", "-buchholz_score"))

    # Create match pairings based on Swiss system
    # In Swiss, teams with same record play each other
    matches_to_create = []

    # Group teams by win count
    win_groups = {}
    for team in teams:
        if team.wins not in win_groups:
            win_groups[team.wins] = []
        win_groups[team.wins].append(team)

    # For each group, create matches
    match_number = 1
    for win_count in sorted(win_groups.keys(), reverse=True):
        group = win_groups[win_count]
        # Sort by Buchholz within the group
        group.sort(key=lambda x: x.buchholz_score, reverse=True)

        # Create matches within this group
        while len(group) >= 2:
            team1 = group.pop(0)
            team2 = group.pop(0)

            # Avoid rematches if possible
            previous_match_exists = Match.objects.filter(
                (Q(team1=team1) & Q(team2=team2)) | (Q(team1=team2) & Q(team2=team1))
            ).exists()

            if previous_match_exists and len(group) > 0:
                # Put team1 back and try the next one
                group.insert(0, team1)
                team1 = group.pop(0)

            # Create the match
            matches_to_create.append(
                Match(
                    stage=stage,
                    match_number=match_number,
                    team1=team1,
                    team2=team2,
                    status="scheduled",
                )
            )
            match_number += 1

    # Bulk create the matches
    Match.objects.bulk_create(matches_to_create)

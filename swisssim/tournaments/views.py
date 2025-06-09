from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Match, Tournament


def tournament_home(request):
    """Display the main tournament page."""
    tournament = Tournament.objects.filter(is_active=True).first()
    if not tournament:
        return render(request, "tournaments/no_tournament.html")

    current_stage = tournament.current_stage
    teams = Team.objects.all().order_by("-wins", "-buchholz_score")
    matches = Match.objects.filter(stage=current_stage).order_by("match_number")

    return render(
        request,
        "tournaments/home.html",
        {
            "tournament": tournament,
            "teams": teams,
            "matches": matches,
        },
    )


def tournament_detail(request, tournament_id):
    """Display detailed information about a specific tournament."""
    tournament = get_object_or_404(Tournament, id=tournament_id)
    teams = Team.objects.all().order_by("-wins", "-buchholz_score")
    matches = Match.objects.filter(stage=tournament.current_stage).order_by(
        "match_number"
    )
    edit_mode = request.GET.get("edit_tournament") == "true" and request.user.is_staff

    return render(
        request,
        "tournaments/tournament_details.html",
        {
            "tournament": tournament,
            "teams": teams,
            "matches": matches,
            "edit_mode": edit_mode,
        },
    )


def team_detail(request, team_id):
    """Display detailed information about a team."""
    team = get_object_or_404(Team, team_id=team_id)
    matches = Match.objects.filter(team1=team) | Match.objects.filter(team2=team)
    edit_mode = request.GET.get("edit_team_name") == "true" and request.user.is_staff

    return render(
        request,
        "tournaments/team_details.html",
        {
            "team": team,
            "matches": matches,
            "edit_mode": edit_mode,
        },
    )


def stage_view(request, stage_number):
    """Display matches for a specific stage."""
    tournament = Tournament.objects.filter(is_active=True).first()
    if not tournament:
        return redirect("tournament_home")

    matches = Match.objects.filter(stage=stage_number).order_by("match_number")
    teams = Team.objects.all().order_by("-wins", "-buchholz_score")

    return render(
        request,
        "tournaments/stage.html",
        {
            "tournament": tournament,
            "stage": stage_number,
            "matches": matches,
            "teams": teams,
        },
    )


def standings(request):
    """Display current team standings."""
    teams = Team.objects.all().order_by("-wins", "-buchholz_score")

    if request.headers.get("HX-Request"):
        # This is an HTMX request, return just the table
        return render(
            request, "tournaments/partials/standings_table.html", {"teams": teams}
        )

    # Regular request, return the full page
    return render(request, "tournaments/standings.html", {"teams": teams})


def match_details(request, match_id):
    """Return match details for HTMX."""
    match = get_object_or_404(Match, id=match_id)
    return render(request, "tournaments/partials/match_details.html", {"match": match})


def tier_list(request, tournament_id):
    """Display a tier list maker for a specific tournament."""
    tournament = get_object_or_404(Tournament, id=tournament_id)

    # Get all teams - we need to modify this since there's no direct tournament field
    # This assumes all teams are available for all tournaments
    # You might need to adjust this based on your actual data model
    teams = Team.objects.all().order_by("seed")

    return render(
        request,
        "tournaments/tier_list.html",
        {
            "tournament": tournament,
            "teams": teams,
        },
    )

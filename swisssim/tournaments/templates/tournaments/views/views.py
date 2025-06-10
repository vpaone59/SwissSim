from django.shortcuts import render, redirect, get_object_or_404
from ....models import Team, Match, Tournament, TournamentTeam
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.db.models import Q


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
    teams = (
        TournamentTeam.objects.filter(tournament=tournament)
        .select_related("team")
        .order_by("team__team_name")
    )
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
    teams = TournamentTeam.objects.filter(tournament=tournament).order_by("team")

    return render(
        request,
        "tournaments/tier_list.html",
        {
            "tournament": tournament,
            "teams": teams,
        },
    )


@user_passes_test(lambda u: u.is_staff)
def manage_tournament_teams(request, tournament_id):
    """Display the team management interface for admins."""
    tournament = get_object_or_404(Tournament, id=tournament_id)

    # Get tournament teams
    tournament_teams = (
        TournamentTeam.objects.filter(tournament=tournament)
        .select_related("team")
        .order_by("team__team_name")
    )

    # Get teams not in tournament
    tournament_team_ids = tournament_teams.values_list("team_id", flat=True)
    available_teams = Team.objects.exclude(id__in=tournament_team_ids).order_by(
        "team_name"
    )

    return render(
        request,
        "tournaments/partials/manage_tournament_teams.html",
        {
            "tournament": tournament,
            "available_teams": available_teams,
            "tournament_teams": tournament_teams,
        },
    )


@user_passes_test(lambda u: u.is_staff)
def add_team_to_tournament(request, tournament_id, team_id):
    """Add a team to the tournament."""
    tournament = get_object_or_404(Tournament, id=tournament_id)
    team = get_object_or_404(Team, id=team_id)

    # Create new tournament team with default values
    TournamentTeam.objects.create(
        tournament=tournament,
        team=team,
        seed=TournamentTeam.objects.filter(tournament=tournament).count()
        + 1,  # Auto-increment seed
        starting_stage=1,
        is_active=True,
    )

    # Return updated lists
    return _render_team_lists(request, tournament)


@user_passes_test(lambda u: u.is_staff)
def remove_team_from_tournament(request, tournament_id, team_id):
    """Remove a team from the tournament."""
    tournament = get_object_or_404(Tournament, id=tournament_id)
    team = get_object_or_404(Team, id=team_id)

    # Delete the tournament team entry
    TournamentTeam.objects.filter(tournament=tournament, team=team).delete()

    # Return updated lists
    return _render_team_lists(request, tournament)


@user_passes_test(lambda u: u.is_staff)
def update_team_seed(request, tournament_id, team_id):
    """Update a team's seed in the tournament."""
    tournament = get_object_or_404(Tournament, id=tournament_id)
    team = get_object_or_404(Team, id=team_id)
    tournament_team = get_object_or_404(
        TournamentTeam, tournament=tournament, team=team
    )

    # Update seed
    seed = request.POST.get("seed")
    if seed and seed.isdigit():
        tournament_team.seed = int(seed)
        tournament_team.save()

    return HttpResponse(status=204)  # No content response


@user_passes_test(lambda u: u.is_staff)
def update_team_stage(request, tournament_id, team_id):
    """Update a team's starting stage in the tournament."""
    tournament = get_object_or_404(Tournament, id=tournament_id)
    team = get_object_or_404(Team, id=team_id)
    tournament_team = get_object_or_404(
        TournamentTeam, tournament=tournament, team=team
    )

    # Update starting stage
    starting_stage = request.POST.get("starting_stage")
    if starting_stage and starting_stage.isdigit():
        tournament_team.starting_stage = int(starting_stage)
        tournament_team.save()

    return HttpResponse(status=204)  # No content response


@user_passes_test(lambda u: u.is_staff)
def search_available_teams(request, tournament_id):
    """Search for available teams."""
    tournament = get_object_or_404(Tournament, id=tournament_id)
    query = request.POST.get("query", "")

    # Get tournament team IDs
    tournament_team_ids = TournamentTeam.objects.filter(
        tournament=tournament
    ).values_list("team_id", flat=True)

    # Filter available teams
    available_teams = Team.objects.exclude(id__in=tournament_team_ids)

    if query:
        available_teams = available_teams.filter(
            Q(team_name__icontains=query) | Q(region__icontains=query)
        )

    available_teams = available_teams.order_by("team_name")

    return render(
        request,
        "tournaments/partials/available_teams_list.html",
        {"tournament": tournament, "available_teams": available_teams},
    )


@user_passes_test(lambda u: u.is_staff)
def search_tournament_teams(request, tournament_id):
    """Search for teams in the tournament."""
    tournament = get_object_or_404(Tournament, id=tournament_id)
    query = request.POST.get("query", "")

    # Filter tournament teams
    tournament_teams = TournamentTeam.objects.filter(
        tournament=tournament
    ).select_related("team")

    if query:
        tournament_teams = tournament_teams.filter(
            Q(team__team_name__icontains=query) | Q(team__region__icontains=query)
        )

    tournament_teams = tournament_teams.order_by("team__team_name")

    return render(
        request,
        "tournaments/partials/tournament_teams_list.html",
        {"tournament": tournament, "tournament_teams": tournament_teams},
    )


@user_passes_test(lambda u: u.is_staff)
def tournament_teams_view(request, tournament_id):
    """Return to the normal teams display."""
    tournament = get_object_or_404(Tournament, id=tournament_id)
    teams = (
        TournamentTeam.objects.filter(tournament=tournament)
        .select_related("team")
        .order_by("team__team_name")
    )

    return render(
        request,
        "tournaments/partials/tournament_teams_view.html",
        {
            "tournament": tournament,
            "teams": teams,
        },
    )


# Helper function for rendering team lists
def _render_team_lists(request, tournament):
    """Helper function to render both team lists."""
    # Get tournament teams
    tournament_teams = (
        TournamentTeam.objects.filter(tournament=tournament)
        .select_related("team")
        .order_by("team__team_name")
    )

    # Get teams not in tournament
    tournament_team_ids = tournament_teams.values_list("team_id", flat=True)
    available_teams = Team.objects.exclude(id__in=tournament_team_ids).order_by(
        "team_name"
    )

    # Render both lists and combine them
    available_html = render(
        request,
        "tournaments/partials/available_teams_list.html",
        {"tournament": tournament, "available_teams": available_teams},
    ).content.decode()

    tournament_html = render(
        request,
        "tournaments/partials/tournament_teams_list.html",
        {"tournament": tournament, "tournament_teams": tournament_teams},
    ).content.decode()

    return HttpResponse(available_html + tournament_html)

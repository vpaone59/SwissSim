from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.template.loader import render_to_string
from .utils import calculate_buchholz_scores
from .models import Team, Match, Tournament


@user_passes_test(lambda u: u.is_superuser)
def swiss_admin(request):
    """Admin interface for managing tournaments."""
    # Get current tournament if it exists
    current_tournament = Tournament.objects.filter(is_active=True).first()
    all_teams = Team.objects.all().order_by("team_name")

    # Handle form submission
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create_tournament":
            # Create a new tournament
            try:
                with transaction.atomic():
                    # Get form data
                    name = request.POST.get("tournament_name")
                    start_date = request.POST.get("start_date")
                    end_date = request.POST.get("end_date")

                    # Set all existing tournaments to inactive
                    Tournament.objects.update(is_active=False)

                    # Create new tournament
                    tournament = Tournament.objects.create(
                        name=name,
                        current_stage=1,
                        is_active=True,
                        start_date=start_date,
                        end_date=end_date,
                    )

                    messages.success(
                        request, f"Tournament '{name}' created successfully."
                    )
                    return HttpResponseRedirect(reverse("swiss_admin"))
            except Exception as e:
                messages.error(request, f"Error creating tournament: {str(e)}")

        elif action == "add_team":
            try:
                # Add a new team
                team_name = request.POST.get("team_name")
                team_id = request.POST.get("team_id", "")
                seed = request.POST.get("seed", 0)

                if not team_id:
                    team_id = "".join(team_name.split()).lower()[:32]

                team = Team.objects.create(
                    team_id=team_id, team_name=team_name, seed=seed
                )

                messages.success(request, f"Team '{team_name}' added successfully.")
                return HttpResponseRedirect(reverse("swiss_admin"))
            except Exception as e:
                messages.error(request, f"Error adding team: {str(e)}")

        elif action == "update_match":
            try:
                match_id = request.POST.get("match_id")
                team1_score = request.POST.get("team1_score", 0)
                team2_score = request.POST.get("team2_score", 0)
                status = request.POST.get("status", "scheduled")

                match = Match.objects.get(id=match_id)
                match.team1_score = team1_score
                match.team2_score = team2_score
                match.status = status

                if status == "completed":
                    if int(team1_score) > int(team2_score):
                        match.winner = match.team1
                        match.team1.wins += 1
                        match.team2.losses += 1
                    elif int(team2_score) > int(team1_score):
                        match.winner = match.team2
                        match.team2.wins += 1
                        match.team1.losses += 1

                    match.team1.save()
                    match.team2.save()

                match.save()

                # Recalculate Buchholz scores
                calculate_buchholz_scores()

                messages.success(request, f"Match updated successfully.")
                return HttpResponseRedirect(reverse("swiss_admin"))
            except Exception as e:
                messages.error(request, f"Error updating match: {str(e)}")

        elif action == "advance_stage":
            try:
                if not current_tournament:
                    messages.error(request, "No active tournament found.")
                    return HttpResponseRedirect(reverse("swiss_admin"))

                current_tournament.current_stage += 1
                current_tournament.save()

                messages.success(
                    request, f"Advanced to Stage {current_tournament.current_stage}."
                )
                return HttpResponseRedirect(reverse("swiss_admin"))
            except Exception as e:
                messages.error(request, f"Error advancing stage: {str(e)}")

    # Get matches for the current tournament
    matches = []
    if current_tournament:
        matches = Match.objects.filter(stage=current_tournament.current_stage).order_by(
            "match_number"
        )

    return render(
        request,
        "tournaments/swiss_admin.html",
        {
            "current_tournament": current_tournament,
            "all_teams": all_teams,
            "matches": matches,
        },
    )


@staff_member_required
def update_team_name(request, team_id):
    """Update team name via HTMX request."""
    team = get_object_or_404(Team, team_id=team_id)

    if request.method == "POST":
        team_name = request.POST.get("team_name")
        if team_name:
            team.team_name = team_name
            team.save()

    # Return the updated header section
    html = render_to_string(
        "tournaments/partials/team_header.html", {"team": team, "user": request.user}
    )
    return HttpResponse(html)


@staff_member_required
def update_tournament(request, tournament_id):
    """Update tournament details."""
    tournament = get_object_or_404(Tournament, id=tournament_id)

    if request.method == "POST":
        # Update tournament name if present
        if "name" in request.POST:
            tournament.name = request.POST.get("name")

        # Update other fields if present
        if "current_stage" in request.POST:
            tournament.current_stage = int(request.POST.get("current_stage"))

        if "start_date" in request.POST:
            start_date = request.POST.get("start_date")
            if start_date:
                tournament.start_date = start_date

        if "end_date" in request.POST:
            end_date = request.POST.get("end_date")
            if end_date:
                tournament.end_date = end_date

        if "number_of_teams" in request.POST:
            tournament.number_of_teams = int(request.POST.get("number_of_teams"))

        tournament.save()

    return redirect("tournament_detail", tournament_id=tournament_id)

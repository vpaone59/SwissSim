from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .templates.tournaments.views import views
from .admin_views import swiss_admin, update_team_name, update_tournament

urlpatterns = [
    path("", views.tournament_home, name="tournament_home"),
    path(
        "tournament/<int:tournament_id>/",
        views.tournament_detail,
        name="tournament_detail",
    ),
    path(
        "tournament/<int:tournament_id>/tier-list/", views.tier_list, name="tier_list"
    ),
    path(
        "tournament/<int:tournament_id>/update/",
        update_tournament,
        name="update_tournament",
    ),
    path("team/<str:team_id>/", views.team_detail, name="team_detail"),
    path(
        "team/<str:team_id>/update-name/",
        update_team_name,
        name="update_team_name",
    ),
    path("stage/<int:stage_number>/", views.stage_view, name="stage_view"),
    path("standings/", views.standings, name="standings"),
    path("match/<int:match_id>/", views.match_details, name="match_details"),
    path("admin/", swiss_admin, name="swiss_admin"),
    path(
        "login/",
        LoginView.as_view(
            template_name="tournaments/auth/login.html", next_page="/tournaments"
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(next_page="/tournaments", http_method_names=["get", "post"]),
        name="logout",
    ),
    path(
        "tournaments/<int:tournament_id>/manage-teams/",
        views.manage_tournament_teams,
        name="manage_tournament_teams",
    ),
    path(
        "tournaments/<int:tournament_id>/add-team/<int:team_id>/",
        views.add_team_to_tournament,
        name="add_team_to_tournament",
    ),
    path(
        "tournaments/<int:tournament_id>/remove-team/<int:team_id>/",
        views.remove_team_from_tournament,
        name="remove_team_from_tournament",
    ),
    path(
        "tournaments/<int:tournament_id>/update-team-seed/<int:team_id>/",
        views.update_team_seed,
        name="update_team_seed",
    ),
    path(
        "tournaments/<int:tournament_id>/update-team-stage/<int:team_id>/",
        views.update_team_stage,
        name="update_team_stage",
    ),
    path(
        "tournaments/<int:tournament_id>/search-available-teams/",
        views.search_available_teams,
        name="search_available_teams",
    ),
    path(
        "tournaments/<int:tournament_id>/search-tournament-teams/",
        views.search_tournament_teams,
        name="search_tournament_teams",
    ),
    path(
        "tournaments/<int:tournament_id>/teams-view/",
        views.tournament_teams_view,
        name="tournament_teams_view",
    ),
]

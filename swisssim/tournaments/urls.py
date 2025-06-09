from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    tournament_home,
    tournament_detail,
    team_detail,
    stage_view,
    standings,
    match_details,
    tier_list,
)
from .admin_views import swiss_admin, update_team_name, update_tournament

urlpatterns = [
    path("", tournament_home, name="tournament_home"),
    path(
        "tournament/<int:tournament_id>/",
        tournament_detail,
        name="tournament_detail",
    ),
    path("tournament/<int:tournament_id>/tier-list/", tier_list, name="tier_list"),
    path(
        "tournament/<int:tournament_id>/update/",
        update_tournament,
        name="update_tournament",
    ),
    path("team/<str:team_id>/", team_detail, name="team_detail"),
    path("team/<str:team_id>/update-name/", update_team_name, name="update_team_name"),
    path("stage/<int:stage_number>/", stage_view, name="stage_view"),
    path("standings/", standings, name="standings"),
    path("match/<int:match_id>/", match_details, name="match_details"),
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
]

from tournaments.models import Tournament


def tournaments_processor(request):
    """Add tournaments to context for all templates."""
    return {"tournaments": Tournament.objects.filter(is_active=True)}

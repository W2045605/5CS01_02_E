from django.shortcuts import render, get_object_or_404
from .models import Team, Session, Vote, HealthCard

def team_results(request):
    sessions = Session.objects.all()
    teams = Team.objects.all()
    votes_summary = {}
    selected_session = None
    selected_team = None

    if request.method == 'POST':
        session_id = request.POST.get('session')
        team_id = request.POST.get('team')

        selected_session = get_object_or_404(Session, id=session_id)
        selected_team = get_object_or_404(Team, id=team_id)

        votes = Vote.objects.filter(session=selected_session, team=selected_team)

        for card in HealthCard.objects.all().order_by('title'):
            card_votes = votes.filter(card=card)
            total_card_votes = card_votes.count()

            green_count = card_votes.filter(vote='green').count()
            amber_count = card_votes.filter(vote='amber').count()
            red_count = card_votes.filter(vote='red').count()

            if total_card_votes > 0:
                votes_summary[card.title] = {
                    'green': green_count,
                    'amber': amber_count,
                    'red': red_count,
                    'green_pct': round((green_count / total_card_votes) * 100),
                    'amber_pct': round((amber_count / total_card_votes) * 100),
                    'red_pct': round((red_count / total_card_votes) * 100),
                }
            else:
                votes_summary[card.title] = {
                    'green': 0,
                    'amber': 0,
                    'red': 0,
                    'green_pct': 0,
                    'amber_pct': 0,
                    'red_pct': 0,
                }

    return render(request, 'team_results.html', {
        'sessions': sessions,
        'teams': teams,
        'votes_summary': votes_summary,
        'selected_session': selected_session,
        'selected_team': selected_team,
    })

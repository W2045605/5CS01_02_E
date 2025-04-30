from django.shortcuts import render
from .models import Team, Session, Vote, HealthCard

def team_results(request):
    # Get all sessions and teams to show in dropdowns
    sessions = Session.objects.all()
    teams = Team.objects.all()

    # Variables for the selected session/team and vote summary
    votes_summary = {}
    selected_session = None
    selected_team = None

    # If the user submitted the form (POST request)
    if request.method == 'POST':
        session_id = request.POST.get('session')
        team_id = request.POST.get('team')

        # Get selected session and team objects from DB
        selected_session = Session.objects.get(id=session_id)
        selected_team = Team.objects.get(id=team_id)

        # Get all votes for that session and team
        votes = Vote.objects.filter(session=selected_session, team=selected_team)

        total_votes = votes.count()

        for card in HealthCard.objects.all().order_by('title'):
            card_votes = votes.filter(card=card)
            green = card_votes.filter(vote='green').count()
            amber = card_votes.filter(vote='amber').count()
            red = card_votes.filter(vote='red').count()

            if total_votes > 0:
                votes_summary[card.title] = {
                    'green': green,
                    'amber': amber,
                    'red': red,
                    'green_pct': round((green / total_votes) * 100),
                    'amber_pct': round((amber / total_votes) * 100),
                    'red_pct': round((red / total_votes) * 100),
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

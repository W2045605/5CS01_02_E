from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Session, Vote, HealthCard

@login_required
def session_list(request):
    sessions = Session.objects.order_by('-start_date')
    return render(request, 'voting/session_list.html', {'sessions': sessions})

@login_required
def user_vote_chart(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    votes = Vote.objects.filter(user=request.user, session=session)

    data = {
        'labels': [],
        'votes': [],
    }

    for vote in votes:
        data['labels'].append(vote.card.card_name)
        data['votes'].append(vote.vote_status)

    return render(request, 'voting/vote_chart.html', {
        'session': session,
        'data': data,
    })

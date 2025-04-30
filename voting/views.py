
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Vote, HealthCard, Session

@login_required
def submit_vote(request):
    if request.user.userprofile.role != 'engineer':
        return HttpResponseForbidden("Only engineers can submit votes.")
    
    if request.method == 'POST':
        card_id = request.POST.get('card')
        session_id = request.POST.get('session')
        vote_value = request.POST.get('vote')
        feedback = request.POST.get('feedback', '')

        Vote.objects.create(
            user=request.user,
            card_id=card_id,
            session_id=session_id,
            vote_status=vote_value,
            feedback=feedback
        )
        return redirect('session_list')

    cards = HealthCard.objects.all()
    sessions = Session.objects.all()
    return render(request, 'voting/submit_vote.html', {'cards': cards, 'sessions': sessions})


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


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


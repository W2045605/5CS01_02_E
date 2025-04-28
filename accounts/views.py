from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Session, Card, UserCardProgress

@login_required
def session_list(request):
    sessions = Session.objects.all()
    return render(request, 'session_list.html', {'sessions': sessions})

@login_required
def session_detail(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    cards = Card.objects.filter(session=session)
    # Fetch user's progress for all cards in this session
    progress = {
        p.card.id: {'status': p.status, 'vote': p.vote}
        for p in UserCardProgress.objects.filter(user=request.user, session=session)
    }
    return render(request, 'session_detail.html', {
        'session': session,
        'cards': cards,
        'progress': progress
    })

@login_required
def submit_progress(request, session_id):
    if request.method == 'POST':
        card_id = request.POST.get('card_id')
        status = request.POST.get('status')
        vote = request.POST.get('vote') or None
        card = get_object_or_404(Card, id=card_id)
        UserCardProgress.objects.update_or_create(
            user=request.user,
            session_id=session_id,
            card=card,
            defaults={'status': status, 'vote': vote}
        )
    return redirect('session_detail', session_id=session_id)


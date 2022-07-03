from django.shortcuts import render, redirect
from django.db.models import Max, Q, Count
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from litreview.models import Ticket, Review, UserFollows


# Create your views here.


@login_required
def flux(request):
    try:
        follows = request.user.userfollows.all()
        tickets = Ticket.objects.filter(
            Q(user__in=follows) | Q(user=request.user))
        reviews = Review.objects.filter(
            Q(user__in=follows) | Q(user=request.user))
        articles = tickets.union(reviews).order_by('time_created')
    except AttributeError:
        articles = False
    context = {'articles': articles}
    return render(request, 'litreview/flux.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('flux')
        else:
            pass
    return render(request, 'registration/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login_v')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login_v')
    return render(request, 'registration/signup.html')

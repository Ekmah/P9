from django.shortcuts import render, redirect
from django.db.models import Max, Q, Count
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from litreview.models import Ticket, Review, UserFollows
from litreview.forms import AskCriticForm, AnswerCriticForm


# Create your views here.


@login_required
def flux(request):
    try:
        follows = UserFollows.objects.filter(user=request.user).values_list(
            'followed_user', flat=True)
        tickets = Ticket.objects.filter(
            Q(user__in=follows) | Q(user=request.user))
        reviews = Review.objects.filter(
            Q(user__in=follows) | Q(user=request.user))
        print(tickets, reviews)
        articles = list(tickets.values())
        articles.extend(list(reviews.values()))
        articles = sorted(articles, key=lambda d: d['time_created'])
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


def ask_critic(request):
    if request.method == 'POST':
        form_ask = AskCriticForm(request.POST, request.FILES)
        if form_ask.is_valid():
            ticket = form_ask.save(commit=False)
            ticket.user = User.objects.get(id=request.user.id)
            ticket.save()
            return redirect('flux')
    else:
        form_ask = AskCriticForm()
    context = {'form_ask': form_ask}
    return render(request, 'litreview/critic_form.html', context)


def create_critic(request):
    if request.method == 'POST':
        form_ask = AskCriticForm(request.POST, request.FILES)
        form_answr = AnswerCriticForm(request.POST)

        if form_ask.is_valid() and form_answr.is_valid():
            ticket = form_ask.save(commit=False)
            ticket.user = User.objects.get(id=request.user.id)
            ticket.save()
            review = form_answr.save(commit=False)
            review.user = User.objects.get(id=request.user.id)
            review.ticket = ticket
            review.save()
            return redirect('flux')
    else:
        form_ask = AskCriticForm()
        form_answr = AnswerCriticForm()
    context = {'form_ask': form_ask, 'form_answr': form_answr}
    return render(request, 'litreview/critic_form.html', context)


def answer_critic(request, ticket_id):
    if request.method == 'POST':
        form_answr = AnswerCriticForm(request.POST)
        if form_answr.is_valid():
            review = form_answr.save(commit=False)
            review.user = User.objects.get(id=request.user.id)
            review.save()
            return redirect('flux')
    else:
        form_answr = AnswerCriticForm()
    context = {'form_answr': form_answr}
    return render(request, 'litreview/critic_form.html', context)


def modify_critic(request):
    pass


def modify_ask(request):
    pass


def follows(request):
    users_following = UserFollows.objects.filter(
        user=request.user).values_list('followed_user', flat=True)
    users_followed = UserFollows.objects.filter(user=request.user).values_list(
        'user', flat=True)


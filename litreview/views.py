from itertools import chain
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from litreview.models import Ticket, Review, UserFollows
from litreview.forms import AskCriticForm, AnswerCriticForm


@login_required
def flux(request):
    try:
        follows = UserFollows.objects.filter(user=request.user).values_list(
            'followed_user', flat=True)
        tickets = Ticket.objects.filter(
            Q(user__in=follows) | Q(user=request.user))
        reviews = Review.objects.filter(
            Q(user__in=follows) | Q(user=request.user))
        articles = sorted(chain(tickets, reviews),
                          key=lambda d: d.time_created, reverse=True)
    except AttributeError:
        articles = False
    context = {'articles': articles}
    return render(request, 'litreview/flux.html', context)


@login_required
def posts(request):
    if request.method == 'POST':
        if 'delete_ask' in request.POST:
            Ticket.objects.get(id=request.POST['delete_ask']).delete()
        if 'delete_review' in request.POST:
            Review.objects.get(id=request.POST['delete_review']).delete()
    try:
        tickets = Ticket.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)
        articles = sorted(chain(tickets, reviews),
                          key=lambda d: d.time_created, reverse=True)
    except AttributeError:
        articles = False
    context = {'articles': articles, 'posts': True}
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


@login_required
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


@login_required
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


@login_required
def answer_critic(request, ticket_id):
    ticket = False
    if request.method == 'POST':
        form_answr = AnswerCriticForm(request.POST)
        if form_answr.is_valid():
            review = form_answr.save(commit=False)
            review.user = User.objects.get(id=request.user.id)
            review.ticket = Ticket.objects.get(id=ticket_id)
            review.save()
            return redirect('flux')
    else:
        form_answr = AnswerCriticForm()
        ticket = Ticket.objects.get(id=ticket_id)
    context = {'form_answr': form_answr, 'ticket': ticket}
    return render(request, 'litreview/critic_form.html', context)


@login_required
def modify_critic(request, review_id):
    review = Review.objects.get(id=review_id)
    if request.method == 'POST':
        ticket = False
        form_answr = AnswerCriticForm(request.POST, instance=review)
        if form_answr.is_valid():
            review = form_answr.save(commit=False)
            review.save()
            return redirect('posts')
    else:
        form_answr = AnswerCriticForm(instance=review)
        ticket = review.ticket
    context = {'form_answr': form_answr, 'ticket': ticket}
    return render(request, 'litreview/critic_form.html', context)


@login_required
def modify_ask(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        form_ask = AskCriticForm(request.POST, request.FILES, instance=ticket)
        if form_ask.is_valid():
            ticket = form_ask.save(commit=False)
            ticket.user = User.objects.get(id=request.user.id)
            ticket.save()
            return redirect('posts')
    else:
        form_ask = AskCriticForm(instance=ticket)
    context = {'form_ask': form_ask}
    return render(request, 'litreview/critic_form.html', context)


@login_required
def follows(request):
    if request.method == 'POST':
        data = dict(request.POST.items())
        if 'add_follow' in request.POST:
            followed = User.objects.get(username=data['new_followed'])
            UserFollows.objects.get_or_create(user=request.user,
                                              followed_user=followed)
        if 'unfollow' in request.POST:
            relation = UserFollows.objects.get(user=request.user,
                                               followed_user=data['unfollow'])
            relation.delete()
    the_user_follow_those_users = [user.followed_user for user in
                                   UserFollows.objects.filter(
                                       user=request.user)]
    those_users_follow_the_user = [user.user for user in
                                   UserFollows.objects.filter(
                                       followed_user=request.user)]
    context = {'users_following': those_users_follow_the_user,
               'users_followed': the_user_follow_those_users}
    return render(request, 'litreview/follows.html', context)

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, UserManager
from django.contrib import messages 

# Create your views here.

def index(request):
    # Trip.objects.all().delete()
    return render(request, "friends_app/index.html")

def register(request):
    check = User.objects.register(
        request.POST["name"],
        request.POST["username"],
        request.POST["password"],
        request.POST["confirm"],
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")
    else:
        request.session["user_id"] = check["user"].id
        messages.add_message(request, messages.SUCCESS, "Welcome to Friends App, {}".format(request.POST["username"]))
        return redirect("/dashboard")

def login(request):
    print 'Test register'
    print request.POST
    check = User.objects.login(
        request.POST["username"],
        request.POST["password"]
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")
    else:
        request.session["user_id"] = check["user"].id
        messages.add_message(request, messages.SUCCESS, "Welcome back, {}".format(check["user"].username))
        return redirect("/dashboard")

def dashboard(request):
    print 'testing dashboard'
    friend_ids=[]
    friends=User.friends.through.objects.filter(from_user_id=request.session['user_id'])
    friend_objs = []
    for friend in friends:
        friend_ids.append(friend.to_user_id)
    for friend_id in friend_ids:
        friend_objs.append(User.objects.get(id=friend_id))
    all_users=User.objects.all()
    not_friend_objs=[]
    for user in all_users:
        if user.id not in friend_ids and user.id!=request.session['user_id']:
            not_friend_objs.append(user)
    print request.session['user_id']
    print friend_objs
    request.session["friend"] = "friend1"
    data = {
        "friends": friend_objs,
        'not_friends': not_friend_objs
    }
    return render(request, "friends_app/dashboard.html", data)

def logout(request):
    request.session.clear()
    messages.add_message(request, messages.SUCCESS, "See you later")
    return redirect("/")

def view_profile(request, id):
    User.objects.get(id=id)
    data = {
        "user": User.objects.get(id=id)
        }
    return render(request, "friends_app/friend_profile.html", data)

def add_friend(request, id):
    friend = User.objects.get(id=id)
    user = User.objects.get(id=request.session["user_id"])
    if user != friend:
        user.friends.add(friend)
    return redirect("/dashboard")

def remove_friend(request, f_id):
    friends=User.friends.through.objects.filter(to_user_id=f_id)
    friends.delete()
    return redirect('/dashboard')



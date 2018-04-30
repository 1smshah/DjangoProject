# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
# Create your models here.

class UserManager(models.Manager):
    def register(self, name, username, password, confirm):
        errors = []
        if len(name) < 2:
            errors.append("Name must be 2 characters or more")

        if len(username) < 2:
            errors.append("Username must be 2 characters or more")

        if len(password) < 1:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be 8 characters or more")

        if len(confirm) < 1:
            errors.append("Confirm Password is required")
        elif password != confirm:
            errors.append("Confirm Password must match Password")

        response = {
            "errors": errors,
            "valid": True,
            "user": None 
        }

        if len(errors) > 0:
            response["valid"] = False
            response["errors"] = errors
        else:
            response["user"] = User.objects.create(
                name=name,
                username=username,
                password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            )

        return response

    def login(self, username, password):
        errors = []

        if len(username) < 1:
            errors.append("Userename is required")
        else:
            userMatchingUsername = User.objects.filter(username=username)
            if len(userMatchingUsername) == 0:
                errors.append("Unknown username")

        if len(password) < 1:
            errors.append("Password is required")
        elif len(password) < 8:
            errors.append("Password must be 8 characters or more")

        response = {
            "errors": errors,
            "valid": True,
            "user": None 
        }

        if len(errors) == 0:
            if bcrypt.checkpw(password.encode(), userMatchingUsername[0].password.encode()):
                response["user"] = userMatchingUsername[0]
            else:
                errors.append("Incorrect password")

        if len(errors) > 0:
            response["errors"] = errors
            response["valid"] = False

        return response

class User(models.Model):
    name = models.CharField(max_length=255) 
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    friends = models.ManyToManyField("self", related_name="user_friends", symmetrical=False)

    objects = UserManager()
from django.db import models
import re

class UserManager(models.Manager):
    def Validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name should be at least 3 characters'
        if len(postData['last_name']) < 3:
            errors['last_name'] = 'Last Name should be at least 4 characters'
        if len(postData['email']) < 1:
            errors['email'] = 'Email is required'
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invaild email address!"
        # check if the email is already in the database
        if User.objects.filter(email=postData['email']):
            # if the email is in the database display an error message that says "email already in use"
            errors['email'] = 'Email is already in use'  
        if len(postData['password']) < 5:
            errors['password'] = 'Password must be at least 4 characters'
        if not re.search(r'[A-Z]', postData['password']):
            errors['password'] = 'Password must contain at least one capital letter'
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]',postData['password']):
            errors['password'] = 'Password must contain at least one symbol'
        if postData['password'] != postData['confirmPw']:
            errors['confirmPw'] = 'Passwords must match'

        return errors

class Track(models.Model):
    title = models.CharField(max_length=256)
    link = models.URLField()
    duration = models.PositiveIntegerField()
    preview = models.URLField()
    album = models.ForeignKey(
        'Album',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title  

class Artist(models.Model):
    name = models.CharField(max_length=256)
    link = models.URLField()
    tracklist = models.URLField
    picture = models.URLField()
    picture_small = models.URLField()
    picture_medium = models.URLField()
    picture_big = models.URLField()

    def __str__(self):
        return self.name
    
class Album(models.Model):
    title = models.CharField(max_length=256)
    cover = models.URLField()
    cover_small = models.URLField()
    cover_medium = models.URLField()
    cover_big = models.URLField()

    def __str__(self):
        return self.title  
class User(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    password = models.CharField(max_length=256)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    favorite_tracks = models.ManyToManyField(Track, related_name='users_who_like', blank=True)
    favorite_artist = models.ManyToManyField(Artist, related_name='users_who_like', blank=True)
    favorite_album = models.ManyToManyField(Album, related_name='users_who_like', blank=True )
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    




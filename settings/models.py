from django.db import models

# Create your models here.


class SiteSetting(models.Model):
    email = models.EmailField()
    mobile_number = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    description = models.TextField()
    mailgun_domain = models.URLField()
    mailgun_Api_Key = models.CharField(max_length=500)
    code = models.CharField(max_length=50)


class SocialSetting(models.Model):
    discord = models.URLField()
    twitter = models.URLField()
    youTube = models.URLField()
    instagram = models.URLField()
    medium = models.URLField()
    telegram = models.URLField()
    reddit = models.URLField()
    github = models.URLField()
    code = models.CharField(max_length=50)


class PercentageSetting(models.Model):
    royalty = models.IntegerField()
    platform_share = models.IntegerField()
    code = models.CharField(max_length=50)

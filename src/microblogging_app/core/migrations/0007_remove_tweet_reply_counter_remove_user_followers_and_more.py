# Generated by Django 4.2.4 on 2023-08-22 11:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_alter_tweet_reply_to"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tweet",
            name="reply_counter",
        ),
        migrations.RemoveField(
            model_name="user",
            name="followers",
        ),
        migrations.AddField(
            model_name="user",
            name="following",
            field=models.ManyToManyField(db_table="followers", related_name="followers", to=settings.AUTH_USER_MODEL),
        ),
    ]
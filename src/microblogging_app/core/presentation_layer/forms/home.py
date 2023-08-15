from django import forms


class TweetForm(forms.Form):
    user = forms.CharField(label="Tweet", max_length=200, strip=True, required=False)
    reply_to = forms.CharField(label="Tweet Replyers", max_length=400, strip=True, required=False)
    reply_counter = forms.IntegerField(label="Reply counter", min_value=0, required=False)
    like = forms.IntegerField(label="Like", min_value=0, required=False)
    repost = forms.IntegerField(label="Reposts", min_value=0, required=False)
    tags = forms.CharField(label="Tags", max_length=20, strip=True, required=False)

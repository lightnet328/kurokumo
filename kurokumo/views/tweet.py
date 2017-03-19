from django.template import RequestContext
from django.shortcuts import render, redirect
from django.conf import settings
from twitter import *
import MeCab
from kumo.kumo import Kumo
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache

@csrf_protect
def tweet(request):
    if request.user.is_authenticated() and cache.get(request.session.session_key) is not None and request.method == "POST":
        social = request.user.social_auth.get(provider='twitter')
        access_token = social.extra_data['access_token']
        oauth_token = access_token['oauth_token']
        oauth_secret = access_token['oauth_token_secret']

        authentication = OAuth(
            oauth_token,
            oauth_secret,
            settings.SOCIAL_AUTH_TWITTER_KEY,
            settings.SOCIAL_AUTH_TWITTER_SECRET,
        )

        tm = Twitter(domain='upload.twitter.com', auth=authentication)
        image = cache.get(request.session.session_key)
        media_id = tm.media.upload(media_data=image)["media_id_string"]

        t = Twitter(auth=authentication)
        tweet = request.POST["tweet"]
        status = t.statuses.update(status=tweet, media_ids=media_id)
        if status["user"]["protected"]:
            context = {"screen_name": status["user"]["screen_name"], "status_id": status["id"]}
        else:
            oembed = t.statuses.oembed(_id=status["id"], hide_media=False)
            context = {"oembed": oembed}
        context.update({"login": True, "protected": status["user"]["protected"]})
        cache.delete(request.session.session_key)
        request.session.clear()

        return render(request, 'tweet.html', context)
    else:
        return redirect('/')

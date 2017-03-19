from django.template import RequestContext
from django.shortcuts import render, redirect
from django.conf import settings
from twitter import *
import MeCab
from kumo.kumo import Kumo
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache

@csrf_protect
def index(request):
    if request.user.is_authenticated():
        if cache.get(request.session.session_key) is None:
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

            t = Twitter(auth=authentication)
            mc = MeCab.Tagger(settings.MECAB["ARGUMENT"])
            kumo = Kumo(twitter=t, mecab= mc)
            kumo.generate({"font_path": settings.FONT_PATH})
            image = kumo.to_encoded_image()
            cache.set(request.session.session_key, image)
        context = {"image": cache.get(request.session.session_key), "login": True}
        return render(request, 'home.html', RequestContext(request, context))
    else:
        context = {"login": False}
        return render(request, 'top.html', context)

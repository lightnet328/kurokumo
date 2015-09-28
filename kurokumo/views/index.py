from django.shortcuts import render
from django.conf import settings
from twitter import *
import MeCab
from kumo.kumo import Kumo

def index(request):
    if request.user.is_authenticated():
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
        context = {"image": image}
        return render(request, 'index.html', context)

    return render(request, 'index.html')

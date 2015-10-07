# coding: utf8
from twitter import *
from xml.sax.saxutils import *
from . import normalize_neologd as Normalizer
import MeCab
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud
import io
import base64

class Kumo:
    def __init__(self, twitter, mecab):
        if isinstance(twitter, Twitter):
            self._twitter = twitter
        else:
            raise Exception('Instance is not Twitter')
        if isinstance(mecab, MeCab.Tagger):
            self._mecab = mecab
            self._mecab.parse('')
        else:
            raise Exception('Instance is not MeCab')

    def _get_user_timeline(self):
        account = self._twitter.account.verify_credentials()
        params = {
            "user_id": account["id"],
            "count": 200,
            "include_entities": 1,
        }
        timeline = self._twitter.statuses.user_timeline(**params)
        return timeline

    def _get_original_tweets(self, tweets):
        original_tweets = []
        for tweet in tweets:
            if "retweeted_status" in tweet:
                original_tweets.append(tweet["retweeted_status"])
            else:
                original_tweets.append(tweet)
        return original_tweets

    def _extract_text_from_tweets(self, tweets):
        texts = []
        for tweet in tweets:
            if "entities" in tweet:
                entities = tweet["entities"]
                if "urls" in entities:
                    for url in entities["urls"]:
                        tweet["text"] = tweet["text"].replace(url["url"], "")
                if "hashtags" in entities:
                    for hashtag in entities["hashtags"]:
                        tweet["text"] = tweet["text"].replace("#" + hashtag["text"], "")
                if "symbols" in entities:
                    for symbol in entities["symbols"]:
                        tweet["text"] = tweet["text"].replace("$" + symbol["text"], "")
                if "user_mentions" in entities:
                    for mention in entities["user_mentions"]:
                        tweet["text"] = tweet["text"].replace("@" + mention["screen_name"], "")
                if "media" in entities:
                    for media in entities["media"]:
                        tweet["text"] = tweet["text"].replace(media["url"], "")
            texts.append(unescape(tweet["text"]))
        return texts

    def _normalize_texts(self, texts):
        normalized_texts = []
        for text in texts:
            normalized_texts.append(Normalizer.normalize_neologd(text))
        return normalized_texts

    def _feature_to_dict(self, feature):
        keys = [
            "品詞",
            "品詞細分類1",
            "品詞細分類2",
            "品詞細分類3",
            "活用形",
            "活用型",
            "原形",
            "読み",
            "発音",
        ]
        values = feature.split(",")
        feature_dict = {}
        for key in range(len(keys) - 1):
            if key < len(values):
                feature_dict[keys[key]] = values[key]
        return feature_dict

    def _is_ignore_feature(self, feature):
        ignore = {
            "品詞": ["助詞", "助動詞", "連体詞", "副詞", "接頭詞", "感動詞", "記号", "BOS/EOS"],
            "品詞細分類1": ["非自立", "接尾", "数"],
            "活用形": ["サ変・スル", "五段・ラ行"]
        }
        is_partical_match = False
        for feature_key, feature_value in feature.items():
            if feature_key in ignore:
                for ignore_value in ignore[feature_key]:
                    if feature_value == ignore_value:
                        is_partical_match = True
                        break
        return is_partical_match

    def _get_dictionary_form(self, word, feature):
        if "原形" in feature and feature["原形"] != "*":
            return feature["原形"]
        else:
            return word

    def _get_normalized_texts_from_twitter(self):
        tweets = self._get_user_timeline()
        texts = self._get_original_tweets(tweets)
        texts = self._extract_text_from_tweets(texts)
        normalized_texts = self._normalize_texts(texts)
        return normalized_texts

    def _get_words(self):
        texts = self._get_normalized_texts_from_twitter()
        words = []
        for text in texts:
            node = self._mecab.parseToNode(text)
            while node:
                feature = self._feature_to_dict(node.feature)
                if self._is_ignore_feature(feature) == False:
                    word = self._get_dictionary_form(node.surface, feature)
                    words.append(word)
                node = node.next
        return words

    def _get_word_frequencies(self):
        words = self._get_words()
        counter = Counter(words)
        word_frequencies = counter.most_common()
        return word_frequencies

    def generate(self, params={}):
        default_params = {
            "background_color": "white",
            "width": 640,
            "height": 400,
        }
        if params:
            default_params.update(params)
        params = default_params
        word_frequencies = self._get_word_frequencies()
        self._wordcloud = WordCloud(**params).generate_from_frequencies(word_frequencies)

    def to_encoded_image(self):
        image = self._wordcloud.to_image()
        output = io.BytesIO()
        image.save(output, "png")
        encoded_image = base64.b64encode(output.getvalue()).decode('utf-8')
        return encoded_image

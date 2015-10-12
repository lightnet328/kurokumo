========
kurokumo
========
Web application to create a wordcloud from Twitter.

Features
--------
* Create a wordcloud from Twitter
* Post to created wordcloud

Requirements
------------
* Python 3.4.3
* MeCab
* mecab-ipadic-neologd
* Gulp
* Bower

Preparation
-----------
* Install Python 3.4.3
* Install MeCab
* Install mecab-ipadic-neologd
* Install Gulp (needs to compile sass)
* Install Bower (needs Pure)

Installation
------------
Install Kurokumo
~~~~~~~~~~~~~~~~
::

    pip install https://github.com/lightnet328/kurokumo

If such an error has occurred, try the following command
::

    wget -nc -P /tmp http://bugs.python.org/file25808/14894.patch
    patch -p3 -f -d (your python path)/distutils < /tmp/14894.patch
e.g. /usr/local/lib/python3.4/, /usr/local/pyenv/versions/3.4.3/lib/python3.4

Configure
~~~~~~~~~
::

    cd kurokumo/kurokumo
    # Edit SECRET_KEY, SOCIAL_AUTH_TWITTER_KEY, SOCIAL_AUTH_TWITTER_SECRET, MECAB["ARGUMENT"], FONT_PATH
    vi settings.py

Create database
~~~~~~~~~~~~~~~
::

    cd ../kurokumo
    python manage.py migrate

Install npm packages
~~~~~~~~~~~~~~~~~~~~
::

    npm install

Install bower packages
~~~~~~~~~~~~~~~~~~~~~~
::

    bower install

Compile scss
~~~~~~~~~~~~
::

    gulp sass

Run server
~~~~~~~~~~
::

    python manage.py runserver
see http://127.0.0.1:8000

License
-------
MIT

Copyright (c) 2015 lightnet328

See LICENSE.txt

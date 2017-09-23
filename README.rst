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
* Python 3.6.0
* MeCab
* mecab-ipadic-neologd
* Gulp
* Bower

Preparation
-----------
* Install Python 3.6.0
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

Configure
~~~~~~~~~
::

    cd kurokumo/kurokumo
    cp .env.example .env
    # Edit
    vim .env

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

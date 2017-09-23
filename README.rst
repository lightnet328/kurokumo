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
* Docker
* docker-compose

Setup
-----
Clone
~~~~~
::

    git clone https://github.com/lightnet328/kurokumo

Configure
~~~~~~~~~
::

    cd kurokumo
    cp .env.example .env
    # Edit
    vim .env

Create database
~~~~~~~~~~~~~~~
::

    python manage.py migrate

Run
~~~
::

    docker-compose -f docker-compose.development.yml up
see http://127.0.0.1:8080

License
-------
MIT

Copyright (c) 2015 lightnet328

See LICENSE.txt

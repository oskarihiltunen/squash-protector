squash! protector
=================

Requirements
------------

- Python 3.4
- `virtualenvwrapper <http://virtualenvwrapper.readthedocs.org/>`_
- `autoenv <https://github.com/kennethreitz/autoenv>`_


Development
-----------

Follow the instructions below to set up the development environment.

1. Set up the Heroku application Git remotes::

    $ git remote add production git@heroku.com:squash-protector.git

2. Create a new virtualenv::

    $ mkvirtualenv --python=$(which python3.4) squash-protector

3. Make the virtualenv activate automagically when traversing inside the
   project directory::

    $ echo -e "workon squash-protector\n" > .env

4. Create databases for development and testing::

    $ createdb squash-protector

5. Create database tables::

    $ alembic upgrade head

6. Finally, start the development server::

    $ python manage.py runserver

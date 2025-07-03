![A paper tray with a "!!!" poster with the text "ClubFeed"](static/logo/logo-black-on-transparent.svg "ClubFeed logo")

# ClubFeed: A tool for distraction-free school communication
## What is ClubFeed?
Well, it's not Instagram!

**ClubFeed** is a mix between Instagram's club communication usage, the simplicity of other school communication apps,
and Reddit's grouping of posts.

Once the ClubFeed admin sets up clubs, club owners and posters can post to them and anyone can follow clubs to see them
on their own ClubFeed.

## What does it use?
ClubFeed uses the _Django_ web framework, which is powered by _Python_.

## How do I set it up?
First, take a look at the [Django project website](https://www.djangoproject.com/).
After you know the basics of Django, create an environment file (`.env`) using the template from `.env.dist`.

Running `python3 manage.py runserver` will give you a _**development**_ server. _**Don't use it in production!**_

ClubFeed is compatible with SQLite and PostgreSQL.
SQLite is easier for development purposes, while PostgreSQL is more robust for production.

# `INSTALL.md`: Your guide to setting up a ClubFeed server
You should be familiar with technologies that ClubFeed uses, including:
- Python
- Django
- PostgreSQL
- Networking and general web hosting

## Software
- Python
- `requirements.txt` packages
- PostgreSQL

The latest version of Python and packages using a venv(-like) system is encouraged.

## Environment variables
Copy `.env.dist` to `.env` for the environment variables you will need to change.

## What you can do in the admin
First, remember to migrate your database (should be done after every ClubFeed upgrade or config change).

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

In a command line (Terminal, PowerShell) in the same directory as `manage.py`:

```shell
python3 manage.py createsuperuser
```

This will give you some prompts to enter a username, email, and password for the superuser account.
After you log in to ClubFeed, the Admin tab will appear, which is the administration interface (admin).

If you want to give others admin access, find their username in the Users section in the admin,
select the Staff option, and either:
- Select permissions
  - Has the advantage of being more fine-grained.
- Superuser access (all permissions)
  - Set-and-forget. Only give this to users you trust (superusers has full access!)

### Why is the admin calling ClubFeed "example.com"? What is Sites in the admin?
ClubFeed's site name is set in the Django "Sites framework."
Using a superuser account or another staff account with "Change site" permission, go to `/admin/sites/site/{pk}/change/`
where `{pk}` is the `SITE_ID` (primary key) in `.env`.
This name will also appear in other different locations, like the site's title bar.

Setting the site name and domain is the only feature using the Sites framework;
as Django was originally developed for a newspaper, the Sites framework could be used to associate articles with
multiple sites (for example, both a world news and an entertainment site), but this is not supported by ClubFeed.

Despite this, the individual user feeds shown on the home page will always be called "ClubFeeds."

## Configuring allauth social (single sign-on) accounts
allauth, the authentication system that ClubFeed uses, allows adding social authentication to create accounts.

To use this, take a look at the [allauth quick start](https://docs.allauth.org/en/latest/installation/quickstart.html),
find the `INSTALLED_APPS` that correspond with the providers you want to use
(starting with `'allauth.socialaccount.providers.'`), and add them to your `.env` file:

```dotenv
INSTALLED_APPS=allauth.socialaccount.providers.slack,allauth.socialaccount.providers.atlassian
```

Then, find the [provider in the allauth docs](https://docs.allauth.org/en/dev/socialaccount/providers/index.html),
register your app, replacing `http://localhost:8000` with `https://` followed by your ClubFeed server's domain name.

Lastly, in the admin, go to the Social applications section in the admin and replace the fields with the information you
received from the service.
If the guide asks you to add something to `SOCIALACCOUNT_PROVIDERS`, add the dictionary in (parse this in your head)
`SOCIALACCOUNT_PROVIDERS[0][serv_name]` to the Settings field.

## Change the ClubFeed logo
Replace `static/logo/sitelogo.svg` with an SVG logo.

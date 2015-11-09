=====
FHoSS-API
=====

FHoSS-API is a simple Django app to control FHoSS.
For each question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Install "django-fhossapi" from git::

    sudo pip install django-fhossapi
    notice: if you fail to install MysqlDBLib, check libmysqlclient-dev package installed.
            if not, you can install libmysqlclient-dev by apt-get (sudo apt-get install libmysqlclient-dev)

2. Add "fhossapi" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'rest_framework',
        'rest_framework.authtoken',
        'rest_framework_swagger',   # swagger optional
        'fhossapi',
    )

3. Add rest_framwork settings::

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
        )
    }

4. Add rest_framwork_swagger settings (swagger optional)::

    SWAGGER_SETTINGS = {
        'info': {
            'title': 'HSS APIs',
            'description': 'APIs for control FHoSS (FOKUS Home Subscriber Server).',
        },
    }

4. Include the fhossapi URLconf in your project urls.py like this::

    url(r'^fhossapi/', include('fhossapi.urls')),
    url(r'^fhossapi/docs/', include('rest_framework_swagger.urls')),    # swagger optional

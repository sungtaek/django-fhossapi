=====
FHoSS-API
=====

FHoSS-API is a simple Django app to control FHoSS.
For each question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Install "django-fhossapi" from git::

    $ sudo pip install git+http://10.251.31.45:8088/ims/django-fhossapi.git

* Notice:
if you fail to install MysqlDBLib, please check the libmysqlclient-dev package already installed.
if not, you can install libmysqlclient-dev by using apt-get
$ sudo apt-get install libmysqlclient-dev

2. Add "fhossapi" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'rest_framework',
        'rest_framework.authtoken',
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

4. Include the fhossapi URLconf in your project urls.py like this::

    ...
    url(r'^fhossapi/', include('fhossapi.urls')),
    ...


Add API document page (Optional)
-----------

1. Install "rest_framework_swagger" from git::

    $ sudo pip install rest_framework_swagger

2. Add "rest_framework_swagger" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'rest_framework_swagger',
        ...
    )

3. Add rest_framwork_swagger settings::

    SWAGGER_SETTINGS = {
        'info': {
            'title': 'HSS APIs',
            'description': 'APIs for control FHoSS (FOKUS Home Subscriber Server).',
        },
    }

4. Include the rest_framework_swagger URLconf in your project urls.py like this::

    ...
    url(r'^fhossapi/docs/', include('rest_framework_swagger.urls')),
    ...
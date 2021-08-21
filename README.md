# drf_scaffold

**Scaffold django rest apis like a champion** ⚡

## Overview

Coming from a ruby on rails ecosystem I've been always wondering if there's a CLI we can use with Django to generate a bare minimum setup for our apps like the one we have in rails, so I started looking a django CLI that does the same but couldn't find anything that suits my needs.. so I decided to create one.

This Library should help you generate a full **Rest API App structure** using one command:

```
python manage.py drf_scaffold blog Post title:charfield body:textfield author:foreignkey:Author
```

- **models.py** containing Models with all fields generated using CLI ⚡
- **admin.py** containing with the previous Models already registered ⚡
- **views.py** including Django Rest Framework ViewSets with all actions necessary for CRUD operations using Mixins, documented using swagger.⚡
- **urls.py** containing all needed URLs necessary for CRUD endpoints.⚡
- **serializers.py** contains Model Serializers for a bare minimum DRF setup to get started ⚡

## Installation and usage

⚠️ **This library assumes that you have setup your project with Django Rest Framework. if not, please refer to this guide first : [Getting Started with DRF](https://www.django-rest-framework.org/#installation)**

Currently as we don't have a package ready to use yet, please follow the instructions below:
Clone this repository :

```
git clone https://github.com/Abdenasser/drf_scaffold.git
```

And cd into the project directory :

```
cd drf_scaffold
```

Copy the `drf_scaffold_core` application folder (not the project folder) into your Django project.
Add the application to your INSTALLED_APPS like the following:

```
INSTALLED_APPS = [
    ...
    'drf_scaffold_core'
]

```

Enjoy running the CLI command as follow :

```
python manage.py drf_scaffold apps_folder_name/app_name Article title:charfield body:textfield author:foreignkey:Author category:foreignkey:Category
```

Don't forget to add the generated application to your INSTALLED_APPS:

```
INSTALLED_APPS = [
    ...,
    'your_scaffolded_app_name'
]
```

And in your project urls file add:

```
urlpatterns = [
    ...,
    path("your_scaffolded_app_name/", include("your_scaffolded_app_name.urls")),
]
```

## TODO

- write some tests

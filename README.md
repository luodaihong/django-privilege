django-privilege
================

A smart, simple django app to manage user,  group, permission easily.

# What can 'django-privilege' do for you? #
`django-privilege` is a django app, offering frequently-used permission mangement, include user, group, permission. It works on django build-in models, and supports South to migrate db data.

You can CRUD group, permission and relationships between them. Also you can create user, reset his password, switch his active status and superuser status.All features are humanized.

# How to install 'django-privilege'? #
`pip install https://github.com/luodaihong/django-privilege/archive/master.zip`

Tips:

    You should run syncdb before runserver after add django-privilege into project.

# How to download 'django-privilege' source code? #
`git clone https://github.com/luodaihong/django-privilege`

# More config? #

    You can set the following in your settings file.

- `PRIVILEGE_PAGE_SIZE`

 How many users or groups will be displayed in one page? Default is 20.

- `ACTIVE_WHEN_ADDED`

 Specify whether an user's account will immediately be active after added from `django-privilege`. Default is True.

 If set False, the account added from `django-privilege` will not be able to login.

- `SITE_NAME`

 Set you site's name. Default is 'HomePage' in English, '首页' in Chinese.

- `ACCESSIBLE_APPS`

 specify which app's permissions will be managered in `django-privilege`? Default is `ACCESSIBLE_APPS = ["privilege"]` . You can append your other app_names into it.

 It is strongly recommended to keep "privilege" in the list, if that, `django-privilege` can offer a king of custom permission. We suggest you to have a try to use custom permission, enjoy it!

# contribute to django-privilege #
[django-privilege@github](https://github.com/luodaihong/django-privilege "https://github.com/luodaihong/django-privilege")

Waiting for your code.


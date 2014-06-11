=====
Privilege
=====

Privilege is a simple Django app to manage user, group, permission easyly. 

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "privilege" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'privilege',
      )

2. Include the polls URLconf in your project urls.py like this::

      url(r'^privilege/', include('privilege.urls')),

3. Run `python manage.py syncdb` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/privilege/
   to manage user, group and permission (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/privilege/ to participate in the privilege.
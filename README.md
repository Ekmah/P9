# P9
## Installation:
Install Django:
```
pip install django
```
Install Pillow to use ImageFields:
```
pip install Pillow
```
Initialize the project's settings:
- by renaming settings_base.py in settings.py
  - or by copy/paste settings_pase.py THEN rename it in settings.py
- then create a random SECRET_KEY for the SECRET_KEY line 23 of the settings file

## Running:
simply use:
```
python manage.py runserver
```
admin IDs in annexed file under the project link.

## Utilisation:
User after launching the server and going to the app page should land
in the connexion & inscription interface.
Either create a new User or use a provided set of IDs.

When logged in, the User can add usernames of other Users in the 'follows' tab
to follow them and see their content. 

The User can, in the 'flux' tab either ask for a review or create a review.
They can also answer to a review demand of someone they follow.

The User, in the 'Posts' tab can see, edit and delete the content they have created.








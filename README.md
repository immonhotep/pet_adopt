# DJANGO  PET ADOPTATION PLATFROM

A simple web application to help manage pet adoptation between registered users.
Backend code: developed with python django generic, and custom class based views.
Frontend code: Free boostrap css mdb elements, and templates with  custom css and javascripts.
Application reason: only for eucational purposes, practise django. 

Application Functions

Accounts:

- User registration and Authentication system with email confirmation.
- User profile management with password change option.
- List users, and see user details.
- Reset password function with email confirmation.
- Authentication security with google recaptcha confirmation.
- Delete accounts ( superuser can delete other user accounts, normal users can delete own accounts)

Category, pet and adoptation:

-  Create, modify, delete pet category (superuser only)
-  Add, modify, delete pets ( normal user has permission to delete, and modify own pets,  superuser can do this with other user pets too )
-  List categories, and pets under categories, list own pets, list other user pets.
-  View category, and pet details
-  Search in pet names and description
-  Send and remove adoptation request, list own adoptation request, and list possible adopters related own pets.


Communication between users:

-  Users can send private messages to other users, and reply messages.
-  Unreplied messages notification in navbar, and users page.

Communication with admins:

- users and unregistered users, can send messages to site admins on contact page
- Superuser can list User contact messages, and can send answer with email, answers also saved in database, superuser can list answers.

Other features: 

- TinyMce text editor, included and configured for nicer message forms. 

INSTALL:

1. clone the repository ( git clone https://github.com/immonhotep/pet_adopt.git )
2. create python virtual environment (depending to plaform on linux: virtualenv venv)
3. activate python virtual environment ( depending to platform on linux: source venv/bin/activate )
4. install requirements within the virtual environment ( pip install -r requirements.txt )
5. prepare the database: manage.py makemigrations and then:  manage.py migrate
6. create an admin user: manage.py createsuperuser
7. Login with admin user and add some pet category first.




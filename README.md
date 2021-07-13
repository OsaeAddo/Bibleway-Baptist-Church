# ChurchRecordsManager
A web app to help churches safely keep records of their members

## Functions
### ChurchAdmin
- Create an admin account. Login to account(No approval)
- Can view & perform CRUD operations on Church executive(verifies accounts created by an exec)
- Can view & perform CRUD operations on Church member(verifies accounts created by a church member)
- Access to searched results of members

### Church Executive
- Create an executive account.(Approval required by church admin, can login can login to account only after)
- Has access to only church member details(Name, Phone Number, Role)

### Church Member
- Can create a member account for record keeping.(Admin approval required)

## PROJECT SETUP
### Software required
*Python3.8.10
*VSCode
*MySql
*MySql client
*Django

### Install pipenv on your computer
'''
pip install pipenv
'''

### Install packages (including dev)
'''
pipenv install --dev
'''
Run this instruction to install the packages (including dev packages) associated with the project

### Install packages (without dev)
'''
pipenv install --dev
'''
Run this instruction to install the packages (without the dev packages) associated with the project


### Create a database


### Perform database migrations
'''
python manage.py makemigrations
python manage.py migrate
'''

### Runserver to test the app
''' 
python manage.py runserver
'''

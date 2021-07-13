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
* Python3.8.10
* VSCode
* MySql
* MySql client
* Django
* Pipenv



# Install pipenv on your computer
```
pip install pipenv
```

### Install Packages (including dev)
```
pipenv install --dev
```



# Install MySQL on your computer(Linux)
## A more comprehensive guide: 

https://phoenixnap.com/kb/install-mysql-ubuntu-20-04

```
sudo apt-get update
sudo apt-get install mysql-server libmysqlclient-dev
```

## Secure the installation
```
sudo mysql_secure_installation
```


## Create a DataBase Instance
### In the terminal:
Login to an interactive session with the mysql software

```
mysql -u root -p
```

### In the MySQL shell:
```
CREATE DATABASE database_name CHARACTER SET UTF8;
```
## Create a User
To connect to & interact with the database
```
CREATE USER mydatabase_user@localhost IDENTIFIED BY 'password';
```

## Give Access rights to the DataBase User
```
GRANT ALL PRIVILEGES ON database_name.* TO mydatabase_user@localhost;
```

## Flush Changes
Make changes available during the current session and exit
```
FLUSH PRIVILEGES;
exit;
```

## Update settings.py to use MySQL database
Add these lines to the default in DATABASES. Replace database_name, database_user & password with their respective values
```
'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database_name',
        'USER': 'database_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
}
```
# Perform Database Migrations
```
python manage.py makemigrations
python manage.py migrate
```

# Run Server To Test the App
```
python manage.py runserver
```

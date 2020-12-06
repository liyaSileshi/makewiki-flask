# MakeWiki Flask

# After cloning/forking the repo, to start the app

## 1. Navigate to your terminal
 
## 2. create a virtual env 
```python3 -m venv env```

## 3. activate your virtual env
``` source env/bin/activate```

## 4. install the requirements
```pip3 install -r requirements.txt```

# To create a new db in your local machine, 

## 1. delete the ```site.db``` file located inside your makewiki folder.

## 2. open python repl 
In your terminal, type ```python3```, which will open the python repl
```
>>> from makewiki import db, models
>>> db.create_all()
(ignore the SQLAlchemy warnings 😅)
```
After running these 2 commands, the ```site.db``` file will be created inside your makewiki folder. 

# Run the app using this command
In a terminal, you can set the FLASK_APP and FLASK_DEBUG values:
Then use *flask run* command to run the app
```
export FLASK_APP=makewiki
export FLASK_DEBUG=1
flask run
```

# For the 'forgot password' feature:
1. Create a ```.env``` file in your main directory
1. enter your credentials in the ```.env``` file
```
EMAIL_USER=myemail@gmail.com
EMAIL_PASS=my secret password
```
1. You might have to turn on 'less secure app access' for the email you put in the ```.env``` file. 

[Read more here](https://support.google.com/accounts/answer/6010255?authuser=2&p=lsa_blocked&hl=en&authuser=2&visit_id=637428262880099931-3692899904&rd=1)
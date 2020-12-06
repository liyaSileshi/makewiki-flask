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
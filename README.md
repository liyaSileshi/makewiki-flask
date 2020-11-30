
# After cloning/forking the repo, to start the app
 
## create a virtual env 
```python3 -m venv env```

## activate your virtual env
``` source env/bin/activate```

## install the requirements
```pip3 install -r requirements.txt```

## run the app using this command
In a terminal, you can set the FLASK_APP and FLASK_DEBUG values:
Then use *flask run* command to run the app
```
export FLASK_APP=flaskblog
export FLASK_DEBUG=1
flask run
```

# To create the db in your local machine
## open python repl
```
>>> from flaskblog import db, models
>>> db.create_all()
```
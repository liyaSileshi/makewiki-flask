from makewiki import create_app

app = create_app() #use the function from init.py

if __name__ == '__main__':
  app.run(debug=True)
import os
from flask import Flask, render_template
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)

# Debugging
app.debug = (os.environ.get('ENV', 'production') != True)

# Routing
@app.route('/')
@app.route('/decks')
def decks_index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run()

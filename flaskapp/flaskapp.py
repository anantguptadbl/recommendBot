import os
from flask import Flask
from flask import Flask,render_template,request
print "the file path is " + os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.dirname(os.path.abspath(__file__)) + '/static'
print "The template dir is " + template_dir
app = Flask(__name__,static_folder=template_dir,template_folder=template_dir)

#app = Flask(__name__)

#@app.route('/')
#def hello_world():
#  return 'Hello from Flask!'

@app.route('/')
def hello_world():
	return render_template('index.html')

if __name__ == '__main__':
  app.run()


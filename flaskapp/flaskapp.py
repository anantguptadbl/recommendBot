# Imports
import os,json
from flask import Flask
from flask import Flask,render_template,request
import numpy as np
from sklearn import preprocessing
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
from keras.models import load_model

# Initial level flask configuration
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

def trainModel(inputData,labels):
	model = load_model('tictactoe_model')
	#inputData=np.reshape(a,(7,9,))
	model.fit(inputData, labels, batch_size=32, nb_epoch=20, verbose=2, validation_split=0.15)
	#Save partly trained model
	model.save('tictactoe_model')

def getProb(x,curInput,model):
	modifiedInput=np.array([y if i !=x else 1 for i,y in enumerate(curInput[0])]).reshape(1,9,)
	return(model.predict(modifiedInput)[0][0])

def getModifiedArray(curInput,model):
	opps=[i for i, x in enumerate(curInput[0]) if x==0]
	oppProbs=[[getProb(x,curInput,model),x] for x in opps]
	oppProbs.sort()
	newPlace=oppProbs[-1][1]
	#print("Probs is {} and the new place is {}".format(oppProbs,newPlace))
	modifiedInput=np.array([y if i !=newPlace else 1 for i,y in enumerate(curInput[0])]).reshape(1,9,)
	modifiedInput=FlaskBoardtoJSONSingle(modifiedInput[0])
	return(modifiedInput)

@app.route('/getNextMove', methods=["GET","POST"])
def getNextMove():
	currentState=request.args.get('currentState') 
	currentState=JSONtoFlaskBoardSingle(json.loads(currentState))
	#print("the current state in get next move is is {}".format(currentState))
	currentState=np.reshape(currentState,(1,9,))
	model = load_model('tictactoe_model')
	return(json.dumps(getModifiedArray(currentState,model)))

@app.route('/reTrainModel', methods=["GET","POST"])
def reTrainModel():
	inputData=request.args.get('allSteps') 
	label=request.args.get('label') 
	if(label==1):
		label=1
	else:
		label=0
	inputData=JSONtoFlaskBoardMultiple(inputData)
	inputData=np.reshape(inputData,(len(inputData),9,))
	labels=[label] * len(inputData)
	print("the inputData for retraining is {}".format(inputData))
	print("the labels for retraining is {}".format(labels))
	trainModel(inputData,labels)
	print("Model has been retrained")
	return("Model has been retrained")

def checkRows(board):
    for row in board:
        if (len(set(row)) == 1) and (row[0] != 0):
            return row[0]

def checkDiagonals(board):
    if (len(set([board[i][i] for i in range(len(board))])) == 1) and (board[0][0] != 0):
        return board[0][0]
    if (len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1) and (board[0][0] !=0):
        return board[0][len(board)-1]
    return 999

def checkWin(board):
    #transposition to check rows, then columns
    for newBoard in [board, np.transpose(board)]:
        result = checkRows(newBoard)
        if result:
            return result
    return checkDiagonals(board)

def FlaskBoardtoJSONSingle(state):
	#print("the State entering is {}".format(state))
	state=['-' if x==0 else 'X' if x==-1 else 'O' for x in state]
	state=[{'value':x} for x in state]
	state=[[state[0] , state[1] , state[2]],[state[3] , state[4] , state[5]],[state[6] , state[7] , state[8]]]
	return(state)

def JSONtoFlaskBoardSingle(a):
	#a=json.loads(a)
	#print("After jsonifying the value is {}".format(a))
	row1=[ 0 if x['value']=='-' else -1 if x['value']=='X' else 1 for x in a[0]]
	row2=[ 0 if x['value']=='-' else -1 if x['value']=='X' else 1 for x in a[1]]
	row3=[ 0 if x['value']=='-' else -1 if x['value']=='X' else 1 for x in a[2]]
	return([row1,row2,row3])

def JSONtoFlaskBoardMultiple(a):
	a=json.loads(a)
	print("the json format string is {}".format(a))
	return([JSONtoFlaskBoardSingle(x) for x in a])

@app.route('/checkWinner', methods=["GET","POST"])
def checkWinner():
	currentState=request.args.get('currentState')
	currentState=JSONtoFlaskBoardSingle(json.loads(currentState))
	#print("The current state is {}".format(currentState))
	#print("The checkWin return for the currentState is {}".format(checkWin(currentState)))
	if(checkWin(currentState)==1):
		return(json.dumps([1]))
	if(checkWin(currentState)==-1):
		return(json.dumps([-1]))
	if( (checkWin(currentState)==999) and (sum(np.array(currentState).reshape(9,)==0)==0) ):
		return(json.dumps([0]))
	else:
		return(json.dumps([999]))
	
if __name__ == '__main__':
  app.run()


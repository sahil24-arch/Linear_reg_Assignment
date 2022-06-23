# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle
import numpy as np

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            #
            RM =float(request.form['RM'])
            PTRATIO = float(request.form['PTRATIO'])
            LSTAT = float(request.form['LSTAT'])


            filename2 = 'stand.sav'
            filename3 = 'linear_model.sav'

            load_trans = pickle.load(open(filename1, 'rb'))  #Load power transformer object
            load_stand = pickle.load(open(filename2, 'rb'))  #Load standardisation object
            load_model = pickle.load(open(filename3, 'rb'))  #Load Linear regression model object
            # predictions using the loaded model file

            a1=np.array([RM],ndmin=2)
            a2=load_trans.transform(np.array([PTRATIO,LSTAT]).reshape(1,-1))
            arr = np.append(a1, a2)
            stand = load_stand.transform([arr])

            prediction=load_model.predict(stand)
            print('prediction is', prediction)
            # showing the prediction results in a UI
            return render_template('results.html',prediction=prediction)
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')



if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)
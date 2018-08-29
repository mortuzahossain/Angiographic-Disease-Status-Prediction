"""
TODO:
Actual result  are store in database
query executed by the user are save in database -- as test data
"""


from flask import Flask, render_template,url_for,request,redirect
from flask_restplus import Api, Resource, fields, Namespace
import datetime

from sklearn.externals import joblib
model = joblib.load('model.pkl')

app = Flask(__name__)

@app.route('/',methods = ['POST', 'GET'])
def index():
    now = datetime.datetime.now()

    # FOR POST METHOD
    if request.method == 'POST':

        age = request.form['age']
        sex = request.form['sexoptradio']
        cp = request.form['cp']
        testbps = request.form['testbps']
        chol = request.form['chol']
        fbs = request.form['fbs']
        restecg = request.form['restecg']
        thalach= request.form['thalach']
        exang = request.form['exang']
        oldpeak = request.form['oldpeak']
        slope = request.form['slope']
        ca = request.form['ca']
        thal = request.form['thal']

        result = model.predict([
            [age,sex,cp,testbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal]
        ])[0]
        
        actualresult = -1
        return render_template('result.html',year = now.year,result = result,actualresult = actualresult)

    return render_template('index.html',year = now.year)


"""
Bellow this all code are relates to API
"""

api = Api(app, doc='/api/')
data_model = api.model('Predict',{
    'age':fields.Float(63),
    'sex':fields.Float(1),
    'cp':fields.Float(1),
    'testbps':fields.Float(145),
    'chol':fields.Float(233),
    'fbs':fields.Float(1),
    'restecg':fields.Float(2),
    'thalach':fields.Float(150),
    'exang':fields.Float(0.0),
    'oldpeak':fields.Float(2.3),
    'slope':fields.Float(3),
    'ca':fields.Float(0.0),
    'thal':fields.Float(6.0)
    })

@api.route('/predict')
class Predict(Resource):
    def get(self):
        return "Hello API"

    @api.expect(data_model)
    def post(self):
        return {'error':0,'predict':model.predict([api.payload.values()])[0]}


# Remove Before Deployment
if __name__ == '__main__':
    app.run(debug=True)

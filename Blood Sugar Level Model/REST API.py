from flask import Flask, request
from flask_cors import CORS, cross_origin
import pickle

app = Flask(__name__)
CORS(app, support_credentials=True)

with open("C:/Users/shrut/Desktop/2nd Sem/DA Python/Python Final Submission/diabetes_model_final.pkl", "rb") as file:
    diabetes_model = pickle.load(file)
@app.route("/diabetesPredict", methods=['POST'])
def diabetesPredict():
    data = request.get_json()
    age = float(data['age'])
    sex = float(data['sex'])
    bmi = float(data['bmi'])
    bp = float(data['bp'])
    s1 = float(data['s1'])
    s2 = float(data['s2'])
    s3 = float(data['s3'])
    s4 = float(data['s4'])
    s5 = float(data['s5'])
    s6 = float(data['s6'])

    print(age, sex, bmi, bp, s1, s2, s3, s4, s5, s6)

    x = [age, sex, bmi, bp, s1, s2, s3, s4, s5, s6]

    y_predicted = diabetes_model.predict([x])[0]
    print(y_predicted)

    return str(y_predicted)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
    


from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import warnings
import csv
from flask_cors import CORS

warnings.filterwarnings("ignore", category=DeprecationWarning)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "Hello, Flask!"

training = pd.read_csv('Data/Training.csv')
testing = pd.read_csv('Data/Testing.csv')

cols = training.columns[:-1]
x = training[cols]
y = training['prognosis']
reduced_data = training.groupby(training['prognosis']).max()

le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

clf = DecisionTreeClassifier().fit(x_train, y_train)
model = SVC().fit(x_train, y_train)

severityDictionary = {}
description_list = {}
precautionDictionary = {}
# Initialize symptoms_dict with symptom names in lowercase and their indices
symptoms_list = [
    "Itching", "Skin Rash", "Nodal Skin Eruptions", "Continuous Sneezing", "Shivering",
    "Chills", "Joint Pain", "Stomach Pain", "Acidity", "Ulcers on Tongue", "Muscle Wasting",
    "Vomiting", "Burning Micturition", "Spotting Urination", "Fatigue", "Weight Gain",
    "Anxiety", "Cold Hands and Feets", "Mood Swings", "Weight Loss", "Restlessness",
    "Lethargy", "Patches in Throat", "Irregular Sugar Level", "Cough", "High Fever",
    "Sunken Eyes", "Breathlessness", "Sweating", "Dehydration", "Indigestion",
    "Headache", "Yellowish Skin", "Dark Urine", "Nausea", "Loss of Appetite",
    "Pain Behind the Eyes", "Back Pain", "Constipation", "Abdominal Pain", "Diarrhoea",
    "Mild Fever", "Yellow Urine", "Yellowing of Eyes", "Acute Liver Failure", "Fluid Overload",
    "Swelling of Stomach", "Swelled Lymph Nodes", "Malaise", "Blurred and Distorted Vision",
    "Phlegm", "Throat Irritation", "Redness of Eyes", "Sinus Pressure", "Runny Nose",
    "Congestion", "Chest Pain", "Weakness in Limbs", "Fast Heart Rate",
    "Pain During Bowel Movements", "Pain in Anal Region", "Bloody Stool",
    "Irritation in Anus", "Neck Pain", "Dizziness", "Cramps", "Bruising",
    "Obesity", "Swollen Legs", "Swollen Blood Vessels", "Puffy Face and Eyes",
    "Enlarged Thyroid", "Brittle Nails", "Swollen Extremeties", "Excessive Hunger",
    "Extra Marital Contacts", "Drying and Tingling Lips", "Slurred Speech",
    "Knee Pain", "Hip Joint Pain", "Muscle Weakness", "Stiff Neck", "Swelling Joints",
    "Movement Stiffness", "Spinning Movements", "Loss of Balance", "Unsteadiness",
    "Weakness of One Body Side", "Loss of Smell", "Bladder Discomfort", "Foul Smell of Urine",
    "Continuous Feel of Urine", "Passage of Gases", "Internal Itching", "Toxic Look (Typhos)",
    "Depression", "Irritability", "Muscle Pain", "Altered Sensorium", "Red Spots Over Body",
    "Belly Pain", "Abnormal Menstruation", "Dischromic Patches", "Watering from Eyes",
    "Increased Appetite", "Polyuria", "Family History", "Mucoid Sputum", "Rusty Sputum",
    "Lack of Concentration", "Visual Disturbances", "Receiving Blood Transfusion",
    "Receiving Unsterile Injections", "Coma", "Stomach Bleeding", "Distention of Abdomen",
    "History of Alcohol Consumption"
]

# Create a dictionary with symptoms in lowercase as keys and their indices as values
symptoms_dict = {symptom.lower(): index for index, symptom in enumerate(symptoms_list)}

# print(symptoms_dict)
def getDescription():
    global description_list
    with open('MasterData/symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) < 2: 
                continue  
            description_list[row[0].strip().lower()] = row[1]

def getSeverityDict():
    global severityDictionary
    severityDictionary = {} 

    try:
        with open('MasterData/symptom_severity.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if len(row) < 2:
                    continue  
                symptom = row[0].strip().lower()
                try:
                    severity = int(row[1].strip())
                    severityDictionary[symptom] = severity
                except ValueError:
                    print(f"Skipping row with invalid severity value: {row}")
    except FileNotFoundError:
        print("Severity file not found. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")

def getprecautionDict():
    global precautionDictionary
    with open('MasterData/symptom_precaution.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            _prec = {row[0].strip().lower(): [row[1], row[2], row[3], row[4]]}
            precautionDictionary.update(_prec)

def sec_predict(symptoms_exp):
    df = pd.read_csv('Data/Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=20)
    rf_clf = DecisionTreeClassifier()
    rf_clf.fit(X_train, y_train)

    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
        item_lower = item.lower()
        if item_lower in symptoms_dict:
            input_vector[symptoms_dict[item_lower]] = 1

    return rf_clf.predict([input_vector])

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    symptoms = data.get('symptoms', [])
    num_days = data.get('days', 1)
    
    if not isinstance(symptoms, list) or not all(isinstance(symptom, str) for symptom in symptoms):
        return jsonify({"error": "Symptoms should be a list of strings."}), 400

    features = [0] * 132
    
    for symptom in symptoms:
        symptom_lower = symptom.lower()
        if symptom_lower in symptoms_dict:
            features[symptoms_dict[symptom_lower]] = 1

    features_array = np.array([features])
    # print(features_array)
    prediction = clf.predict(features_array)
    present_disease = le.inverse_transform(prediction)
    response = {
        "predicted_disease": present_disease[0],
        "description": description_list.get(present_disease[0].lower(), "No description available."),
        "precautions": precautionDictionary.get(present_disease[0].lower(), []),
    }
    
    return jsonify(response)

@app.route('/description/<disease>', methods=['GET'])
def get_description(disease):
    return jsonify({"description": description_list.get(disease.lower(), "No description available.")})

@app.route('/precautions/<disease>', methods=['GET'])
def get_precautions(disease):
    return jsonify({"precautions": precautionDictionary.get(disease.lower(), [])})

def calc_condition(symptoms_exp, days):
    print(f"Symptoms: {symptoms_exp}")
    print(f"Days: {days}")
    severity_sum = sum(severityDictionary.get(symptom.lower(), 0) for symptom in symptoms_exp)
    condition_level = (severity_sum * days) / (len(symptoms_exp) + 1)
    if condition_level > 13:
        return "You should take consultation from a doctor."
    else:
        return "It might not be that bad, but you should take precautions."

if __name__ == '__main__':
    getSeverityDict()
    getDescription()
    getprecautionDict()
    app.run(debug=True)

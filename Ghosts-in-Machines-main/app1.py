from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.utils import shuffle
import random

app1 = Flask(__name__)
CORS(app1)
def preprocess(df):
    for col in df.columns:
        df[col] = df[col].str.replace('_', ' ')

    cols = df.columns
    data = df[cols].values.flatten()

    s = pd.Series(data)
    s = s.str.strip()
    s = s.values.reshape(df.shape)

    df = pd.DataFrame(s, columns=df.columns)
    df = df.fillna(0)
    return df

def analyze_symptoms(symptoms):
    df = pd.read_csv('dataset.csv')
    df = preprocess(df)
    df = df.drop_duplicates()

    a = df.values.tolist()
    b = [[x for x in inner_list if x != 0] for inner_list in a]

    diseases = []

    for i in b:
        if all(j in str(i) for j in symptoms):
            diseases.append(i)

    x = set()
    dis = []
    for j in diseases:
        f = j[0]
        if f not in x:
            dis.append(j)
            x.add(f)

    df = shuffle(df)

    qn = ['Are you suffering from ', 'Do you have ', 'Are you feeling ']

    def asx(sym):
        for i in dis:
            for j in i:
                if j in sym:
                    i.remove(j)

    asx(symptoms)
    while len(dis) > 1:
        for i in dis:
            sym = random.choice(i[1:])
            choice = input(random.choice(qn) + sym + " ")

            if choice == 'yes':
                for i in dis:
                    if sym not in i:
                        dis.remove(i)
                        asx(sym)

            elif choice == 'no':
                for i in dis:
                    if sym in i:
                        dis.remove(i)
                        asx(sym)

    disease_name = dis[0][0]
    symptoms_list = dis[0][1:]

    sd = pd.read_csv('symptom_Description.csv')
    sd = preprocess(sd)

    symptom_description = sd.loc[sd['Disease'] == disease_name, 'Description'].iloc[0]

    pr = pd.read_csv('symptom_precaution.csv')
    pr = preprocess(pr)

    precautions = pr.loc[pr['Disease'] == disease_name].iloc[:, 1:].values.tolist()
    precautions = [precaution.capitalize() for precaution in precautions[0]] if precautions else []

    return disease_name, symptoms_list, symptom_description, precautions

@app1.route('/analyze', methods=['POST'])
def handle_analysis():
    request_data = request.json
    symptoms = request_data.get('symptoms', [])
    disease_name, symptoms_list, symptom_description, precautions = analyze_symptoms(symptoms)
    return jsonify({
        "disease_name": disease_name,
        "symptoms_list": symptoms_list,
        "symptom_description": symptom_description,
        "precautions": precautions
    })

if __name__ == '__main__':
    app1.run(debug=True)
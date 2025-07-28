# Things to include in the app

# Pictures of fighters along with the record
# Face off when prediction being done

from flask import Flask, render_template, request  
import json
import os


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fighters')
def fighters():
    with open('data/fighters.json') as f:
        fighter_data = json.load(f)
    return render_template('fighter_stats.html', fighters=fighter_data)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    with open('data/fighters.json') as f:
        fighter_data = json.load(f)  

    if request.method == 'POST':
        fighter1_name = request.form['fighter1']
        fighter2_name = request.form['fighter2']

        f1 = next(f for f in fighter_data if f['name'] == fighter1_name)
        f2 = next(f for f in fighter_data if f['name'] == fighter2_name)

        # simple prediction logic
        # based on reach and record only

        # make it better later
        # by integrating last 2-3 matches
        # lost? or won? was it dominant or decisive? etc
        # win streak? 
        score1 = int(f1['reach'].split()[0]) + int(f1['record'].split('-')[0])
        score2 = int(f2['reach'].split()[0]) + int(f2['record'].split('-')[0])

        predicted_winner = f1['name'] if score1 >= score2 else f2['name']
        # later, for equal score, apply some other logic

        # also for each prediction correct, do something to show it on the app

        return render_template('prediction_result.html', f1=f1, f2=f2, winner=predicted_winner)

    return render_template('predict.html', fighters=fighter_data)


if __name__ == '__main__':
    app.run(debug=True)

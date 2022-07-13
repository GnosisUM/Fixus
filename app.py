from flask import Flask, render_template, url_for

app = Flask(__name__)

#-----------TABLE MANIPULATION------------------
import pandas as pd
import numpy as np
df = pd.read_csv('Data\DC Battery Report.csv')
data = df[['LRD','Rano Base Code', 'Administrative Status', 'Total Current Load']].copy()


data['Total Current Load'] = data['Total Current Load'].fillna(0).astype(float)
conditions = [
    (data['Total Current Load'] <=20),
    ((data['Total Current Load'] >20) & (data['Total Current Load'] <= 40)),
    ((data['Total Current Load'] >40) & (data['Total Current Load'] <= 70)),
    (data['Total Current Load'] >70)
]

values = ['Healthy', 'P1', 'P2', 'P3']
data = data.sort_values(by= 'LRD')
data = data.reset_index(drop=True)

#set p1, p2, p3
data['Category'] = np.select(conditions, values)
#/-----------TABLE MANIPULATION------------------

@app.route('/')

@app.route('/index')
def index():
    return render_template('index.html', tables=[data.to_html(classes=["table table-striped table-bordered table-sm"])], titles=[''])

@app.route('/EquipStats')
def EquipStats():
    return render_template('EquipStats.html', title='Equipment Stats')

@app.route('/MaintenanceSchedule')
def MaintenanceSchedule():
    return render_template('MaintenanceSchedule.html', title='Maintenance Schedule')


if __name__ == "__main__":
    app.run(debug=True) 
from flask import Flask, render_template, request
import numpy as np
import pandas as pd

from src.data_pipeline.predict_pipeline_script import CustomData, PredictPipeline 

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def predict_results():
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        data = CustomData(
            step=int(request.form.get('step')),
            amount=float(request.form.get('amount')),
            oldbalanceOrg=float(request.form.get('oldbalanceOrg')),
            newbalanceOrig=float(request.form.get('newbalanceOrig')),
            oldbalanceDest=float(request.form.get('oldbalanceDest')),
            newbalanceDest=float(request.form.get('newbalanceDest')),
            trans_type=request.form.get('trans_type')
        )
        pred_df = data.to_dataframe()
        print(pred_df)
        prediction_pipeline = PredictPipeline()
        prediction_result = prediction_pipeline.predict(pred_df)

        return render_template('home.html', result=prediction_result[0])


if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)

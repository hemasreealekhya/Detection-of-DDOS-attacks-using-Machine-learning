# Flask code

from flask import Flask, request, render_template
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load the trained model
rf_model = joblib.load('random_forest_model.pkl')

# Load the dataset
df = pd.read_csv(r'C:\Users\Alekhya Reddy\Downloads\emma-main (1)\emma-main\code\DDos.csv')  # Replace 'your_dataset.csv' with the actual file path

# Handle missing values
df.dropna(inplace=True)

# Selecting two columns for prediction
X = df[['Destination Port', 'Flow Duration']]
y = df[' Label']

# Fit the model
rf_model.fit(X, y)





@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        
        
        # Get input values from the form
        dest_port = float(request.form['Destination Port'])
        flow_duration = float(request.form['Flow Duration'])
        
        # Make prediction
        prediction = rf_model.predict([[dest_port, flow_duration]])
        
        # Determine the result message and result class
        if prediction[0] == 'DDoS':
            result_message = 'DDoS Attack Detected'
            result_class = 'positive'
        else:
            result_message = 'No DDoS Attack Detected'
            result_class = 'negative'
            
        # Pass result information to the template
        return render_template('result.html', result_message=result_message, result_class=result_class)
    
    except ValueError:
        return "Error: Please enter valid numeric values for all fields."

if __name__ == '__main__':
    app.run(debug=True)

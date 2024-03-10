from flask import Flask, send_file, request, render_template
import pandas as pd
from modules.model import is_failure, failure_type

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        # Retrieve the uploaded file from the request
        f = request.files['file']
        
        # Save the uploaded file to a specific location
        f.save('uploaded/input.csv')

        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv('uploaded/input.csv')

        # Add columns for 'is_failure' and 'failure_type' based on the model predictions
        df['is_failure'] = is_failure(df)
        df['failure_type'] = failure_type(df)

        # Filter the DataFrame to include only rows with 'is_failure' equal to 1
        df = df[df['is_failure'] == 1]

        # Save the resulting DataFrame to an output CSV file
        df.to_csv('uploaded/output.csv', index=False)

        # Send the output CSV file as an attachment in the response
        return send_file('uploaded/output.csv', as_attachment=True)

    # Render the HTML template for the home page with an attractive interface
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask app on host '0.0.0.0' and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)

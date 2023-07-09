from flask import Flask, render_template, jsonify
import pandas as pd
app = Flask(__name__)

@app.route('/')
def home():
    # Prepare tabular data as a list of dictionaries
    tabular_data = [
        {"Name": "John", "Age": 30, "Country": "USA"},
        {"Name": "Jane", "Age": 28, "Country": "Canada"},
        {"Name": "Mike", "Age": 35, "Country": "UK"}
    ]

    return render_template('index.html', tabular_data=tabular_data)

@app.route('/api/stats', methods=['GET'])
def api_data():
    # get all seasons from database using pandas as pd
    seasons = pd.read_sql('SELECT * FROM seasons', con=db.conn)
    # convert seasons to json rows
    seasons_json = seasons.to_json(orient='records')
    return jsonify({'status_code':200, 'data':seasons_json})

if __name__ == '__main__':
    app.run()

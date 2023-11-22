# get | post | pudb | pack | delete
from flask import Flask, jsonify, request, render_template
import joblib
import pandas as pd
import pickle

# create a flask app
app = Flask(__name__, template_folder='templates')

# load the model
filename = 'pm25-prediction20231110_noPM10_v4_randfor_est40.model'
model = pickle.load(open(filename, 'rb'))

# define the routes
@app.route('/', methods = ['GET'])
def home():
    return render_template('home.html', current_page = 'home')

@app.route('/aboutus', methods = ['GET'])
def aboutus():
    return render_template('aboutus.html', current_page = 'aboutus')

@app.route('/ourdata', methods = ['GET'])
def ourdata():
    return render_template('ourdata.html', current_page = 'ourdata')

@app.route('/prediction', methods = ['GET'])
def prediction():
    return render_template('prediction.html', current_page = 'prediction')

# Define a route to serve the images
@app.route('/static/<filename>')
def serve_image(filename):
    return app.send_static_file(filename)


@app.route('/predict', methods=['POST'])
# POST will not store data in web
def predict():
    try:
        data = request.get_json() # get json object
        district = data.get('station')
        CO_var = data.get('CO')
        NO_var = data.get('NO')
        NO2_var = data.get('NO2')
        NOX_var = data.get('NOX')
        O3_var = data.get('O3')
        windspeed = data.get('windspeed')
        winddir = data.get('winddir')
        temp = data.get('temp')
        humidity = data.get('humidity')
        rain = data.get('rain')

        ###### prediction stuff here
        input = pd.DataFrame(data = {
            'District': [district],
            'CO': [CO_var],
            'NO': [NO_var],
            'NO2': [NO2_var],
            'NOX': [NOX_var],
            'O3': [O3_var],
            'Windspeed': [windspeed],
            'Winddir': [winddir],
            'Temp': [temp],
            'Relhum': [humidity],
            'Rain': [rain]
        })
        prediction = model.predict(input)[0]
        message = 'PM2.5 Predicted'
        message_combine = f"{message} is {prediction}"
        
        ### result
        result = {
            'message': message_combine
        }
        print(prediction)
        print(result)

        return jsonify(result), 200
    
    except Exception as e:
        return jsonify ({'error': 'an error occured'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    # app.run()


from flask import Flask, jsonify, request
import json
import pdb
import requests
from math import ceil

app = Flask(__name__)

def get_sample_data():
    '''
    Reads the sample_data.json and returns the 'list' object as a dict. Raises an exception if sample_data.json cannot be read. 
    RETURNS: 
        sample_data(dict) dictionary constructed from sample_data.json
    '''
    with open('sample_data.json') as data_file:
        data_string = data_file.read()    
        try:
            sample_data = json.loads(data_string)
            print('Success!')
        except ValueError:
            print('Failed:')
            print(repr(data_string))
    return sample_data['list']


@app.route('/weather/api/v1.0/london/full', methods=['GET'])
def get_full_data():
    '''

    GET route - returns full sample data as JSON object
    RETURNS: 
        sample_data(JSON) - unfiltered JSON object
    '''
    return jsonify(get_sample_data())


def filter_date_time(date, timestamp):
    '''
    Finds matching date time datapoints in the sample_data 
    INPUTS: 
        date(str) - format: yyyy-mm-dd (2017-10-28)
        time(str) - format: hh:mm:ss (18:00:00)
    RETURNS: 
        results(list) - list of results or empty list
    '''
    sample_data = get_sample_data()
    results = []
    for item in sample_data:
        match_date = item['dt_txt'].split()[0] == date
        match_time = item['dt_txt'].split()[1] == timestamp
        if match_date and match_time:
            results.append(item)
    if not results: 
        results = [{"status": "error", "message": "No data for {}{}{}".format(date, ' ', timestamp)}]
    return results

def convert_temperate(temperature, unit):
    '''
    Converts Kelvin to Celius by by minusing 273 and rounding to the nearest int
    INPUTS: 
        temperature(float) - Kelvin
    RETURNS:
        temperature(int) - Celius
    '''
    print(unit)
    if unit == 'celius':
        temperature = temperature - 273
    elif unit == 'kelvin': 
        temperature = temperature
    elif unit == 'fahrenheit':
        temperature = temperature * 1.8 - 459.67
    else: 
        return {"status": "error", "message": "Invalid temperature unit {} specified".format(unit)}
    return ceil(temperature)


@app.route('/weather/api/v1.0/london/<string:date>/<string:timestamp>', methods=['GET'])
def get_weather_summary(date, timestamp, unit='celius'):
    '''
    GET route - Summary data returning full JSON response for the date/timestamp params
    INPUTS: 
        date(str) - format: yyyy-mm-dd (2017-10-28)
        timestamp(str) - format: hh:mm:ss (18:00:00)
    RETURNS: 
        results(JSON) JSON object of matching results
    '''
    sample_data = get_sample_data()
    if 'unit' in request.args:          # Check if the unit arg has been sent in
        unit = request.args['unit']
    results = filter_date_time(date, timestamp)
    if 'status' not in results[0]:          # if results were found for the date
            results[0]['main']['temp'] = convert_temperate(results[0]['main']['temp'], unit)
    return jsonify(results)


@app.route('/weather/api/v1.0/london/<string:date>/<string:timestamp>/<string:param>', methods=['GET'])
def get_weather_with_param(param, date, timestamp):
    '''
    GET route - Returns only the specified param from filtered results - returns an error is the date/time is not in JSON or the param is not in the JSON 
    INPUTS: 
        param(str): string of param to filter 
        date(str) - format: yyyy-mm-dd (2017-10-28)
        timestamp(str) - format: hh:mm:ss (18:00:00)
    RETURNS: 
        results(JSON) JSON object of matching results
    '''
    results = filter_date_time(date, timestamp)
    sample_data = get_sample_data()
    if 'status' not in results[0]:              # if results were found for the date
        if param in results[0]['main']:
            results = {param: str(results[0]['main'][param])}
        else: 
            results = {"status": "error", "message": "Invalid paramater {} specified".format(param)}
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)



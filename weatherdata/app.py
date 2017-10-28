
from flask import Flask, jsonify
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
    return jsonify(sample_data)


def filter_date_time(date, timestamp):
    '''
    Finds matching date time datapoints in the sample_data 
    INPUTS: 
        date(str) - format: yyyy-mm-dd (2017-10-28)
        time(str) - format: hh:mm:ss (18:00:00)
    RETURNS: 
        results(list) - list of results or empty list
    '''
    results = []
    for item in sample_data:
        match_date = item['dt_txt'].split()[0] == date
        match_time = item['dt_txt'].split()[1] == timestamp
        if match_date and match_time:
            results.append(item)
    return results

def convert_temperate(temperature):
    '''
    Converts Kelvin to Celius by by minusing 273 and rounding to the nearest int
    INPUTS: 
        temperature(float) - Kelvin
    RETURNS:
        temperature(int) - Celius
    '''
    return ceil(temperature - 273)


@app.route('/weather/api/v1.0/london/<string:date>/<string:timestamp>', methods=['GET'])
def get_weather_summary(date, timestamp):
    '''
    GET route - Summary data returning full JSON response for the date/timestamp params
    INPUTS: 
        date(str) - format: yyyy-mm-dd (2017-10-28)
        timestamp(str) - format: hh:mm:ss (18:00:00)
    RETURNS: 
        results(JSON) JSON object of matching results
    '''
    results = filter_date_time(date, timestamp)
    if results: 
        for result in results: 
            result['main']['temp'] = convert_temperate(result['main']['temp'])
    else: 
        results = [{"status": "error", "message": "No data for {}{}{}".format(date, ' ', timestamp)}]
    return jsonify(results)


@app.route('/weather/api/v1.0/london/<string:date>/<string:timestamp>/<string:param>', methods=['GET'])
def get_weather_with_param(param, date, timestamp):
    '''
    GET route - Returns only the specified param from filtered results
    '''
    results = filter_date_time(date, timestamp)
    if results:
        if param in results[0]['main']:
            results = {param: str(results[0]['main'][param])}
        else: 
            results = [{"status": "error", "message": "{} not found in response for {}{}{}".format(param, date, ' ', timestamp)}]
    return jsonify(results)


if __name__ == '__main__':
    sample_data = get_sample_data()
    app.run(debug=True)

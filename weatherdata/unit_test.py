import openweather
import unittest
from unittest.mock import patch

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        openweather.app.testing = True
        self.app = openweather.app.test_client()
        self.app.sample_data = openweather.get_sample_data()
        

    def test_get_sample_data(self):
        print('testing get_sample_data:')
        self.assertEqual(type(openweather.get_sample_data()), list)

    
    def test_convert_temperature(self):
        print('testing test_convert_temperature:')
        self.assertEqual(openweather.convert_temperate(285, 'celius'), 12)
        self.assertEqual(openweather.convert_temperate(285, 'kelvin'), 285)
        self.assertEqual(openweather.convert_temperate(285, 'fahrenheit'),  54)
        self.assertEqual(openweather.convert_temperate(285, 'blah'),  {"status": "error", "message": "Invalid temperature unit {} specified".format('blah')})


    def test_filter_date_time(self):
        print('testing filter_date_time - no data for date/time in sample_data:')
        r = openweather.filter_date_time('2001-10-09', '15-00-00')
        assert b'No data for' not in r
        print('testing filter_date_time - data found for date/time in sample_data:')
        r = openweather.filter_date_time('2017-10-09', '15-00-00')
        self.assertEqual(type(openweather.get_sample_data()), list) 
    
    def test_get_weather_summary(self):
        print('testing get weather data - no data found')
        r = self.app.get('weather/api/v1.0/london/2017-10-09/15-00-00')

        print('testing get weather data - data found')
        r = self.app.get('weather/api/v1.0/london/2017-11-02/15:00:00')
        assert b'clouds' in r.data


    def test_get_weather_with_param(self):
        params = [
        "grnd_level",
        "humidity",
        "pressure",
        "sea_level",
        "temp",
        "temp_kf",
        "temp_max",
        "temp_min"]
        
        print('testing get_weather_with_param - valid param')
        for param in params: 
            r = self.app.get('/weather/api/v1.0/london/2017-11-02/15:00:00/{}'.format(param))
            assert b'{' in r.data
        
        print('testing get_weather_with_param - invalid param')
        r = self.app.get('/weather/api/v1.0/london/2017-11-02/15:00:00/blah')
        assert b'error' in r.data



if __name__ == '__main__':
    unittest.main()
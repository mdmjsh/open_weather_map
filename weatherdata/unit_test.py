import openweather
import unittest

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        openweather.app.testing = True
        self.app = openweather.app.test_client()
        sample_data = openweather.get_sample_data()

    def test_get_sample_data(self):
        self.assertEqual(type(openweather.get_sample_data()), list)

    
    def test_convert_temperature(self):
        self.assertEqual(openweather.convert_temperate(285, 'celius'), 12)
        self.assertEqual(openweather.convert_temperate(285, 'kelvin'), 285)
        self.assertEqual(openweather.convert_temperate(285, 'fahrenheit'),  54)
        self.assertEqual(openweather.convert_temperate(285, 'blah'),  {"status": "error", "message": "Invalid temperature unit {} specified".format('blah')})
        # rv = self.logout()
        # assert b'You were logged out' in rv.data
        # rv = self.login('adminx', 'default')
        # assert b'Invalid username' in rv.data
        # rv = self.login('admin', 'defaultx')
        # assert b'Invalid password' in rv.data


    # def test_filter_date_time(self):
    #     sample_data = openweather.get_sample_data()
    #     r = openweather.filter_date_time('2001-10-09', '15-00-00')
    #     assert b'No data for' not in r.data


if __name__ == '__main__':
    sample_data = openweather.get_sample_data()
    unittest.main()
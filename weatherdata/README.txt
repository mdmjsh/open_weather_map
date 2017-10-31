To setup the containerised application: 

docker build -t openweathermap .
docker run -p 5000:5000 openweathermap

--------------------------------------------------------------------------------------------------------

A general summary of the weather:

curl -i http://0.0.0.0:5000/weather/api/v1.0/london/2017-11-02/15:00:

You can also run curl -i http://0.0.0.0:5000/weather/api/v1.0/london/full to get a response of all data (no date range). 

--------------------------------------------------------------------------------------------------------

Ask for individual pieces of information:

curl -i http://0.0.0.0:5000/weather/api/v1.0/london/2017-11-02/15:00:00/[param]

NOTE: The querable fields are pulled from the 'main' object in the JSON response, therefore the allowed parameters to query for are: 

"grnd_level"
"humidity"
"pressure"
"sea_level"
"temp"
"temp_kf"
"temp_max"
"temp_min"

A future improvement would be to add full support for any parameter in the JSON repsonse outside of the 'main' object. 

--------------------------------------------------------------------------------------------------------

No data found: 

curl -i http://0.0.0.0:5000/weather/api/v1.0/london/2027-11-02/15:00:00



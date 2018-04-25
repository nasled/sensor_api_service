
## Sensor API service

The service was built using python3, pipenv, gevent, sqlite, pytest, tavern. This stack was used because it satisfies the requirements.


### Installation

* Copy the project to a directory
```
git clone https://github.com/nasled/sensor_api_service.git
```
* Activate virtualenv (install pipenv if necessary)
```
pipenv shell
```
* Install the required dependencies
```
pipenv install 
```
* Update the required dependencies
```
pipenv update
```
* Run service
```
./python sensor-api.py 
```
* Run tests
```
pytest
```

### Usage

Retrive a sensor data for a given device in a time range 
```
curl -X GET http://localhost:8088 -d '{"device_uuid": "b21ad0676f26439482cc9b1c7e827de4","sensor_type": "humidity","start_time": 1,"end_time": 211111111111}'
```

Upload a sensor data endpoint (PUT also available)
```
curl -XPOST http://localhost:8088 -d '{"device_uuid": "b21ad0676f26439482cc9b1c7e827de4", "sensor_type": "humidity", "sensor_value": 12.0, "sensor_reading_time": 1510093444}'
```

Delete all sensor data
```
curl -XDELETE http://localhost:8088
```

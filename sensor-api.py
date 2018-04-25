from gevent.pywsgi import WSGIServer
import json
import sqlite3
import re


# init db connection
conn = sqlite3.connect('db.sqlite')
c = conn.cursor()

# handle requests
def application(env, start_response):
    wsgi_input = env['wsgi.input'].read()
    
    if env['REQUEST_METHOD'] == 'GET':
        start_time = 1
        end_time = 2999999999
        sensor_type = ""
        device_uuid = ""
        
        if len(wsgi_input) > 0:
            json_request = json.loads(wsgi_input)
            
            if "start_time" in json_request:
                start_time = int(json_request['start_time'])
    
            if "end_time" in json_request:
                end_time = int(json_request['end_time'])
                
            if "sensor_type" in json_request and json_request["sensor_type"] in ['temperature', 'humidity']:
                sensor_type = json_request["sensor_type"]
            
            if "device_uuid" in json_request and re.match("^[a-z0-9]*$", json_request['device_uuid']):
                device_uuid = json_request['device_uuid']
            
        entries = c.execute('select * from sensor_data where sensor_reading_time > ? and sensor_reading_time < ? and sensor_type = ? and device_uuid = ?', 
                            [start_time, end_time, sensor_type, device_uuid])

        json_response = []
        for entry in entries:
            json_response.append(entry)
        json_response = {'bundles': json_response}
        json_response = json.dumps(json_response)
        
        start_response('200 OK', [('Content-Type', 'application/json')])
        return [json_response.encode('UTF-8')]


    elif env['REQUEST_METHOD'] in ['POST', 'PUT']:
        if len(wsgi_input) == 0:
            start_response('422 Unprocessable Entity', [('Content-Type', 'application/json')])
            return [b'{"error":"Wrong body length"}']

        json_request = json.loads(wsgi_input)

        fields = ['device_uuid', 'sensor_type', 'sensor_value', 'sensor_reading_time']
        for field in fields:
            if field not in json_request:
                start_response('422 Unprocessable Entity', [('Content-Type', 'application/json')])
                return [b'{"error":"Wrong body"}']

        if json_request["sensor_type"] not in ['temperature', 'humidity']:
            start_response('422 Unprocessable Entity', [('Content-Type', 'application/json')])
            return [b'{"error":"Wrong type"}']

        if json_request["sensor_value"] not in range(0, 100):
            start_response('422 Unprocessable Entity', [('Content-Type', 'application/json')])
            return [b'{"error":"Wrong value"}']

        if json_request["sensor_reading_time"] < 0:
            start_response('422 Unprocessable Entity', [('Content-Type', 'application/json')])
            return [b'{"error":"Wrong reading time"}']

        try:
            query = "insert into sensor_data values('{0}', '{1}', {2}, {3});"\
                .format(json_request['device_uuid'], json_request['sensor_type'], json_request['sensor_value'], json_request['sensor_reading_time'])
            c.execute(query)
            conn.commit()
        except:
            start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
            return [b'Could not write to DB']

        start_response('202 OK', [('Content-Type', 'application/json')])
        return []
    
    # debug
    elif env['REQUEST_METHOD'] == 'DELETE':
        c.execute('DELETE FROM sensor_data;')
        conn.commit()
        start_response('202 Accepted', [('Content-Type', 'application/json')])
        return []

    start_response('404 Not Found', [('Content-Type', 'application/json')])
    return []


if __name__ == '__main__':
    print('Sensor endpoint server started...')

WSGIServer(('127.0.0.1', 8088), application).serve_forever()
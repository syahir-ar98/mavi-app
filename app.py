import urllib.request
import io
import json
import os
import ssl
from flask import Flask, jsonify, request
from flask_cors import CORS
from gevent.pywsgi import WSGIServer


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


# this line is needed if you use self-signed certificate in your scoring service.
allowSelfSignedHttps(True)

app = Flask(__name__)
cors = CORS(app)

value1 = " "
input1 = "true"
input2 = "true"
input3 = "true"

@app.route('/', methods=['GET', 'POST'])
def runModel():

    global value1
    global input1
    global input2
    global input3

    if(request.method == "POST"):

        request_data = request.data
        request_data = json.loads(request_data.decode('utf-8'))
        input1 = request_data['input1']
        input2 = request_data['input2']
        input3 = request_data['input3']
        return ""
        
    else:
        # Request data goes here
        data = {
            "Inputs": {
                "WebServiceInput0":
                [
                    {
                        'Quiz 1_Q1 Score': input1,
                        'Quiz 1_Q2 Score': input2,
                        'Quiz 1_Q3 Score': input3,
                        'Quiz 1_Q4 Score': "true",
                        'Quiz 1_Q5 Score': "true",
                        'Quiz 1_Q1 Time': "0",
                        'Quiz 1_Q2 Time': "1",
                        'Quiz 1_Q3 Time': "2",
                        'Quiz 1_Q4 Time': "1",
                        'Quiz 1_Q5 Time': "2",
                    },
                ],
            },
            "GlobalParameters": {
            }
        }

        body = str.encode(json.dumps(data))

        url = 'http://20.195.98.200:80/api/v1/service/model-decisiontree/score'
        # Replace this with the API key for the web service
        api_key = 'fiUUUwL28J9AxzAbxB8gLmg3n4bcGEkJ'
        headers = {'Content-Type': 'application/json',
                'Authorization': ('Bearer ' + api_key)}

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()

            final_result = result.replace(b"'", b"'")
            my_json = json.load(io.BytesIO(final_result))
            print(my_json)
            return my_json

        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(json.loads(error.read().decode("utf8", 'ignore')))

if __name__ == "__main__":
    app.run(debug=True)
    # http_server = WSGIServer(('', 5000), app)
    # http_server.serve_forever()
    # print(http_server)

from flask import *
from huxley_requests import load_departures, huxley_departure_formatter

# Create the application instance
app = Flask(__name__)

# Create some test data for our catalog in the form of a list of dictionaries.
departures = {
    "station_name": "Hitchin",
    "departures": {
        "all": [
            {
                "mode": "train",
                "service": "22729000",
                "train_uid": "C09716",
                "platform": "2",
                "aimed_departure_time": "11:13",
                "aimed_arrival_time": "11:12",
                "origin_name": "Brighton",
                "destination_name": "Royston",
                "status": "LATE",
                "expected_arrival_time": "11:13",
                "expected_departure_time": "11:14",
                "calingPoints": [
                    {
                        "station_code": "BTN",
                        "station_name": "Brighton",
                        "platform": "5",
                        "aimed_departure_time": "09:20",
                        "aimed_arrival_time": None,
                        "expected_departure_time": "09:21",
                        "status": "LATE"
                    },
                ]
            }
        ]
    }
}


# A route to return all of the available entries in our catalog.
@app.route('/publictransport/v1/departures/all', methods=['GET'])
def api_all():
    # Check if an ID was provided as part of the URL.
    if 'station' not in request.args or 'station' == '':
        status_code = 400
        json_body = jsonify({"error": "No departure station provided in request. Please specify a station."})
        return json_body, status_code
    else:
        station = str(request.args['station'])

    # Check auth provided
    if 'Authorization' not in request.headers:
        status_code = 401
        json_body = jsonify({})
        return json_body, status_code
    else:
        accessToken = str(request.headers['Authorization'])

    r, huxley_status_code = load_departures(station, accessToken)

    print(r)

    # if request fails, return:
    if huxley_status_code != 200:
        status_code = 503
        json_body = jsonify({"error": "Huxley api failure",
                             "huxley_status_code": huxley_status_code})
        return json_body, status_code

    # render things right
    return jsonify(huxley_departure_formatter(r))


app.run()

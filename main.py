from flask import *
from huxley_requests import load_departures, huxley_departure_formatter

# Create the application instance
app = Flask(__name__)


# Get departures for a station
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

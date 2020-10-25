import requests


def load_departures(departureStation, apiKey):
    URL = f"https://huxley.apphb.com/all/{departureStation}?accessToken={apiKey}&expand=true"

    r = requests.get(url=URL)

    data = r.json()

    if "error" in data:
        return 'error'

    return data, r.status_code


def calculate_status(expected_departure_time, isCancelled):
    if expected_departure_time == "On time":
        return "On time"
    elif isCancelled == True:
        return "Cancelled"
    elif expected_departure_time == "Delayed":
        return "Delayed"
    else:
        return "Late"


def huxley_departure_formatter(huxleyData):
    station_name = huxleyData["locationName"]
    max_index = len(huxleyData["trainServices"])
    departures = []

    # top level info here, for actions once per train
    for i in range(0, max_index):
        stops = []
        trainJson = huxleyData["trainServices"][i]
        origin = trainJson["origin"][0]["locationName"]
        destination = trainJson["destination"][0]["locationName"]
        standard_departure_time = trainJson['std']
        standard_arrival_time = trainJson['sta']
        expected_arrival_time = trainJson['eta']
        expected_departure_time = trainJson['etd']
        platform = trainJson['platform']
        status = calculate_status(expected_departure_time, trainJson['isCancelled'])

        # Render stops
        callingJson = trainJson["subsequentCallingPoints"][0]["callingPoint"]
        max_calling_index = len(callingJson)

        for ic in range(0, max_calling_index):
            callingStopJson = callingJson[ic]
            stop_location_name = callingStopJson["locationName"]
            stop_standard_departure_time = callingStopJson['st']
            stop_expected_arrival_time = callingStopJson['at']
            stop_expected_departure_time = callingStopJson['et']
            stop_status = calculate_status(expected_departure_time, callingStopJson['isCancelled'])
            stop = {
                "locationName": stop_location_name,
                "standard_departure_time": stop_standard_departure_time,
                "expected_arrival_time": stop_expected_arrival_time,
                "expected_departure_time": stop_expected_departure_time,
                "status": stop_status
            }
            stops.append(stop)

        departure = {
            "origin": origin,
            "destination": destination,
            "standard_departure_time": standard_departure_time,
            "standard_arrival_time": standard_arrival_time,
            "expected_arrival_time": expected_arrival_time,
            "expected_departure_time": expected_departure_time,
            "platform": platform,
            "status": status,
            "stops": stops
        }
        departures.append(departure)

    response = {
        "station_name": station_name,
        "departures": departures
    }

    return response

from flask import Flask , request , jsonify , abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import secrets
import random

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

app = Flask(__name__)
limiter.init_app(app)

FLIGHTS = [
    {
        "pnr": "ABC123",
        "origin": "BOM",
        "destination": "AMD",
        "flightDate": "2023-06-01",
        "seats": ["1A", "1B", "1C", "1D", "1E", "1F", "2A", "2B", "2C", "2D", "2E"],
        "seatPriceMap": ["1500", "500", "500", "500", "500", "1500", "1000", "800", "800", "800", "800"],
        "basicFare": "5500"
    },
    {
        "pnr": "DEF456",
        "origin": "DEL",
        "destination": "BOM",
        "flightDate": "2023-06-03",
        "seats": ["1A", "1B", "1C", "1D", "1E"],
        "seatPriceMap": ["2000", "1000", "1000", "1000", "1000"],
        "basicFare": "6000"
    },
    {
        "pnr": "GHI789",
        "origin": "BLR",
        "destination": "HYD",
        "flightDate": "2023-06-05",
        "seats": ["1A", "1B", "1C", "1D", "1E", "1F", "2A", "2B", "2C", "2D", "2E"],
        "seatPriceMap": ["1200", "400", "400", "400", "400", "1200", "1000", "800", "800", "800", "800"],
        "basicFare": "4500"
    },
    {
        "pnr": "JKL012",
        "origin": "CCU",
        "destination": "DEL",
        "flightDate": "2023-06-07",
        "seats": ["1A", "1B", "1C", "1D", "1E", "1F", "2A", "2B"],
        "seatPriceMap": ["1800", "600", "600", "600", "600", "1800", "1500", "1200"],
        "basicFare": "6500"
    },
    {
        "pnr": "MNO345",
        "origin": "MAA",
        "destination": "CCU",
        "flightDate": "2023-06-09",
        "seats": ["1A", "1B", "1C", "1D"],
        "seatPriceMap": ["1500", "500", "500", "500"],
        "basicFare": "5000"
    },
    {
        "pnr": "PQR678",
        "origin": "HYD",
        "destination": "BLR",
        "flightDate": "2023-06-11",
        "seats": ["1A", "1B", "1C", "1D", "1E", "1F", "2A", "2B", "2C", "2D"],
        "seatPriceMap": ["1000", "300", "300", "300", "300", "1000", "800", "600", "600", "600"],
        "basicFare": "4000"
    },
    {
        "pnr": "QTR789",
        "origin": "AMD",
        "destination": "MAA",
        "flightDate": "2023-06-13",
        "seats": ["1A", "1B", "1C", "1D", "1E"],
        "seatPriceMap": ["1200", "400", "400", "400", "400"],
        "basicFare": "5500"
    },
    {
        "pnr": "PRL123",
        "origin": "DEL",
        "destination": "HYD",
        "flightDate": "2023-06-15",
        "seats": ["1A", "1B", "1C", "1D", "1E", "1F", "2A", "2B", "2C"],
        "seatPriceMap": ["2000", "700", "700", "700", "700", "2000", "1500", "1200", "1200"],
        "basicFare": "7500"
    },
    {
        "pnr": "XYZ234",
        "origin": "BLR",
        "destination": "CCU",
        "flightDate": "2023-06-17",
        "seats": ["1A", "1B", "1C", "1D", "1E", "1F", "2A", "2B", "2C", "2D"],
        "seatPriceMap": ["1300", "500", "500", "500", "500", "1300", "1000", "800", "800", "800"],
        "basicFare": "6000"
    },
    {
        "pnr": "RTY567",
        "origin": "HYD",
        "destination": "MAA",
        "flightDate": "2023-06-19",
        "seats": ["1A", "1B", "1C", "1D", "1E", "1F", "2A", "2B", "2C", "2D", "2E", "2F"],
        "seatPriceMap": ["1200", "400", "400", "400", "400", "1200", "1000", "800", "800", "800", "500", "500"],
        "basicFare": "5000"
    },
    {
        "pnr": "UOI012",
        "origin": "CCU",
        "destination": "BOM",
        "flightDate": "2023-06-21",
        "seats": ["1A", "1B", "1C", "1D", "1E", "1F", "2A", "2B", "2C", "2D"],
        "seatPriceMap": ["2200", "800", "800", "800", "800", "2200", "1800", "1500", "1500", "1500"],
        "basicFare": "8500"
    }
]



PASSENGERS = [
    {
        "firstName": "John",
        "lastName": "Doe",
        "auth_token": "1234567890",
        "flightDetails":[{
            "flightDate": "2022-06-15",
            "pnr": "ABC123",
            "origin": "US",
            "destination": "CA",
            "passengersDetails": [
                {"firstName": "John", "lastName": "Doe", "seat": "12A"},
                {"firstName": "Jane", "lastName": "Doe", "seat": "12B"},
                ]
            }
        ]
    },
    {
        "firstName": "Alice",
        "lastName": "Smith",
        "auth_token": "0987654321",
        "flightDetails":[{
            "flightDate": "2022-07-10",
            "pnr": "DEF456",
            "origin": "CA",
            "destination": "MX",
            "passengersDetails": [
                {"firstName": "Alice", "lastName": "Smith", "seat": "7C"},
                {"firstName": "Bob", "lastName": "Jones", "seat": "7D"},
                ]
            }
        ]
    },
    {
        "firstName": "Michael",
        "lastName": "Nguyen",
        "auth_token": "1357924680",
        "flightDetails":[{
            "flightDate": "2022-08-20",
            "pnr": "GHI789",
            "origin": "FR",
            "destination": "US",
            "passengersDetails": [
                {"firstName": "Michael", "lastName": "Nguyen", "seat": "21F"},
                {"firstName": "Sarah", "lastName": "Lee", "seat": "21G"},
                ]
            }
        ]
    },
    {
        "firstName": "Emily",
        "lastName": "Chen",
        "auth_token": "2468135790",
        "flightDetails":[{
            "flightDate": "2022-09-05",
            "pnr": "JKL012",
            "origin": "AU",
            "destination": "NZ",
            "passengersDetails": [
                {"firstName": "Emily", "lastName": "Chen", "seat": "10B"},
                {"firstName": "David", "lastName": "Nguyen", "seat": "10C"},
                ]
            }
        ]
    },
    {
        "firstName": "David",
        "lastName": "Wang",
        "auth_token": "8024691357",
        "flightDetails":[{
            "flightDate": "2022-10-30",
            "pnr": "MNO345",
            "origin": "JP",
            "destination": "CN",
            "passengersDetails": [
                {"firstName": "David", "lastName": "Wang", "seat": "2A"},
                {"firstName": "Sophia", "lastName": "Kim", "seat": "2B"},
                ]
            }
        ]
    },
    {
        "firstName": "Sophie",
        "lastName": "Lee",
        "auth_token": "9753102468",
        "flightDetails":[{
            "flightDate": "2022-11-25",
            "pnr": "PQR678",
            "origin": "KR",
            "destination": "JP",
            "passengersDetails": [
                {"firstName": "Sophie", "lastName": "Lee", "seat": "15C"},
                {"firstName": "Daniel", "lastName": "Kim", "seat": "15D"},
                ]
            }
        ]
    },
    {
        "firstName": "Maria",
        "lastName": "Garcia",
        "auth_token": "8642097531",
        "flightDetails":[{
            "flightDate": "2022-12-20",
            "pnr": "STU901",
            "origin": "MX",
            "destination": "US",
            "passengersDetails": [
                {"firstName": "Maria", "lastName": "Garcia", "seat": "8F"},
                {"firstName": "Juan", "lastName": "Rodriguez", "seat": "8G"},
                ]
            }
        ]
    },
    {
        "firstName": "Mohammed",
        "lastName": "Ali",
        "auth_token": "2190384756",
        "flightDetails":[{
            "flightDate": "2023-01-10",
            "pnr": "VWX234",
            "origin": "SA",
            "destination": "FR",
            "passengersDetails": [
                {"firstName": "Mohammed", "lastName": "Ali", "seat": "5D"},
                {"firstName": "Fatima", "lastName": "Khan", "seat": "5E"},
                ]
            }
        ]
    },
    {
        "firstName": "Yuki",
        "lastName": "Sato",
        "auth_token": "3579246801",
        "flightDetails":[{
            "flightDate": "2023-02-05",
            "pnr": "YZA567",
            "origin": "JP",
            "destination": "KR",
            "passengersDetails": [
                {"firstName": "Yuki", "lastName": "Sato", "seat": "14A"},
                {"firstName": "Takashi", "lastName": "Nakamura", "seat": "14B"},
                ]
            }
        ]
    },
    {
        "firstName": "Emma",
        "lastName": "Johnson",
        "auth_token": "4680239157",
        "flightDetails":[{
            "flightDate": "2023-03-15",
            "pnr": "BCD789",
            "origin": "CA",
            "destination": "US",
            "passengersDetails": [
                {"firstName": "Emma", "lastName": "Johnson", "seat": "3C"},
                {"firstName": "Oliver", "lastName": "Brown", "seat": "3D"},
                ]
            }
        ]
    },
]


@app.route('/api/flight/retrieve' , methods=['GET'])
@limiter.limit("5 per minute")
def get_passenger_det():
    pnr = request.args.get('pnr')
    lastname = request.args.get('lastName')
    token = request.headers.get('Authorization')
    print((pnr , lastname , token))
    for passenger in PASSENGERS:
        if passenger['lastName'] == lastname:
            if f"Bearer <{passenger['auth_token']}>" == token:
                for flights in passenger['flightDetails']:
                    if flights['pnr'] == pnr:
                        resp = {}
                        for info in passenger.keys():
                            if info != "auth_token":
                                resp[info] = passenger[info]
                    else: abort(404 , 'No flights Found')
                return jsonify(resp)
            else: return abort(401 , 'Invalid Token')
    return abort(404 , 'Passenger Not Found')


            
@app.route('/api/flight/details' , methods=['POST'])
@limiter.limit("5 per minute")
def get_flight_det():
    request_dict = request.get_json()
    token = request.headers.get('Authorization')
    for passenger in PASSENGERS:
        if f"Bearer <{passenger['auth_token']}>" == token:
            for flight in FLIGHTS:
                if request_dict['origin'] == flight['origin'] and request_dict['destination'] == flight['destination'] and request_dict['flightDate'] == flight['flightDate']:
                    return jsonify(flight)
            return abort(404 , 'No Flights Found')
    return abort(401 , 'Invalid Token')
                

@app.route('/api/flight/book' , methods=['POST'])
@limiter.limit("5 per minute")
def book_flight():
    request_dict = request.get_json()
    flightDetails = request_dict['flightDetails']
    passengerDetails = request_dict['passengerDetails']
    token = request.headers.get('Authorization')

    for passenger in PASSENGERS:
        if f"Bearer <{passenger['auth_token']}>" == token:
            for flight in FLIGHTS:
                if flightDetails['origin'] == flight['origin'] and flightDetails['destination'] == flight['destination'] and flightDetails['flightDate'] == flight['flightDate']:

                    flightDetails['pnr'] = flight['pnr']
                    flightDetails['passengerDetails'] = passengerDetails
                    passenger['flightDetails'].append(flightDetails)

                    resp = {}
                    resp['pnr'] = flight['pnr']
                    resp['total'] = sum([int(val) for val , seat in zip(flight['seatPriceMap'] , flight['seats']) if seat in [passenger_['seat'] for passenger_ in passengerDetails]])
                    return jsonify(resp)
            return abort(404 , 'No Flights Found')
    return abort(401 , 'Invalid Token')


@app.route('/api/auth' , methods=['GET'])
@limiter.limit("5 per minute")
def get_new_auth():
    old_token = request.headers.get('Authorization')
    new_token = secrets.SystemRandom().getrandbits(32)
    for passenger in PASSENGERS:
        if f"Bearer <{passenger['auth_token']}>" == old_token:
            passenger['auth_token'] = new_token

            resp = {'expires':random.randint(3000 , 6000) , 'token': f'<{new_token}>'}
            return jsonify(resp)
    return abort(401 , 'Invalid Token')
            


if __name__ == '__main__':
    app.run(debug=True)
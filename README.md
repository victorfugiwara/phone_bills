# phone_bills

This is an api used to calculate the cost of Phone Bills.

There is an endpoint to receive the record calls in the json format and another one to calculate the cost of the phone call of the period.
The calculation uses different charges according to the time of the day that the call occur. 
The result of the calculation shows the costs of each call and also the total cos of the bill for the period. 


## Running Locally

Make sure you have Python 3.6.5 installed.

```sh
$ git clone https://github.com/victorfugiwara/phone_bills.git
$ cd phone_bills/

$ virtualenv env -p python3
$ source env/bin/activate

$ pip install -r requirements.txt

$ make init-db
$ make run
```

Your app should now be running on [localhost:5000](http://localhost:5000/).


## Test instructions

To execute the unit tests you just need to run the pytest:
```sh
$ pytest
```

You can also check the coverage:
```sh
$ pytest --cov api
```


## Deploying to Heroku

To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

```sh
$ git clone https://github.com/victorfugiwara/phone_bills.git
$ cd phone_bills/

$ heroku create
$ git push heroku master

$ heroku config:set FLASK_APP='api'
$ heroku open
```


## Work enviroment

The project was developed using Flask, sqlite and for the unit tests was used the libraries pytest and pytest-cov. It was coded in Sublime Text on a Lenovo T470 with Ubuntu 18.04.


## API usage

After deploy the application it can be tested using the data inside the file contrib/sample_data. There are 2 sets of data that can be used.
The data also can be used as example to create a new set of data.

The tests will be easier using a tool like [Postman](https://www.getpostman.com/). 

### POST - http://localhost:5000/api/v1/phone_call

This endpoint is used to send the call records.

Example:
```sh
{
    "call_id": 70,
    "type": "start",
    "timestamp": "2018-10-28T12:00:00Z",
    "source": "99988526423",
    "destination": "9933468278"
}
```

The response will be a json with a field "success" that indicates if the call record was saved correctly (True/False).
If false, also will has a field "errors" containing a list of errors. If true, also will has a field "processed" indicating the number of records added on database.

Example:
```sh
{
    "success": false,
    "errors": [
        "The field record_timestamp has an invalid value."
    ]
}


{
    "success": true,
    "processed": 1
}
```


### GET - http://localhost:5000/api/v1/phone_bill?subscriber=PHONE_NUMBER&period=MONTH_YEAR

This endpoint is used to retrieve the Phone Bill of the given phone number and period.
The MONTH_YEAR is not a mandatory field, but once that it is present it should follow the format mm/yyyy. If it is not given, the last closed period will be used.

Example:
```sh
http://localhost:5000/api/v1/phone_bill?subscriber=99988526423&period=10/2018
```

The response will be a json with a field "success" that indicates if the call record was saved correctly (True/False).
If false, also will has a field "errors" containing a list of errors. If true, also will has a field "data" indicating the details of the phone bill.

Example:
```sh
{
    "success": false,
    "errors": [
        "The field phone_number has an invalid value."
    ],
}


{
    "success": true,
    "data": {
        "period": "10/2018",
        "subscriber": "99988526423",
        "total": 15.39,
        "calls": [
            {
                "call_end": "Fri, 05 Oct 2018 06:00:02 GMT",
                "call_start": "Fri, 05 Oct 2018 06:00:00 GMT",
                "destination_number": "14998887654",
                "duration": "0:00:02",
                "id": 12,
                "price": 0.36
            },
            {
                "call_end": "Thu, 18 Oct 2018 12:02:45 GMT",
                "call_start": "Thu, 18 Oct 2018 12:01:45 GMT",
                "destination_number": "1833445566",
                "duration": "0:01:00",
                "id": 13,
                "price": 0.45
            },
            {
                "call_end": "Thu, 25 Oct 2018 22:00:00 GMT",
                "call_start": "Thu, 25 Oct 2018 19:56:23 GMT",
                "destination_number": "1943536785",
                "duration": "2:03:37",
                "id": 14,
                "price": 11.43
            },
            {
                "call_end": "Tue, 30 Oct 2018 06:30:26 GMT",
                "call_start": "Tue, 30 Oct 2018 05:30:04 GMT",
                "destination_number": "1345632789",
                "duration": "1:00:22",
                "id": 15,
                "price": 3.15
            }
        ]
    }
}
```



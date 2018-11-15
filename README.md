# phone_bills

This is an api used to calculate the cost of Phone Bills.

## Running Locally

Make sure you have Python 3.6.5 installed.


To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

```sh
$ git clone https://github.com/victorfugiwara/phone_bills.git
$ cd phone_bills

$ python3 -m venv phone_bills
$ pip install -r requirements.txt

$ make init-db
$ make run
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku config:set FLASK_APP='api'
$ heroku open
```

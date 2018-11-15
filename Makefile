run:
	export FLASK_APP='api' && export FLASK_ENV=development && flask run

init-db:
	export FLASK_APP='api' && export FLASK_ENV=development && flask init-db

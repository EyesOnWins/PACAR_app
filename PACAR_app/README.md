# PACAR_app

The functional application uses blockchains to manage patient medical records at any health facility.

## Instructions to run the app

Clone the project,

```sh
$ git clone https://github.com/EyesOnWins/PACAR_app.git
```

#Install the dependencies,

```sh
$ cd PACAR_app
$ pip install -r requirements.txt
```

#Start a blockchain node server,

#For linux users
```sh
$ export FLASK_APP=node_server.py 
$ flask run --port 8000
```

#For windows users
```sh
$ set FLASK_APP=node_server.py 
$ flask run --port 8000
```

One instance of our blockchain node is now up and running at port 8000.


#Run the application on a different terminal session,

```sh
$ cd PACAR_app
$ python run_app.py
```

The application should be up and running at [http://localhost:5000/login].



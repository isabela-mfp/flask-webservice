# Flask API

## A service that collects data from an Open Weather API and store it as a JSON data.

### Technologies

* Flask: This framework was chosen because it's simple and quick to develop applications. Furthermore, I already developed an application in Flask to run in a Docker container, so I was able to use previous knowledge.
* SQLite: This database was chosen because it's included in the standard library since Python 2.5 and it's a good choice for simple and lightweight databases. 
* Dotenv: This tool was chosen because it's a good popular tool and I was able to use previous knowledge since I use it every time a project needs to have private information stored.

### Endpoints

The project have two endpoints on the same url:

* `POST`: Receives a user defined ID, collect weather data from Open Weather API and stores it on database
* `GET`: Receives the user defined ID, returns with the percentage of the POST progress ID (collected cities completed) until the current moment.

## Requirements

Before you start, make sure you have:

* Docker 
* Make

## Running the Service

To run the Docker application, just run the Makefile inside the directory of the project

```
$ make
```

The Makefile will run `docker compose build` and `docker compose up` commands and get the Dockerfile's services initialized and executed.

## Testing the Service

The tests were made using `Postman` software, download it here: [https://www.postman.com/downloads/](https://www.postman.com/downloads/), no need to install it.
Open the software downloaded and create a new HTTP Request. Select `POST` or `GET` and copy the URL given by Flask running app. The port used is 32187. Here's a example URL for localhost:

```
http://127.0.0.1:32187
```
On the Query Params, create a new 'key' called `user_id` and assign a desired number to its value in front of it.
Finally, click on `Send` button to send the request. The response will be shown on the field below the Query Params
To test both `POST` and `GET` requests, you'll need to create one HTTP request for `POST` and then another one for `GET` because editing the existing request will cause the previous one to be canceled as it will only be finalized after all processing and data gathering. 

## Comments

* Free account of Open Weather API has a limit of 60 cities per minute so the service also has a limit of 60 requests per minute.
* The endpoint for Several Cities IDs on Open Weather API Several was deleted, it is not in the documentatio. The service calls the "request by city ID" for each city so the requests should take longer than expected to complete.


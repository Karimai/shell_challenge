The API documentation [url](http://www.7timer.info/doc.php#api) of 7timer.info

Four parameters:
* lon and lat: geographic coordinate of the location, 
* product: for the product you wish to use (any of "astro", "civil", "civillight", "meteo" or "two"), and 
* output for the standard you wish to use (either "xml" or "json").


### Dockerized
Includes only one container (service); shell_challenge.

### Web framework
It is written with FastAPI web server framework.

### virtual Environment:
Poetery is used.

### Run
In order to run the service, the following command should be run:
`docker-compose up --build`

### APIs
The app has mainly one API endpoint; `weather`. It can be run in two different ways:
1. Get latitude and longitude
   * latitude should be in range -90 and +90.
   * longitude should be in tange of -180 and +180.
   For example, http://127.0.0.1:8000/weather/?latitude=40.7128&longitude=-74.0060
2. Get a postalcode of Spain
    * postalcode. It supposed to be a valid 5 digit number of Spain postal code
   For example, http://127.0.0.1:8000/weather/?latitude=28014

### Future works:
* The cloud cover should be converted to solar radiation. There are some libraries which potentially are able to estimate this. Those should be investigated and be chosen according to the need. The other way some third-party API can be used, [OpenWeather](https://openweathermap.org/) for example. 
* some unit test. While some very simple unittest have been added, those are pretty simple.
* Caching can also be helpful.
* I would add a separate log service (aka container).

### Code Convention:
I added pre-commit with three hooks for code convention:
* isort
* black
* flake8
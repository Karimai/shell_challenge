import json
import logging
import os
from datetime import datetime, timedelta
from typing import Union

import httpx
import pytz
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from convertor import Convertor

app = FastAPI()
load_dotenv()

logger = logging.getLogger(__name__)


def estimate_solar_radiation(latitude: float, longitude: float, cloud_cover):
    # altitude_deg = pysol.get_altitude(latitude, longitude, current_time)
    # pysolar = "^0.10"
    # pvlib = "^0.9.4"
    # ephem = "^4.1.4"
    # solarutils = "^0.3"
    # pyclearsky = "^0.3.0"
    """
    Seems it is not straightforward to estimate solar radiation
    by cloud cover. However, there are some libraries which may help.
    Those are mentioned here.
    It was not implemented since it is a bounce part of the task assignment.
    It also needs more time since of its RD-based nature.
    """
    return cloud_cover


@app.get("/weather/")
async def get_weather(
    latitude: Union[float, int], longitude: Union[float, None] = None
):
    if longitude is None:
        logger.info("postal code")
        convertor = Convertor(os.getenv("Default_country"))
        latitude, longitude = convertor.get_latlong(str(latitude))

    if latitude < -90 or latitude > 90:
        logger.error("Invalid Latitude range!")
        return JSONResponse(
            content={
                "error": "Invalid range error, Latitude must be between -90 and +90 degrees"
            },
            status_code=400,
        )
    if longitude < -180 or longitude > 180:
        logger.error("Invalid longitude range!")
        return JSONResponse(
            content={
                "error": "Invalid range error, Longitude must be between -180 and +180 degrees"
            },
            status_code=400,
        )
    params = {
        "log": f"{longitude:.2f}",
        "lat": f"{latitude: .2f}",
        "unit": "metric",
        "output": "json",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(os.getenv("URL"), params=params)
    data = response.json()
    start_period_utc = datetime.now(pytz.UTC)
    forecasts = []
    for datum in data["dataseries"][0:16]:
        start_period_utc = start_period_utc
        end_period_utc = start_period_utc + timedelta(hours=datum["timepoint"])
        solar_radiation = estimate_solar_radiation(
            latitude, longitude, datum["cloudcover"]
        )
        temperature = datum["temp2m"]  # It is Celsius temperature
        forecast = {
            "start_period_utc": start_period_utc,
            "end_period_utc": end_period_utc,
            "solar_radiation": solar_radiation,
            "temperature": temperature,
        }
        start_period_utc = end_period_utc
        forecasts.append(forecast)
    logger.debug(f"forecasts data sent: {len(forecasts)}")
    return JSONResponse(content=json.dumps(forecasts, default=str), status_code=200)


@app.get("/")
async def root():
    """
    It is just for test. The app has only one API; /weather/.
    """
    return {"message": "test"}

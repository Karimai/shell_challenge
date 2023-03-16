from geopy.geocoders import Nominatim


class Convertor:
    def __init__(self, country: str):
        self.country = country

    def get_latlong(self, postal_code: str):
        geolocator = Nominatim(user_agent="my-app")

        # use geocode method to get the location information for the specified postal code
        location = geolocator.geocode(postal_code + f", {self.country}")

        # extract the latitude and longitude from the location object
        latitude = location.latitude
        longitude = location.longitude

        print(
            "Postal code {} corresponds to latitude {} and longitude {}.".format(
                postal_code, latitude, longitude
            )
        )

        return latitude, longitude

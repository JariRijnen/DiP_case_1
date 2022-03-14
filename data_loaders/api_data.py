from datetime import date
import os
import sys

from dotenv import load_dotenv
from pathlib import Path

from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauth2client import BearerAuth

sys.path.insert(1, os.path.join(sys.path[0], '..'))
from base_logger import logger


dotenv_path = Path('env_user.env')
load_dotenv(dotenv_path=dotenv_path)


class Amadeus_DB:
    def __init__(self):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.token_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
        self.token = self.generate_token()
        self.api_url = ('https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode'
                        '={departure_airport}&destinationLocationCode={destination}&departureDate='
                        '{flight_day}&adults=1&nonStop=false')

    def generate_token(self) -> str:
        """Generate oauth token."""
        self.client = BackendApplicationClient(client_id=self.client_id)
        self.oauth = OAuth2Session(client=self.client)
        return self.oauth.fetch_token(token_url=(self.token_url), client_id=self.client_id,
                                      client_secret=self.client_secret)['access_token']

    def insert_amadeus_data(self, departure_airport: str, destination: str, deperature_day: date,
                            return_day: date) -> list:
        """
        Insert amadeus data into a list of json type lists

        Parameters:
        departure_airport (str): Departure airport in the Netherlands
        destination (str): Destination airport
        departure_day (date): Day of departure
        return_day (date): Day of return

        Returns:
        list of lists: the first list for outward flights, the second for return flights
        """

        amadeus_outward_data = self.oauth.get(self.api_url.format(
                                              departure_airport=departure_airport,
                                              destination=destination,
                                              flight_day=deperature_day),
                                              auth=BearerAuth(self.token)).json()['data']

        # Log the airports and day if there are no flights available on the departure day
        if amadeus_outward_data == []:
            logger.info((f' No available flights between {departure_airport} and {destination} '
                         f'on day {deperature_day}.'))

        amadeus_return_data = self.oauth.get(self.api_url.format(departure_airport=destination,
                                                                 destination=departure_airport,
                                                                 flight_day=return_day),
                                             auth=BearerAuth(self.token)).json()['data']

        # Log the airports and day if there are no flights available on the return day
        if amadeus_return_data == []:
            logger.info((f' No available flights between {destination} and {departure_airport} '
                         f'on day {return_day}.'))

        return [amadeus_outward_data] + [amadeus_return_data]


if __name__ == '__main__':

    amadeus_db = Amadeus_DB()
    flights_data = amadeus_db.insert_amadeus_data('AMS', 'MAD', '2021-12-18', '2021-12-25')

    print(flights_data[1][-1])

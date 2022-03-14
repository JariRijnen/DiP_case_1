import pandas as pd

from data_loaders import api_data, sql_data
from travel_days import travel_days
from flights_finders import available_flights, select_flights
from base_logger import logger


def main():

    home_airports = ['AMS', 'EIN']

    employee_db = sql_data.Employee_DB()
    dip_df = employee_db.insert_sql_data()

    amadeus_db = api_data.Amadeus_DB()

    deperature_day, return_day = travel_days()

    return_df = pd.DataFrame()
    for __, row in dip_df.iterrows():
        try:
            destination = row['destination_iata_code']
            flights_df = pd.DataFrame()
            # Find all available flights for all home airports.
            for home_airport in home_airports:
                amadeus_data = amadeus_db.insert_amadeus_data(departure_airport=home_airport,
                                                              destination=destination,
                                                              deperature_day=deperature_day,
                                                              return_day=return_day)

                flights_data = available_flights(amadeus_data, row['name'],
                                                 row['favourite_destination'])
                flights_df = flights_df.append(flights_data)

            # Select only the best flights that match the preference
            best_flights = select_flights(flights_df)

            print(best_flights)
            return_df = return_df.append(best_flights)

        # Log the occasions where there is no IATA code given and a KeyError is raised.
        except KeyError:
            logger.info(f" {row['first_name']} has no IATA code present")
    # Save final dataframe as excel file.
    return_df.to_excel(f"output/flights_output.xlsx", index=False)


if __name__ == '__main__':
    main()

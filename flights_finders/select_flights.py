import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd

dotenv_path = Path('env_user.env')
load_dotenv(dotenv_path=dotenv_path)


def select_flights(flights_df: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a dataframe of flights and a preference (fastest/cheapest) and returns the best
    flights as a dataframe

    Parameters:
    flights_df (pd.DataFrame): Dataframe containing flights per row

    Returns:
    pd.DataFrame: Dataframe with the best flights, if there are multiple flights equally good
                  it contains all those flight options."""

    preference = os.getenv('PREFERENCE')
    df = flights_df
    best_flights = pd.DataFrame()

    # select flight(s) for both directions
    for direction in ['outward', 'return']:
        if preference == "fastest":
            fastest_single = df[df['Direction'] == direction].sort_values(['Flighttime', 'Price'])
            # append all flights there are equally good
            best_flights = best_flights.append(df[(df['Flighttime'] == fastest_single[
                                                                        'Flighttime'].iloc[0]) &
                                                  (df['Price'] == fastest_single['Price'].iloc[0])])

        elif preference == "cheapest":
            fastest_single = df[df['Direction'] == direction].sort_values(['Price', 'Flighttime'])
            # append all flights there are equally good
            best_flights = best_flights.append(df[(df['Flighttime'] == fastest_single[
                                                                        'Flighttime'].iloc[0]) &
                                                  (df['Price'] == fastest_single['Price'].iloc[0])])
    return best_flights

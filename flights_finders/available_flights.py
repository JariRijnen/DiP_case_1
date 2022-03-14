import pandas as pd


def available_flights(amadeus_data: list, name: str, destination: str) -> pd.DataFrame:
    """
    Takes a json file as input and returns a dataframe with available retourflights.

    Parameters:
    amadeus_data (list): Contains two lists, the first for outward flights, the second for
                         return flights. Both lists contain json type lists.
    name (str): Name of the employee
    destination (str): City of favourite employee' destination

    Returns:
    pd.DataFrame: Dataframe containing a single flight and related information per row.
    """

    df = pd.DataFrame(columns=('Name', 'Direction', 'IATA departure airport',
                               'IATA arrival airport', 'Price', 'Destination', 'Departure time',
                               'Arrival time', 'Flighttime', 'Stops', 'Airlines'))

    # use both flight directions
    for k, direction in enumerate(['outward', 'return']):
        # iterate over every flight within the direction list
        for data_entry in amadeus_data[k]:
            iata_departure_airport = data_entry['itineraries'][0]['segments'][0]['departure'][
                'iataCode']
            # strip time from irrelevant characters
            departure_time = data_entry['itineraries'][0]['segments'][0][
                                                'departure']['at'].replace('T', ' ')
            iata_arrival_airport = data_entry['itineraries'][0]['segments'][-1]['arrival'][
                'iataCode']
            arrival_time = data_entry['itineraries'][0]['segments'][-1][
                                            'arrival']['at'].replace('T', ' ')
            time = data_entry['itineraries'][0]['duration']
            mins = ':0' if time[-3:-2] == 'H' else (':00:00' if time[-1] == 'H' else ':')
            flighttime = time.replace('H', mins).replace('M', ':00')[2:]

            price = float(data_entry['price']['total'])
            airlines = [
                data_entry['itineraries'][0]['segments'][j]['carrierCode'] for j in range(
                    0, len(data_entry['itineraries'][0]['segments']))]
            stops = [data_entry['itineraries'][0]['segments'][j][
                'arrival']['iataCode'] for j in range(
                    0, len(data_entry['itineraries'][0]['segments'])-1)]

            # append all flight data into a new row for the return dataframe
            df = df.append({'Name': name, 'Direction': direction,
                            'IATA departure airport': iata_departure_airport,
                            'IATA arrival airport': iata_arrival_airport, 'Price': price,
                            'Destination': destination, 'Departure time': departure_time,
                            'Arrival time': arrival_time, 'Flighttime': flighttime,
                            'Stops': stops, 'Airlines': airlines},
                           ignore_index=True)

    return df

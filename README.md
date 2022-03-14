# Project Flighttickets for DiP

### Date created
16-12-2021

### Description
First case of data engineer traineeship by Jari Rijnen.

Project in python to find flight tickets by preference (cheapest or fastest) between the Netherlands and a destination airport for DiP employees for next saturday and the return flight one week later on saturday. Output is returned in a .xlsx file.

Currently uses Amsterdam Schiphol and Eindhoven Airport as departure airports.

### Use
Entire repo is called by main.py. Requires environmental variables to access the data sources. 

Preference (cheapest/fastest) is also set as environmental variable.

If there happen to be no flights between two airports on a given day, this will be logged in the log file.

### Input Data Sources used
- [Amadeus API](https://developers.amadeus.com/)
- PostgreSQL database with DiP Employee name, favourite destination and IATA code. Can chose between 'dip_employees' (dummy data) and 'dip_employees2' (full data).

### Example Output
Name|Direction|IATA departure airport|IATA arrival airport|Price|	Destination|Departure time|Arrival time|Flighttime|Stops|Airlines
--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------
Jari Rijnen|	outward|	AMS|	VNO|	110,33|	Vilnius|	2021-12-18 10:25:00|	2021-12-18 23:30:00|	12:05:00|	['CPH']|	['SK', 'SK']
Jari Rijnen|	return|	VNO|	AMS|	104,14|	Vilnius|	2021-12-25 07:50:00|	2021-12-25 09:20:00|	2:30:00|	[]|	['BT']


### Credits
Thanks to [https://github.com/dennisdickmann-digital-power](https://github.com/dennisdickmann-digital-power), [https://github.com/sandervandorsten](https://github.com/sandervandorsten) and [https://github.com/timmolleman1](https://github.com/timmolleman1).

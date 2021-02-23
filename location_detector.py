"""
DARIA SHABATSKA
LAB 3 TASK 3
GitHub: https://github.com/S-Daria/LAB3_TASK3.git
"""

# import json
import requests
from random import randint
from geopy.geocoders import Nominatim
import csv


def twitter_api(username, bearer_token):
    """
    Get twitter username
    return .json file with friends list of a user with given username from twitter
    """
    base_url = "https://api.twitter.com/"

    search_url = f'{base_url}1.1/friends/list.json'

    search_headers = {
        'Authorization': f'Bearer {bearer_token}'
    }

    search_params = {
        'screen_name': username,
        'count': 15
    }

    response = requests.get(
        search_url, headers=search_headers, params=search_params)
    return response.json()['users']


def coorninates_by_place(place: str) -> tuple:
    """
    get the place as a string
    with geolocator find the coordinates of a place
    return coordinates if the place exist
    return False if not
    """
    geolocator = Nominatim(user_agent="location_detector.py")
    location = geolocator.geocode(place)
    try:
        return (str(location.latitude), str(location.longitude))
    except AttributeError:
        return False


def locator(json_list):
    """
    get list with friends of a user from json file
    return list with five elements (five random friends): tuples
    tuple content following info ('name', 'place', 'latitude', 'longitude')
    """
    index_list = []
    friends_list = []
    while len(index_list) < 5:
        index = randint(0, len(json_list) - 1)
        if index not in index_list and json_list[index]['location']:
            coordinates = coorninates_by_place(json_list[index]['location'])
            if coordinates:
                index_list.append(index)
                friends_list.append(
                    (json_list[index]['name'], json_list[index]['location'], *coordinates))

    return friends_list


def write_data_in_csv(data_list):
    """
    get list fwith data about friends of a user
    write data in csv file
    """
    with open('friends_location.csv', mode='w', encoding="utf-8") as location_file:
        friend_location = csv.writer(location_file, delimiter=',',
                                     quotechar='"', quoting=csv.QUOTE_MINIMAL)
        friend_location.writerow(['name', 'place', 'latitude', 'longitude'])
        for friend in data_list:
            friend = list(friend)
            print(friend)
            friend_location.writerow(friend)


def make_csv_location(username, token):
    """
    navigate through the friends list from twitter of a input user
    """
    decoded_object = twitter_api(username, token)
    locations_list = locator(decoded_object)
    print(locations_list)
    write_data_in_csv(locations_list)

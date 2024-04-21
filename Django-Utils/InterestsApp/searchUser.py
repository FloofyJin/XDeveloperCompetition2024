"""A simple example demonstrating text completion."""

import asyncio
import sys

import xai_sdk

import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time

import environ

env = environ.Env()
environ.Env.read_env()

def auth():
    return "AAAAAAAAAAAAAAAAAAAAAGqWtQEAAAAALiJtoGZUETocIS0KJlWQ0tA8pjA%3DnVnIQCcBDBl6YtckVG7l0ByZttfwZKBEXUHZlWPYJCtUkWU0fd"
    #return os.environ["AUTHORIZATION_TOKEN"]

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    # print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

async def givetweet(usernames):
    """Runs the example."""
    # client = xai_sdk.Client()
    res = []
    for name in usernames:

        username = name
        url = f"https://api.twitter.com/2/users/by/username/{username}"

        # Bearer Token needed for authentication (not your access tokens)
        bearer_token = auth()
        headers = create_headers(bearer_token)
        response = requests.request("GET", url, headers = headers)
        print("Twitter User API response: " + str(response))
        # print("Endpoint Response Code: " + str(response.status_code))
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)
        userId = response.json()["data"]["id"]
        # print(userId)

        user_id = userId
        params = {"tweet.fields": "created_at", "max_results": 5, "exclude": "replies"}
        url = "https://api.twitter.com/2/users/{}/tweets".format(user_id)
        json_response = connect_to_endpoint(url, headers, params)
        userTweets = json.dumps(json_response, indent=4, sort_keys=True)
        print("userTweets: " + userTweets)
        parsedTweet = json.loads(userTweets)
        try:
            if parsedTweet and parsedTweet["data"] and parsedTweet["data"][0] and parsedTweet["data"][0]["text"]:
                latestTweet = parsedTweet["data"][0]["text"]
                res.append((name, latestTweet))
        except Exception as e:
            print(f"parsedTweet error: {e}")
            return []
    
    return res



# asyncio.run(main())

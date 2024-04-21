import requests
from django.shortcuts import render, redirect
from django.urls import reverse
import xai_sdk
import json
from InterestsApp.searchUser import givetweet
import asyncio
import sys
from django.shortcuts import render, redirect
import xai_sdk
import asyncio

global_subtopics = []
global_responses = {}

def user_recommendation():
    print("finding user recommendation")
    # hardcoded_subtopics = {'Risk management': True, 'Asset allocation': True, 'Diversification': False, 'Fundamental analysis': False, 'Technical analysis': False}
    if len(global_responses) == 0:
        print("no subtopic: defaulting")
        return ["elonmusk", "jinnacles", "PeterSchiff", "RedDogT3", "OptionsHawk", "CNBC"]
    else:
        interests = "Human: I am interested in the topics: "
        for k,v in global_responses.items():
            if v:
                interests += str(k) + ", "
        interests += ". can you list me 10 prominent users on X/twitter that is known for that particular topic. give me a response in format: [username1, username2, ...]. Only give "
        
        res = asyncio.run(ask_grok(interests))

        if type(res) != list:
            print("bad response: defaulting")
            return ["elonmusk", "jinnacles", "PeterSchiff", "RedDogT3", "OptionsHawk", "CNBC"]
        return res

def home(request):
    """
    Home page of the website.
    Takes a topic from the user and queries Grok to find 5 subtopics related to the topic
    """
    if request.method == 'POST':
        # Get the text input from the user
        search_query = request.POST.get('search_query', '')
        prompt = "This is a conversation between a human user and a highly intelligent AI. " \
                 "The AI's name is Grok and it makes every effort to truthfully answer a user's questions. " \
                 "It always responds politely but is not shy to use its vast knowledge in order to solve " \
                 "even the most difficult problems. The conversation begins." \
                 "Give me a comma separated list of 5 most important subtopics related to the " \
                 "main topic of " + search_query + ". Only output the 5 subtopics and nothing else." \
                                                   "Also do not number order the output."
        print("Asking grok for subtopics...")
        subtopics = asyncio.run(ask_grok(prompt))
        print("Topic: " + search_query)  # Topic
        print("Subtopic: " + subtopics)  # Grok given subtopics

        # Split the subtopics string by comma and strip whitespace from each subtopic
        subtopics_list = [subtopic.strip() for subtopic in subtopics.split(',')]

        # Remove empty strings from the list
        subtopics_list = [subtopic for subtopic in subtopics_list if subtopic]
        subtopics_list = [subtopic.capitalize() for subtopic in subtopics_list]

        if not subtopics_list or (len(subtopics_list) == 0):
            print("GROK ERROR: no subtopics returned")
            # return render(request, 'home.html')
            subtopics_list = ['Risk management', 'Asset allocation', 'Diversification', 'Fundamental analysis',
                              'Technical analysis']

        # Update the global_subtopics list
        global_subtopics.clear()  # Clear the list before updating
        global_subtopics.extend(subtopics_list)

        print(f'type(subtopics_list): {type(subtopics_list)}')
        print(f'type(global_subtopics): {type(global_subtopics)}')
        print(f'global_subtopics: {global_subtopics}')

        return redirect('choices', search_query=search_query)
    return render(request, 'home.html')


def choices(request, search_query):
    if request.method == 'POST':
        # Handle form submission
        user_responses = {}
        for subtopic in global_subtopics:
            # Get the user's response for each subtopic
            response = request.POST.get(subtopic, None)
            print(f'type(resopnse): {type(response)}')
            if response is not None:
                # Store the user's response in the dictionary
                if response == 'Yes':
                    user_responses[subtopic] = True
                else:
                    user_responses[subtopic] = False

        print("User responses:", user_responses)

        return redirect(reverse('result'))

    # If it's a GET request, render the choices.html template with subtopics
    return render(request, 'choices.html', {'search_query': search_query, 'subtopics': global_subtopics})


async def ask_grok(prompt):
    """Runs the example."""
    client = xai_sdk.Client()

    conversation = client.grok.create_conversation()

    # Hard-coded input message
    user_input = str(prompt)

    token_stream, _ = conversation.add_response(user_input)
    response = ""
    count = 0
    async for token in token_stream:
        response += token
        count += 1
        if count > 500:
            break
    return response
  
def result_view(request):
    usernames = user_recommendation()
    # print(usernames)
    # usernames= ["elonmusk", "jinnacles", "CNBC"]
    userTweets = asyncio.run(givetweet(usernames))
    return render(request, 'result.html', {'response': userTweets})


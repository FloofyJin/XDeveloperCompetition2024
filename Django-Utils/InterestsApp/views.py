import requests
from django.shortcuts import render, redirect
import xai_sdk
import json
from InterestsApp.searchUser import givetweet
import asyncio

def home(request):
    if request.method == 'POST':
        # Get the text input from the user
        search_query = request.POST.get('search_query', '')
        prompt = "Give me a comma separated list of 5 most important subtopics related to the main topic of " + search_query
        subtopics = asyncio.run(ask_grok(prompt))
        print(search_query) # Topic
        print(subtopics) # Grok given subtopics
        return redirect('choices', search_query=subtopics)
    return render(request, 'home.html')

def choices(request, search_query):
    return render(request, 'choices.html', {'search_query': search_query})

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
    usernames= ["elonmusk", "jinnacles"]
    userTweets = asyncio.run(givetweet(usernames))
    return render(request, 'result.html', {'response': userTweets})


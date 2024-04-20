import requests
from django.shortcuts import render, redirect
import xai_sdk
import asyncio

def home(request):
    if request.method == 'POST':
        # Get the text input from the user
        search_query = request.POST.get('search_query', '')
        prompt = "Give me a comma separated list of 5 most important subtopics related to the main topic of " + search_query
        subtopics = asyncio.run(ask_grok(prompt))
        print(subtopics)
        '''
        # Call the external API (replace API_URL with the actual API endpoint)
        API_URL = 'https://api.example.com/search'
        headers = {'Authorization': 'Bearer YOUR_API_KEY'}  # Add your API key or authentication here
        params = {'query': search_query}
        
        response = requests.get(API_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Pass the data to the template
            return render(request, 'home.html', {'data': data, 'search_query': search_query})
        else:
            # Handle API error
            error_message = 'Failed to fetch data from the external API.'
            return render(request, 'home.html', {'error_message': error_message})
    else:
        return render(request, 'home.html')
    '''
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
    async for token in token_stream:
        response += token
    return response
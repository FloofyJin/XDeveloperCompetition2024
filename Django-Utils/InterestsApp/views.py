# views.py

from django.shortcuts import render
import asyncio
import sys
import xai_sdk

async def main():
    """Runs the example."""
    client = xai_sdk.Client()

    conversation = client.grok.create_conversation()

    # Hard-coded input message
    user_input = "What twitter handles should I follow if I like investing,"

    token_stream, _ = conversation.add_response(user_input)
    response = ""
    async for token in token_stream:
        response += token
    return response

def api_view(request):
    response = asyncio.run(main())
    print(f'response: {response}')
    return render(request, 'api.html', {'response': response})
  
def result_view(request):
    return render(request, 'result.html',{'response': "hello world"})

# views.py in InterestsApp

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

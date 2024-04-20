"""A simple example demonstrating text completion."""

import asyncio

import xai_sdk


async def main():
    """Runs the example."""
    client = xai_sdk.Client()

    prompt = "The answer to live and the universe is"
    print(prompt, end="")
    async for token in client.sampler.sample(prompt, max_len=3):
        print(token.token_str, end="")
    print("")


asyncio.run(main())
This bot is based on [spigot-drama-generator](https://github.com/mdcfe/spigot-drama-generator), with data from [mja00's fork](https://github.com/mja00/spigot-drama-generator)

# How to run
1. Run `pip install -r requirements.txt`.
2. Make a copy of `example.env` and rename it to `.env` (or just set the environment variables accordingly).
3. Create a Discord bot and write down its token.
4. Open the `.env` file and configure the bot (Discord token, API base URL, LLM API key...). 
The example.env assumes you will use Google's Gemini LLM. You can log in https://aistudio.google.com/ to get an API key that you can use within the free tier.

## How to use other LLM services
In general, you'll only need to change the base URL and API key. A couple examples of base URLs:

**OpenAI:** `https://api.openai.com/v1` 
**OpenRouter:** `https://openrouter.ai/api/v1`

## Setting up image generation
Make an account in https://fal.ai/ and set your API key.
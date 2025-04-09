from discord_bot import DramaGenDiscordBot
from parameters import Parameters

bot_params = Parameters() # type: ignore - https://github.com/pydantic/pydantic/issues/3753
DramaGenDiscordBot(bot_params).run()
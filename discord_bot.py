import os
import random
import aiohttp
import logging
import discord
import asyncio
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from parameters import Parameters
from drama_generator import AIDramaGenerator

class DramaGenDiscordBot(commands.Cog):
    def __init__(self, parameters: Parameters):
        intents = discord.Intents.default()
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.bot_token = parameters.discord_token
        self.ai_generator = AIDramaGenerator(parameters)

    def run(self):
        main_cog = DramaGenMainCog(self.ai_generator, self.bot)
        asyncio.run(self.bot.add_cog(main_cog))
        self.bot.run(self.bot_token.get_secret_value())

class DramaGenMainCog(commands.Cog):
    def __init__(self, drama_generator: AIDramaGenerator, bot: commands.Bot):
        self.drama_generator = drama_generator
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in')

    @app_commands.command(name="gen_drama", description="Create some Paper Drama")
    async def gen_drama(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False)
        try:
            drama = await self.drama_generator.generate_ai_drama()
        except Exception as ex:
            await interaction.followup.send(f"There was an error :(\n```{ex}```")
            return
        
        random_color = discord.Color(random.randint(0, 0xFFFFFF))    
        embed = discord.Embed(
            title=drama.headline,
            description=drama.body,
            color=random_color
        )

        image_url = drama.image_url
        if not image_url:
            await interaction.followup.send(embed=embed)
            return
        
        drama_file_name = "drama_image_" + datetime.now().strftime("%d%m%y%H%M%S") + ".png"
        file = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status == 200:
                        image_data = await resp.read()
                        with open(drama_file_name, "wb") as f:
                            f.write(image_data)
                        embed.set_image(url=f"attachment://{drama_file_name}")
                        file = discord.File(drama_file_name)
        except Exception:
            logging.exception("Failed to attach drama image")
        finally:
            if file is None:
                await interaction.followup.send(embed=embed)
            else:
                await interaction.followup.send(embed=embed, file=file)

            try:
                os.remove(drama_file_name)
            except Exception:
                logging.exception(f"Failed to delete image {drama_file_name}")
import asyncio
import logging
import logging.handlers
from typing import List, Optional
#import asyncpg TODO database
import discord
from discord.ext import commands
from aiohttp import ClientSession

import settings # api keys

class PlatoBot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        #db_pool: asyncpg.Pool, TODO database
        web_client: ClientSession,
        testing_guild_id: Optional[int] = settings.testing_discord_id, # AI Bot Testing server
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        #self.db_pool = db_pool TODO database
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:
        # load extensions prior to syncing
        for extension in self.initial_extensions:
            await self.load_extension(extension)

        # setup sync for testing guild only
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            # copy in global commands to test
            self.tree.copy_global_to(guild=guild)
            # then sync to testing guild
            await self.tree.sync(guild=guild)
        
        # TODO load db here later

async def main():
    # start loggingW
    # using rotating file logger

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024, # 32MiB
        backupCount=5 # rotate through 5 files
    )
    date_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', date_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create web client & db pool which cleanup at exit
    # then start bot
    async with ClientSession() as our_client: # asyncpg.create_pool(user='postgres', command_timeout=30) as pool: TODO uncomment when db is implemented
        exts = [] # TODO list cogs later
        intents = discord.Intents.default() # default permissions
        intents.message_content = True # privleged TODO review if bot gets invited to 100 servers
        async with PlatoBot(
            commands.when_mentioned,
            #db_pool=pool, TODO database
            web_client=our_client,
            initial_extensions=exts,
            intents=intents,
        ) as bot:
            await bot.start(settings.discord_bot_token)

# now that what needs to run has been defined, tell asyncio to run it
asyncio.run(main())

# code sourced from https://github.com/Rapptz/discord.py/blob/v2.6.3/examples/advanced_startup.py (thank you!)
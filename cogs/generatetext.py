from discord.ext import commands
from gentext import gen_text

class GenerateText(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # prevent bot from replying to itself        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
             return

        if f'<@{self.bot.user.id}>' in message.content:
            # first, grab most recent 20 messages in that channel
            channel = self.bot.get_channel(message.channel.id)
            history_data = [past_message async for past_message in channel.history(limit=20)]
            
            # history currently has all data on every message, get author id and message
            history = []
            for msg in history_data:
                past_message = await channel.fetch_message(msg.id)
                history.append({
                    "author_id": msg.author.id,
                    "message": past_message.content
                })
            
            # send prompt and message history to bot
            response = await gen_text(f'user prompt: {message.content}\nlist of past 20 messages in channel:\n{history}')
            await message.reply(response)

async def setup(bot):
    await bot.add_cog(GenerateText(bot))
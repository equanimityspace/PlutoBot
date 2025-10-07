from discord.ext import commands
from gentext import gen_text

class GenerateText(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
             return

        if f'<@{self.bot.user.id}>' in message.content:
            response = await gen_text(message.content)
            await message.reply(response)

async def setup(bot):
    await bot.add_cog(GenerateText(bot))
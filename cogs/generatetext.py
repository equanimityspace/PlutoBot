from discord.ext import commands


class GenerateText(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
             return

        if f'<@{self.bot.user.id}>' in message.content:
            await message.reply(f'Hello! You said {message.content}')

async def setup(bot):
    await bot.add_cog(GenerateText(bot))
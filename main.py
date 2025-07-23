import discord
import random
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.command(name="say")
@commands.has_permissions(administrator=True)
async def announce(ctx, *, message: str):
    """Prefix command: !say <message>"""
    await ctx.send(message)


@bot.command(name="guess")
async def guess(ctx):
    """Prefix command: !guess - Number guessing game (reply-based)"""
    number = random.randint(1, 50)
    bot_message = await ctx.send("Guess a number between 1 and 50! **Reply to this message** with your guess.")

    def check(m):
        return (
            m.author == ctx.author and
            m.channel == ctx.channel and
            m.reference is not None and
            m.reference.message_id == bot_message.id
        )

    try:
        msg = await bot.wait_for("message", check=check, timeout=15)
        try:
            guess_number = int(msg.content.strip())
            if 1 <= guess_number <= 50:
                if guess_number == number:
                    await ctx.send(f"🎉 Correct, {ctx.author.mention}! The number was {number}.")
                else:
                    await ctx.send(f"❌ Incorrect, {ctx.author.mention}. The correct number was {number}.")
            else:
                await ctx.send("Your guess must be between 1 and 50.")
        except ValueError:
            await ctx.send("Please reply with a **number only**, not text.")
    except:
        await ctx.send("⏰ Time's up! Try again with `!guess`.")


class AnnounceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="say", description="Send an announcement (slash command)")
    @app_commands.describe(message="The announcement message")
    async def announce_slash(self, interaction: discord.Interaction, message: str):
        if interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(message)
        else:
            await interaction.response.send_message(
                "You need administrator permissions to use this command.",
                ephemeral=True
            )


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"✅ {len(synced)} slash commands synced.")
    except Exception as e:
        print(f"❌ Failed to sync slash commands: {e}")

    await bot.add_cog(AnnounceCog(bot))


bot.run("MTM5NzE0NDE4OTIwODEwNTEwMg.GQDhoC.C2xX48fovRQ7PzGfu9G2yGsVH7YWflX7P3bdvQ")
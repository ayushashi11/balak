import json
import os
from typing import Callable, Union
import discord
from discord.embeds import Embed
from discord.ext.commands.core import command
from discord.ext.commands.errors import MissingAnyRole, MissingPermissions, MissingRole
import pyowm
import pyowm.weatherapi25.observation
import ai_m2
import random
from discord.ext import commands
from settings_manager import SettingsManager
from pyowm import OWM
from math import *
from dotenv import load_dotenv
from youtube import search as searchy, subprocess as sb
load_dotenv()
TOKEN="NzQ5NjQwMDIyNzUxMTgyODY4.X0u6rQ.1chmygOPmi8ZqzO2Aiqx3Kqs7vE"
bot = commands.Bot(command_prefix='b')
r=random.random
#DB=int(os.getenv("DBID"))
key="2223ec0573fa9465ff0aeff7557ccfc8"
owm=OWM(key)
owm=owm.weather_manager()
sm = SettingsManager()

def get_bool(s: str) -> bool:
    if s.lower() in ["t", "true", "yes", "y", "enable", "on"]:
        return True
    return False

def tes(f: Callable) -> Callable:
    print(f, f.name)
    return f

def get_role(guild, name):
    tc = discord.utils.find(lambda g: g.name==name, guild.roles)
    return tc

def get_channel(guild, id):
    tc = discord.utils.find(lambda g: g.id==id, guild.channels)
    return tc

async def error(ctx, error):
    print(error)
    em=Embed(title="Error!", description='*The following error has occured* **'+repr(error).replace('*','\\*')+'**', url="https://discord.gg/VXFsKzf", color=0xff0000)
    if not (isinstance(error, commands.ArgumentParsingError) or isinstance(error, commands.MissingRequiredArgument) or isinstance(error, MissingRole) or isinstance(error, MissingAnyRole) or isinstance(error, MissingPermissions)):
        em.set_footer(text="**Please report this to the dev**\nClick on the title to get the report server invite")
    await ctx.send(embed=em)

@bot.command(name='.',help='talk to velcem', )
async def on_message(ctx: commands.Context, *messages):
    async with ctx.typing():
        message=" ".join(messages)
        print(message)
        await ctx.send(ai_m2.reply(message))
@bot.command(name='.roll_dice', help='Simulates rolling dice.', )
async def roll(ctx, number_of_dice: int, number_of_sides: int):
    await ctx.trigger_typing()
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))
@bot.command(name='.calculate', help='Does simple math stuff')
async def calc(ctx, string: str):
    await ctx.trigger_typing()
    await ctx.send(str(eval(string)))

@bot.command(name='.create-channel')
async def create_channel(ctx, channel_name='!stonks_chennel'):
    auth_roles = [x.name for x in ctx.author.roles]
    print("Coder" in auth_roles,auth_roles)
    if not ("Edminh" in auth_roles or "Programmer" in auth_roles):
        return
    guild = ctx.guild
    print(ctx.command,ctx.command.__dict__)
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        catg = discord.utils.get(guild.categories, name="chat")
        await guild.create_text_channel(channel_name,category=catg)

@bot.command(name=".info",help="get server and user info")
async def info(ctx: commands.Context):
    await ctx.trigger_typing()
    ret = f"Guild id:- {ctx.guild.id}\nMembers:\n- "
    ret += "- ".join([f"{member.name} {member.status}" for member in ctx.guild.members])
    await ctx.send(ret)

@bot.command(name=".weather")
async def weather(ctx,city: str):
    ctx.send(
        embed=Embed(
            title="This command is under testing",
            description="due to the recent updates to the Open Weather api,  the bot's weather api is broken, but still a new api is under work",
            color=0x0000ff
        )
    )
    async with ctx.typing():
        obs: pyowm.weatherapi25.observation.Observation=owm.weather_at_place(city)
        print(obs)
        await ctx.send(repr(obs))
        ret: pyowm.weatherapi25.observation.weather.Weather = obs.weather
        print(ret)
        await ctx.send(f'the weather conditions will most likely be {ret["detailed_status"]},\nTemperature will remain around {ret["temperature"]["temp"]-273.15}\u00b0C, Humidity {ret["humidity"]}%. Winds will blow at {ret["wind"]["speed"]*3.6} kph at {ret["wind"]["deg"]}\u00b0 from North')

@bot.command(name="connect")
async def connect(ctx, chan: discord.VoiceChannel):
    vc=ctx.voice_client
    if vc:
        await vc.move_to(chan)
    else:
        await chan.connect()
        vc=ctx.voice_client
    vc.play(discord.FFmpegPCMAudio('text.mp3'), after=(lambda e: print(f"Finished playing: {e}")))
    # Lets set the volume to 1
    vc.source = discord.PCMVolumeTransformer(vc.source)
    vc.source.volume = 1

@bot.command()
async def search(ctx, query: str):
    async with ctx.typing():
        await ctx.send("searching...")
        await ctx.send(repr(await searchy(ctx, query)))

@bot.command()
async def play(ctx, chan: discord.VoiceChannel, query: str):
    await search(ctx, query)
    await connect(ctx, chan)

@bot.command()
async def repeat(ctx: commands.Context, message: str, number: int=1):
    if ctx.author.id != 303140523038998529 and number>=10:
        await ctx.trigger_typing()
        await ctx.send("Sorry but you dont have permissions to get more than 10 repeats")
        return
    async with ctx.typing():
        for i in range(number):
            await ctx.send(message)

@bot.command()
async def make_me_admin(ctx):
    await ctx.trigger_typing()
    print(ctx)
    if ctx.author.id == 303140523038998529:
        await ctx.author.add_roles(role:=get_role(ctx.guild,"Admin"))
        print(role)
    else:
        await ctx.send("No. Imma lazy and don't want to")

@bot.command()
async def what_are_my_roles(ctx):
    await ctx.trigger_typing()
    await ctx.send("\n".join([x.name.lstrip("@") for x in ctx.author.roles]))

@bot.command()
async def disconnect(ctx):
    vc=ctx.voice_client
    await vc.disconnect()

#@bot.command()
#async def execute(ctx, *command):
#    async with ctx.typing():
#        auth_roles = [x.name for x in ctx.author.roles]
#        print("Coder" in auth_roles,auth_roles)
#        if not ("Edminh" in auth_roles or "Programmer" in auth_roles):
#            return
#        res = sb.Popen(["bash","-c",f"{' '.join(command)}"], stdout=sb.PIPE)
#        while res.poll() is None:
#            pass
#        await ctx.send(res.stdout.read().decode())

@bot.command()
async def alak(ctx):
    await ctx.trigger_typing()
    await ctx.send("Han! balak."+ctx.author.mention)

@bot.command()
async def clear(ctx, amount=2.0):
    await ctx.trigger_typing()
    negflag, embed = False, None
    if amount < 0:
        embed = discord.Embed(title="Negative", description=f"your given value was negative, so I took the absolute value **{-amount}**", color=0xcc0000)
        amount = -amount
        negflag = True
    amount = round(amount)
    if amount > 100:
        embed = discord.Embed(title="Overflow", description=f"Amount too large **{-amount}**\nNot allowed", color=0xcc0000)
        await ctx.send(emed=embed)
    await ctx.channel.purge(limit=amount)
    if negflag:
        await ctx.send(embed=embed)
    await ctx.send(f"**__{amount}__** messages were deleted")

@bot.command(name=".kick")
async def perms(ctx: commands.Context, user: discord.Member, reason: str):
    await ctx.trigger_typing()
    user_can: discord.Permissions = ctx.author.permissions_in(ctx.channel)
    if user_can.kick_members:
        embed = discord.Embed(title="Kicked!", description=f"**{user.name}** was kicked by {ctx.author.mention}", color=0xcc2222)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Reason", value=reason)
        await ctx.send(embed=embed)
        await user.kick(reason=reason)
        chan: discord.DMChannel = await user.create_dm()
        await chan.trigger_typing()
        await chan.send(f"You kicked by __{ctx.author.mention}__ from {ctx.guild.name}\nfor {reason}")
    else:
        embed = discord.Embed(title="Denied!", description=f"{ctx.author.mention}, you arent allowed to kick", color=0xcc0055)
        await ctx.send(embed=embed)

@bot.command(name=".settings", aliases=[".s"])
async def settings(ctx: commands.Context, *args):
    print(args)
    with sm as s:
        for arg in args:
            if "=" in arg:
                key, value = arg.split("=")
                if key == "system_channel":
                    c = int(value[value.index("#")+1:-1])
                    print(c)
                    s.set_sys_channel(ctx.guild.id, c)
                    await ctx.send("**Done!**")
                elif key == "announcement_channel":
                    c = int(value[value.index("#")+1:-1])
                    print(c)
                    s.set_ann_channel(ctx.guild.id, c)
                    await ctx.send("**Done!**")
                elif key == "greet":
                    s.set_greet(ctx.guild.id, get_bool(value))
                    await ctx.send("**Done!**")
                elif key == "mute on ping":
                    s.set_mute_everyone(ctx.guild.id, get_bool(value))
                    await ctx.send("**Done!**")
                else:
                    embed = discord.Embed(title="Error!", description=f"incorrect key!", color=0xcc0055)
                    await ctx.send(embed=embed)

@bot.command(".announce", aliases=[".ann"])
async def announce(ctx: commands.Context, text: str, *args):
    with sm as s:
        chan: Union[discord.TextChannel, None] = None
        if (cha_id := s.get_ann_channel(str(ctx.guild.id))) is not None:
            chan = get_channel(ctx.guild, cha_id)
        else:
            chan = ctx.guild.system_channel
        await chan.trigger_typing()
        reactor = {}
        for emoji, role in map(lambda x: x.split("="), args):
            reactor[emoji.strip()] = role.strip()
        embed = Embed(title=f"Announcement by {ctx.author.mention}", description=text, color=0x0000ff)
        embed.add_field(name="Reactions", value="\n\t".join(args))
        msg: discord.Message = await chan.send(embed=embed)
        print(msg, reactor)
        s.add_reactor_channel(str(ctx.guild.id), str(msg.id), reactor)

@bot.command(name=".report", aliases=[".r", "r"])
async def report(ctx,text: discord.Message):
    await text.add_reaction("😠")

@bot.command()
async def please_unmute(ctx: commands.Context):
    guild = ctx.guild
    with sm as s:
        cha_id = s.get_sys_channel(str(guild.id))
        if cha_id is not None:
            cha: discord.TextChannel = get_channel(guild, cha_id)
            await cha.send(f"**Alert __Admins__**,\n {ctx.author.mention} wants to be unmuted, if his punishment is complete please unmute him")
        else:
            await guild.system_channel.send(f"**Alert __Admins__**,\n {ctx.author.mention} wants to be unmuted, if his punishment is complete please unmute him")

@bot.command()
async def test(ctx: commands.Context):
    async for entry in ctx.guild.audit_logs(limit=100):
        print(entry.__dict__)
    await ctx.send("***This is a testing/ developement command, if you aren't the developers of this don't use it***")
    raise BaseException("lol")

@bot.command(aliases=[".v"])
async def version(ctx):
    await ctx.send("1.0.7")

for command in bot.commands:
    command.error(error)

bot.run(TOKEN)

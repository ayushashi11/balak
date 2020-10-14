import os
import asyncio
from os import name
import discord
from discord.activity import Game
from dotenv import load_dotenv
from settings_manager import SettingsManager
load_dotenv()
TOKEN="NzQ5NjQwMDIyNzUxMTgyODY4.X0u6rQ.1chmygOPmi8ZqzO2Aiqx3Kqs7vE"
client = discord.Client()
o = True
sm = SettingsManager()

def get_role(guild, name):
    tc = discord.utils.find(lambda g: g.name==name, guild.roles)
    return tc

def get_channel(guild, id):
    tc = discord.utils.find(lambda g: g.id==id, guild.channels)
    return tc

@client.event
async def on_ready():
    print("-\n".join(x.name for x in client.guilds))
    activity = Game(name="balak | bhelp")
    await client.change_presence(activity=activity)

@client.event
async def on_member_join(member: discord.Member):
    g: discord.Guild = member.guild
    channel: discord.TextChannel = g.system_channel
    embed = discord.Embed(title="Welcome!", description="Welcome "+member.mention)
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)
    await member.create_dm()

@client.event
async def on_invite_create(invite):
    nm=invite.inviter.name
    await invite.channel.send(f"{nm} created an invite ")

@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    print(reaction, reaction.emoji)
    if reaction.emoji != "😠":
        print("raw", reaction.emoji)
        with sm as s:
            msg: discord.Message = reaction.message
            guild0: discord.Guild = msg.guild
            rid = s.get_reaction_role(str(guild0.id), str(msg.id), reaction.emoji)
            print(rid, guild0.id, msg.id, type(reaction.emoji))
            role = get_role(guild0, rid)
            await user.add_roles(role)
        return
    message: discord.Message = reaction.message
    chan: discord.TextChannel = message.channel
    guild: discord.Guild = chan.guild
    ln=(discord.utils.find(lambda r: r.emoji == "😠", message.reactions)).count
    if ln>=3:
        with sm as s:
            cha_id = s.get_sys_channel(str(guild.id))
            if cha_id is not None:
                cha: discord.TextChannel = get_channel(guild, cha_id)
                await cha.send(f"**Alert __Admins__**, The message ||{message.content}|| by {message.author.mention} was flagged offensive.")
            else:
                await guild.system_channel.send(f"**Alert __Admins__**, The message ||{message.content}|| by {message.author.mention} was flagged offensive.")
        await message.delete()
        embed = discord.Embed(
            title="Alert!",
            description="Offensive Message Deleted",
            color=0xff0000
        )
        embed.add_field(name="Info", value=f"{message.author.mention} a message by you was tagged offensive. Please talk to the admins")
        embed.set_thumbnail(url=message.author.avatar_url)
        await chan.send(embed=embed)
        await user.add_roles(get_role(guild, "warning given"))
        await asyncio.sleep(12*60*60)
        await user.remove_roles(get_role(guild, "warning given"))
    return

@client.event
async def on_message(text: discord.Message):
    roles = [x.name for x in text.author.roles]
    if "myuted" in roles:
        await text.channel.send(f"{text.author.mention} you are barred from speaking since you have the @Muted role ask admins to remove it by saying bplease_unmute")
        if text.content.strip() != "bplease_unmute":
            await text.delete()

client.run(TOKEN)


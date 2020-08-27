import discord
from discord.ext import commands
from discord.utils import get
import os
import time
import datetime
import requests
import bs4
from bs4 import BeautifulSoup
import socket
import re
import sys
from requests import get

TOKEN = 'TOKEN-HRRE'
BOT_PREFIX = 'PREFIX HERE'
bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name} : {bot.user.id}\n-----\nMy current prefix is: {BOT_PREFIX}\n-----")

@bot.command()
async def geo(ctx, *, ipadd):
    r = requests.get(f'http://extreme-ip-lookup.com/json/{ipadd}')
    geo = r.json()
    IP = geo['query']
    ISP = geo['isp']
    Country = geo['country']
    City = geo['city']
    Continent = geo['continent']
    Region = geo['region']
    ORG = geo['org']
    em = discord.Embed(description=f"**IP**: {ipadd}\n \n**City**: ``{City}``\n**Region**: ``{Region}``\n**Country**: ``{Country}``\n**ISP**: ``{ISP}``\n**ORG**: ``{ORG}``", color=0x7bf2ad)
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/744132540998221864/748121107764084856/51zdsrq20LL.png")
    await ctx.send(embed=em)

@geo.error
async def geo_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description=f'❌ Please make sure to include the IP\n```%geo <IP>```', color=discord.Color.dark_red())
        embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)        

@bot.command()
async def scan(ctx, arg1):
    scanyuh = get(f"https://api.hackertarget.com/nmap/?q={arg1}")
    result = scanyuh.text.strip(" ( https://nmap.org/ )")
    em = discord.Embed(title=f"Scan Completed", description=f"**{result}**", color=0x7bf2ad)
    await ctx.send(embed=em)

@scan.error
async def scan_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description=f'❌ Please make sure to include the IP\n```%scan <IP>```', color=discord.Color.dark_red())
        embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)       

@bot.command()
async def ports(ctx):
    em = discord.Embed(description=f"STANDARD PORTS:\n**HOME**: ``80``, ``53``, ``22``, ``8080``\n**XBOX**: ``3074``\n**PS4**: ``9307``", color=0x7bf2ad)
    await ctx.send(embed=em)

@bot.command()
async def ping(ctx, ip):
    response = os.popen(f"ping {ip} -n 1").read()
    if "Received = 1" and "Approximate" in response:
        embed = discord.Embed(description=f"``Pinging {ip}.``", color=0x7bf2ad)
        m = await ctx.send(embed=embed)
        time.sleep(1)
        embed=discord.Embed(title=f"``Pinging {ip}..``", color=0x7bf2ad)
        await m.edit(embed=embed) 
        time.sleep(1) 
        embed=discord.Embed(title=f"``Pinging {ip}...``", color=0x7bf2ad)
        await m.edit(embed=embed)     
        time.sleep(1)   
        embed=discord.Embed(title=f":white_check_mark: Host ``{ip}`` is UP", color=0x0CFF00)
        await m.edit(embed=embed) 
        time.sleep(1)             
    else:
        embed = discord.Embed(description=f"``Pinging {ip}.``", color=0x7bf2ad)
        m = await ctx.send(embed=embed)
        time.sleep(1)
        embed=discord.Embed(title=f"``Pinging {ip}..``", color=0x7bf2ad)
        await m.edit(embed=embed) 
        time.sleep(1) 
        embed=discord.Embed(title=f"``Pinging {ip}...``", color=0x7bf2ad)
        await m.edit(embed=embed)     
        time.sleep(1)   
        embed=discord.Embed(description=f"❌ Host ``{ip}`` is Down", color=0xff0000)
        await m.edit(embed=embed) 
        time.sleep(1) 

@ping.error
async def ping_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(description=f'❌ Please make sure to include the IP\n```%ping <IP>```', color=discord.Color.dark_red())
        embed.set_author(name=f'{ctx.author}', icon_url=f'{ctx.author.avatar_url}')
        await ctx.send(embed=embed)

start_time = datetime.datetime.utcnow() # Timestamp of when it came online
@bot.command(pass_context=True)
async def uptime(ctx: commands.Context):
    now = datetime.datetime.utcnow() # Timestamp of when uptime function is run
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."

    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)

    embed=discord.Embed(title=f"`⌚Client Uptime:` {format(uptime_stamp)}", color=0x7bf2ad)
    await ctx.send(embed=embed)

bot.run(TOKEN)

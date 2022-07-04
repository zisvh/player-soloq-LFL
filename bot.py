import discord
from discord.ext import commands, tasks
import random
from riotwatcher import LolWatcher, ApiError
import dataframe_image as dfi
import pandas as pd
import csv
import time
import sys
from bokeh.io import export_png, export_svgs
from bokeh.models import ColumnDataSource, DataTable, TableColumn
import os

#VARIABLES
api_key = 'RGAPI-67929562-be1b-40b0-b5e6-fdb2370619c2' # here please put in-between the quotes your Riot API Developer Key
watcher = LolWatcher(api_key)
my_region = 'euw1'
region = 'europe'
current_time = int(time.time())
last = (current_time - 86400)
week = (current_time - 604800)
two = (current_time - 172800)




#DISCORD BOT COMMANDS ----------------------------------
bot = commands.Bot(command_prefix = "/", description = "SoloQ Bot")

@bot.event
async def on_ready():
	print("Your soloQ bot is ready for use !")

def save_df_as_image(df, path):
    source = ColumnDataSource(df)
    df_columns = [df.index.name]
    df_columns.extend(df.columns.values)
    columns_for_table=[]
    print(df_columns)
    for column in df_columns:
        if column != None:
            columns_for_table.append(TableColumn(field=column, title=column))

    data_table = DataTable(source=source, columns=columns_for_table,height_policy="auto",width_policy="auto",index_position=None)
    export_png(data_table, filename = path)

@bot.command()
async def fetch(ctx):
       pt = os.getcwd()
       save_df_as_image(df, os.path.join(pt,'plot.png'))
       file=discord.File('plot.png')
       e = discord.Embed()
       e.set_image(url="attachment://plot.png")
       # await ctx.send(file=discord.File('plot.png'))
       await ctx.send(file = file, embed = e)

@bot.command()
async def test(ctx, arg1):
    compte = []
    newfinal = []
    champions = []
    final = []
    player = arg1
    puuid = watcher.summoner.by_name(my_region, player)['puuid']
    mh = list(watcher.match.matchlist_by_puuid(region, puuid, type="ranked", start_time=week, end_time=current_time, count=100))
    for i in mh:
        data = watcher.match.by_id(region, i)
        for j in range(10):
            if data['info']['participants'][j]['puuid'] == puuid:
                champ_name = data['info']['participants'][j]['championName']
                url1 = '**__{}__**'.format(champ_name)
                champions.append(url1)
    for i in champions:
        compte.append(champions.count(i))
    for i in range(len(champions)):
        final.append([champions[i], compte[i]])

    for i in final:
        if i not in newfinal:
            newfinal.append(i)
    df = pd.DataFrame(newfinal, columns=['Champion', 'Games'])
    sorted_df = df.sort_values(by=['Games'], ascending=False)
    sorted_df=sorted_df.set_index('Champion')
    print(sorted_df)
    msg=player + " Has played theses champions the past 2 weeks:\n"
    await ctx.send(sorted_df.to_csv(header=False))

@bot.command()
async def soloQ(ctx):
    await ctx.send("https://tenor.com/view/cops-police-sirens-catching-crminals-what-you-gonna-do-gif-22472645")
    for i in range(5):
        df1 = df.loc[[i]]
        await ctx.send(df1.to_string(header=False, index=False))
        i = i + 1

bot.run(os.environ["DISCORD_TOKEN"]) # here paste in-between double quotes your discord bot token
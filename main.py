from hashlib import new
import discord
from discord.ext import commands
import asyncio
import g2048
import numpy as np
import os, shutil
import copy
import numpy as np
from PIL import Image
# Client (dabot)
# client = discord.Client(command_prefix  = '/',  intents=discord.Intents.all())

global board



async def reset_game():
    global board
    g2048.print_board(board) 

board = g2048.make_empty_board()

client = commands.Bot(command_prefix = 'ska ', intents=discord.Intents.all())

@client.command(name = 'emote')
async def emote(context):
    print('eemote') 

@client.event
async def on_ready():
    print('Ready')

async def run_game(mes, direc):
    # ctx = mes.channel
    game_over = False
    global board
    temp = copy.deepcopy(board)
    
    if direc == 'up':
        up = g2048.up(board)
        board = copy.deepcopy(up)
        if g2048.compare_board(temp, board) == False:
            g2048.add_two(board)
        img = g2048.convert_toimg(board)
        img.save('img.jpg')
        
    if direc == 'down':
        down = g2048.down(board)
        board = copy.deepcopy(down)
        if g2048.compare_board(temp, board) == False:
            g2048.add_two(board)
        img = g2048.convert_toimg(board)
        img.save('img.jpg')
        
    if direc == 'left':
        left = g2048.left(board)
        board = copy.deepcopy(left)
        if g2048.compare_board(temp, board) == False:
            g2048.add_two(board)
        img = g2048.convert_toimg(board)
        img.save('img.jpg')
   
    if direc == 'right':
        right = g2048.right(board)
        board = copy.deepcopy(right)
        if g2048.compare_board(temp, board) == False:
            g2048.add_two(board)
        img = g2048.convert_toimg(board)
        img.save('img.jpg')

    if not game_over:
        newembed = discord.Embed(title='2048', description= '', color=0x077ff7)
        
        direc = ''

        secret_channel = client.get_channel(1013823166373699714)
        file = discord.File('img.jpg')
        temp_message = await secret_channel.send(file = file)
        attachment = temp_message.attachments[0]
        
        newembed.set_image(url = attachment.url)
        
        await mes.edit(embed = newembed)
        await temp_message.delete()
        


@client.command()
async def start(ctx):
    global board
    await reset_game()
    img = g2048.convert_toimg(board)
    img.save('img.jpg')
    file = discord.File('img.jpg')
    
    
    
    embed = discord.Embed(title='2048', description= '', color=0x077ff7)
    embed.set_image(url = "attachment://img.jpg")
    msg = await ctx.send(embed = embed, file = file)
    await msg.add_reaction('▶')



@client.event
async def on_reaction_add(reaction, user):
    direc = ''
    global board
    
    if user != client.user:
        msg = reaction.message
        if str(reaction.emoji) == '▶':
            print('Pressed play')
            await reset_game()
            g2048.add_two(board)
            
            img = g2048.convert_toimg(board)
            img.save('img.jpg')
            file = discord.File('img.jpg')
            
            newembed = discord.Embed(title='2048', description= '', color=0x077ff7)
            secret_channel = client.get_channel(1013823166373699714)
            temp_message = await secret_channel.send(file = file)
            attachment = temp_message.attachments[0]
            
            newembed.set_image(url = attachment.url)

            await msg.remove_reaction("▶", user)
            await msg.remove_reaction("▶", client.user) 
            await msg.edit(embed = newembed)
            await msg.add_reaction("⬅") #Left
            await msg.add_reaction("⬇") #Down
            await msg.add_reaction("➡") #Right
            await msg.add_reaction("⬆") #Rotate
            await msg.add_reaction("❌") #Stop game
            await run_game(msg, direc)
            
  
            
        if str(reaction.emoji) == '⬇':
            print('Pressed down')
            direc = 'down'
            await msg.remove_reaction("⬇", user)
            await run_game(msg, direc)
            
        if str(reaction.emoji) == '⬅':
            print('Pressed left')
            direc = 'left'
            await msg.remove_reaction("⬅", user)
            await run_game(msg, direc)
            
        if str(reaction.emoji) == '➡':
            print('Pressed right')
            direc = 'right'
            await msg.remove_reaction("➡", user)
            await run_game(msg, direc)
            
        if str(reaction.emoji) == '⬆':
            print('Pressed up')
            direc = 'up'
            await msg.remove_reaction("⬆", user)
            await run_game(msg, direc)
        
        if str(reaction.emoji) == "❌": #Stop game button pressed
            #In future maybe put score screen here or a message saying stopping.
            await reset_game()
            await msg.channel.send('Game stopped!')
            await msg.delete()
        

        

        
            
@client.event
async def on_message(mes): 
    channel = mes.channel
    content = mes.content
    if  content == 'hello':
        # await channel.send('skahere')
        await mes.delete()
    await client.process_commands(mes)


    


 
with open('token.txt', 'r') as file:
    token = file.readlines()[0]
       
client.run(token)
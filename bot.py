import discord
import asyncio
import settings
from typing             import Optional
import shutil
import os

client = settings.discord_init("(IP2P) ")

async def console():

    while True:

        channel_id = 0

        channel = discord.utils.get(client.get_all_channels(), name="node")

        if channel:            
            channel_id = channel.id
            channel_id_choice = await asyncio.to_thread(input, f"Adicionar {channel_id} (Node definido) como local da transmissão? [S][N]\n>")
            if channel_id_choice.upper() == "N":
                channel_id = 0
            

        if channel_id == 0:
            channel_id = await asyncio.to_thread(input, "Channel ID:\n> ")
        archive_type = await asyncio.to_thread(input, "Archive Type\n[1] Folder\n[2] File\n>")
        archive = await asyncio.to_thread(input, "File:\n> ")

        if archive_type == "1":
            await send_to_node(channel_id, 0, archive)
        if archive_type == "2":
            if archive in os.listdir():
                await send_to_node(channel_id, archive, 0)

async def send_to_node(channel_id, file = 0, folder = 0):

    if folder != 0 or file != 0:
        if folder != 0:
            shutil.make_archive(folder, "zip", folder)
            archive = folder + ".zip"
        else:
            archive = file

        pv_channel = client.get_channel(int(channel_id))
        pv_file = discord.File(fp=archive)
        await pv_channel.send(file = pv_file)

@client.command()
async def create_node(ctx):
        
        context = "node"
            
        role = discord.utils.get(ctx.guild.roles, name="Node")
        if role is None:

            role = await ctx.guild.create_role(name="Node")                                                
            await ctx.author.add_roles(role)

            created_embed = discord.Embed(
            title= "Node",
            description="Node criado.",
            )  

            showcase_embed = discord.Embed(
                title= "Node criado",
            )  

            pv_channel = await ctx.guild.create_text_channel(name=context)
            default = discord.utils.get(ctx.guild.roles, name="@everyone")

            await pv_channel.set_permissions(default, send_messages = False)  
            await pv_channel.set_permissions(role, send_messages = True)
            await pv_channel.set_permissions(discord.utils.get(ctx.guild.roles, name="IP2P"), send_message = True)

            await asyncio.sleep(1)
            try:
                await ctx.send(embed = created_embed)
                await pv_channel.send(embed = showcase_embed)
            except AttributeError:
                await ctx.send("Embed indisponível.")
        else:
            await ctx.send("Já existe um Node para esse servidor.")

@client.event
async def on_ready():
    
    settings.message("Iniciado", "green", client.user.name, client.user.id)
    asyncio.create_task(console())

client.run(settings.token)

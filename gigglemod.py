#!/usr/bin/env python

import discord

from settings import bot_token

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_guild_channel_update(before, after):
    if before.name != after.name:
        vc_ping_role = discord.utils.get(before.guild.roles, name=f"{before.name} Ping")
        if vc_ping_role:
            await vc_ping_role.edit(name=f"{after.name} Ping")

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel == after.channel:
        return

    if before.channel:
        role = discord.utils.get(member.guild.roles, name=f"{before.channel.name} Ping")
        if role:
            await member.remove_roles(role)

    if after.channel:
        role = discord.utils.get(member.guild.roles, name=f"{after.channel.name} Ping")
        if not role:
            role_name = f"{after.channel.name} Ping"
            role = await member.guild.create_role(name=role_name)
        await member.add_roles(role)

if __name__ == "__main__":
    client.run(bot_token)

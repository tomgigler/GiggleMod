#!/usr/bin/env python

import discord

import gigdb
import gigguild
from settings import bot_token

intents = discord.Intents.none()
intents.guilds = True
intents.messages = True
intents.voice_states = True
client = discord.Client(intents=intents)

@client.event
async def on_guild_channel_update(before, after):
    if before.name != after.name:
        vc_ping_role = discord.utils.get(before.guild.roles, name=f"{before.name} Ping")
        if vc_ping_role:
            await vc_ping_role.edit(name=f"{after.name} Ping")

@client.event
async def on_message(msg):
    if msg.content.startswith('$g '):
        for key in msg.channel.overwrites:
            allow, deny = msg.channel.overwrites[key].pair()
            print('{}:'.format(key))
            if allow.view_channel:
                print('\tAllow view_channel')
            if deny.view_channel:
                print('\tDeny view_channel')
            if allow.manage_channels:
                print('\tAllow manage_channels')
            if deny.manage_channels:
                print('\tDeny manage_channels')
            if allow.manage_permissions:
                print('\tAllow manage_permissions')
            if deny.manage_permissions:
                print('\tDeny manage_permissions')
            if allow.manage_webhooks:
                print('\tAllow manage_webhooks')
            if deny.manage_webhooks:
                print('\tDeny manage_webhooks')
            if allow.create_instant_invite:
                print('\tAllow create_instant_invite')
            if deny.create_instant_invite:
                print('\tDeny create_instant_invite')
            if allow.send_messages:
                print('\tAllow send_messages')
            if deny.send_messages:
                print('\tDeny send_messages')
            if allow.embed_links:
                print('\tAllow embed_links')
            if deny.embed_links:
                print('\tDeny embed_links')
            if allow.attach_files:
                print('\tAllow attach_files')
            if deny.attach_files:
                print('\tDeny attach_files')
            if allow.add_reactions:
                print('\tAllow add_reactions')
            if deny.add_reactions:
                print('\tDeny add_reactions')
            if allow.use_external_emojis:
                print('\tAllow use_external_emojis')
            if deny.use_external_emojis:
                print('\tDeny use_external_emojis')
            if allow.mention_everyone:
                print('\tAllow mention_everyone')
            if deny.mention_everyone:
                print('\tDeny mention_everyone')
            if allow.manage_messages:
                print('\tAllow manage_messages')
            if deny.manage_messages:
                print('\tDeny manage_messages')
            if allow.read_message_history:
                print('\tAllow read_message_history')
            if deny.read_message_history:
                print('\tDeny read_message_history')
            if allow.send_tts_messages:
                print('\tAllow send_tts_messages')
            if deny.send_tts_messages:
                print('\tDeny send_tts_messages')
"""
            # New in Version 2.0
            if allow.send_messages_in_threads:
                print('\tAllow send_messages_in_threads')
            if deny.send_messages_in_threads:
                print('\tDeny send_messages_in_threads')
            if allow.create_public_threads:
                print('\tAllow create_public_threads')
            if deny.create_public_threads:
                print('\tDeny create_public_threads')
            if allow.create_private_threads:
                print('\tAllow create_private_threads')
            if deny.create_private_threads:
                print('\tDeny create_private_threads')
            if allow.use_external_stickers:
                print('\tAllow use_external_stickers')
            if deny.use_external_stickers:
                print('\tDeny use_external_stickers')
            if allow.manage_threads:
                print('\tAllow manage_threads')
            if deny.manage_threads:
                print('\tDeny manage_threads')
            if allow.use_application_commands:
                print('\tAllow use_application_commands')
            if deny.use_application_commands:
                print('\tDeny use_application_commands')
""" 

@client.event
async def on_voice_state_update(member, before, after):
    if before.mute and not after.mute:
        gigdb.delete_mute_member(member.guild.id, member.id)
        if member.guild.id in gigguild.guilds:
            channel = member.guild.get_channel(gigguild.guilds[member.guild.id].mod_log_channel_id)
            if channel:
                await channel.send(embed=discord.Embed(description=f"{member.mention} has been unmuted", color=0x00ff00))

    if after.mute:
        gigdb.add_mute_member(member.guild.id, member.id, member.name)
        if member.guild.id in gigguild.guilds:
            channel = member.guild.get_channel(gigguild.guilds[member.guild.id].mod_log_channel_id)
            if channel:
                await channel.send(embed=discord.Embed(description=f"{member.mention} has been muted", color=0x00ff00))

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
    gigguild.load_guilds()
    client.run(bot_token)

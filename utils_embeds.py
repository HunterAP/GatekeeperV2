'''
   Copyright (C) 2021-2022 Katelynn Cadwallader.

   This file is part of Gatekeeper, the AMP Minecraft Discord Bot.

   Gatekeeper is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3, or (at your option)
   any later version.

   Gatekeeper is distributed in the hope that it will be useful, but WITHOUT
   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
   or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
   License for more details.

   You should have received a copy of the GNU General Public License
   along with Gatekeeper; see the file COPYING.  If not, write to the Free
   Software Foundation, 51 Franklin Street - Fifth Floor, Boston, MA
   02110-1301, USA. 
'''
import logging
import discord
from discord.ext import commands

import DB
import AMP
import utils

class botEmbeds():
    """Gatekeeper Embeds/Banners"""
    def __init__ (self, client:commands.Bot=None):
        self._client = client
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Utils Bot Loaded')

        self.DBHandler = DB.getDBHandler()
        self.DB = self.DBHandler.DB #Main Database object
        self.DBConfig = self.DBHandler.DBConfig
        self.uBot = utils.botUtils(client)

        self.AMPHandler = AMP.getAMPHandler()
        self.AMPInstances = self.AMPHandler.AMP_Instances
        self.AMPServer_Avatar_urls = []

    def default_embedmsg(self, title, context:commands.Context, description=None, field=None, field_value=None) -> discord.Embed:
        """This Embed has only one Field Entry."""
        embed=discord.Embed(title=title, description=description, color=0x808000) #color is RED 
        embed.set_author(name=context.author.display_name, icon_url=context.author.avatar)
        embed.add_field(name=field, value=field_value, inline=False)
        return embed

    async def server_info_embed(self, server:AMP.AMPInstance, context:commands.Context) -> discord.Embed:
        """For Individual Server info embed replies"""
        db_server = self.DB.GetServer(InstanceID = server.InstanceID)
        server_name = db_server.InstanceName
        if db_server.DisplayName != None:
            server_name = db_server.DisplayName

        embed=discord.Embed(title=f'__**{server_name}**__', color=0x00ff00, description=server.Description)

        discord_role = db_server.Discord_Role
        if discord_role != None:
            discord_role = context.guild.get_role(int(db_server.Discord_Role)).name

        avatar = await self.uBot.validate_avatar(db_server)
        if avatar != None:
            embed.set_thumbnail(url= avatar)

        embed.add_field(name=f'Server IP: ', value=str(db_server.IP), inline=False)
        embed.add_field(name='Donator Only:', value= str(bool(db_server.Donator)), inline=True)
        embed.add_field(name='Whitelist Open:' , value= str(bool(db_server.Whitelist)), inline=True)
        embed.add_field(name='Role:', value= str(discord_role), inline=False)
        embed.add_field(name='Hidden', value= bool(db_server.Hidden), inline= True)
        embed.add_field(name='Discord Chat Prefix:', value= str(db_server.Discord_Chat_Prefix), inline=True)
        embed.add_field(name='Filtered Console:', value= str(bool(db_server.Whitelist)), inline=True)

        if db_server.Discord_Console_Channel != None:
            discord_channel = context.guild.get_channel(db_server.Discord_Console_Channel)
            embed.add_field(name='Console Channel:', value= discord_channel.name, inline=False)
        else:
            embed.add_field(name='Console Channel:', value= db_server.Discord_Console_Channel, inline=False)

        if db_server.Discord_Chat_Channel != None:
            discord_channel = context.guild.get_channel(db_server.Discord_Chat_Channel)
            embed.add_field(name='Chat Channel:', value= discord_channel.name, inline=True)
        else:
            embed.add_field(name='Chat Channel:', value= db_server.Discord_Chat_Channel, inline=True)
        
        if db_server.Discord_Event_Channel != None:
            discord_channel = context.guild.get_channel(db_server.Discord_Event_Channel)
            embed.add_field(name='Event Channel:', value= discord_channel.name, inline=True)
        else:
            embed.add_field(name='Event Channel:', value= db_server.Discord_Event_Channel, inline=True)

        if len(db_server.Nicknames) != 0:
            embed.add_field(name='Nicknames:', value=(", ").join(db_server.Nicknames),inline=False)
        return embed

    async def server_display_embed(self, guild:discord.Guild=None) -> list[discord.Embed]:
        """Used for `/server display command`"""
        embed_list = []
        for server in self.AMPInstances:
            server = self.AMPInstances[server]

            db_server = self.DB.GetServer(InstanceID= server.InstanceID)
            if db_server != None and db_server.Hidden != 1:

                status = 'Offline'
                Users = None
                User_list = None
                if server.Running and server._ADScheck() and server.ADS_Running:
                    Users = server.getUsersOnline()
                    if len(server.getUserList()) > 1:
                        User_list = (', ').join(server.getUserList())
                    status = 'Online'

                embed_color = 0x71368a
                if guild != None and db_server.Discord_Role != None:
                    db_server_role = guild.get_role(int(db_server.Discord_Role))
                    if db_server_role != None:
                        embed_color = db_server_role.color

                server_name = server.FriendlyName
                if server.DisplayName != None:
                    server_name = db_server.DisplayName

                nicknames = None
                if len(db_server.Nicknames) != 0:
                    nicknames = (", ").join(db_server.Nicknames)

                embed=discord.Embed(title=f'**=======  {server_name}  =======**',description= db_server.Description, color=embed_color)
                #This is for future custom avatar support.
                avatar = await self.uBot.validate_avatar(db_server)
                if avatar != None:
                    embed.set_thumbnail(url=avatar)

                embed.add_field(name='**IP**:', value= str(db_server.IP), inline=True)
                embed.add_field(name='**Status**:' , value= status, inline= True)
                embed.add_field(name='**Donator Only**:', value= str(bool(db_server.Donator)), inline= True)
                embed.add_field(name='**Whitelist Open**:', value= str(bool(db_server.Whitelist)), inline= True)
                embed.add_field(name='**Nicknames**:' , value= str(nicknames) ,inline=True)
                if Users != None:
                    embed.add_field(name=f'**Players**:', value= f'{Users[0]}/{Users[1]}',inline=True)
                else:
                    embed.add_field(name='**Player Limit**:', value= str(Users), inline= True)
                embed.add_field(name='**Players Online**:', value=str(User_list), inline=False)
                embed_list.append(embed)
        
        return embed_list

    async def server_status_embed(self, context:commands.Context, server:AMP.AMPInstance, TPS=None, Users=None, CPU=None, Memory=None, Uptime=None, Users_Online=None) -> discord.Embed:
        """This is the Server Status Embed Message"""
        db_server = self.DB.GetServer(InstanceID= server.InstanceID)
        
        if server.ADS_Running:
            server_status = 'Online'
        else:
            server_status = 'Offline'

        embed_color = 0x71368a
        if db_server.Discord_Role != None:
            db_server_role = context.guild.get_role(int(db_server.Discord_Role))
            if db_server_role != None:
                embed_color = db_server_role.color

        server_name = server.FriendlyName
        if server.DisplayName != None:
            server_name = db_server.DisplayName

        embed=discord.Embed(title=server_name, description=f'Dedicated Server Status: **{server_status}**', color=embed_color)
        
        avatar = await self.uBot.validate_avatar(db_server)
        if avatar != None:
            embed.set_thumbnail(url=avatar)

        if db_server.IP != None:
            embed.add_field(name=f'Server IP: ', value=db_server.IP, inline=False)

        if len(db_server.Nicknames) != 0:
            embed.add_field(name='Nicknames:' , value=db_server.Nicknames, inline=False)

        #embed.add_field(name='\u1CBC\u1CBC',value='\u1CBC\u1CBC',inline=False)
        embed.add_field(name='Donator Only:', value= str(bool(db_server.Donator)), inline=True)
        embed.add_field(name='Whitelist Open:' , value= str(bool(db_server.Whitelist)), inline=True)
        #embed.add_field(name='\u1CBC\u1CBC',value='\u1CBC\u1CBC',inline=False) #This Generates a BLANK Field entirely.

        if server.ADS_Running:
            embed.add_field(name='TPS', value=TPS, inline=True)
            embed.add_field(name='Player Count', value=f'{Users[0]}/{Users[1]}', inline=True)
            embed.add_field(name='Memory Usage', value=f'{Memory[0]}/{Memory[1]}', inline=False)
            embed.add_field(name='CPU Usage', value=f'{CPU}/100%', inline=True)
            embed.add_field(name='Uptime', value=Uptime, inline=True)
            embed.add_field(name='Players Online', value=Users_Online, inline=False)
        return embed
                
    async def server_whitelist_embed(self, context:commands.Context, server:AMP.AMPInstance) -> discord.Embed:
        """Default Embed Reply for Successful Whitelist requests"""
        db_server = self.DB.GetServer(InstanceID= server.InstanceID)

        embed_color = 0x71368a
        if db_server != None:
            if db_server.Discord_Role != None:
                db_server_role = context.guild.get_role(int(db_server.Discord_Role))
                if db_server_role != None:
                    embed_color = db_server_role.color

            User_list = None
            if len(server.getUserList()) > 1:
                User_list = (', ').join(server.getUserList())

            server_name = server.FriendlyName
            if server.DisplayName != None:
                server_name = db_server.DisplayName

            embed=discord.Embed(title=f'**=======  {server_name}  =======**',description= db_server.Description, color=embed_color)
            avatar = await self.uBot.validate_avatar(db_server)
            if avatar != None:
                embed.set_thumbnail(url=avatar)

            embed.add_field(name='**IP**:', value= str(db_server.IP), inline=True)
            embed.add_field(name='Users Online:' , value=str(User_list), inline=False)
            return embed
            
    def bot_settings_embed(self, context:commands.Context, settings:list) -> discord.Embed:
        """Default Embed Reply for command /bot settings, please pass in a List of Dictionaries eg {'setting_name': 'value'}"""
        embed=discord.Embed(title=f'**Bot Settings**', color=0x71368a)
        embed.set_thumbnail(url= context.guild.icon)
        embed.add_field(name='\u1CBC\u1CBC',value='\u1CBC\u1CBC',inline=False)
        for value in settings:
            key_value = list(value.values())[0]
            key = list(value.keys())[0]
            #print(key, key_value)

            if key == 'Whitelist_emoji_pending' or key == 'Whitelist_emoji_done':
                if key_value != 'None':
                    emoji = context.get_emoji(int(key_value))
                    embed.add_field(name=f'{key.replace("_"," ")}', value=emoji, inline=True)
                else:
                    embed.add_field(name=f'{key.replace("_"," ")}', value='None', inline=True)

            if key == 'Whitelist_wait_time':
                embed.add_field(name='Whitelist Wait Time:', value=f'{key_value} Minutes', inline= False)

            if key.lower() == 'permissions':

                if key_value == 0:
                    key_value = 'Default'
                if key_value == 1:
                    key_value = 'Custom'

                embed.add_field(name='Permissions:', value=f'{key_value}', inline= True)
            
            if key.lower() == 'banner_type':
                if key_value == 0:
                    key_value = 'Discord Embeds'
                if key_value == 1:
                    key_value = 'Custom Banner Images'

                embed.add_field(name='Banner Type:', value=f'{key_value}', inline= True)

            if key.lower() == 'db_version':
                embed.add_field(name='SQL Database Version:', value=f'{key_value}', inline= True)

            if key.lower() == 'bot_version':
                embed.add_field(name='Gatekeeper Version:', value=f'{key_value}', inline= True)

            if key.lower() == 'guild_id':
                if self._client != None:
                    key_value = f'**{self._client.get_guild(int(key_value)).name}**'
                    if key_value == None:
                        key_value = 'None'

                    embed.add_field(name='Guild ID:', value=f'{key_value}', inline= False)

            if key.lower() == 'moderator_role_id':
                role = context.guild.get_role(key_value)
                if role == None:
                    role = 'None'

                embed.add_field(name=f'Moderator Role:', value=f'{key_value}',inline= False)
                
            if key.lower() == 'whitelist_channel':
                channel = context.guild.get_channel(key_value)
                
                if channel != None:
                    channel = f'<#{channel.id}>'
                else:
                    channel = 'None'
                embed.add_field(name='Whitelist Channel', value=f'{channel}',inline=False)

            if key_value == '0' or key_value == '1':
                key_value = bool(key_value)
                embed.add_field(name=f'{list(value.keys())[0].replace("_", " ")}', value=f'{key_value}',inline=False)

        return embed

    def user_info_embed(self, db_user:DB.DBUser, discord_user:discord.User)-> discord.Embed:
        #print(db_user.DiscordID,db_user.DiscordName,db_user.MC_IngameName,db_user.MC_UUID,db_user.SteamID,db_user.Donator)
        embed=discord.Embed(title=f'{discord_user.name}',description=f'Discord ID: {discord_user.id}', color=discord_user.color)
        embed.set_thumbnail(url= discord_user.avatar.url)
        if db_user != None:
            embed.add_field(name='In Database:', value='True')
            if db_user.MC_IngameName != None:
                embed.add_field(name='Minecraft IGN:', value=f'{db_user.MC_IngameName}',inline= False)

            if db_user.MC_UUID != None:
                embed.add_field(name='Minecraft UUID:', value=f'{db_user.MC_UUID}',inline= True)

            if db_user.SteamID != None:
                embed.add_field(name='Steam ID:', value=f'{db_user.SteamID}',inline=False)

            if db_user.Role != None:
                embed.add_field(name='Permission Role:', value=f'{db_user.Role}', inline=False)
                
        return embed
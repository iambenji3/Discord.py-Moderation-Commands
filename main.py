import discord
import asyncio

from discord.ext import commands
from datetime import datetime

bot = commands.Bot(command_prefix='?')

@bot.command()
@commands.has_role("Bot-Mod")
async def kick(ctx, member: discord.Member, *, reason=None):

  if str(ctx.author) != member:
      if reason == None:
          reason = 'No Reason Provided'

      mbed = discord.Embed(
          title=f'You Have Been Kicked From {ctx.guild.name}',
          timestamp=datetime.utcnow(),
          color=discord.Color.red())

      mbed.add_field(name="Reason", value=reason, inline=True)

      await ctx.send(f'Kicked {member} for {reason}')

      #this is because some people has message dm disable
      try:
          await member.send(embed=mbed)
      except:
          pass
      await member.kick(reason=reason)
  else:
      await ctx.send(f"{ctx.author.mention} You Can't Kick YourSelf!")

@bot.command()
@commands.has_role("Bot-Mod")
async def ban(ctx, member: discord.Member, *, reason=None):

  if str(ctx.author) != member:
      if reason == None:
          reason = 'No Reason Provided'

      mbed = discord.Embed(
          title=f'You Have Been Banned From {ctx.guild.name}',
          timestamp=datetime.utcnow(),
          color=discord.Color.red())

      mbed.add_field(name="Reason", value=reason, inline=True)

      await ctx.send(f'Banned {member} for {reason}')

      try:
          await member.send(embed=mbed)
      except:
          pass
        
      await member.ban(reason=reason)
  else:
      await ctx.channel.send(
          f"{ctx.author.mention} You Can't Ban YourSelf!")

@bot.command()
@commands.has_role("Bot-Mod")
async def unban(ctx, member):
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = member.split('#')

  for ban_entry in banned_users:
      user = ban_entry.user

      if (user.name, user.discriminator) == (member_name, member_discriminator):
          await ctx.guild.unban(user)
          await ctx.channel.send(
              f'Unbanned {user.name}#{user.discriminator}')
          return

@bot.command(name="mute")
@commands.has_role("Bot-Mod")
async def mute(ctx, member: discord.Member, *, reason=None):
    if str(ctx.author) != member:
      guild = ctx.guild
      mutedRole = discord.utils.get(guild.roles, name="Muted")

      #this is for creating muted role if already not created
      if not mutedRole:
          mutedRole = await guild.create_role(name="Muted")

          for channel in guild.channels:
              await channel.set_permissions(mutedRole, speak=False, send_messages=False)

      mbed = discord.Embed(title=f'You Have Been Muted In {ctx.guild.name}',
                            timestamp=datetime.utcnow(),
                            color=discord.Color.red())

      mbed.add_field(name="Reason", value=reason, inline=True)

      await member.add_roles(mutedRole, reason=reason)
      await ctx.send(f'Muted {member.mention} for reason {reason}')

      try:
        await member.send(embed=mbed)
      except: 
        pass
    else:
        await ctx.channel.send(f"{member.mention} You Can't Mute Yourself!")

@bot.command()
@commands.has_role("Bot-Mod")
async def unmute(ctx, member: discord.Member):

  mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

  mbed = discord.Embed(title=f'You Have Been Unmuted In {ctx.guild.name}',
                        timestamp=datetime.utcnow(),
                        color=discord.Color.red())

  await member.remove_roles(mutedRole)
  await ctx.send(f'Unmuted {member.mention}')

  try:
    await member.send(embed=mbed)
  except:
    pass

@bot.command()
@commands.has_role("Bot-Mod")
async def temp_mute(ctx, member: discord.Member, seconds: int):

  mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

  await member.add_roles(mutedRole)
  await asyncio.sleep(seconds)
  await member.remove_roles(mutedRole)

@bot.command()
@commands.has_role("Bot-Mod")
async def warn_user(ctx, member: discord.Member, *, reason=None):

  try:
      mbed = discord.Embed(title='You Have Been Warned ',
                            color=discord.Color.red())
      mbed.add_field(name="Reason", value=reason, inline=True)
      await member.send(embed=mbed)
      await ctx.channel.send(member.mention + ' Has Been Warned!')
  except:
      await ctx.channel.send("Couldn't Dm The Given User")

#if you want to remove slowmode then just use this command with slow mode of 0
@bot.command(name="slowmode", aliases=["sm"])
async def slowmode(ctx, sm: int, channel=None):
    if channel is None:
        channel = ctx.channel
    if sm < 0:
        await ctx.send("Slow Mode Should be 0 or Positive")
        return
    else:
        await channel.edit(slowmode_delay=sm)

#this will lock the channel so that no user can send any message
@bot.command()
@commands.has_role("Bot-Mod")
async def lock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f'Locked #{channel}')

@bot.command()
@commands.has_role("Bot-Mod")
async def unlock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f'Unlocked #{channel}')

#this is for deleting message 
@bot.command()
@commands.has_role("Bot-Mod")
async def clear(ctx, number=None):
  await ctx.message.delete()
  if number is None:
    await ctx.send("Provide Some number", delete_after=5)
  else:
    if number == "all":
      count=0
      async for message in ctx.channel.history():
        count=count+1
        await message.delete()
    else:
      count=0
      async for message in ctx.channel.history(limit=int(number)):
        count=count+1
        await message.delete()


bot.run("ODg0MzYxODU5MjYyNzIyMDU5.YTXYKQ.38ov_YqBon2IieFHjUSPy0f2VyM")
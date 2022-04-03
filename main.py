import discord
import requests
import json
import major_scrapper
import reference
import private
import helpers
from discord.ext import commands

client = commands.Bot(command_prefix='.')

url = "https://registrar.princeton.edu/academic-calendar-and-deadlines"


@client.event
async def on_read():
    # 0 gets replaced with client
    print('We have logged in as {0.user}.format(client)')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$department '):
        parse = ''.join(message.content.split(
            "$department ")).split(" ")
        name = helpers.valid_department(parse[0])
        await message.channel.send(name)

    if message.content.startswith('$class '):
        poll = ''.join(message.content.split("$class ")).split(" ")
        name = poll[0] + " " + poll[1]
        department = reference.courses[poll[0]]
        courses = helpers.major_courses(department)
        course = ""
        for i in courses:
            if name in i[0]:
                course += "Department: " + department + "\n" + \
                    "Course Number: " + poll[1] + "\n" + \
                    "Course Name: " + i[1] + "\n" + \
                    i[2] + "\n" + \
                    "Description: " + i[3]
        await message.channel.send(course)

    if message.content.startswith('$major '):
        poll = ''.join(message.content.lower().split("$major "))
        majors = major_scrapper.get_majors(
            "https://www.princeton.edu/academics/areas-of-study")
        classes = ""
        if poll == "all":
            classes += "Areas of Study: \n"
            for i in majors:
                if "Engineering" in i[0]:
                    i[0] = i[0].replace("Engineering", "Eng")
                if "and" in i[0]:
                    i[0] = i[0].replace("and", "&")
                classes += i[0] + "\n"
        else:
            for i in helpers.major_courses(poll):
                classes += i[0] + " " + i[1] + "\n"
        await message.channel.send(classes)


@client.command()
async def embed(ctx):
    embed = discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/",
                          description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    await ctx.send(embed=embed)

# @client.command(pass_context=True)
# async def displayembed(ctx):
#     channel = ctx.message.channel
#     embed = discord.Embed(
#         title="Title",
#         description="This is a description.",
#         color=discord.Color.orange()
#     )

#     embed.set_footer(text="this is a footer")
#     embed.set_image(
#         url="https://irs.princeton.edu/sites/g/files/toruqf276/themes/site/logo.svg")
#     embed.set_thumbnail(
#         url="https://irs.princeton.edu/sites/g/files/toruqf276/themes/site/logo.svg")
#     embed.set_author(name="Michael")
#     embed.add_field(name="field name", value="field value", inline=False)
#     embed.add_field(name="field name", value="field value", inline=True)
#     embed.add_field(name="field name", value="field value", inline=True)

#     await client.say(embed=embed)
#     await client.send_message(channel, embed=embed)


# runs bot
client.run(private.get_token())

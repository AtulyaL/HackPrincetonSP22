import discord
import requests
import json
import random
import major_scrapper
import reference
import private

client = discord.Client()

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = ["Cheer up!",
                          "Hang in there.", "You are a great person / bot!"]
url = "https://registrar.princeton.edu/academic-calendar-and-deadlines"


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)


def major_courses(major):
    major = major.lower()
    major = major.replace(" ", "-")
    url = "https://www.princeton.edu/academics/area-of-study/" + \
        major.lower().replace(" ", "-")
    return major_scrapper.get_major_courses(url)


def valid_department(department):
    try:
        return reference.courses[department.upper()]
    except:
        return "Invalid Department. Please try again"


@client.event
async def on_read():
    # 0 gets replaced with client
    print('We have logged in as {0.user}.format(client)')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if message.content.startswith('$department '):
        parse = ''.join(message.content.split(
            "$department ")).split(" ")
        name = valid_department(parse[0])
        await message.channel.send(name)

    if message.content.startswith('$class '):
        poll = ''.join(message.content.split("$class ")).split(" ")
        await message.channel.send("Subject: " + poll[0] + "; Number: " + poll[1])

    if message.content.startswith('$major'):
        await message.channel.send(major_scrapper.major_course_list[0])
    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))

# runs bot
client.run(private.get_token())

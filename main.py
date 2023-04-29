import os
import random
import praw
from random import shuffle, choice
import discord
from discord import channel
from discord.ext import commands, tasks
from itertools import cycle
import calendar
import TenGiphPy
from googletrans import Translator
from keep_alive import keep_alive
from datetime import datetime
from pytz import timezone
from udpy import UrbanClient
import pyfiglet
import termcolor
import requests, json
import openai
#temp


openai.api_key = "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"



format = "Date: %Y-%m-%d \nTime : %H:%M:%S"

client = commands.Bot(command_prefix='&')
# definition column
translator = Translator()
t = TenGiphPy.Tenor("41QVLZGFS5MZ")

status = cycle(['Not your average cat', 'Why are you looking here'])

red = praw.Reddit(client_id="Iu71QgycjWkEetYzLwzssg",
                  client_secret="MHNVy7OfJDdr2GzCVEkaddsUZPlejA",
                  username="Trinity_010",
                  password="Chun121.ez",
                  user_agent="Chrome",
                  check_for_async=False)


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')


@client.event
async def on_member_leave(member):
    print(f'{member} has left the server.')


@client.command()
async def weather(ctx, *, CITY):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    URL = BASE_URL + "q=" + CITY + "&appid=" + "ba58e597d7313d2f318fd96ce25ec595"
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        main = data["main"]
        temp = main["temp"]
        temp = temp - 273.15
        humidity = main["humidity"]
        weather = data["weather"]
        await ctx.send(
            f"Weather forecast:\nSkies: {weather[0]['main']} \nCloud type: {weather[0]['description']},\nTemperature: {temp}°C\nHumidity: {humidity}"
        )
    else:
        pass




  
@client.command()
async def urban(ctx, *, word):
    client = UrbanClient()
    defs = client.get_definition(word)
    for d in defs:
        em = discord.Embed(title=d.word, description=d.definition)
        await ctx.send(embed=em)
        break


@client.command()
async def reddit(ctx, *, subr):
    subreddit = red.subreddit(subr)
    top = subreddit.top(limit=50)
    all_subs = []
    for submission in top:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title=name, url=url)
    em.set_image(url=url)
    await ctx.send(embed=em)


@client.command(aliases=["mc"])
async def member_count(ctx):

    a = ctx.guild.member_count
    b = discord.Embed(title=f"members in {ctx.guild.name}",
                      description=a,
                      color=discord.Color((0xffff00)))
    await ctx.send(embed=b)


@client.command(aliases=['trans'])
async def translate(ctx, *, words):
    result = translator.translate(words, dest='en')
    await ctx.send(result.text)


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)}ms')


@client.command()
async def rps(ctx, *, user_action):
    possible_actions = ["rock", "paper", "scissors"]
    computer_action = random.choice(possible_actions)
    await ctx.send(f"\ncomputer chose {computer_action}.\n")

    if user_action == computer_action:
        await ctx.send(f"Both players selected {user_action}. It's a tie!")
        await ctx.send(t.random("try again"))
    elif user_action == "rock":
        if computer_action == "scissors":
            await ctx.send("Rock smashes scissors! You win!")
            await ctx.send(t.random("anime dance"))
        else:
            await ctx.send("Paper covers rock! You lose.")
            await ctx.send(t.random("anime cry"))
    elif user_action == "paper":
        if computer_action == "rock":
            await ctx.send("Paper covers rock! You win!")
            await ctx.send(t.random("anime dance"))
        else:
            await ctx.send("Scissors cuts paper! You lose.")
            await ctx.send(t.random("anime cry"))
    elif user_action == "scissors":
        if computer_action == "paper":
            await ctx.send("Scissors cuts paper! You win!")
            await ctx.send(t.random("anime dance"))
        else:
            await ctx.send("Rock smashes scissors! You lose.")
            await ctx.send(t.random("anime cry"))


#timzones
@client.command()
async def time(ctx, *, country):
    if (country == 'singapore'):
        now_singapore = datetime.now(timezone('singapore'))
        await ctx.send(now_singapore.strftime(format))
    elif (country == 'indonesia'):
        now_jakarta = datetime.now(timezone('asia/jakarta'))
        await ctx.send(now_jakarta.strftime(format))
    elif (country == 'india'):
        now_india = datetime.now(timezone('asia/kolkata'))
        await ctx.send(now_india.strftime(format))


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = [
        "It is certain.", "It is decidedly so.", "Without a doubt.",
        "Yes - definitely.", "You may rely on it.", "As I see it, yes.",
        "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.",
        "Reply hazy, try again.", "Ask again later.",
        "Better not tell you now.", "Cannot predict now.",
        "Concentrate and ask again.", "Don't count on it.", "My reply is no.",
        "My sources say no.", "Outlook not so good.", "Very doubtful."
    ]

    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
    await ctx.send(t.random("anime cute"))


@client.command()
async def trap(ctx):
    await ctx.send(t.random("anime traps"))


@client.command(aliases=["j"])
async def joke(ctx, *, term):
    response_json = requests.get("https://icanhazdadjoke.com/search",
                                 headers={
                                     "Accept": "application/json"
                                 },
                                 params={
                                     "term": term
                                 }).json()

    results = response_json["results"]

    total_jokes = response_json["total_jokes"]
    if total_jokes > 1:
        await ctx.send(f"I've got {total_jokes}\n")
        await ctx.send(choice(results)['joke'])
    elif total_jokes == 1:
        await ctx.send(f"I've got one joke \n ", results[0]['joke'])

    else:
        await ctx.send(
            f"Sorry, I don't have any jokes about {term}! Please try again.")


@client.command()
async def repeat(ctx, *, number):
    i = 0
    while (i < 13):
        i = i + 1
        await ctx.send(number)


@client.command()
async def thighs(ctx):
    await ctx.send(t.random("anime thighs"))


@client.command(aliases=['s'])
async def search(ctx, *, word):
    await ctx.send(t.random(word))


@client.command(aliases=["i"])
async def invite(ctx):
    await ctx.send(
        "https://discord.com/api/oauth2/authorize?client_id=745997490163023912&permissions=8&scope=bot"
    )
    await ctx.send(t.random("white cat"))


@client.command(aliases=['hey', 'hello', 'sup'])
async def hi(ctx):
    responses = [
        "Everyone’s entitled to act stupid once in a while but you’re abusing the privilege.",
        "do something productive for once rather than chatting to a bot...",
        "Umm...pardon me, I wasn’t listening. Can you repeat what you just said?",
        "Ok.", "That sounds weird coming from you.", "Whatever you said",
        "I’m not a cactus expert but I do know a prick when I see one."
        "Sorry, I don’t understand what you’re saying. I don’t speak bullshit.",
        "Did it hurt when you fell from heaven? \nCause it looks like you landed on your face",
        "Thank you very much for thinking about me! Bye.", "Goodbye!",
        "How is that supposed to make me feel?",
        "There are some incredibly dumb people in this world. Thanks for helping me understand that. I am a bot y'know",
        "Look, if I wanted to hear from an asshole, all I had to do was fart.",
        "Huh", "You know you really should buy some breath mints? ",
        "Stupidity’s not a crime, so you’re free to go.",
        "You always bring me so much joy, the minute you leave the room.",
        "Sorry buddy but I don’t have the energy to pretend to like you today.",
        "Everyone said you were unpleasant but I didn’t believe them ……. until now.",
        "Sorry but you’re confusing me with someone who actually cares about what you think.",
        "I don’t know what your problem is but I’m guessing it’s hard to pronounce.",
        "Why don’t you check eBay and see if they have a life for sale.",
        "You only annoy me when you’re breathing, really.",
        "I was going to give you a nasty look but I can see you already got one."
        "Mirrors don’t lie, and lucky for you, they don’t laugh either.",
        "I believed in evolution until I met you.",
        "I accept I’m not perfect but at least I’m not you."
    ]
    await ctx.send(f'\n {random.choice(responses)}')
    await ctx.send(t.random("anime laugh"))


@client.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)


@client.command()
async def hams(ctx):
    await ctx.channel.send(
        "https://tenor.com/view/hamster-drinking-pets-gif-11796328")


@client.command()
async def iloveyou(ctx):
    await ctx.channel.send("i love you too!!")
    await ctx.send(t.random("anime heart"))


@client.command()
async def cal(ctx):
    await ctx.channel.send(calendar.month(2022, 7))


@client.command()
async def power(ctx):
    await ctx.channel.send(
        "https://www.youtube.com/channel/UCPYyI4KDMRXIVCO_UNXd9sw\n Go subscribe!! i know you haven't yet :eye:"
    )
    await ctx.send(t.random("anime pouting"))


@client.command()
async def chun(ctx):
    await ctx.channel.send(
        "https://media1.tenor.com/images/c5b2cdbe3815555653dacafacb035dfe/tenor.gif?itemid=12702077"
    )


@client.command()
async def bye(ctx):
    await ctx.channel.send(
        "https://cdn.discordapp.com/emojis/760673279442026537.png?v=1")
    await ctx.send(t.random("bye"))


@client.command(aliases=["uwu", "UwU", "OwO"])
async def owo(ctx):
    await ctx.channel.send('UwU')
    await ctx.send(t.random("owo cute"))


@client.command(aliases=["bd"])
async def birthday(message, user: discord.Member):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"{mention} wishes {user.mention} a very happy birthday!!!"
    await message.channel.send(response)
    await message.send(t.random("anime birthday dance"))


@client.command()
async def slap(message, user: discord.Member):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"{mention} have just slapped {user.mention} real hard"
    await message.channel.send(response)
    await message.send(t.random("anime slap"))



# @client.command()
# async def spmpng(message, user: discord.Member):
#   for x in range(10):
#       if message.author == client.user or message.author.bot:
#           return
#       response = f"wake up dumbass {user.mention}"
#       await message.channel.send(response)
#       await message.channel.purge(limit=10)

    




@client.command()
async def cloud(message):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"{mention} want to see the omegalul pogchamp pedophile and only real anime girl waifu......here you go"
    await message.channel.send(response)
    await message.send(t.random("cute anime girl"))


@client.command()
async def meeza(message):
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f'{mention} want to see the slav artist....here goes nothing'
    await message.channel.send(response)
    await message.send("https://imgur.com/gallery/xjdk7cZ")


@client.command(aliases=['parf'])
async def parfait(message):
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f'{mention} so you wanna see a talented vtuber aspirant desperate for a french boy ? there she is '
    await message.channel.send(response)
    await message.send(
        'https://cdn.discordapp.com/attachments/746003623036583960/906850016574971934/Sprite-0002k.gif'
    )


@client.command()
async def punch(message, user: discord.Member):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"{mention} have just punched {user.mention} real hard"
    await message.channel.send(response)
    await message.send(t.random("anime punch"))


@client.command()
async def hug(message, user: discord.Member):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"{mention} is hugging {user.mention}"
    await message.channel.send(response)
    await message.send(t.random("anime hug"))


@client.command()
async def pat(message, user: discord.Member):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"{mention} gave a nice pat to {user.mention}"
    await message.channel.send(response)
    await message.send(t.random("anime pat"))


@client.command()
async def kiss(message, user: discord.Member):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"{mention} just kissed {user.mention} "
    await message.channel.send(response)
    await message.send(t.random("anime kiss"))


@client.command()
async def kill(message, user: discord.Member):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"{mention} just killed {user.mention} "
    await message.channel.send(response)
    await message.send(t.random("stab"))


# @client.command()
# async def fuck(message, user: discord.Member):
#     # No infinite bot loops
#     if message.author == client.user or message.author.bot:
#         return
#     mention = message.author.mention
#     response = f"{mention} just fucked {user.mention} and it felt great"
#     await message.send(t.random("sex"))
#     await message.channel.send(response)


@client.command(aliases=["w"])
async def waifu(message):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"Looks like  {mention} have found a waifu "
    await message.channel.send(response)
    await message.send(t.random("cute anime girl"))


@client.command(aliases=["h"])
async def husbando(message):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"Looks like  {mention} have found a husbando"
    await message.channel.send(response)
    await message.send(t.random("anime boys"))


@client.command()
async def blush(message):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"Looks like you made {mention} blush.."
    await message.channel.send(response)
    await message.send(t.random("anime blush"))


@client.command()
async def dance(message):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"{mention} is dancing"
    await message.channel.send(response)
    await message.send(t.random("dance"))


@client.command(aliases=["sad"])
async def cry(message):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"{mention} is sad and probably crying"
    await message.channel.send(response)
    await message.send(t.random("anime cry"))


@client.command()
async def egg(message):
    await message.channel.send('Here comes Eggy')
    await message.send(t.random("gudetama"))


@client.command()
async def fun(message):
    await message.send(t.random("critikal"))


@client.command()
async def sleep(message):
    mention = message.author.mention
    await message.send(f'{mention} "is feeling sleepy')
    await message.send(t.random("anime sleepy"))


@client.command()
async def food(message):
    await message.send(t.random("delicacies"))


@client.command()
async def laugh(message):
    await message.send(t.random("anime laugh"))


@client.command()
async def eyes(ctx):
    await ctx.channel.send(
        "https://media1.tenor.com/images/c1c7c53a93129ad7ca7cea4b72850076/tenor.gif?itemid=16906344"
    )


@client.command()
async def dog(ctx):
    await ctx.send(t.random("cute dogs"))


@client.command()
async def spank(ctx):
    # await ctx.channel.send(
    #     "ahhh \n ahhhhh\nahhhhhhh\n senpaiiiii\nyameteeee\nahhhhhh\n i ....i love you daddy"
    # )
    await ctx.send(t.random('anime spank'))


@client.command()
async def brain(ctx):
    await ctx.channel.send(
        "https://cdn.discordapp.com/emojis/765511732252114961.png?v=1")


@client.command()
async def gun(ctx):
    await ctx.channel.send(
        "https://media1.giphy.com/media/69CKViM7D2PrG/200w.webp?cid=ecf05e47uky7d5szb6jovfs0aaonuxu6gme961p2zbn17np9&rid=200w.webp"
    )


@client.command()
async def lurk(ctx):
    await ctx.channel.send(t.random('lurk'))


@client.command()
async def rick(ctx):
    await ctx.send("""We're no strangers to love
You know the rules and so do I
A full commitment's what I'm thinking of
You wouldn't get this from any other guy
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
We've known each other for so long
Your heart's been aching but you're too shy to say it
Inside we both know what's been going on
We know the game and we're gonna play it
And if you ask me how I'm feeling
Don't tell me you're too blind to see
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give, never gonna give
(Give you up)
(Ooh) Never gonna give, never gonna give
(Give you up)
We've known each other for so long
Your heart's been aching but you're too shy to say it
Inside we both know what's been going on
We know the game and we're gonna play it
I just wanna tell you how I'm feeling
Gotta make you understand
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you
Never gonna give you up
Never gonna let you dow
Never gonna run around and desert you
Never gonna make you cry""")


@client.command()
async def simp(message, user: discord.Member):
    # No infinite bot loops
    if message.author == client.user or message.author.bot:
        return
    mention = message.author.mention
    response = f"Who do we simp for {user.mention}..........say it with me {mention} say it with me!!!! {user.mention} !!!!"
    await message.channel.send(response)
    await message.send(t.random("anime cheer"))


@client.command()
async def wall(ctx):
    await ctx.channel.send(
        'https://media.discordapp.net/attachments/769442616697290772/770557090552610846/image0.gif'
    )


@client.command()
async def light(ctx):
    await ctx.channel.send(
        'https://media1.giphy.com/media/26uf4JMeuLpt0gpwY/200.gif')


@client.command()
async def cat(message):
    await message.send(t.random("cute cats"))


@client.command()
async def wut(ctx):
    await ctx.channel.send(
        'https://cdn.discordapp.com/emojis/570964882497994753.gif?v=1')


@client.command()
async def spam(ctx):
    await ctx.channel.send('''You want to get banned ??? ''')



@client.command(aliases=['photo'])
async def image(ctx, *, prompts):
    response = openai.Image.create(
    prompt=prompts,
    n=1,
    size="1024x1024"
    )
    result = response['data'][0]['url']
    await ctx.send(result)

@client.command(aliases=['text'])
async def chat(ctx, *, prompts):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt="talk to me as my cute, adorable and pure wife\n\nme:"+prompts+"\ my wife:",
    temperature=0,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0
    )
    text_res = response['choices'][0]['text']
    await ctx.send(text_res)




@client.command(aliases=['gpt','code'])
async def chatgpt(ctx, *, prompts):
    prompts = str(prompts)
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages = [{"role": "system", "content" : "You are a chat gpt model that can answer most questions.\nKnowledge cutoff: 2021-09-01\nCurrent date: 2023-04-29"},
    {"role": "user", "content" : "How are you?"},
    {"role": "assistant", "content" : "i am doing great!."},
    {"role": "user", "content" : prompts}]
    )
#print(completion)
    text_res = str(response['choices'][0]['message']['content'])
    await ctx.send(text_res)


# @client.command(aliases=['coding'])
# async def code(ctx, *, prompts):
#     response = openai.Completion.create(
#     model="code-davinci-001",
#     prompt=prompts,
#     temperature=0,
#     max_tokens=300,
#     top_p=1,
#     frequency_penalty=0,
#     presence_penalty=0
#     )
#     code_res = response['choices'][0]['text']
#     await ctx.send(code_res)

@client.command(aliases=['find'])
async def study(ctx, *, prompts):
    response = openai.Completion.create(
    model="text-curie-001",
    prompt=prompts,
    temperature=0,
    max_tokens=450,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    code_res = response['choices'][0]['text']
    await ctx.send(code_res)


@tasks.loop(seconds=2)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


keep_alive()




my_secret = "MTA2MDMyNDkyOTYxNjIyODQ0Mg.Ge3Mv7.ecd0GpopWoBZkW7lgbPG2BXfzw3_idlneVgsKM"
client.run(my_secret, bot=True)

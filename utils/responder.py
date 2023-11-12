import discord
import time
import random
from discord.ext import commands, tasks

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"I turned myself into a discord bot M-Morty!! I'm {client.user} Rick!!!")
    check_response_condition.start()


# global variables
# last_message_time is the time of the last message sent in the server
last_message_time = 0
# response_delay is the amount of time in seconds the bot waits before responding
response_delay = 1800
# last_message_content is the content of the last message sent, so you can use it in the check_response_condition function
last_message_content = None
# required_role checks if the user has the required role to trigger the bot
required_role = False

@client.event


async def on_message(message):
    
    global last_message_time
    global required_role
    global last_message_content

    if message.author == client.user:
        return

    # save the message content so i can use it in the check_response_condition function
    last_message_content = message

    # Script only works if you have the required role; change 'TEST' to specified role:
    required_role = discord.utils.get(message.guild.roles, name='TEST')  

    if required_role in message.author.roles:
        required_role = True

    # (possible role name examples: 
    # 'misunderstood genius', 
    # 'too thoughtful for this wolrd',
    # 'big hearted introvert'
    #  etc... up to you tho)

    last_message_time = time.time()



@tasks.loop(seconds=10)
async def check_response_condition():


    global last_message_time
    global last_message_content
    global response_delay
    global required_role


    current_time = time.time()
    time_difference = current_time - last_message_time

    if time_difference >= response_delay and required_role == True:

        response_messages = [
            "Real",
            "That's actually so smart",
            "lmaooooo",
            "huh, never thought of it that way",
            "that's actually so true",
            "oh damn yea",
            "lol thats crazy",
            "hahahahha bro trueee",
            "literally this",
            "Yea",
            "Youp ahahh :joy:",
            "holy FUCK",
            "true as F",
            "fuck",
            "boobs are aweomse.",
            "nice",
            "oh swag, I'll have to check that out sometimes",
            ":heart_on_fire:",
            "wait what do you mean?",
            "hmm what a unique perspective",
            "YIKES! CRINGE!, lmao jk nahh thats actually thoughtful as fuck",
            "100% this",
            "swag",
            "poop CAN taste good",
            "you know what? I know this is meant to be a joke feature but can I be real for a moment? It's actually legit sad as F you write these thoughtful ass messages just to be completely ignored for hours if not forever, and for you to keep on posting them pretending like you don't even fucking care even tho its clear as fuck theres real motherfuckin pain in your words actually makes you real as fuck and i respect your ass for that shit",

            ]

        random_num = random.randrange(0, len(response_messages))

        await last_message_content.channel.send(response_messages[random_num])
            
        last_message_time = current_time
        required_role = False


    #not sure if this should be uncommented or not, gives an error and still works without it so idk
    
    #await client.process_commands(message)





client.run('MTE3MzI4NTI4MDkwMDQ1MjM3Mg.GrewSV.9AhrRi7_UC5LvHS9BeGZlezq8QikxLUPaeD20c')
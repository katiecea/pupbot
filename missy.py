import discord
import os
import random
import aiohttp
from ec2_metadata import ec2_metadata
from dotenv import load_dotenv

# Loading environment variables from token.env file.
load_dotenv('token.env')

# Retrieving Discord bot token from environment variable.
token = str(os.getenv('Token'))
print(token)

# Creating Discord intents for the bot.
intents = discord.Intents.default()
# Enabling message content intent.
intents.message_content = True
# Creating a Discord client with intents.
client = discord.Client(intents=intents)


greet = ["Hello","hey","hi"]

# Class for managing puppy and its happiness.
class Puppy:
    def __init__(self, name):
        self.name = name
        self.happiness = 50

# Method to give a treat to the puppy.
    def give_treat(self):
        self.happiness += 10
        return f"You gave {self.name} a treat! Happiness level increased to {self.happiness}."
# Method to cuddle with the puppy.
    def cuddle(self):
        self.happiness += 20
        return f"You cuddled with {self.name}! Happiness level increased to {self.happiness}."
 # Method to display the happiness level of the puppy.
    def display_happiness(self):
        return f"{self.name}'s happiness level: {self.happiness}"
    
# Asynchronous function to fetch a random puppy image.
async def fetch_random_puppy_image():
    url = "https://dog.ceo/api/breeds/image/random"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("message")
            else:
                return None

# Creating an instance of Puppy class.
puppy = Puppy("YourPuppy")

# Function to print EC2 instance metadata.
def print_ec2_metadata():
    instance_id = ec2_metadata.instance_id
    instance_type = ec2_metadata.instance_type
    availability_zone = ec2_metadata.availability_zone
    print(f"EC2 Instance ID: {instance_id}")
    print(f"Instance Type: {instance_type}")
    print(f"Availability Zone: {availability_zone}")
print_ec2_metadata()

# Event handler for bot's on_ready event.
@client.event
async def on_ready():
    print(f"logged in as{client.user}")
     # Fetch and print EC2 instance metadata


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if any(word in message.content.lower() for word in greet):
        await message.channel.send(f"Hello {message.author.mention}!")

 # Responding to requests for random puppy images.
    if "puppies" in message.content.lower():
        puppy_image = await fetch_random_puppy_image()
        if puppy_image:
            await message.channel.send("Here's a random puppy image for you:")
            await message.channel.send(puppy_image)
        else:
            await message.channel.send("Sorry, I couldn't fetch a puppy image at the moment.")
# Responding to requests for treating the puppy.
    if "treat" in message.content.lower():
        response = puppy.give_treat()
        puppy_image = await fetch_random_puppy_image()
        if puppy_image:
            await message.channel.send(response)
            await message.channel.send("Here's a random happy dog image for you:")
            await message.channel.send(puppy_image)
        else:
            await message.channel.send("Sorry, I couldn't fetch a puppy image at the moment.")
 # Responding to requests for cuddling with the puppy.
    if "cuddle" in message.content.lower():
        response = puppy.cuddle()
        puppy_image = await fetch_random_puppy_image()
        if puppy_image:
            await message.channel.send(response)
            await message.channel.send("Here's a random happy dog image for you:")
            await message.channel.send(puppy_image)
        else:
            await message.channel.send("Sorry, I couldn't fetch a puppy image at the moment.")

# Responding to requests for checking puppy's happiness.
    if "check happiness" in message.content.lower():
        response = puppy.display_happiness()
        await message.channel.send(response)

# Responding to requests for server information.
    if "tell me about my server" in message.content.lower():
        instance_id = ec2_metadata.instance_id
        instance_type = ec2_metadata.instance_type
        availability_zone = ec2_metadata.availability_zone
        metadata_str = f"EC2 Instance ID: {instance_id}, Instance Type: {instance_type}, Availability Zone: {availability_zone}"
        await message.channel.send(metadata_str)

        

    
client.run(token)
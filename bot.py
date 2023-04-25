from dotenv import load_dotenv
import os
load_dotenv()

import discord
import json
from string import ascii_lowercase



intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)



counter = {}

def is_aww(text):
	text = [char for char in text.lower() if char in ascii_lowercase]
	return all([char in ["a", "w"] for char in text]) and (list(text) == sorted(text)) and ("a" in text) and ("w" in text)

async def aww(message):
	counter[str(message.author.id)] = (count := counter.get(str(message.author.id), 0) + 1)
	try:
		with open("counts.json", "w") as count_file:
			json.dump(counter, count_file)
	except e:
		print(f"ERROR: {e}\n\n\n\n{counter}")

	await message.channel.send(f"<@{message.author.id}> said aww {count} time{'s' if count > 1 else ''}")

def total_awws():
	return sum(counter.values())

async def update_status():
	await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=3, name=f"{total_awws()} awws total"))


@bot.event
async def on_message(message: discord.Message):
	if message.author == bot.user:
		return

	if is_aww(message.content):
		await aww(message)
		await update_status()

	elif f"<@{bot.user.id}>" in message.content:
		c = counter.get(str(message.author.id), 0)
		await message.channel.send(f"<@{message.author.id}> said aww {c} time{'s' if c != 1 else ''}\nTotal awws: {total_awws()}")
		
@bot.event
async def on_ready():
	print(f"Logged in as {bot.user}")
	await update_status()



with open("counts.json", "r") as count_file:
	try:
		counter = json.load(count_file)
	except:
		print("error opening counts.json")
	print(counter)
try:
	TOKEN = os.getenv("BOT_TOKEN")
	if TOKEN:
		bot.run(TOKEN)
finally:
	print(counter)
	with open("counts.json", "w") as count_file:
		json.dump(counter, count_file)

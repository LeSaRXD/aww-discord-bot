from dotenv import load_dotenv
import os
load_dotenv()

import discord
import json
from string import ascii_lowercase



intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)



def is_aww(text):
	text = [char for char in text.lower() if char in ascii_lowercase]
	return all([char in ["a", "w"] for char in text]) and (list(text) == sorted(text)) and ("a" in text) and ("w" in text)

@bot.event
async def on_ready():
	print(f"Logged in as {bot.user}")



with open("counts.json", "r") as count_file:
	try:
		counter = json.load(count_file)
	except:
		counter = {}
	print(counter)

with open("counts.json", "w") as count_file:
	@bot.event
	async def on_message(message: discord.Message):
		if message.author == bot.user:
			return

		if not is_aww(message.content):
			return
		
		counter[str(message.author.id)] = (count := counter.get(str(message.author.id), 0) + 1)

		await message.channel.send(f"<@{message.author.id}> said aww {count} time{'s' if count > 1 else ''}")

	try:
		TOKEN = os.getenv("BOT_TOKEN")
		if TOKEN:
			bot.run(TOKEN)
	finally:
		print(counter)
		json.dump(counter, count_file)

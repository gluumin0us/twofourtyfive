import os

import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv

import random

import data
import timeline

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://luxxin40:3n5wPzXnX4HwEJxT@cluster0.hb65i.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

my_db = client["0245_data"]
print(my_db.list_collection_names())

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("it."), intents=intents)
channels = {}
cats = {}


async def setup_hook() -> None:  # This function is automatically called before the bot starts
    await bot.tree.sync()

bot.setup_hook = setup_hook

@bot.event
async def on_ready() -> None:  # This event is called when the bot is ready
    print(f"Logged in as {bot.user}")

@bot.tree.command()
async def sync(inter: discord.Interaction) -> None:
    if inter.user.id == 262320046653702145:
        await bot.tree.sync(guild=inter.guild)
        await inter.response.send_message(content="Command Tree synced!", ephemeral=True)
    else:
        await inter.response.send_message("You do not have permission to use this command!")

@bot.tree.command()
async def ping(inter: discord.Interaction) -> None:
    await inter.response.send_message(f"> Pong! {round(bot.latency * 1000)}ms")

@bot.tree.command()
async def hello(inter: discord.Interaction) -> None:
    await inter.response.send_message("Hello!")

@bot.tree.command()
async def setup(inter: discord.Interaction) -> None:
    db = client["0245_data"]
    if str(inter.guild.id) in db.list_collection_names():
        await inter.response.send_message("Server already set up!")
        return
    db.create_collection(str(inter.guild.id))

    pass

@bot.tree.command()
async def reset(inter: discord.Interaction) -> None:
    await inter.response.send_message("Resetting gameplay channels...")
    guild_db = client["0245_data"][str(inter.guild.id)]
    db_filter = [{"channel_type": "base_exhibit"},
                 {"channel_type": "variable_exhibit"},
                 {"channel_type": "traveler"}]
    exhibit_cursor = guild_db.find({"$or": db_filter})
    for ex in exhibit_cursor:
        channel_id = ex["id"]
        channel = inter.guild.get_channel(channel_id)
        new_channel = await channel.clone()
        await channel.delete()
        guild_db.update_one({"id": channel_id},
                            {'$set': {"id": new_channel.id}})
        if ex["channel_type"] == "variable_exhibit":
            guild_db.update_one({"id": new_channel.id},
                                {'$set': {"type": None,
                                          "items": [],
                                          "traps": [],
                                          "conditions": []}})
        if ex["channel_type"] == "base_exhibit":
            guild_db.update_one({"id": new_channel.id},
                                {'$set': {"items": [],
                                          "traps": [],
                                          "conditions": []}})
        if ex["channel_type"] == "traveler":
            guild_db.update_one({"id": new_channel.id},
                                {'$set': {"hp": 10,
                                          "supplies": [0, 0, 0, 0],
                                          "items": [],
                                          "location": None,
                                          "vision": [],
                                          "timeline": [],
                                          "player_id": None,
                                          "tr_type": None}})

@bot.tree.command()
async def db(inter: discord.Interaction):
    """
    Prints out the information in the database.

    Parameters
    ----------
    :param inter: discord.Interaction
        the interaction object
    :return:
    """
    guild_db = client["0245_data"][str(inter.guild.id)]
    await inter.response.send_message(list(guild_db.find({})))

# Exhibit Commands
exhibit = app_commands.Group(name="exhibit", description="channel exhibit management")

@exhibit.command()
async def info(inter: discord.Interaction):
    """
    Prints out info about the current channel's exhibit.

    Parameters
    ----------
    :param inter: discord.Interaction
        the interaction object
    """
    guild_db = client["0245_data"][str(inter.guild.id)]
    ex = guild_db.find_one({"id": inter.channel_id})
    if (not ex) or ("exhibit" not in ex["channel_type"]):
        await inter.response.send_message("This channel is not an exhibit!")
        return
    printable = ""
    printable += f"Current Exhibit: {ex['type']}\n"
    printable += f"Available Items: {ex['items']}\n"
    await inter.response.send_message(printable)

@exhibit.command()
async def set(inter: discord.Interaction, ex_type: data.ExhibitNames):
    """
    Sets the current channel to an exhibit type.
    Parameters
    ----------
    :param inter: discord.Interaction
        the interaction object
    :param ex_type: data.ExhibitNames
        the type of exhibit you want to set the channel to
    """
    guild_db = client["0245_data"][str(inter.guild.id)]
    ex = guild_db.find_one({"id": inter.channel_id})
    if (not ex) or (ex["channel_type"] != "variable_exhibit"):
        await inter.response.send_message("You cannot set this channel to an exhibit!")
        return
    await inter.response.send_message(f"Setting current channel to exhibit {ex_type}!")
    guild_db.update_one({"id": inter.channel_id},
                        {"$set": {"type": ex_type,
                                  "items": data.exhibit_items[ex_type],
                                  "traps": [],
                                  "conditions": []}})

bot.tree.add_command(exhibit)


tr = app_commands.Group(name="tr", description="character management")

@tr.command()
async def info(inter: discord.Interaction):
    guild_db = client["0245_data"][str(inter.guild_id)]
    ex = guild_db.find_one({"id": inter.channel_id})
    if (not ex) or (ex["channel_type"] != "traveler"):
        await inter.response.send_message("This is not a traveler channel!")
        return
    if not ex["player_id"]:
        await inter.response.send_message("This traveler has not been claimed yet!")
        return
    sup = ex["supplies"]
    printable = ""
    user = await bot.fetch_user(ex["player_id"])
    traveler = ex["tr_type"] if ex["tr_type"] else "Deciding..."
    location = ex["location"] if ex["location"] else "02:44"
    printable += f"Player: {user.display_name}\n"
    printable += f"Traveler: {traveler}\n"
    printable += f"HP: {ex['hp']}\t WPN: {sup[0]}\t MAT: {sup[1]}\t RES: {sup[2]}\t VOID: {sup[3]}\n"
    printable += f"Items: {ex['items']}\n"
    printable += f"Location: {location}\n"
    await inter.response.send_message(printable)

@tr.command()
async def claim(inter: discord.Interaction):
    guild_db = client["0245_data"][str(inter.guild_id)]
    ex = guild_db.find_one({"id": inter.channel_id})
    if (not ex) or (ex["channel_type"] != "traveler"):
        await inter.response.send_message("This is not a traveler channel!")
        return
    if ex["player_id"]:
        user = await bot.fetch_user(ex["player_id"])
        await inter.response.send_message(f"This traveler has already been claimed by {user.display_name}!")
        return
    await inter.response.send_message("Channel claimed!")
    guild_db.update_one({"id": inter.channel_id}, {"$set": {"player_id": inter.user.id}})
    return

@tr.command()
async def set(inter: discord.Interaction):
    view = TravelerChoice()
    await inter.response.send_message(view=view)

bot.tree.add_command(tr)

class TravelerChoice(View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(placeholder="Choose a Traveler...",  min_values=1, max_values=1, options=data.tr_options)
    async def select_callback(self, inter: discord.Interaction, select):
        game_db = client["0245_data"][str(inter.guild_id)]
        traveler = game_db.find_one({"player_id": inter.user.id})
        if not traveler:
            await inter.response.send_message("You're not in this game!", ephemeral=True)
            return
        game_db.update_one({"player_id": inter.user.id},
                           {"$set": {"tr_type": select.values[0]}})
        await inter.response.send_message(f"Traveler Selected: [{select.values[0]}]")
        self._disable_all()
        await self._edit(view=self)
        self.stop()
        return

class StartView(View):

    def __init__(self):
        super().__init__(timeout=None)
        self.player_number = 0

    @discord.ui.button(label="Join Game", style=discord.ButtonStyle.green, custom_id="join_btn")
    async def join_button_callback(self, inter: discord.Interaction, button):
        test_db = client["0245_data"]["test"]
        if test_db.find_one({"id": inter.user.id}):
            await inter.response.send_message("You've already joined the game, sit tight!", ephemeral=True)
            return
        if self.player_number == 4:
            await inter.response.send_message("Sorry, game's full!", ephemeral=True)
        test_db.insert_one({"name": inter.user.display_name, "id": inter.user.id})
        self.player_number += 1
        current_players = test_db.find()
        printable = "Current Players:\n"
        for player in current_players:
            printable += f"{player['name']}\n"

        embed = discord.Embed(title="Game Starting Soon...",
                              description="")
        embed.add_field(name="Current Players:",
                        value=printable)
        await inter.response.edit_message(embed=embed)
        return

    @discord.ui.button(label="Leave Game", style=discord.ButtonStyle.red, custom_id="leave_btn")
    async def leave_button_callback(self, inter: discord.Interaction, button):
        test_db = client["0245_data"]["test"]
        if not test_db.find_one({"id": inter.user.id}):
            await inter.response.send_message("You're not currently in the game!", ephemeral=True)
            return
        test_db.delete_one({"id": inter.user.id})
        self.player_number -= 1
        current_players = test_db.find()
        printable = "Current Players:\n"
        for player in current_players:
            printable += f"{player['name']}\n"
        embed = discord.Embed(title="Game Starting Soon...",
                              description=printable)
        await inter.response.edit_message(embed=embed)
        return

    @discord.ui.button(style=discord.ButtonStyle.blurple, custom_id="start_btn", emoji="▶️")
    async def start_button_callback(self, inter: discord.Interaction, button):
        test_db = client["0245_data"]["test"]
        game_db = client["0245_data"][str(inter.guild_id)]
        if self.player_number < 3:
            await inter.response.send_message("Too few players!", ephemeral=True)
            return
        if self.player_number > 4:
            await inter.response.send_message("Too many players!", ephemeral=True)
            return
        self._disable_all()
        await self._edit(view=self)
        all_players = test_db.find()
        traveler_channels = game_db.find({"channel_type": "traveler"})
        museum = timeline.generate_museum()
        starting_location = random.shuffle(["ex1", "ex2", "ex3", "ex4"])
        for i in range(self.player_number):
            traveler = traveler_channels[i]
            my_timeline = timeline.generate_timeline()
            game_db.update_one({"name": traveler["name"]},
                               {"$set": {"player_id": all_players[i]["id"],
                                         "timeline": my_timeline,
                                         "location": starting_location[i],
                                         "vision": starting_location[i]}})
            player_role = inter.guild.get_role(traveler["role_id"])
            player = inter.guild.get_member(traveler["player_id"])
            await player.add_roles(player_role)
            channel = inter.guild.get_channel(traveler["id"])
            await channel.send(content=f"Welcome to the museum, {player.mention}! Now pick a traveler!",
                               view=TravelerChoice)
        self.stop()
        return

@bot.tree.command()
async def start(inter: discord.Interaction):
    view = StartView()
    embed = discord.Embed(title="Game Starting Soon...",
                          description="Current Players:")
    await inter.response.send_message(embed=embed, view=view)


@bot.tree.command()
async def search(inter: discord.Interaction):
    game_db = client["0245_data"][str(inter.guild_id)]
    ex = game_db.find_one({"id": inter.channel_id})
    traveler = game_db.find_one({"player_id": inter.user.id})
    if (not ex) or ((ex["channel_type"] != "base_exhibit") and (ex["channel_type"] != "variable_exhibit")):
        await inter.response.send_message("You cannot search here!")
        return
    if not traveler:
        await inter.response.send_message("You're not in a game!")
        return
    luck = traveler["stats"][3]
    dice_result = random.randint(1, 6) + luck
    gets_item = False
    if dice_result >= 6:
        dice_result = 6
        gets_item = True
    supply = data.exhibit_supplies[ex["type"]]
    loot = traveler["supplies"]
    new_loot = [0, 0, 0, 0]
    for i in range(dice_result):
        search_attempt = random.randint(1, 10)
        for j in range(len(supply)):
            search_attempt -= supply[j]
            if search_attempt <= 0:
                loot[j] += 1
                new_loot[j] += 1
                break
    game_db.update_one({"player_id": inter.user.id},
                       {"$set": {"supplies": loot}})

    printable = "You've found:\n"
    if new_loot == [0, 0, 0, 0] and not gets_item:
        printable += "Nothing!"
    printable += f"+{new_loot[0]} Weapons\n" if new_loot[0] > 0 else ""
    printable += f"+{new_loot[1]} Materials\n" if new_loot[1] > 0 else ""
    printable += f"+{new_loot[2]} Restoratives\n" if new_loot[2] > 0 else ""
    printable += f"+{new_loot[3]} Void Shards\n" if new_loot[3] > 0 else ""

    if gets_item:
        exhibit_items = ex["items"]
        for i in range(2 if ex["type"] == "gems" else 1):
            if exhibit_items:
                item = random.choice(exhibit_items)
                exhibit_items.remove(item)
                items = []
                for j in traveler["items"]:
                    items.append(j)
                items.append(item)
                print(traveler["items"])
                game_db.update_one({"player_id": inter.user.id},
                                   {"$set": {"items": items}})
                game_db.update_one({"id": inter.channel_id},
                                   {"$set": {"items": exhibit_items}})
                printable += f"{item}\n"

    await inter.response.send_message(printable)


bot.run(TOKEN)

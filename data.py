import enum
import discord

lobby_id = 1291934579061428236
ex1_id = 1291974600930103376
ex2_id = 1291934512502018098
security_id = 1291934475646799957
ex3_id = 1291950148020338762
ex4_id = 1291934392096133134
artifact_id = 1291933953199968277

channel_ids = {
    "ts1": 1291936871516995635,
    "ts2": 1291936833013420043,
    "ts3": 1291936803309486185,
    "ts4": 1288273236601208953,
    "lobby": 1291934579061428236,
    "security": 1291934475646799957,
    "artifact": 1291933953199968277,
    "ex1": 1291974600930103376,
    "ex2": 1291934512502018098,
    "ex3": 1291950148020338762,
    "ex4": 1291934392096133134,
}

class ExhibitNames(str, enum.Enum):
    Dino = "dino"
    Cosmos = "cosmos"
    Inventions = "inventions"
    Conflict = "conflict"
    Gems = "gems"
    Canvas = "canvas"
    Silk = "silk"
    Floral = "floral"
    Faith = "faith"
    Void = "void"


exhibit_supplies = {
    "lobby": [1, 3, 0, 0],
    "security": [3, 0, 1, 0],
    "artifact": [0, 1, 3, 0],
    "dino": [3, 4, 1, 0],
    "cosmos": [2, 2, 4, 0],
    "inventions": [3, 5, 0, 0],
    "conflict": [5, 1, 2, 0],
    "gems": [1, 3, 0, 0],
    "canvas": [0, 0, 0, 0],
    "silk": [2, 2, 2, 0],
    "floral": [0, 4, 4, 0],
    "faith": [2, 1, 5, 0],
    "void": [1, 1, 1, 7]
}

exhibit_items = {
    "lobby": [],
    "security": [],
    "artifact": [],
    "dino": ["Brutal Club", "Fur Cloak", "Strange Skull"],
    "cosmos": ["Exo Suit", "Ansible Unit", "Telescope"],
    "inventions": ["Tesla Coil", "Prototype X", "Universal Tool"],
    "conflict": ["Snowfox Mk. III", "Betsy 680", "H91", "C&S Model 10", "Gas Grenade", "Body Armor"],
    "gems": ["Citrine", "Black Tourmaline", "Opal", "Moonstone", "Sunstone",
             "Ruby", "Sapphire", "Topaz", "Jade", "Quartz"],
    "canvas": ["Paintbrush", "Palette Knife", "Protractor"],
    "silk": ["The Golden Lotus", "The Fire-Wreathe Silk", "The Porcelain Blade",
             "The Linglong Pandola", "Scroll of the Seven Realms", "Ravenbloom Tea"],
    "floral": ["Compost Box", "Flower Crown", "Sundown Scanner"],
    "faith": ["Karmic Wheel", "Braided Bracelet", "Spiritbane Charm"],
    "void": []
}

class TravelerNames(enum.Enum):
    Baltimore = "baltimore"
    Friedrich = "friedrich"
    Telekles = "telekles"
    Annie = "annie"
    Mira = "mira"
    VIVIAN = "vivian"
    Johnathan = "johnathan"
    Lost = "lost"
    Samirah = "samirah"
    Inoran = "inoran"
    Ahkbad = "ahkbad"
    Sinker = "sinker"
    Psyche = "psyche"
    Lance = "lance"
    Rainbird = "rainbird"
    Kraken = "kraken"


tr_options = [
    discord.SelectOption(
        label="Baltimore Black",
        description="The Mafioso",
        # value="baltimore"
    ),
    discord.SelectOption(
        label="Friedrich Hohmann",
        description="The Inventor",
        # value="friedrich"
    ),
    discord.SelectOption(
        label="Telekles",
        description="The Herald",
        # value="telekles"
    ),
    discord.SelectOption(
        label="Annie Wei",
        description="The Scav",
        # value="annie"
    ),
    discord.SelectOption(
        label="Mira Carino & The Other Mira Carino",
        description="The Duo",
        # value="mira"
    ),
    discord.SelectOption(
        label="VIVIAN",
        description="The AI",
        # value="vivian"
    ),
    discord.SelectOption(
        label="Johnathan Mills",
        description="The Reporter",
        # value="johnathan"
    ),
    discord.SelectOption(
        label="???",
        description='"The Lost"',
        # value="lost"
    ),
    discord.SelectOption(
        label="Samirah Karim",
        description="The Security Guard",
        # value="samirah"
    ),
    discord.SelectOption(
        label="Inoran Xymoira",
        description="The Swordmage",
        # value="xymoira"
    ),
    discord.SelectOption(
        label="Ahkbad Telján",
        description="The Collector",
        # value="ahkbad"
    ),
    discord.SelectOption(
        label="Sinker",
        description="The Contraptionist",
        # value="sinker"
    ),
    discord.SelectOption(
        label="Psyche",
        description="The Voidmade",
        # value="psyche"
    ),
    discord.SelectOption(
        label="Lance Peters",
        description="The 2985516th",
        # value="lance"
    ),
    discord.SelectOption(
        label="Rainbird",
        description="The Warden",
        # value="rainbird"
    ),
    discord.SelectOption(
        label="Agent Kraken",
        description="The Mixologist",
        # value="kraken"
    )
]

# total_weapons = 0
# total_materials = 0
# total_restoratives = 0
# for ex in exhibit_supplies:
#     supply = exhibit_supplies[ex]
#     total_weapons += supply[0]
#     total_materials += supply[1]
#     total_restoratives += supply[2]
# print(total_weapons, total_materials, total_restoratives)

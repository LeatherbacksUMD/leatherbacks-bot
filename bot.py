import discord
import os

intents = discord.Intents.default()
intents.members = True

TOKEN = os.getenv('TOKEN')
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'{client.user} has connected')
    global guild, rules_channel, warlock, kerfuffle, open_combat, antweights
    global leatherback
    guild = client.get_guild(928046831013879889)
    rules_channel = client.get_channel(931948457512538152)
    warlock = client.get_emoji(932764756903874562)
    kerfuffle = client.get_emoji(932752842916233257)
    open_combat = guild.get_role(932767230318477343)
    antweights = guild.get_role(932766907986214922)
    leatherback = guild.get_role(933951506112188446)

    global rule
    # use this when rule message already exists
    rule = await rules_channel.fetch_message(933045310186459157)

    # use this sequence if rule message needs to be recreated
    # embed = discord.Embed(color=0xe03a3e)
    # embed.add_field(name='Rules', value='1. Treat everyone with respect. '
    #                 'Absolutely no harassment, witch hunting, sexism, racism, '
    #                 'or hate speech will be tolerated.\n2. No NSFW or obscene '
    #                 'content. This includes text, images, or links featuring '
    #                 'nudity, sex, hard violence, or other graphically '
    #                 'disturbing content.\n3. If you see something against the '
    #                 'rules or something that makes you feel unsafe, let the '
    #                 'officers know. We want this server to be a welcoming '
    #                 'space!', inline=False)
    # embed.add_field(name='Recommendations', value='1. It would be helpful to '
    #                 'everyone if you could make your nickname for this server '
    #                 'your real name (or what you want to go by)!\n2. You\'re '
    #                 'welcome to participate in whatever category of bot you '
    #                 f'see fit! To indicate this, please react with {warlock} '
    #                 'if you want to get into open combat (larger bots) and '
    #                 f'with {kerfuffle} if you want to get into antweights '
    #                 '(1lb). If you don\'t want to receive notifications from '
    #                 'the part(s) of the club you\'re not involved in, please '
    #                 'change your notification settings for that channel ONLY '
    #                 'and not the entire server.', inline=False)
    # rule = await rules_channel.send(embed=embed)
    # await rule.add_reaction(kerfuffle)
    # await rule.add_reaction(warlock)


@client.event
async def on_raw_reaction_add(payload):
    if payload.member != client.user and payload.message_id == rule.id:
        if payload.emoji == warlock:
            await payload.member.add_roles(open_combat)
        elif payload.emoji == kerfuffle:
            await payload.member.add_roles(antweights)


@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == rule.id:
        user = guild.get_member(payload.user_id)
        if payload.emoji == warlock:
            await user.remove_roles(open_combat)
        elif payload.emoji == kerfuffle:
            await user.remove_roles(antweights)


@client.event
async def on_member_join(member):
    member.add_roles(leatherback)

client.run(TOKEN)

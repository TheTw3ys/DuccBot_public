import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord import Member
import asyncio
import random
import requests
import json
bot = commands.Bot(command_prefix=',', case_intensitive=True,intents=discord.Intents.all())
reactrole = r"reactrole.json"
###########################################################################
def mess_not_pinned(mess):
    return not mess.pinned #falls die Nachricht gepinnt ist stoppt der Bot
def to_upper(argument):
    return argument.upper() #siehe @bot.command upper
def mau5ify(args1):
    translation = ""
    for letter in args1:
        if letter in "Ss":
            translation = translation + "5"
        elif letter in 'Aa':
          translation = translation + '4'
        else:
          translation = translation + letter
    return translation #siehe @bot.command mau5ify
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@bot.event
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        print("keine Ahnung ein Bot nervt hier ein bisschen")

    else:
        with open(reactrole) as react_file:
            data = json.load(react_file)
            for x in data:
                if x['message_id'] == payload.message_id: #checks if the found member id is equal to the id from the message where a reaction was added
                    if x['emoji'] == payload.emoji.name: #checks if the found emoji is equal to the reacted emoji

                        role = discord.utils.get(bot.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                        await payload.member.add_roles(role) #gives the member who reacted the role


@bot.event
async def on_raw_reaction_remove(payload):

    with open(reactrole) as react_file:
        data = json.load(react_file)
        for x in data:
            if x['message_id'] == payload.message_id:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(bot.get_guild(
                        payload.guild_id).roles, id=x['role_id'])


                    await bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

@bot.event
async def on_message(ctx):
    lowercase = ctx.content.lower() #ACHTUNG Bsp: 'Egal' funktioniert nicht. (lower())
    if ctx.author.bot:
      return

@bot.event
async def on_command_error(ctx, error):  #Bei bekannten Error
    if isinstance(error, commands.MissingRequiredArgument):
       await ctx.send('Eyyy du hast da was vergessen, kein Plan #was aber irgendwas...')
    if isinstance(error, commands.MissingPermissions):
      await ctx.send("Du darfst das garnicht. Du könntest nach den Rechten fragen...\r\naber ich denke nicht dass du die kriegst ^^")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def reactrole(ctx, emoji, role: discord.Role, *, message): #siehe raw reaction add and remove
    emb = discord.Embed(description=message)
    msg = await ctx.channel.send(embed=emb)
    await msg.add_reaction(emoji)

    with open(reactrole) as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name': role.name,
        'role_id': role.id,
        'emoji': emoji,
        'message_id': msg.id}

        data.append(new_react_role)

    with open(reactrole, 'w') as f:
        json.dump(data, f, indent=4)
#######################################################################

@bot.command(name='aquote')
async def _aquote(ctx):
    quote = [
        ('`Don´t break anyone´s heart, they only have one.\r\nBreak their bones, they have 206.`\r\n~ Ichigo Kurosaki'),
        ('`Lero, Lero, Lero, Lero, Lero, Lero, Lero, Lero, Lero, Lero.`\r\n~ Noriaki Kakyoin'),
        ('`Having overwhelming strength is pretty boring`\r\n~ Saitama'),
        ('`You\'re just afraid of being alone, aren\'t you?`\r\n~ Touka Kirishima'),
        ('`This world is unfair. Justice and evil are decided by others. That’s how the world is.`\r\n~ Garou'),
        ('`Even the most powerful weapon would be meaningless if the wearer was weak.`\r\n~ Genos'),
        ('`Even if no one in the world believes you, stick out your chest and scream in defiance.`\r\n~Rukia Kuchiki'),
        ('`People with talent often have the wrong impression that things will go as they think.`~ Karma Akabane'),
        ('`I didn\`nt came here to fight you. I came here to violently KILL YOU!`\r\n~ Tōshirō Hitsugaya'),
        ('`I\'ll take a potato chip... AND EAT IT!`\r\n~ Yagami Light'),
        ('`An angel? So This is an angel? But he’s got no wings, and his butts not hanging out.`\r\n~ Goku'),
        ('`Do you have any idea how stupid we are? Don’t underestimate us.`\r\n~ Kondou Isao'),
        ('`An apple a day keeps anyone away, if you throw it hard enough!`\r\n~ Marie Mjolnir'),
        ('`If you die, I’ll kill you!`\r\n~ Rorona Zoro'),
        ('`The ocean is so salty because everyone pees in it.`~ Goku'),
        ('`Hey, you spiky, aloe vera bastard! Where the hell\'s Sasuke?`\r\n~ Naruto'),
        ('`There are three things I cannot tolerate: cowardice, bad haircuts, and military insurrection, and it is very unfortunate that our friend Vegeta possesses all three of these.`\r\n~Frieza'),
        ('`People die when they are killed.`\r\n~ Shirō Emiya'),
        ('`If I get reincarnated…. I wanna become a clam`\r\n~ Monkey D. Luffy'),
        ('`Hey Mister! I am mad scientist!  It\'s so coooooooooool! Son of a bitch!`\r\n~ Rintaro Okabe'),
        ('`This is the magic item that suppresses my mighty magical powers. If I were ever to take this off, a great catastrophe would surely befall this world… Well, that was a lie. I just wear it for looks.`\r\n~ Megumin'),
        ('`I\'ll gladly turn into a piece of paper!`\r\n~ Terunosuke Miyamoto'),
        ('`Pornography can save the world!`\r\n~ Okajima Taiga'),
        ('`*touchs boob* Nothing wrong with the heartbeat!`~ Meliodas'),
        ('`Why do woman have butts on their chests?`\r\n~ Goku'),
        ('`You come to me. I\'ll hack the grin out of your Face`\r\n~ Yato'),
        ('`I need healing`\r\n~ Genji Shimada'),
        ('`SAKE!`\r\n~ Hanzo Shimada')
    ]
    response = random.choice(quote)
    embed = discord.Embed(color=0x22a7f0)
    embed.add_field(name=f'Quote for {str(ctx.message.author)}', value=response)
    await ctx.send(embed=embed)
@bot.command(name='quote')
async def _quote(ctx):
    quotes = [
            ('`All war is based on deception`\r\n~ Sun Tzu - The Art of War'),
            ('`If you think you are too small to make a difference,\r\ntry sleeping with a mosquito`\r\n~ Dalai Lama'),
            ('`Politicians and diapers have to be changed often, and for the same reason`\r\n~ Mark Twain'),
            ('`Before you judge a man, walk a mile in his shoes.\r\nAfter that who cares? He is a mile away and you got his shoes`\r\n~ Billy Connolly'),
            ('`The difference between stupidity and genius is that genius has its limits.`\r\n~ Albert Einstein'),
            ('`Expecting the world to treat you fairly because you are a good person is a little like expecting the bull not to attack you because you are a vegetarian.`\r\n~ Dennis Wholey'),
            ('`The road to success is always under construction.`\r\n~ Lily Tomlin'),
            ('`Worrying is like paying a debt you do not owe.`\r\n~ Mark Twain'),
            ('`Always remember that you are absolutely unique. Just like everyone else.`\r\n~ Margaret Mead'),
            ('`The surest sign that intelligent life exists elsewhere in the universe is that it has never tried to contact us.`\r\n~ Bill Watterson'),
            ('`Some folks are wise and some are otherwise.`\r\n~ Tobias Smollett'),
            ('`My opinions may have changed, but not the fact that I am right.`\r\n~ Ashleigh Brilliant'),
            ('`You can put lipstick on a pig, but it is still a pig.`\r\n~ Barack Obama'),
            ('`The German mind has a talent for making no mistakes but the very greatest.`\r\n~ Clifton Fadiman'),
            ('`HOLY SHIIT. Nur noch 20 Zentimeter`\r\n~ Selina'),
            ('`The ability to speak does not make you intelligent.`\r\n~ Qui Gon Yin'),
            ('`Genauso wie kein Kind auf die Welt kommt und irgendwie direkt rassistisch ist, bin ich auf die Welt gekommen und...uhm...und hatte das Bedürfnis 2 Freundinnen gleichzeitig zu haben.`\r\n~Nebelniek'),
            ]
    response = random.choice(quotes)
    embed = discord.Embed(color=0x22a7f0)
    embed.add_field(name=f'Quote for {str(ctx.message.author)}', value=response)
    await ctx.send(embed=embed)
@bot.command(name='partner')
async def _partner(ctx, aliases=['Beziehungen']):
    beziehungen = discord.Embed(title ='**Beziehungen**',
                                color = 0x22a7f0)
    beziehungen.add_field(name ='Besenkammer und Ententeich', value='Julien x Julien\r\nSelina x Julien\r\nSelina x Emma\r\nSelina x Lu\r\n||Serph x Gracos||\r\nPopo x Elisa\r\nCan x Irb\r\nLevi x Manu\r\nPaul x ducc\r\nYuki x Conni\r\nHees x Appls\r\nHamster x Einsamkeit')
    await ctx.send(embed=beziehungen)
@bot.command()
async def inspire(ctx): #siege get_quote()
  quote = get_quote()
  embed = discord.Embed(title='Inspiration')
  embed.add_field(name = None, value = str(quote))
  await ctx.message.channel.send(quote)
@bot.command(name='slap')
async def _slap(ctx, args1 , args2= None, *, args3 = None):
    boolean = True
    if 'weil' in args2:
        boolean = False
    else:
        pass
    emb_weil = discord.Embed(title='**Slap**', # wenn 'weil' geschrieben wird
                          description= '**' + args1 + '**' + ' **wurde geslapped.**\r\n' + args2 + '\r\n' + '```' + args3 + '```',
                          color=0x22a7f0)

    emb_n_weil = discord.Embed(title='**SLAP**', # wenn 'weil' nicht geschrieben wird
                          description= '**' + args1 + '**' + ' **wurde geslapped.**\r\n**Weil:**\r\n' + '```' + args2 + ' ' + args3 + '```',
                          color=0x22a7f0)
    if boolean == True:
        await ctx.send(embed=emb_n_weil)
    else:
        await ctx.send(embed=emb_weil)
@bot.command(name='claim')
async def _claim(ctx, member: discord.Member):
    claim = discord.Embed(title='Claim',
                          description=f'{member} wurde von' + str(ctx.message.author.mention) + ' geclaimt',
                          color=0x22a7f0)
    await ctx.message.channel.send(embed=claim)
@bot.command(name='someone', aliases=['irgendwer'])
@has_permissions(kick_members=True)
async def _someone(ctx):
  members = discord.bot.users
  for x in members:
    await ctx.send(x)
@bot.command(name='noone', aliases=['niemand'])
async def _noone(ctx):
    await ctx.send('Tja, halt niemand ne.')
###################################
@bot.command(name='video' ,aliases=['random-video'])
async def video(ctx, videoart):
    lowercase = videoart.lower()
    if 'kkk' in lowercase:
        kkkresponse=[
        ('https://www.youtube.com/watch?v=ZxC9UG6s7BQ'),
        ('https://www.youtube.com/watch?v=cDnBGsjJSnU'),
        ('https://www.youtube.com/watch?v=jEV4n_NF8AQ'),
        ('https://www.youtube.com/watch?v=978u3BZIrYA'),
        ('https://www.youtube.com/watch?v=-PG4QklSP70'),
        ('https://www.youtube.com/watch?v=XWNvhWsj3cs'),
        ('https://www.youtube.com/watch?v=yBEBNdu8208'),
        ('https://www.youtube.com/watch?v=-CvBNgxnzKQ'),
        ('https://www.youtube.com/watch?v=KhSSBrs6RTk'),
        ('https://www.youtube.com/watch?v=bPMA-Vm-6iE'),
        ('https://www.youtube.com/watch?v=c-a1faxgw1Q'),
                    ]
        embed = f'Zufälliges Video für {ctx.author.mention}\r\n{random.choice(kkkresponse)}'
        await ctx.send(embed)

    elif 'swsg' in lowercase:
        swsgresponse=[
        ('https://www.youtube.com/watch?v=2tWMZPxnQNg'),
        ('https://www.youtube.com/watch?v=qE__wAywuaE'),
        ('https://www.youtube.com/watch?v=yjd0OKcMqdU'),
        ('https://www.youtube.com/watch?v=YFlN9ToJfpU'),
        ('https://www.youtube.com/watch?v=piuX64u9E0w'),
        ('https://www.youtube.com/watch?v=p8CTP2MmRbk'),
        ('https://www.youtube.com/watch?v=IYjxm5COloI'),
        ('https://www.youtube.com/watch?v=NTVB9AFW58Q'),
        ('https://www.youtube.com/watch?v=7rAxzuFoStE'),
        ('https://www.youtube.com/watch?v=9DadYUnlMR0'),
        ('https://www.youtube.com/watch?v=_nQHdxatwT0'),
        ('https://www.youtube.com/watch?v=mLI0aHnVa58'),
        ('https://www.youtube.com/watch?v=zvR-AYGZyCM'),
        ('https://www.youtube.com/watch?v=irdsLnjBPrQ'),
        ('https://www.youtube.com/watch?v=OxzUxsYxtiw'),
        ('https://www.youtube.com/watch?v=M9J-CRpBvPY'),
        ('https://www.youtube.com/watch?v=ijXhRgQABDs'),
        ('https://www.youtube.com/watch?v=nJToWbeLTaw'),
        ('https://www.youtube.com/watch?v=j-ZD2_M-It4'),
        ('https://www.youtube.com/watch?v=1SJeayUq22g'),
        ('https://www.youtube.com/watch?v=kqssKL5Rbck'),
        ('https://www.youtube.com/watch?v=5t7NzXKCnHM'),
        ('https://www.youtube.com/watch?v=8_raSTNGkQY'),
        ('https://www.youtube.com/watch?v=CC-wRDWF9os'),
        ('https://www.youtube.com/watch?v=9gYTFVikHlc'),
        ('https://www.youtube.com/watch?v=gKNZsBt9P6o'),
        ]
        embed = f'Zufälliges Video für {ctx.author.mention}\r\n{random.choice(swsgresponse)}'
        await ctx.send(embed)
########################################################################
@bot.command(name='upper')
async def _upper(ctx, *, content: to_upper):
    await ctx.send(content)
@bot.command(name='mau5ify')
async def _mau5ify(ctx, *, args1 : mau5ify):
    await ctx.send(args1)
########################################################################
@bot.command(name='clear', description='Entfernt eine bestimmte Anzahl an Nachrichten')
@has_permissions(manage_messages=True)
async def _clear(ctx, count=5):
    await ctx.channel.purge(limit=count + 1, check=mess_not_pinned)
    if count == 1:
        await ctx.send('Es wurde eine Nachricht gelöscht.\r\nIrgendwie unnötig, dass kann man auch selber machen.')
    else:
        await ctx.send(f'Es wurden {str(count)} Nachrichten gelöscht')
@bot.command(name='rolle')
async def rolle(ctx, *, rolle : discord.Role):
    antwort = rolle.permissions
    await ctx.send(antwort)
@bot.command(name='ping')
async def _ping(ctx, ):
        await ctx.send(f'Pong! {round(bot.latency * 1000)}ms' )
########################################################################
@bot.command() #Kickt einen User
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Kicked {member.mention}')
#########################################################################
@bot.command() #Bannt einen User
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'Banned {member.mention}')
@bot.command()#Unbannt einen gebannten User
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
#########################################################################
@bot.command(name='userinfo') #infos für einen User
async def _userinfo(ctx, member : discord.Member):
    embed = discord.Embed(title='Userinfo für {}'.format(member),
                          description='Dies ist eine Userinfo für den User {}'.format(member.mention),
                          color=0x22a7f0)
    embed.add_field(name='Server beigetreten', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                        inline=True)
    embed.add_field(name='Discord beigetreten', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                        inline=True)
    rollen = ''
    for role in member.roles:
        if not role.is_default():
            rollen += '{} \r\n'.format(role.mention)
    if rollen:
        embed.add_field(name='Rollen', value=rollen, inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text='hehe a:hehefishii: ')
    mess = await ctx.message.channel.send(embed=embed)
    await mess.add_reaction('🇱')
    await mess.add_reaction('🇴')
    await mess.add_reaction('🇻')
    await mess.add_reaction('🇪')
    await mess.add_reaction('❤')
    await mess.add_reaction('🇺')
    await mess.add_reaction('a:besen:680490201822527521')
    await mess.add_reaction('a:Doggo:715691301466538037')

@bot.command(name='avatar', aliases=['pb','profilepicture'])
async def avatar(ctx, member: discord.Member = None):
    if member:
      await ctx.send(member.avatar_url)
    else:
      await ctx.send(ctx.author.avatar_url)
@bot.event
async def on_ready():
    print(f"we have logged in as {bot.user}")



#bot.run('') #TestBot
bot.run('') #DuccBot


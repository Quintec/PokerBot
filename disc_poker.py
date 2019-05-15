import discord
import random
from objects import *

first_run = True

deck = []
def reset_deck():
    global deck
    suits = ["hearts", "diamonds", "spades", "clubs"]
    deck = []
    for x in range(1,14):
        for s in suits:
            deck.append(Card(x,s))
    random.shuffle(deck)
reset_deck()

bot = discord.Client()
players = []
game_info = []
in_g = False
first = 0
curr = 0
bet = 0
pot = 0
best = 0
commands = True
pictures = False
def run():
    print("This isn't broken yet")
    bot.run('MzgxOTM0OTY1Mjg3Mjg4ODM1.DT6ZHg.nq3-giTgG83lZDAJ0i33KAeWfy4')




    

@bot.event
async def on_ready():
    global first_run
    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name='p!help'))
    if first_run:
        channel = bot.get_channel(448910359718395908)
        await channel.send("PokerBot is now online. Get your chips ready!")
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
        first_run = False


async def calc_winner(ch):
    global in_g
    global players
    global deck
    global first
    global game_info
    global bet
    global curr
    global pot
    global best
    global commands
    global pictures

    await ch.send("Everyone has called!")
    for player in game_info:
        player.tsa_precheck()
        if not player.folded:
            player.rank_hand()

    winners = []
    idxs = []
    high_rank = 0
    
    for i in range(0, len(game_info)):
        if game_info[i].rank > high_rank and not game_info[i].folded:
            winners.clear()
            idxs.clear()
            high_rank = game_info[i].rank
            winners.append(game_info[i])
            idxs.append(i)
        elif game_info[i].rank == high_rank and not game_info[i].folded:
            winners.append(game_info[i])
            idxs.append(i)

    high_high = 0
    high_2 = 0
    for highhigh in winners:
        if highhigh.high > high_high:
            high_high = highhigh.high
            high_2 = highhigh.high2
        elif highhigh.high == high_high and highhigh.high2 > high_2:
            high_2 = highhigh.high2

    for w in winners:
        if w.high != high_high or w.high2 != high_2:
            winners.remove(w)
    for player in game_info:
        if not player.folded:
            await ch.send(player.user.display_name + ": " + str([str(x) for x in player.hand]))
    winnings = pot // len(winners)
    
    for w in winners:
        await ch.send(w.user.mention + " has won **" + str(winnings) + "** chips with **" + w.hand_name + "**!" )
        w.money += winnings
    
    if first < (len(players) - 1):
        first = first + 1
    else:
        first = 0
    
    curr = first
    best = first
    bet = 0
    reset_deck()
    remove_list = []
    pot = 0
    for i in range(0, len(game_info)):
        p = game_info[i]
        p.hand = []
        p.folded = False
        p.has_moved = False
        p.bet = 0
        if p.money <= 0:
            remove_list.append(p)
            players.pop(i)
    for r in remove_list:
        game_info.remove(r)
    if len(players) == 1:
        await ch.send( players[0].mention + ", you have won the game!")
        players = []
        game_info = []
        in_g = False
        first = 0
        curr = 0
        bet = 0
        pot = 0
        best = 0
        return
    await ch.send("Reshuffling and redealing...")
    for p in range(0, len(players)):
        game_info[p].hand.clear() #HAND TEXT+PICNO MATCH
        for x in range(0, 5):
            c = deck.pop()

            game_info[p].hand.append(c)
            await players[p].send(str(c))
        if pictures:
            await players[p].send(files=game_info[p].d_files)
        await players[p].send("-----------")
        game_info[p].money -= 5
        if game_info[p].money < 0:
            pot += game_info[p].money + 5
            game_info[p].money = 0
        else:
            pot += 5
    await ch.send("Each player has put 5 chips into the pot.")
        
    await ch.send( players[first].mention + ", it is your turn!")
    await ch.send( "The current bet is 0.")

    
        
        

def is_dealer(member):
    for r in member.roles:
        if 'Dealer'==(r.name):
              return True
    return False

async def join(member, ch):
    global in_g
    global players
    global game_info
    if not in_g:
        n = member
        if n not in players:
            await ch.send( n.mention + ", you have joined the game!")
            players.append(n)
            game_info.append(Player(n))
        else:
            await ch.send( n.mention + ", you are already in the game!")
    else:
        await ch.send( "Sorry, but a game is already in progress.")

async def start(member, ch):
    global in_g
    global players
    global game_info
    global commands
    global pictures
    global pot
    if not in_g:
        if is_dealer(member):#CHANGEAHGHAGHAEHGHA
            in_g = True
            for p in players:
                await ch.send( p.mention)
            await ch.send( "The game has started! Dealing cards...")
            commands = False
            for p in range(0, len(players)):
                for x in range(0, 5):
                    c = deck.pop()
                    
                    game_info[p].hand.append(c)
                    game_info[p].d_files.append(discord.File(c.to_img_str()))
                    await players[p].send(str(c))
                if pictures:
                    await players[p].send(files=game_info[p].d_files)
                await players[p].send("-----------")
                game_info[p].money -= 5
                pot += 5
            await ch.send("Each player has put 5 chips into the pot.")

            await ch.send( players[first].mention + ", it is your turn!")
            await ch.send( "The current bet is 0.")
            commands = True
        else:
            await ch.send( "Sorry, you do not have permission to start the game.")
    else:
        await ch.send( "There is already a game in progress!")

async def next_player(ch):
    global players
    global game_info
    global bet
    global curr
    curr = curr + 1
    if curr > (len(players) - 1):
        curr = 0
    while game_info[curr].folded:
        if curr < (len(players) - 1):
            curr = curr + 1
        else:
            curr = 0
    await ch.send( players[curr].mention + ", it is your turn!")
    await ch.send( "The current bet is " + str(bet) + ".")

def all_moved():
    global game_info
    for p in game_info:
        if not (p.has_moved or p.folded):
            return False
    return True
    
async def check(member, ch):
    global in_g
    global players
    global game_info
    global bet
    if in_g:
        if member!=players[curr]:
            await ch.send( "It's not your turn!")
            return
        else:
            if  bet!=0:
                await ch.send( "You need to at least call the current bet!")
                return
            else:
                game_info[curr].has_moved = True
            if all_moved():
                await calc_winner(ch)
            else:
                await next_player(ch)
                
    else:
        await ch.send( "There is no game currently in progress!")

async def p_raise(member, ch, message):
    global in_g
    global players
    global game_info
    global bet
    global curr
    global pot
    global best
    if in_g:
        if member!=players[curr]:
            await ch.send( "It's not your turn!")
            return
        else:
            try:
                inf = message.content.split(" ")##ADD MESSAGE FROM CALL IN MAIN
            except (ValueError, IndexError) as e:
                print(e)
                await ch.send( "Not a valid raise! The format is p!raise [amount].")
            if len(inf) != 2:
                    await ch.send( "Not a valid raise! The format is p!raise [amount]")
                    return
            else:
                amt = int(inf[1])
                if amt <= bet:
                    await ch.send( "A raise must be greater than the current bet.")
                    return
                else:
                    if amt > game_info[curr].bet + game_info[curr].money:
                        await ch.send( "You don't have enough chips to raise this amount!")
                    else:
                        pot = pot - game_info[curr].bet
                        game_info[curr].money = game_info[curr].money + game_info[curr].bet - amt
                        game_info[curr].bet = amt
                        pot = pot + amt
                        bet = amt
                        best = curr
                        for p in game_info:
                            p.has_moved = False
                        game_info[curr].has_moved = True
                        await ch.send( players[curr].mention + " has bet " + str(amt) + ".")
                        await next_player(ch)
    else:
        await ch.send( "There is no game currently in progress!")

async def call(member, ch):
    global in_g
    global players
    global deck
    global first
    global game_info
    global bet
    global curr
    global pot
    global best
    global commands
    if in_g:
        if member!=players[curr]:
            await ch.send( "It's not your turn!")
            return
        else:
            if game_info[curr].money + game_info[curr].bet < bet:
                game_info[curr].bet = game_info[curr].money 
                game_info[curr].money = 0
                pot = pot + game_info[curr].bet
                game_info[curr].has_moved = True
            else:
                pot = pot - game_info[curr].bet
                game_info[curr].money = game_info[curr].money + game_info[curr].bet - bet
                game_info[curr].bet = bet
                pot = pot + bet
                game_info[curr].has_moved = True
            await ch.send( players[curr].mention + " has bet " + str(game_info[curr].bet) + ".")

            if all_moved():
                await calc_winner(ch)
            else: 
                await next_player(ch)
    else:
        await ch.send( "There is no game currently in progress!")

async def fold(member, ch):
    global in_g
    global players
    global deck
    global first
    global game_info
    global bet
    global curr
    global pot
    global best
    global commands
    global pictures
    if member!=players[curr]:
        await ch.send( "It's not your turn!")
    else:
        game_info[curr].folded = True
        await ch.send( member.mention + " has folded.")
        while game_info[curr].folded:
            if curr < (len(players) - 1):
                curr = curr + 1
            else:
                curr = 0
        left = 0
        pleft = Player(0)
        ix = 0
        for i in range(0, len(game_info)):
            if not game_info[i].folded:
                left += 1
                pleft = game_info[i]
                ix = i
        if left==1:
            await ch.send( players[ix].mention + " has won " + str(pot) + " chips.")
            pleft.money += pot
            pot = 0
            if first < (len(players) - 1):
                first = first + 1
            else:
                first = 0
            curr = first
            best = first
            bet = 0
            reset_deck()
            pot = 0
            remove_list = []
            for i in range(0, len(game_info)):
                p = game_info[i]
                p.hand = []
                p.folded = False
                p.has_moved = False
                p.bet = 0
                if p.money <= 0:
                    remove_list.append(p)
                    players.pop(i)
            for r in remove_list:
                game_info.remove(r)
            if len(players) == 1:
                await ch.send( players[0].mention + ", you have won the game!")
                players = []
                game_info = []
                in_g = False
                first = 0
                curr = 0
                bet = 0
                pot = 0
                best = 0
                return
            await ch.send("Reshuffling and redealing...")
            for p in range(0, len(players)):
                
                game_info[p].hand.clear() #HAND TEXT+PICNO MATCH
                for x in range(0, 5):
                    c = deck.pop()
     
                    game_info[p].hand.append(c)
                    await players[p].send(str(c))
                if pictures:
                    await players[p].send(files=game_info[p].d_files)
                await players[p].send("-----------")
                game_info[p].money -= 5
                if game_info[p].money < 0:
                    pot += game_info[p].money + 5
                    game_info[p].money = 0
                else:
                    pot += 5
            await ch.send("Each player has put 5 chips into the pot.")
                
            await ch.send( players[first].mention + ", it is your turn!")
            await ch.send( "The current bet is 0.")
        else:
            if all_moved():
                await calc_winner(ch)
            else:
                await ch.send( players[curr].mention + ", it is your turn!")
                await ch.send( "The current bet is " + str(bet) + ".")

@bot.event
async def on_message(message):
    global in_g
    global players
    global deck
    global first
    global game_info
    global bet
    global curr
    global pot
    global best
    global commands
    global pictures

    ch = message.channel
    try:
        print(message.author.name + ": " + message.content)
    except UnicodeEncodeError:
        print(message.author.name + ": " + "<unprintable message>")
    
    if message.author == bot.user:
        return
    
    if not commands:
        return

    if message.content.startswith('p!remove'):
        if not (is_dealer(message.author)):#CHANGEAHGHAGHAEHGHA
            await ch.send("Sorry, you don't have permission to do this.")
        else:
            try:
                info = message.content.split(" ")
                del players[int(info[1])]
                del game_info[int(info[1])]
                await ch.send("Player succesfully removed!")
            except (ValueError, IndexError) as e:
                await ch.send("Invalid index of player to remove.")

    if message.content.startswith('p!pictures'):
        pictures = not pictures
        await ch.send("I will now DM you pictures of your cards in addition to text." if pictures else "Ok, no more pictures of cards. Just text.")
    
    if message.content.startswith('p!rules'):
        await ch.send('https://en.wikipedia.org/wiki/Five-card_draw')
        
    if message.content.startswith('p!fixyourself'):
        if is_dealer(message.author):
            await ch.send('Why would I make it easy for you, ' + message.author.mention + " ?")
            
    if message.content.startswith('p!join'):
        await join(message.author, ch)
        
    if message.content.startswith('p!start'):
        await start(message.author, ch)

    if message.content.startswith('p!check'):
        await check(message.author, ch)
        
    if message.content.startswith('p!raise'):
        await p_raise(message.author, ch, message)
            
    if message.content.startswith('p!call'):
        await call(message.author, ch)
        
    if message.content.startswith('p!chips'):
        if message.author in players:
            chip_num = 0
            for x in game_info:
                if x.user == message.author:
                    chip_num = x.money
                    break
            await ch.send( message.author.mention + ", you have " + str(chip_num)
                                   + " chips.")
        else:
            await ch.send( message.author.mention + ", you are not in the game!")
            
    if message.content.startswith('p!fold'):
        await fold(message.author, ch)
            
            
        
    if message.content.startswith('p!pot'):
        if in_g:
            await ch.send( "The pot contains " + str(pot) + " chips.")
        else:
            await ch.send( "There is no game currently in progress!")


    if message.content.startswith('p!end'):
        if in_g:
            allowed = False
            for r in message.author.roles:
                if 'Dealer'==(r.name):
                    allowed = True
                    break
            if allowed:
                in_g = False
                await ch.send( "Game ended!")
                players = []
                reset_deck()
                game_info = []
                first = 0
                curr = 0
                bet = 0
                pot = 0
            else:
                await ch.send( "Sorry, you do not have permission to stop the game.")
        else:
            await ch.send( "There is no game currently going on.")


    if message.content.startswith('p!players'):
        plist = list(map((lambda p: p.display_name), players))
        await ch.send( plist)

    if message.content.startswith('p!help'):
        msg = """p!join: Joins the game, if there are none going on.
p!start: Starts the game. Only dealers can do this(anyone for now)
p!end: Ends the game. Only dealers can do this.(anyone for now)
p!players: Lists the current players.
p!rules: Lists the rules.
p!remove: Removes a player from the game. Only dealers can do this.(anyone for now)
-------IN GAME-------
p!check: Checks(bets 0).
p!call: Calls the current bet.
p!raise [amount]: Raises the bet to [amount].
p!fold: Folds the current hand.
p!pot: Shows the number of chips in the pot.
p!chips: Shows your number of chips.
"""
        await ch.send( msg)


run()


#DONE Deal out hands to each player from single deck
#DONE Card class only

#TO-DO-KEEP-UPDATING: Rules command

#TO-DO: actual game mechanics

#Rank hands from highest to lowest
#Bash bash bash go

#DONE dict for money - start at 100?

#DONE Betting algorithm
#DONE if in_game: (accept only betting and end commands)
#    current bet is minimum
#    p!call command
#    p!raise x command
#    reveal hands option?
#    reset redeal whee

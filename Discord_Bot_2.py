import discord
import datetime
import sqlite3
import random
#import youtube_dl
from discord.ext import commands

def AccountCheck(UserID) :

    IDBuffer = []

    DBAccess = sqlite3.connect("AKKYUBOT.sqlite", isolation_level=None)
    DB = DBAccess.cursor()

    DB.execute("SELECT UserID FROM CoinAccount WHERE UserID=?", (UserID,))

    for i in DB.fetchall():
        IDBuffer.append(i[0])

    if UserID in IDBuffer :
        return True
    elif UserID not in IDBuffer :
        return False

    DB.close()

bot = commands.Bot(command_prefix='!')
BotToken = 'ODQzODMwODEwODQ2MDM2MDI3.YKJkrg.uh0Ex92TXv2Ezg3FIdjKB0gu6Ds'


@bot.event
async def on_ready():

    print('봇을 실행합니다...')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def 민수(ctx):

    await ctx.send("바보")


@bot.command()
async def 카지노(ctx):

    embed=discord.Embed(title=":slot_machine: CA$1N0 :slot_machine:", description="카지노 안내입니다.", color=0xA52A2A)
    embed.add_field(name="<:yCoinBeta:837627374664417282> Y-COIN 안내",
                    value="베타 테스트를 끝내고 드디어 <:yCoinBeta:837627374664417282> Y-COIN이 정식 출시되었습니다.", inline=False)
    embed.add_field(name="명령어 안내", value="`!가입` - Y-COIN 지갑을 만듭니다.\n`!홀짝 [홀/짝] [배팅금]` - 홀짝 게임을 합니다\n`!주사위 [배팅금]` - 주사위 게임을 합니다.\n`!로또` - 로또에 관한 안내를 봅니다.", inline=False)
    embed.set_footer(text="불/법/도/박/신/고/1855-0112")

    await ctx.send(embed=embed)


@bot.command()
async def 순위(ctx):

    NameRanking = []

    DBAccess = sqlite3.connect("AKKYUBOT.sqlite", isolation_level=None)
    DB = DBAccess.cursor()

    DB.execute("SELECT Coins FROM CoinAccount")

    CoinRanking = DB.fetchall()
    
    CoinRanking.sort(reverse=True)

    for i in CoinRanking[0:10]:

        DB.execute("SELECT UserName FROM CoinAccount WHERE Coins=?", (i[0],))

        UserName = DB.fetchone()

        NameRanking.append(UserName[0])

    embed = discord.Embed(title=":trophy: COIN RANKING :trophy:", description="현재 순위입니다.", color=0xFFD700)

    for i in range(0, 10):

        if i == 0:
            embed.add_field(name=":first_place: `{}`".format(NameRanking[i]), value="{} <:yCoinBeta:837627374664417282>".format(CoinRanking[i][0]), inline=False)
        elif i == 1:
            embed.add_field(name=":second_place: `{}`".format(NameRanking[i]), value="{} <:yCoinBeta:837627374664417282>".format(CoinRanking[i][0]), inline=False)
        elif i == 2:
            embed.add_field(name=":third_place: `{}`".format(NameRanking[i]), value="{} <:yCoinBeta:837627374664417282>".format(CoinRanking[i][0]), inline=False)
        else:
            embed.add_field(name="{} - `{}`".format(i + 1, NameRanking[i]), value="{} <:yCoinBeta:837627374664417282>".format(CoinRanking[i][0]), inline=False)

    embed.set_footer(text="Y/C/O/I/N/거/래/소")

    await ctx.send(embed=embed)

    DB.close()



@bot.command()
async def 홀짝(ctx, choice, bet):

    UserID = ctx.author.id
    UserName = ctx.author.name

    IsUserExist = AccountCheck(UserID)

    if IsUserExist:
        DBAccess = sqlite3.connect("AKKYUBOT.sqlite", isolation_level=None)
        DB = DBAccess.cursor()

        DB.execute("SELECT Coins FROM CoinAccount WHERE UserID=?", (UserID,))

        UserCoin = DB.fetchone()

        if UserCoin[0] < int(bet) :
            await ctx.send(":smiling_face_with_tear: 잔액이 부족합니다.")
            return
        if UserCoin[0] == int(bet) :
           await ctx.send(":open_mouth: 와우! 올인!")

        RNG = random.randint(1, 99)

        await ctx.send("`당신의 선택 : {}`, `나온 숫자 = {}`".format(choice, RNG))

        if choice == '홀' :
            if RNG % 2 == 1 :
                await ctx.send(":tada: 축하합니다! `얻은 코인 = {}` <:yCoinBeta:837627374664417282>, `총 코인 = {}` <:yCoinBeta:837627374664417282>".format(int(bet) * 2, UserCoin[0] + int(bet)))
                DB.execute("UPDATE CoinAccount SET Coins=? WHERE UserID=?", (UserCoin[0] + int(bet), UserID))
            else :
                await ctx.send(":boom: 틀렸습니다! `잃은 코인 = {}` <:yCoinBeta:837627374664417282>, `총 코인 = {}` <:yCoinBeta:837627374664417282>".format(int(bet), UserCoin[0] - int(bet)))
                DB.execute("UPDATE CoinAccount SET Coins=? WHERE UserID=?", (UserCoin[0] - int(bet), UserID))
        elif choice == '짝' :
            if RNG % 2 == 0:
                await ctx.send(":tada: 축하합니다! `얻은 코인 = {}` <:yCoinBeta:837627374664417282>, `총 코인 = {}` <:yCoinBeta:837627374664417282>".format(int(bet) * 2, UserCoin[0] + int(bet)))
                DB.execute("UPDATE CoinAccount SET Coins=? WHERE UserID=?", (UserCoin[0] + int(bet), UserID))
            else:
                await ctx.send(":boom: 틀렸습니다! `잃은 코인 = {}` <:yCoinBeta:837627374664417282>, `총 코인 = {}` <:yCoinBeta:837627374664417282>".format(int(bet), UserCoin[0] - int(bet)))
                DB.execute("UPDATE CoinAccount SET Coins=? WHERE UserID=?", (UserCoin[0] - int(bet), UserID))
        else :
            await ctx.send("잘못 입력하셨습니다. `!홀짝 [홀/짝] [배팅금]` 형태로 입력해주세요.")
    else:

        await ctx.send("{} 님은 아직 <:yCoinBeta:837627374664417282> `Y-COIN 지갑`이 없습니다. `!가입` 명령어를 통해 <:yCoinBeta:837627374664417282> Y-COIN 지갑을 먼저 만드세요.".format(UserName))

    DB.close()

@bot.command()
async def 주사위(ctx, bet):

    UserID = ctx.author.id
    UserName = ctx.author.name

    IsUserExist = AccountCheck(UserID)

    if IsUserExist:

        DBAccess = sqlite3.connect("AKKYUBOT.sqlite", isolation_level=None)
        DB = DBAccess.cursor()

        DB.execute("SELECT Coins FROM CoinAccount WHERE UserID=?", (UserID,))

        UserCoin = DB.fetchone()

        if UserCoin[0] < int(bet):
            await ctx.send(":smiling_face_with_tear: 잔액이 부족합니다.")
            return
        if UserCoin[0] == int(bet):
            await ctx.send(":open_mouth: 와우! 올인!")

        User = random.randint(1, 6)
        AI = random.randint(1, 6)

        await ctx.send("당신의 :game_die: : `{}`, 상대의 :game_die: `{}`".format(User, AI))

        if User > AI :
            await ctx.send(":tada: 축하합니다! `얻은 코인 = {}` <:yCoinBeta:837627374664417282>, `총 코인 = {}` <:yCoinBeta:837627374664417282>".format(int(bet) * 2, UserCoin[0] + int(bet)))
            DB.execute("UPDATE CoinAccount SET Coins=? WHERE UserID=?", (UserCoin[0] + int(bet), UserID))
        elif User < AI :
            await ctx.send(":boom: 틀렸습니다! `잃은 코인 = {}` <:yCoinBeta:837627374664417282>, `총 코인 = {}` <:yCoinBeta:837627374664417282>".format(int(bet), UserCoin[0] - int(bet)))
            DB.execute("UPDATE CoinAccount SET Coins=? WHERE UserID=?", (UserCoin[0] - int(bet), UserID))
        else:
            await ctx.send(":rolling_eyes: 비겼습니다! `총 코인 = {}` <:yCoinBeta:837627374664417282>".format(UserCoin[0]))
    else:
        
        await ctx.send("{} 님은 아직 <:yCoinBeta:837627374664417282> `Y-COIN 지갑`이 없습니다. `!가입` 명령어를 통해 <:yCoinBeta:837627374664417282> Y-COIN 지갑을 먼저 만드세요.".format(UserName))

    DB.close()


@bot.command()
async def 로또(ctx):

    await ctx.send("`아직 준비 중입니다. 많은 기대 부탁드립니다...`")


@bot.command()
async def 룰렛(ctx, bet):

    UserID = ctx.author.id
    UserName = ctx.author.name

    IsUserExist = AccountCheck(UserID)

    if IsUserExist:

        DBAccess = sqlite3.connect("AKKYUBOT.sqlite", isolation_level=None)
        DB = DBAccess.cursor()

        DB.execute("SELECT Coins FROM CoinAccount WHERE UserID=?", (UserID,))

        UserCoin = DB.fetchone()

        Percent = random.randint(0,100)
        await ctx.send(":persevere::gun: {} 님이 총을 들고 모든 걸 운에 맞깁니다... (생존 확률 : {})".format(UserName, Percent))

        if random.randint(0,100) < Percent:

            await ctx.send(":sunglasses: {} 님은 당당하게 살아남아 `{}` <:yCoinBeta:837627374664417282>을 챙겨갑니다... `총 코인 = {}` <:yCoinBeta:837627374664417282>".format(UserName, bet * 2, UserCoin[0] + bet))

    else:

        await ctx.send("{} 님은 아직 <:yCoinBeta:837627374664417282> Y-COIN 지갑이 없습니다. `!가입` 명령어를 통해 <:yCoinBeta:837627374664417282> Y-COIN 지갑을 먼저 만드세요.".format(UserName))

@bot.command()
async def 가입(ctx):

    UserID = ctx.author.id
    UserName = ctx.author.name

    DBAccess = sqlite3.connect("AKKYUBOT.sqlite", isolation_level=None)
    DB = DBAccess.cursor()

    now = datetime.datetime.now()
    CurrentTime = now.strftime('%Y-%m-%d %H:%M:%S')

    IsUserExist = AccountCheck(UserID)

    if IsUserExist:
        await ctx.send("안녕하세요 {} 님, 고객님은 이미 <:yCoinBeta:837627374664417282> Y-COIN 지갑이 있으십니다.".format(UserName))
    elif not(IsUserExist):
        DB.execute("INSERT INTO CoinAccount VALUES(?, ?, ?, ?, ?)", (CurrentTime, UserID, UserName, 200, 0))

        embed = discord.Embed(title="<:yCoinBeta:837627374664417282> Y-COIN 지갑 개설 완료", description="Y-COIN 지갑 알림", color=0x0000CD)
        embed.add_field(name="개설 축하금 지급 완료", value="{} 님의 지갑 개설이 완료되었습니다.\n가입 축하금 200 <:yCoinBeta:837627374664417282>이 지급되었습니다.".format(ctx.message.author.mention), inline=False)
        embed.add_field(name="명령어 안내", value="`!내돈` - 지금 가지고 있는 코인 잔액을 확인합니다.\n`!돈줘` - 하루 한 번 200원을 줍니다.", inline=False)
        embed.set_footer(text="Y/C/O/I/N/거/래/소")

        await ctx.send(embed=embed)

    DB.close()


@bot.command()
async def 탈퇴(ctx):

    UserID = ctx.author.id
    UserName = ctx.author.name

    DBAccess = sqlite3.connect("AKKYUBOT.sqlite", isolation_level=None)
    DB = DBAccess.cursor()

    IsUserExist = AccountCheck(UserID)

    if IsUserExist:
        await ctx.send("안녕하세요 {} 님의 <:yCoinBeta:837627374664417282> Y-COIN 지갑을 삭제합니다.".format(UserName))
        await ctx.send("지갑을 삭제하면 모든 계정 정보를 포함한 <:yCoinBeta:837627374664417282> Y-COIN이 사라집니다!".format(UserName))
        DB.execute("DELETE FROM CoinAccount WHERE UserID=?", (UserID,))
        await ctx.send("정상적으로 삭제되었습니다. 다음에 또 이용해주세요.".format(UserName))
    elif not(IsUserExist):

        await ctx.send("{} 님은 아직 <:yCoinBeta:837627374664417282> Y-COIN 지갑이 없습니다. `!가입` 명령어를 통해 <:yCoinBeta:837627374664417282> Y-COIN 지갑을 먼저 만드세요.".format(UserName))

    DB.close()


@bot.command()
async def 돈줘(ctx):

    UserID = ctx.author.id
    UserName = ctx.author.name

    DBAccess = sqlite3.connect("AKKYUBOT.sqlite", isolation_level=None)
    DB = DBAccess.cursor()

    now = datetime.datetime.now()
    CurrentTime = int(now.strftime('%d'))

    IsUserExist = AccountCheck(UserID)

    if IsUserExist :

        DB.execute("SELECT LastClaimed FROM CoinAccount WHERE UserId=?", (UserID,))
        LastClaimed = DB.fetchone()

        DB.execute("SELECT Coins FROM CoinAccount WHERE UserId=?", (UserID,))
        CoinLoad = DB.fetchone()

        if CurrentTime != LastClaimed[0]:

            DB.execute("UPDATE CoinAccount SET Coins=? WHERE UserID=?", (CoinLoad[0] + 200, UserID))

            await ctx.send("안녕하세요 {} 님, 하루 지원금 200 <:yCoinBeta:837627374664417282>가 지급되었습니다.\n현재 잔액 : {} <:yCoinBeta:837627374664417282>".format(UserName, CoinLoad[0] + 200))

            DB.execute("UPDATE CoinAccount SET LastClaimed=? WHERE UserID=?", (CurrentTime, UserID))

        else :
            await ctx.send("{} 님은 이미 하루 지원금이 지급되었습니다.\n현재 잔액 : {} <:yCoinBeta:837627374664417282>".format(UserName, CoinLoad[0]))

    elif IsUserExist == False :
        await ctx.send("{} 님, `!가입` 명령어를 통해 <:yCoinBeta:837627374664417282> Y-COIN 지갑을 먼저 만드세요.".format(UserName))

    DB.close()

@bot.command()
async def 내돈(ctx):

    UserID = ctx.author.id
    UserName = ctx.author.name

    DBAccess = sqlite3.connect("AKKYUBOT.sqlite", isolation_level=None)
    DB = DBAccess.cursor()

    IsUserExist = AccountCheck(UserID)

    if IsUserExist:
        DB.execute("SELECT Coins FROM CoinAccount WHERE UserId=?", (UserID,))
        CoinLoad = DB.fetchone()

        await ctx.send("{} 님의 현재 잔액 : {} <:yCoinBeta:837627374664417282>".format(UserName, CoinLoad[0]))
    elif IsUserExist == False:
        await ctx.send("{} 님, `!가입` 명령어를 통해 <:yCoinBeta:837627374664417282> Y-COIN 지갑을 먼저 만드세요.".format(UserName))

    DB.close()


@bot.command()
async def 초기화야옹(ctx):

    DBAccess = sqlite3.connect("AKKYUBOT.sqlite", isolation_level=None)
    DB = DBAccess.cursor()

    DB.execute("DROP TABLE IF EXISTS CoinAccount")

    DB.execute("CREATE TABLE CoinAccount(RegisterDate TEXT, UserID INTEGER, UserName TEXT, Coins INTEGER, LastClaimed INTEGER)")

    DB.close()

    await ctx.send("DB RESETED...")

bot.run(BotToken)

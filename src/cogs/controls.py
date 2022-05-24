import discord
from discord.ext import commands
from PIL import Image,ImageDraw,ImageChops, ImageFont

def circle(pfp):
    size = (270,270)
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def get_profile(self,member:discord.Member,level,fails,hint_used):
        pfp=circle(member.avatar)
        color="#ffffff"
        bg=Image.open("asset/img/bg.png")
        bg.paste(pfp,(17,67),pfp)
        font=ImageFont.truetype("src/asset/fonts/font.ttf",104)
        # 330,135
        draw=ImageDraw.Draw(bg)
        draw.text(
            xy=(330,135),
            text=f"User Id",
            font=font,
            fill=color
            )
        # 48,392
        name=input("Enter Name: ")
        font2=ImageFont.truetype("src/asset/fonts/font.ttf",62)
        if len(name)>16:
            name=f"{name[0:16]}..."
        draw.text(
            xy=(48,392),
            text=name,
            font=font2,
            fill=color
        )

        font3=ImageFont.truetype("src/asset/fonts/font.ttf",105)
        # 90,585
        draw.text(
            xy=(90,585),
            text=f"Level: {input('Enter Level: ')}",
            font=font3,
            fill=color
        )

        draw.text(
            xy=(90,735),
            text=f"Fails: {input('Enter Fail: ')}",
            font=font3,
            fill=color
        )

        draw.text(
            xy=(90,885),
            text=f"Tries: {input('Enter Tries: ')}",
            font=font3,
            fill=color
        )

        draw.text(
            xy=(90,1035),
            text=f"Hints: {input('Enter Hints: ')}",
            font=font3,
            fill=color
        )

class Controls(commands.Cog):
    """
    ALL THE COMMANDS AND EVENTS RELATED TO CONTROLS
    """
    def __init__(self,bot:commands.Bot):
        self.bot=bot
    

def setup(bot):
    bot.add_cog(Controls(bot))
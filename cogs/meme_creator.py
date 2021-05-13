import discord
from discord.embeds import Embed
from discord.ext import commands
from discord.ext import menus
from discord.ext.commands.errors import MissingRequiredArgument
from discord.message import Message
import requests

meme_template_names = None

with open("cogs\meme_templates.txt", "r") as txt_file:
    meme_template_names = txt_file.read().splitlines()


class MemeCreator(commands.Cog):
    def __init__(self, kazuma_bot: commands.Bot) -> None:
        self.kazuma_bot = kazuma_bot

    @commands.group(aliases=["meme", "m"], invoke_without_command=True)
    async def meme_main(self, ctx):
        await ctx.send("If you need help, please use **#meme help**")

    @meme_main.command(aliases=["help", "commands"])
    async def meme_help(self, ctx):
        help_embed = discord.Embed(
            title="__Commands__", description='***All Commands Must Have A "#meme" Prefix Before It.***', colour=discord.Colour.dark_blue())

        help_embed.add_field(
            name="To See The Available Meme Templates:", value="templates (optional param: id of the meme, 0-998)", inline=False)
        help_embed.add_field(name="To Create A Meme:",
                             value="create (top text), (bottom text), (name of the image template you want to use)", inline=False)

        help_embed.set_footer(text="Created By ChilledFrost#7765")

        await ctx.send(embed=help_embed)

    @meme_main.command(aliases=["c"])
    async def create(self, ctx: commands.Context, *, arguments: str = None):

        try:
            top_text, bottom_text, img_name = arguments.split(", ")
        except AttributeError:
            await ctx.send("__**Please enter values for the command.**__")
            await self.meme_help(ctx)
            return

        if not img_name in meme_template_names:
            await ctx.send("**The template image name you have provided is invalid.**")

        img_embed = discord.Embed(title=f"{ctx.author.name}'s Meme: ")

        top_text = top_text.replace(" ", "+")
        bottom_text = bottom_text.replace(" ", "+")

        img_embed.set_image(
            url=f"http://apimeme.com/meme?meme={img_name}&top={top_text}&bottom={bottom_text}")

        await ctx.send(embed=img_embed)
        await ctx.message.delete()

    @meme_main.command(aliases=["template", "t"])
    async def templates(self, ctx: commands.Context, id=0):
        if id < 0 or id > len(meme_template_names):
            await ctx.send("That is not a valid id. (0-998)")
            return

        template_menu = TemplateMenu(id, ctx.author.name)
        await template_menu.start(ctx)

# The Menu For A Template


class TemplateMenu(menus.Menu):
    def __init__(self, image_index, user):
        super().__init__(timeout=60.0, delete_message_after=True,
                         check_embeds=True)
        self.current_image_index = image_index
        self.user = user

    def create_template_embed(self) -> discord.Embed:
        template_embed = discord.Embed(
            title="Meme Template: ", description=f'ID: {self.current_image_index}, Template Name: "{meme_template_names[self.current_image_index]}"', colour=discord.Colour.dark_blue())
        template_embed.set_image(
            url=f'http://apimeme.com/thumbnail?name={meme_template_names[self.current_image_index]}')

        template_embed.set_footer(
            text=f"This Menu Can Only Be Accesed By {self.user}")

        return template_embed

    async def send_initial_message(self, ctx, channel):
        return await ctx.send(embed=self.create_template_embed())

    @menus.button('⬅', )
    async def on_left(self, payload):

        if payload.member == None:
            return

        await self.message.remove_reaction(payload.emoji, payload.member)

        if self.current_image_index == 0:
            self.current_image_index = len(meme_template_names) - 1
        else:
            self.current_image_index -= 1

        await self.message.edit(embed=self.create_template_embed())

    @menus.button('➡')
    async def on_right(self, payload):

        if payload.member == None:
            return

        await self.message.remove_reaction(payload.emoji, payload.member)

        if self.current_image_index == len(meme_template_names) - 1:
            self.current_image_index = 0
        else:
            self.current_image_index += 1

        print(self.current_image_index)

        await self.message.edit(embed=self.create_template_embed())


def setup(kazuma_bot):
    kazuma_bot.add_cog(MemeCreator(kazuma_bot))

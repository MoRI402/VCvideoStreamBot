import os
import sys
import asyncio
from config import Config
from helpers.logger import LOGGER
from helpers.utils import update, is_admin
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaDocument


HOME_TEXT = "ð **Wtsup [{}](tg://user?id={})**, \n\nI Am **VcVideoPlayer**. \n`Lets Enjoy Cinematic View  of Group Video Player With Your Friends â¤ï¸ð` \n\n**Made With ð By @Animax_Industry!**"
HELP_TEXT = """
ð --**SETTINGS**-- :

\u2022 `Add me to your group and my assistant too make admin both!`
\u2022 `Start a voice chat in your group & Restart the boy if not join to vc.`
\u2022 `Try /stream [video name] and /stream reply to amy video and yt link!`

ð --**COMMANDS**-- :

\u2022 `/seek` - seek the video
\u2022 `/skip` - skip current video
\u2022 `/live` - start live stream
\u2022 `/pause` - pause playing video
\u2022 `/resume` - resume playing video
\u2022 `/mute` - mute the vc userbot
\u2022 `/unmute` - unmute the vc userbot
\u2022 `/leave` - leave the voice chat
\u2022 `/shuffle` - shuffle the playlist
\u2022 `/volume` - change volume (0-200)
\u2022 `/replay` - play from the beginning
\u2022 `/clear` - clear the playlist queue
\u2022 `/restart` - update & restart the bot
\u2022 `/setvar` - set/change heroku configs
\u2022 `/getlogs` - get the ffmpeg & bot logs

Â© **Powered By** : 
**@TeamDeeCoDe** ð©âð»
"""

admin_filter=filters.create(is_admin) 

@Client.on_message(filters.command(["start", f"start@{Config.BOT_USERNAME}"]))
async def start(client, message):
    if message.chat.type == 'private':
        buttons = [
            [
                InlineKeyboardButton("Sá´á´Êá´Ê", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("CÊá´É´É´á´Ê", url="https://t.me/Animax_Industry"),
                InlineKeyboardButton("GÊá´á´á´", url="https://t.me/AnimaxchatZone"),
            ],
            [
                InlineKeyboardButton("Bá´á´ LÉªê±á´", url="https://t.me/weetaku_anime"),
                InlineKeyboardButton("Sá´á´Êá´á´", url="https://t.me/Animax_Industry"),
            ],
            [
                InlineKeyboardButton("Há´Êá´ & Cá´á´á´á´É´á´ê±", callback_data="help"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    else:
        await message.reply_text(f"**ð I'm Alive ð¥**")

@Client.on_message(filters.command(["help", f"help@{Config.BOT_USERNAME}"]))
async def show_help(client, message):
    if message.chat.type == 'private':
        buttons = [
            [
                InlineKeyboardButton("CÊá´ê±á´", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        if Config.msg.get('help') is not None:
            await Config.msg['help'].delete()
        Config.msg['help'] = await message.reply_text(
            HELP_TEXT,
            reply_markup=reply_markup
            )
    else:
        await message.reply_text(
            "**Contact me in PM to get a List of Commands â¨**", 
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Há´Êá´ â", url=f"http://t.me/{Config.BOT_USERNAME}?start=help")
                    ]
                ]
            )
        )


@Client.on_message(filters.command(["restart", "update", f"restart@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]) & admin_filter)
async def update_handler(client, message):
    if Config.HEROKU_APP:
        k=await message.reply_text("â¨ **Heroku Detected, \nRestarting Your App!**")
    else:
        k=await message.reply_text("ð **Processing...**")
    await update()
    try:
        await k.edit("ð **Restarted Successfully!**")
    except:
        pass


@Client.on_message(filters.command(["getlogs", f"getlogs@{Config.BOT_USERNAME}"]) & admin_filter)
async def get_logs(client, message):
    logs=[]
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("ffmpeg.txt", caption="FFMPEG Logs"))
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("botlog.txt", caption="Video Player Logs"))
    if logs:
        try:
            await message.reply_media_group(logs)
        except:
            await message.reply_text("â **An Error Occurred !**")
            pass
        logs.clear()
    else:
        await message.reply_text("â **No Logs File Find !**")


@Client.on_message(filters.command(["setvar", f"setvar@{Config.BOT_USERNAME}"]) & admin_filter)
async def set_heroku_var(client, message):
    if not Config.HEROKU_APP:
        buttons = [[InlineKeyboardButton('HEROKU_API_KEY', url='https://dashboard.heroku.com/account/applications/authorizations/new')]]
        await message.reply_text(
            text="â **No Heroku App Found !** \n__Please Note That, This Command Needs The Following Heroku Vars To Be Set :__ \n\n1. `HEROKU_API_KEY` : Your heroku account api key.\n2. `HEROKU_APP_NAME` : Your heroku app name. \n\n**For More Ask In @DeCodeSupport !!**", 
            reply_markup=InlineKeyboardMarkup(buttons))
        return     
    if " " in message.text:
        cmd, env = message.text.split(" ", 1)
        if  not "=" in env:
            return await message.reply_text("â **You Should Specify The Value For Variable!** \n\nFor Example: \n`/setvar CHAT_ID=-1001173097859`")
        var, value = env.split("=", 2)
        config = Config.HEROKU_APP.config()
        if not value:
            m=await message.reply_text(f"â **No Value Specified, So Deleting `{var}` Variable !**")
            await asyncio.sleep(2)
            if var in config:
                del config[var]
                await m.edit(f"ð **Sucessfully Deleted `{var}` !**")
                config[var] = None
            else:
                await m.edit(f"ð¤·ââï¸ **Variable Named `{var}` Not Found, Nothing Was Changed !**")
            return
        if var in config:
            m=await message.reply_text(f"â ï¸ **Variable Already Found, So Edited Value To `{value}` !**")
        else:
            m=await message.reply_text(f"â ï¸ **Variable Not Found, So Setting As New Var !**")
        await asyncio.sleep(2)
        await m.edit(f"ð **Succesfully Set Variable `{var}` With Value `{value}`, Now Restarting To Apply Changes !**")
        config[var] = str(value)
    else:
        await message.reply_text("â **You Haven't Provided Any Variable, You Should Follow The Correct Format !** \n\nFor Example: \nâ¢ `/setvar CHAT_ID=-1001173097859` to change or set CHAT_ID var. \nâ¢ `/setvar REPLY_MESSAGE=` to delete REPLY_MESSAGE var.") 

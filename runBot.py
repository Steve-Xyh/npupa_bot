#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
* File Name    : runBot.py
* Description  : Main entry of the robot
* Create Time  : 2020-03-13 12:14:47
* Version      : 1.0
* Author       : Steve X
* GitHub       : https://github.com/Steve-Xyh
'''


"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""


import os
import logging
from telegram.ext import Updater
from functions import command_list as cmd
from functions import message_handler as msg
from functions import token as tk
from apps import random_choice, check_new_member
msg.PARSE_MODE = 'MarkdownV2'
tk.TOKEN_FILE = './token'
PROXY = False if os.sys.platform.lower() == 'linux' else True
PROXY_CONFIG = {'proxy_url': 'socks5://127.0.0.1:1081/'}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Error handlers also receive the raised TelegramError object in error.


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        token=tk.get_token(),
        use_context=True,
        request_kwargs=PROXY_CONFIG if PROXY else None
    )

    print(f'Use PROXY:\t {PROXY_CONFIG if PROXY else None}')

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Init functions
    random_choice.init_app(dp)
    check_new_member.init_app(dp)
    cmd.init_command(dp)
    msg.init_message(dp)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

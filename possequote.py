"""
plugin to return random posse quote
"""

import urllib.request
import os
import logging
import hangups
import plugins
from fuzzywuzzy import process

logger = logging.getLogger(__name__)
commands = ["add"]

def sanitize_command(command):
    return process.extractOne(command, commands)[0]

def _initialise(bot):
    plugins.register_user_command(["possequote"])

def possepic(bot, event, *args):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    rel_path = "possequote.txt"
    possequote_path = os.path.join(script_dir, rel_path)

    dirty_command = ''.join(args).strip().lower()
    sanitized_command = sanitize_command(dirty_command)
    if sanitized_command == "add":
        try:
            quote = ''.join(args).split(' ')[4:]
            f = open(possequote_path, "a+")
            f.write(quote + "\r\n")
            f.close()
            logger.info("quote '{}' has been added by {}".format(quote, event.user.full_name))
            yield from bot.coro_send_message(
                event.conv,
                _("'" + quote + "' has been to the posse archive").format(
                    event.user.full_name, 'yay'))
        except KeyError:
            logger.warning("Error adding posse '{}' to {}".format(quote, possequote_path))
            yield from bot.coro_send_message(
                event.conv.id_,
                _("Error adding quote to archive").format(
                    event.user.full_name, 'yay'))
    else:
        f = open(possequote_path, "r")
        quotes = f.read().splitlines()
        f.close()

        quotes = [x for x in quotes if x]

        from random import randrange
        random_index = randrange(0, len(quotes))
        quote = quotes[random_index]
        yield from bot.coro_send_message(
            event.conv.id_,
            _(quote).format(
                event.user.full_name, 'yay'))

from exchange_bot_rates import exchange_rates
from config import currency_base, telegram_bot_token, REQUEST_KWARGS
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ParseMode

end_l = "\n"

if __name__ == '__main__':
    rates = exchange_rates()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        # level=logging.DEBUG)
                        level=logging.INFO)
    logger = logging.getLogger()

    updater = Updater(token=telegram_bot_token, use_context=True, request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher

# Start Handler
    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="This is simple exchange rate bot")

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)


# /list or /lst - returns list of all available rates
    def list(update, context):
        lst = rates.list_all(currency_base)
        text = "List of Exchange rates:" + end_l
        for r in lst:
            text += f"<code>{r}: {'{:9.2f}'.format(lst[r])}</code>" + end_l
        context.bot.send_message(chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML)

    list_handler = CommandHandler('list', list)
    lst_handler = CommandHandler('lst', list)
    dispatcher.add_handler(list_handler)
    dispatcher.add_handler(lst_handler)


# /exchange $10 to CAD
    def exchange(update, context):
        answer = ""
        amount = 0
        cur_from = ""
        cur_to = ""
        try:
            if len(context.args) == 3:
                if context.args[0].find('$') >= 0:
                    cur_from = 'USD'
                    amount = float(context.args[0].replace('$', '').replace(',', "."))
                cur_to = context.args[2].upper()
            elif len(context.args) == 4:
                amount = float(context.args[0].replace('$', '').replace(',', "."))
                cur_from = context.args[1].upper()
                cur_to = context.args[3].upper()
            else:
                raise Exception("Can't recognize arguments.")
            answer = '{:9.2f}'.format(rates.exchange(amount, cur_from, cur_to)) + f" {cur_to}"
        except Exception as e:
            answer = "Error in parsing parameters"
        context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
        return answer
    exchange_handler = CommandHandler('exchange', exchange)
    dispatcher.add_handler(exchange_handler)


# /history {FROM}}/{TO} for 7 days
    def history(update, context):
        if len(context.args) == 1:
            cur_from, cur_to = context.args[0].split('/')
            buf = rates.hist(cur_from.upper(), cur_to.upper())
            if buf:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=buf)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="No exchange rate data is available for the selected currency")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Wrong arguments")

    history_handler = CommandHandler('history', history)
    dispatcher.add_handler(history_handler)


# /help
    def help(update, context):
        help_text = """
        This is demo of simple exchange rates bot. 
        Available commands:
        /start - start bot
        /help - show this message
        /list or /lst - show all actual exhange rates
        /history USD/CAD - show history for currency pair (replace USD or CAD to any available symbol)
        /exchange 10 USD to CAD or /exchange $10 to CAD - calculate 10 USD in CADs (replace USD or CAD to any available symbol)
        """
        context.bot.send_message(chat_id=update.effective_chat.id, text=help_text)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)


    # Simple answer to anything...
    def echo(update, context):
        help(update, context)

    echo_handler = MessageHandler(Filters.text, echo)
    dispatcher.add_handler(echo_handler)


    updater.start_polling()



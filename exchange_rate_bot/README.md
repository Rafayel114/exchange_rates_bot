Small exchange rate telegram bot
=====================

Installation (For debian based linux systems)
-----------------------------------
1. Download sources files: `git clone https://github.com/DrDeepDreamer/exchange_bot.git` - it will create folder `exchange_bot/`
2. CD into exchange_bot folder
`cd exchange_bot/`
3. Check your python version:
`python3 -V`
It should be 3.7 or higher
4.  Create virtual environment:
`python3 -m venv env`
5. Activate vertual environment:
`source env/bin/activate`
6. Install prerequisites (libraries needed for bot):
`pip install matplotlib python-telegram-bot`
7. Run bot: 
`python3 exchange_bot.py`

Usage notes
-----------------------------------
Telegram is blocked by Russian goverment, so to bypass blocking we use free anonymous proxy server outside of Russia.
But is not needed if you Run bot via VPN or on non-Russia servers.

If you need proxy - check it address in `config.py`

If you do not need proxy - just comment line `proxy_url` in `config.py`


To find it in Telegram: type `@simple_exchange_bot` in search

Implementation Features
-----------------------------------
1. The SQL database (sqlite3) is used as a data storage. For caching purposes like in this app it is not the best solution. It would be possible to use Redis with expiring keys. However, in case we want to develop this application to store historical data for graphs - it is the right way. 
2. Since this software was created for demonstration purposes, there are some shortcomings in the implementation, for example, accessing the SQL file database from different threads. That shouldn't be used in production environments.

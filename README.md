# EvEMarketBot
A Discord Bot for EvE Online Markets

To use this, you'll need to have your own discord bot API token, stored as an environment variable as TOKEN, you can change that as you wish

The bot can query Jita, Perimeter, Amarr, Dodixie, Hek and Rens market systems, as well the 1DQ1-A Market

using commands such as !jita <item> or !perimeter <item> will give market for <item> at those systems
the bot can also compare prices between two systems, allowing for easy market arbitrage using the commans !compare <system1> <system2> <item>
the command !margin <item> can also be used for a direct price comparison, buying in Jita and Selling in 1DQ1-A, a useful tool for members of the GSF

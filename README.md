# Telegram-bot Miki
Bot for assistance in trading and resale of NFT token's

## Libraries
- Requests
  - pip install requests
  - https://github.com/psf/requests
- Pandas
  - pip install pandas
  - https://github.com/pandas-dev/pandas
- Datetime
  - pip install DateTime
  - https://github.com/zopefoundation/DateTime
- BeautifulSoup
  - pip install beautifulsoup4
  - https://www.crummy.com/software/BeautifulSoup/
- Telebot
  - pip install pyTelegramBotAPI
  - https://github.com/eternnoir/pyTelegramBotAPI
 
 ## Config file *config.py*
 ```python
    TOKEN    = '' # Bot token from @BotFather
    DISTOKEN = '' # Discord token (not used)
    
    HEADERS  = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}

    ETHDROPURL = 'https://nextdrop.is/upcoming?chain=ethereum' # Website with information about drops (Ethereum)
    SOLDROPURL = 'https://nextdrop.is/upcoming?chain=solana'   # Website with information about drops (Solana)

    SOLDROPDATA = 'data/solDropData.csv' #A file with the data obtained when parsing Solana drops
    ETHDROPDATA = 'data/ethDropData.csv' #A file with the data obtained when parsing Ethereum drops
 ```

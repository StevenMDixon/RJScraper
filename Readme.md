# Retro Junk Scraper

These scripts are used to download mp4 files from the retrojunk website

## Prerequisites:
1. python

## Installation:
1. Download this repo
    - Clone this repo `git clone https://github.com/StevenMDixon/RJScraper.git`
    - or Download as zip `https://github.com/StevenMDixon/RJScraper/archive/refs/heads/master.zip`
2. unzip the file and navigate to the root 
3. run `pip install -r requirements.txt`

## Steps:
1. update config.json to set your query params
    - categoryId (0 All, 1 Toys, 2 VideoGames, 3 Clothing, 4 Snacks/Food, 5 Fastfood, 6 Cereal, 7 Other, 8 PSA, 9 Promos, 10 Cars, 11 Bumpers)
    - [query, decade, cat] cannot be combined with other settings, they are only for querying. decade example: 1990
2. run `py puller.py`
    - This will generate 2 files (A links file for yt-dlp and mapping file for the renamer)
3. run `./yt-dlp -a "outfiles/OutputLinks.txt" -P "./downloads"`
    - This will start the process of downloading all of the files
    - yt-dlp downloads files and names them from the title of the link example: https://s3.stablecube.com/commercial-videos/zY6WdZdY3s2SPTOk9fDx3.mp4 becomes zY6WdZdY3s2SPTOk9fDx3 [zY6WdZdY3s2SPTOk9fDx3].mp4
4. run `py renamer.py`
    - This will rename the files to their original titles
5. Enjoy!
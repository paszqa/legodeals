# Summary

The scripts need to be run in order, they take the auctions listings as the input and output an IFTTT phone notification.

# 1. getoffers.py
 - RPi3 execution time: **< 30s** 
 - scrapes auctions listing at "https://allegrolokalnie.pl/oferty/klocki/lego-17865" for lines containing valuable data and saves it to **allegro.csv**
 - needs to have a correct **path** configured *(can be changed to script path getter later)*
	
# 2. scan.py
- RPi3 execution time: **15-25 min** 
- runs chrome webdriver and launches a headless browser, because the side uses JS to render objects
- takes **allegro.csv** and reads it line by line - it gets auction name, set ID, auction type, and the price
- searches *BrickLink* site for each set with found IDs
- uses Selenium to find wanted elements - price for a used set & price for a new set
- searches *ZKlockow.pl* site for each set with found IDs
- standard search finds the price in the HTML
- calculates ratio for each found price
- prints & saves all valuable data as **resultsDATE_TIME.csv**
- it counts and displays execution time for each stage

# 3. format.py
- RPi execution time: **< 30s** 
- takes the newest **resultsDATE_TIME.csv** file from the configured **path**
- reads the data and saves it in a human-readable format, as **formatted.csv**

# 4. notification.py
- RPi execution time: < 1 min
- reads **formatted.csv** and for each line it sends a webhook to IFTTT, with color-coded icons according to ratio of each deal
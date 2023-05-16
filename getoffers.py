import requests

#############
# CONFIG
#############
url = "https://allegrolokalnie.pl/oferty/klocki/lego-17865"
path = "/home/pi/legodeals/" #### <--- Needs to be configured
f = open(path+"allegro.csv", "w") # Don't touch unless you change it in all other scripts

#############
# MAGIC
#############

response = requests.get(url)
response.raise_for_status()

lines = response.text.split("\n")

for line in lines:
    if "itemOffered" in line:
        offerName = line.replace('<h3 class="mlc-itembox__title" itemprop="itemOffered">','').replace('</h3>','').replace(";","").replace("  "," ").replace("  "," ").replace("  "," ").replace("  "," ")
        setNumber = 0
        words = offerName.split(" ")
        for word in words: #Get set ID, but only if it falls between 1000 and 1970, as well as higher than 2026, to avoid using production year or count of sets for sale
            if word.isnumeric():
                if (((int(word) > 1000) and (int(word) < 1970)) or (int(word) > 2026)):
                    setNumber = word
        output = offerName + ";" + str(setNumber)
        print(output,end=';')
        f.write(output + ";")
    elif "mlc-itembox__offer-type" in line or '<span class="mlc-itembox__offer-type mlc-itembox__offer-type--bidding">' in line: # Get type of the offer - 'Buy Now' or 'Auction'
        type = line.replace('<span class="mlc-itembox__offer-type mlc-itembox__offer-type--buy_now">','').replace('<span class="mlc-itembox__offer-type mlc-itembox__offer-type--bidding">','').replace("</span>","").replace(" ","")
        print(type, "" , end=';')
        f.write(str(type) + ";")
    elif "ml-offer-price__dollars" in line: # Get price
        price = line.replace('<span class="ml-offer-price__dollars">','').replace("</span>","").replace(" ","")
        print(price)
        f.write(str(price) + "\n")
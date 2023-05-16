import os
import glob

# Find the newest CSV file starting with "results"
path = "/home/pi/legodeals/"
newest_csv = max(glob.glob(path+'results*.csv'), key=os.path.getctime)
formatted_csv = open(path+"formatted.csv", "w")
# Open the file and print its contents line by line
i = 0
with open(newest_csv, 'r') as file:
    for line in file:
        if i == 0:
            i = i+1
            continue
        elements = line.strip().split(";")
        name = elements[0]
        type = elements[3]
        price = elements[4]
        new_price = elements[6]
        new_ratio = elements[7]
        used_price = elements[9]
        used_ratio = elements[10]
        zklockow_price = elements[11]
        if len(elements) > 12:
            zklockow_ratio = elements[12]
        if zklockow_price == "9999":
            zklockow_price = "X"
        #Calculate best ratio from stores
        lowest_ratio = 99
        if new_ratio != "-":
            if float(new_ratio) < lowest_ratio:
                lowest_ratio = float(new_ratio)
        if used_ratio != "-":
            if float(used_ratio) < lowest_ratio:
                lowest_ratio = float(used_ratio)
        if zklockow_price != "X" and zklockow_price != "-":
            if float(zklockow_price) < lowest_ratio:
                lowest_ratio = float(zklockow_price)
        offer_line = ""+ name + "; Cena "+ price + " ("+type+")" +" [New:"+new_price+", Used:"+used_price+", zKlo:"+zklockow_price+"];"+str(lowest_ratio)
        formatted_csv.write(offer_line+"\n")
        print(offer_line)
        
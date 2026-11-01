for url in "atms-kiosks" "coffee-service" "contactless" "foodservice" "micromarkets" "music-games" "payment-technology" "gadgets" "vending" "metaverse"
do
    python ./vendingtimes.py -u ${url} -s csv
done
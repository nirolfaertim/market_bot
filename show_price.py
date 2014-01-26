from urllib import urlencode
import json
import market

items = json.load(open("items.json"))

item_names = {i["name"].lower() for i in items.itervalues()}

while True:
	item = raw_input("Item: ")
	if item.lower() in item_names:
		item = [i for i in items.itervalues() if i["name"].lower() == item.lower()][0]
		print "torishop = {price}tc - {qi}qi".format(**item)
		market_items = market.search(item["name"], 99999999999)
		if market_items:
			market_item = sorted(market_items, key=lambda i: i["item_price"])[0]
			print "market   = {item_price}tc\t".format(**market_item)
		else:
			print "This item is not in the market"
	else:
		print '"%s" not found' % item 
	#items_response = market.get()
	#items = json.load(items_response)
	#print items
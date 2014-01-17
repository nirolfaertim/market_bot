import random
import threading
import time

import config
import market

def update_items():
	if not config.bump:
		return
	while True:
		try:
			print "Removing items"
			market_items = market.inventory(-2)
			for market_item in market_items:
				#print "Removing %s" % market_item["name"]
				market.remove_from_market(market_item["id"])

			deactivated_items = market.inventory()
			sorted_items = sorted(deactivated_items, key=lambda x: config.item_prices.get(x["name"], 0) + random.randint(1, 1000))
			print "Bumping items"
			for deactivated_item in sorted_items:
				#print deactivated_item["name"]
				price = config.item_prices.get(deactivated_item["name"])
				if price:
					#TODO: set price below other seller but not below our buy price
					#print "Selling %s for %i" % (deactivated_item["name"], price)
					market.sell(deactivated_item["id"], price)
			time.sleep(config.bump_time)
		except Exception as e:
			print e

def check_items():
	while True:
		for i in xrange(1, 6):
			try:
				while True:
					items = market.newest(i)
					break
				for item in items:
					#print item["name"]
					if item["name"].startswith("Set: "):
						set_items = market.inventory(item["inventid"], item["seller"])
						max_price = 0
						for set_item in set_items:
							max_price += config.buy_items.get(set_item["name"], config.auto_buy)
						if item["item_price"] <= max_price:
							print "buying %s for %i (max was %i)" % (item["name"], item["item_price"], max_price)
							market.buy(item)
					else:
						max_price = config.buy_items.get(item["name"], config.auto_buy)
						if item["item_price"] <= max_price:
							print "buying %s for %i" % (item["name"], item["item_price"])
							market.buy(item)
						else:
							pass
							#print "Found %s, but not in our price range (%i > %i)" % (item["name"], item["item_price"], max_price)
			except Exception as e:
				print e
		"""for item, value in config.buy_items.iteritems():
			try:
				search = market.search(item, value)
				buy = [i for i in search if i["item_price"] <= value]
				print "Checking %s for %i (found %i)" % (item, value, len(buy))
				for buy_item in buy:
					print "Buying %s for %i" % (item, buy_item["item_price"])
					market.buy(buy_item)
			except Exception as e:
				print e"""
		#time.sleep(300)

update_t = threading.Thread(target=update_items)
update_t.daemon = True
update_t.start()

check_t = threading.Thread(target=check_items)
check_t.daemon = True
check_t.start()

while True:
	try:
		print "tc: %s" % market.tc(config.username)
	except:
		pass
	time.sleep(config.show_tc_every)
	"""if last_item_update + update_items_every < time.time():
		last_item_update = time.time()



	if last_item_check + check_items_every < time.time():
		last_item_check = time.time()
		

	time.sleep(10)"""
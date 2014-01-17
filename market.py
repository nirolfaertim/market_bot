import bs4
from bs4 import BeautifulSoup
from cookielib import CookieJar
import json
from urllib import urlencode
import urllib2

import config

cj = CookieJar()
headers = {'User-agent': "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

BASE = "http://forum.toribash.com/"

def login():
	#'DKOlnJAcqUx=\n'.decode("rot13").decode("base64")
	form_data = {"username": config.username, "password": config.password, "submit": "Login"}
	req = opener.open(BASE + "tori.php", urlencode(form_data))
	response = req.read()

def get(url, *args):
	response = opener.open(BASE + url, *args, timeout=15).read()
	if "login.php" in response:
		login()
		return get(url)
	return response

def search(item, max_, page = 1, action="search"):
	items = []

	page = get("tori_market.php?%s" % urlencode({"action": action, "item": item, "max": max_, "page": page}))
	soup = BeautifulSoup(page)
	table = soup.find("table", class_="market_items")

	for item in table or []:
		try:
			if not isinstance(item, bs4.element.Tag):
				continue
			if not item.attrs.get("class"):
				continue

			name = item.find("td", attrs={"class": "market_item_name"}).a.text

			inventid   = int(item.find("input", attrs={"name": "inventid"}).attrs["value"])
			item_price = int(item.find("input", attrs={"name": "item_price"}).attrs["value"])
			seller     = int(item.find("input", attrs={"name": "seller"}).attrs["value"])

			#print inventid, item_price, seller

			items.append({
				"name":       name,

				"inventid":   inventid,
				"item_price": item_price,
				"seller":     seller,
			})
			if name.startswith("Set: "):
				items[-1]["item_set_checksum"] = item.find("input", attrs={"name": "item_set_checksum"}).attrs["value"]
		except:
			pass
	return items

def newest(page):
	return search("", "", page, "")

def buy(item):
	get("tori_market.php?action=buy_item", urlencode(item))

def inventory(sid=0, userid=None):
	#sid =  0 = deactivated
	#sid = -1 = activated
	#sid = -2 = market

	page = get("tori_inventory.php?%s" % urlencode({"sid": sid, "userid": userid} if userid else {"sid": sid}))
	soup = BeautifulSoup(page)
	items = []

	for item in soup.find_all("tr", class_=lambda s: s in ["market_active", ""]):
		id_ = int(item.find("input").attrs["value"])
		items.append({"id": id_, "name": item.span.text})

	return items

def sell(item_id, price):
	get("tori_item.php?%s" % urlencode({"invid": item_id, "action": "setprice"}), urlencode({"amount": price}))

def remove_from_market(item_id):
	get("tori_inventory.php?%s" % urlencode({"action": "sale", "do": "remove", "inv": item_id}))

def tc(username):
	r = urllib2.urlopen("http://forum.toribash.com/tori_stats.php?format=json&username=%s" % username)
	status = json.load(r)
	return status.get("tc", "0")
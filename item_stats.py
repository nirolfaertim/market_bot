from bs4 import BeautifulSoup
import re

import market

def get_items(min_=0, max_=2000):
	items = {}
	for i in xrange(min_, max_):
		try:
			page = market.get("tori_shop_item.php?id=" + str(i))
			soup = BeautifulSoup(page)
			name = soup.table.h1.text

			stock, qi, price, owned_by, total_items, total_circulation = map(
				lambda s: int(re.sub(r"[^\d]", "", s.string)),
				soup.table.find_all("tr")[5].find_all("td")
			)

			items[i] = {
				"name": name, "stock": stock, "qi": qi, "price": price,
				"owned_by": owned_by, "total_items": total_items,
				"total_circulation": total_circulation
			}
		except KeyboardInterrupt:
			return
		except:
			pass
		print i
	return items

if __name__ == "__main__":
	import json
	items = get_items()
	if items:
		open("items.json", "w").write(json.dumps(items))
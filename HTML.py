import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re
from PyQt5.QtWidgets import QFileDialog
if __name__ == 'main':
	from PyQt5.QtWidgets import QApplication

headers = {'Accept': '*/*', 
		'Connection': 'keep-alive', 
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36', 
		'Accept-Language': 'en-US;q=0.5,en;q=0.3', 
		'Referer': 'https://google.com'
		}

def saveName():
	temp = QFileDialog()
	return temp.getSaveFileName(temp, "", "", "Text files (*.html)")[0]


def importHTML(url, doAsk, defSave):

	url = url.lower()

	pre = "https://archiveofourown.org"

	test = "https://archiveofourown.org/works"

	post = "?view_adult=true"

	def findHTML(href):
		return href and re.compile("html").search(href)
		 # and not re.compile("azw3?").search(href) and not re.compile("epub?").search(href) and not re.compile("mobi?").search(href) and not re.compile("pdf?").search(href)

	def getID(href):
		return href and re.compile("works").search(href)

	def findAdButton(href):
		return href and re.compile("?view_adult=true").search(href)

	if(url.find(test) != -1):
		url = url + post
		req = requests.get(url, headers = headers)
		soup = BeautifulSoup(req.content, 'html.parser')

		test2 = soup.find(href=findHTML).get("href")
		title = soup.find("h2", class_="title heading").get_text()
		title = title.strip()
		author = soup.find("a", rel="author").get_text()
		fandom = soup.find("dd", class_="fandom tags")
		fandom = fandom.find_all("a", class_="tag")
		fanList = ""
		for x in fandom:
			fanList += x.get_text() + ", "
		fanList = fanList[0:-2]
		# print(fanList)
		# fandom = fandom.next_element
		# fandom = fandom.next_element
		
		deets = str(soup.find("head")) + str(soup.find("div", class_="wrapper", id = ""))

		ret = []

		complete_url = pre + test2

		if(doAsk):
			save = saveName()
		else:
			real = re.findall('[0-9]+', url)
		
			save = defSave + real[0] + " - " + re.sub('["/:*?<>|]', '', title).replace("\\", "") + " by " + re.sub('"[/:*?<>|]', '', author).replace("\\", "") + ".html"

		ret.append(save)
		ret.append(title + " by " + author)
		ret.append(deets)
		ret.append(str(fanList))
		# print(ret[3])
		if(save != ""):
			r = requests.get(complete_url, allow_redirects=True)

			open(save, 'wb').write(r.content)

			return ret
		else:
			return "False"
	else:
		return "False"

#https://archiveofourown.org/downloads/25865620/A%20World%20On%20Hold.html?updated_at=1597263062
# print(test2)

# importHTML("test")

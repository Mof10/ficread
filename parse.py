#Plan: end up with a list of lists:
# ind 0: Unused...?
# ind 1: Chapter title
# ind 2: Chapter contents
# ind 3: Chapter notes?

from bs4 import BeautifulSoup
import re
import codecs
import requests
import os.path
from os import path
import PIL.Image

def wordCount(para):
	count = 0
	for x in para:
		if x == ' ':
			count += 1
	return count

def addWords(lis, wholeChap):
	tempC = 0
	tempst = ""
	for x in range(0, len(wholeChap)):

		par = str(wholeChap[x])
		# print(par)
		tempst += par
		tempC += wordCount(par)
		if(((tempC > 50) or (x == len(wholeChap) - 1))):
			lis.append(tempst)
			tempC = 0
			tempst = ""

def getFirNote(soup):
	test = soup.find("p", text="Notes", class_='')
	if(test != None):
		return test.next_element.next_element.next_element
	else:
		return ""

def endnotes(id):
	return id and re.compile("endnotes").search(id)

def noImg(tag):
	return tag.has_attr('class') and not tag.has_attr('img')

def isInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def imageCheck(text, savePath, height, width):
	for x in text:
		img = x.find_all("img")
		for y in img:
			send = y.get("src")
			imgName = send.split("/")[-1]
			if not (os.path.exists(savePath + imgName)):
				image = requests.get(send)			
				f = open(savePath + imgName, 'wb')
				print(savePath + imgName)
				f.write(image.content)
				f.close()
			# print(savePath + imgName)
			#Change to deal with if the width and height were predefined by a number, otherwise do this funky stuff
			y['src'] = savePath + imgName

			#Set the image size, because auto doesn't work for whatever reason
			getSizes = PIL.Image.open(savePath + imgName)
			pwidth, pheight = getSizes.size
			ratio = pwidth / pheight
			if(isInt(y['width'])):
				y['width'] = int(y['width'])
				y['height'] = int(int(y['width']) / ratio)
			else: #Width = something like auto, or 80%. 
				y['width'] = int(width - 75)
				y['height'] = int((width - 75) / ratio)

#Parse the chapters
def getChaps(chapters, filepath, imgsave, height, width):
	#I hate this big block, will probably fix sometime
	file = BeautifulSoup(codecs.open(filepath, 'r', 'utf-8'), "html.parser")
	titles = file.find_all("h2", class_="heading")
	chapTitles = []
	for x in titles:
		chapTitles.append(str(x.get_text()))
	title = file.find("p", class_="message")
	title = title.find("b").get_text()
	first = file.find("blockquote", class_="userstuff")
	first_n = getFirNote(file)
	author = file.find("div", class_='byline', id='')
	#The chapter notes before each chapter
	preNotes = file.find_all("div", class_="meta group", id="")
	endNotes = file.find_all("div", id = endnotes)
	text = file.find_all("div", class_="userstuff", id="")
	imageCheck(text, imgsave, height, width)

	temp = []
	chapterCon = []

	def addFirsts():
		firsts = str(first)
		if(str(first_n) != ""):
		 	firsts += "<p>Author Notes:</p>" + str(first_n)
		chapters[0][2].insert(0, "<h1>" + title + "</h1>" + str(author) + "<p>Work Summary:</p>" + firsts)		

	if(len(chapTitles) > 0):
		for x in range(0, len(titles)):
			temp.clear()
			chapterCon.clear()
			temp = text[x].find_all('p')
			toIns = []
			addWords(toIns, temp)
			chapterCon = [x, chapTitles[x], list(toIns)]
			chapters.append(list(chapterCon))
		for y in endNotes:
			num = re.findall('[0-9]+', y['id'])
			if (len(num) > 0):
				chapters[int(num[0]) - 1][2].append(str(y))
			else: #There is no endnote ID, so it's the final chapter one
				chapters[-1][2].append(str(y))
		for y in range(0, len(preNotes)):
			chapters[y][2][0] = str(preNotes[y]) + "<hr style=\"border:20px solid black;\" />" + chapters[y][2][0]
		addFirsts()

		
	if(len(chapTitles) == 0):
		temp.clear()
		chapterCon.clear()
		temp = text[0].find_all("p")
		toIns = []
		addWords(toIns, temp)
		chapterCon = [0, str(title), list(toIns)]
		chapters.append(list(chapterCon))
		if(len(endNotes) > 0):
			chapters[0][2].append(str(endNotes[0]))
		addFirsts()

if __name__ == "__main__":
	name = "C:\\Users\\Tomoya\\Desktop\\testhtml\\Nine tails of Lust.html"
	temp = []
	getChaps(temp, name)
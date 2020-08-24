
import re
def match(letter, chars):
	for x in chars:
		if letter == x:
			return True
	return False

def rem(text):
	illegalchars = ['\\', '/', ':', '*', '?', '<', '>', '|']
	return re.sub('[/:*?<>|]', '', text).replace("\\", "")
	# return text



title = input()

print(title)

print(rem(title))

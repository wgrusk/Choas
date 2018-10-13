# scraper.py - take jsons and convert into a list of usable comments.
import json
import sys

def main():
	if len(sys.argv) < 2:
		print("give a json as the first argument")
		return
	f = sys.argv[1]
	out = f + ".out.txt"
	if len(sys.argv) == 3:
		out = sys.argv[2]
		print("out:", out)

	print("opening file")
	file = open(f,"r")
	outfile = open(out, "w")
	print("loading", f)
	data = json.load(file)
	file.close()
	comments = 0;
	words = 0
	wordlist = createDict()
	for comment in data:
			if "commentText" in comment:
				line = strip_non_ascii(comment["commentText"])
				line = line.strip('\n')
				line = line.strip('\t')
				line = strip_special(line)
				line = line.lower()
				#print(line.split())
				outstring = ""
				for word in line.split():
					#print("word is", word)
					if word in wordlist :
						#print(word,"is in the list")

						outstring += word + " "
				print("outstring is",outstring)
				if not outstring == "":
					outfile.write(line)
					outfile.write('\n')
					comments += 1
					words += len(line.split())
						
			else :
				continue
	#print(wordlist)
	print("comments recovered:", comments)
	print("average length of comments", words/comments)
	outfile.close()
	sys.exit(comments)

def createDict():
	dic = {}
	FILE = open("outfile.txt", "r")

	for key in FILE:
		dic[key.strip('\n')] = 1

	return dic

# From https://stackoverflow.com/questions/2743070/remove-non-ascii-characters-from-a-string-using-python-django/2743163#2743163

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)

def strip_special(string):
	finalStr = ""
	for c in string:
		if c == ' ' :
			finalStr += " "
		elif not c.isalnum():
			continue
		else :
			finalStr += c
	return finalStr

if __name__ == "__main__":
	main()
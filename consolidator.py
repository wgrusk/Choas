from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir("./data") if isfile(join("./data", f))]
words = {}
for file in onlyfiles:
	if ".txt" in file and "master" not in file and "-stripped" in file:
		fOpen = open("./data/%s"%file, "r")
		print("file", file)
		for line in fOpen:
			print(fOpen)
			line = line.lower()
			for word in line.split():
				if word in words:
					words[word] += 1
				else:
					words[word] = 1

initialwords = len(words)

for key in list(words):
	if words[key] < 10:
		del words[key]

outfile = open("outfile.txt", "w")
for key in words:
	outfile.write(key)
	outfile.write('\n')
outfile.close()

print(initialwords, "unique words found")
print(len(words), "unique words after processing")
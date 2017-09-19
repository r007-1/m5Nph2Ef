import json
import csv
import sys

#python -c 'from manage import fix; fix("sb
#jq '. | length' products/
#sudo du -sh products/

#Shoptiques
##B8: 11:14AM
def resume(name):
	name = str(name)
	input = 'products/' + name + '.json'
	with open(input) as data_file:
		f = file.read(data_file)
		f = f.replace("}[{", "},{")
		data_file.close()

	with open('./flyyy/spiders/shoptiques-done.csv', 'rb') as f:
		reader = csv.reader(f)
		try:
			done = list(reader)[0]
		except Exception as e:
			done = []
			print "blank"
	with open('products/' + name + '.json') as data_file:
		data = json.load(data_file)
	pids = done
	for i in range(0, len(data)):
		pids.append(data[i]['prod_id'])
	fname = 'flyyy/spiders/' + name + '-done.csv'
	os.remove(fname)
	myfile = open(fname, 'wb')
	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	wr.writerow(pids)
	print(len(pids))
	os.remove(input)
	with open('products/' + name + '.json', 'w+') as outfile:
		json.dump(f, outfile)
	return "done"

def fix(name):
	print(name)
	input = 'products/' + name + '.json'
	with open(input) as data_file:
	f = file.read(data_file)
for i in range(0, len(f)):
	pointer = -1*(i + 1)
	if f[pointer] == "{":
		f = f[:pointer - 2] ## remove ',\n' before "{'
		f += "]"
		break
			#f = f.replace("}[{", "},{")
		data_file.close()
	j = json.loads(f)
	name = name + '-edited'
	with open('products/' + name + '.json', 'w+') as outfile:
		json.dump(j, outfile)
	return "done"
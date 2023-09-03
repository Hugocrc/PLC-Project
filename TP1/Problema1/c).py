import re


def freq_by_relationship(file):
	
	dic_by_relation = {}
	for line in file:
		slices = re.split(r'::', line)
		if len(slices) > 1:
			match = re.search(r'([A-Z][a-z]+|\s)+(,+([A-Z][a-z]+\s*)+\.+)+', slices[5])
			if match:
				relationship = match.group(2)
				relationship = relationship.lstrip(",")
				relationship = relationship.rstrip(".")
				
				if relationship not in dic_by_relation.keys():
					dic_by_relation[relationship] = 0

				dic_by_relation[relationship] += 1

	return dic_by_relation


file = open("processos.txt", "r")
dic = freq_by_relationship(file)

for relationship in dic.keys():
	print(relationship + ": " + str(dic[relationship]))
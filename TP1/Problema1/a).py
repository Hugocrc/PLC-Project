import re

#(a) frequência de processos por ano

def freq_by_years(file):
    dic_by_years = {}

    for line in file:
        #slices contém a linha particionada por "::" ou "-"
        slices = re.split(r'[::-]', line)
        if len(slices) > 1:
            #slices[2] contém o ano
            if slices[2] not in dic_by_years.keys():
                dic_by_years[slices[2]] = 0

            dic_by_years[slices[2]] += 1

    return dic_by_years


file = open("processos.txt", "r")
dic = freq_by_years(file)

for key in sorted(dic.keys()):
	print(key + ": " + str(dic[key]))
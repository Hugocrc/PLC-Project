import re
import math


def getFirstName(person, dic, century):
    firstName = re.split(r'\s+', person)
    if re.fullmatch(r'[A-Z][a-z]+', firstName[0]):
        if firstName[0] != '':
            if firstName[0] not in dic[century].keys():
                dic[century][firstName[0]] = 0
            dic[century][firstName[0]] += 1

    return 0


def getLastName(person, dic, century):
    lastName = re.split(r'\s+\n+', person)
    if re.fullmatch(r'[A-Z][a-z]+', lastName[-1]):
        if lastName[-1] != '':
            if lastName[-1] not in dic[century].keys():
                dic[century][lastName[-1]] = 0
            dic[century][lastName[-1]] += 1

    return 0


def freq_by_centuries(file):

    dic_by_centuries = {}
    for line in file:
        #lista que contém a linha particionada pelo padrão do split
        slices = re.split(r'::|,|\.', line)
        #este if serve apenas para ignorar linhas que estejam "inválidas"
        if len(slices) >= 2:
            #este split particiona a data
            date = re.split(r'-', slices[1])
            century = math.ceil(int(date[0])/100)
            if century not in dic_by_centuries.keys():
                dic_by_centuries[century] = {}
            
            #nas posições 3 e 4 de slices encontram-se os nomes que queremos manipular
            dad = slices[3]
            mom = slices[4]
            getFirstName(dad, dic_by_centuries, century)
            getLastName(dad, dic_by_centuries, century)
            getFirstName(mom, dic_by_centuries, century)
            getLastName(mom, dic_by_centuries, century)

    return dic_by_centuries


file = open("processos.txt", "r")
dic = freq_by_centuries(file)

for century in sorted(dic.keys()):
    print("Século: " + str(century))
    
    for name in dic[century].keys():
        print(name + ": " + str(dic[century][name]))
    
    print("\n")






import re


def distribuicao_genero():
    dic = {}

    with open("emd.csv", 'r') as myfile:
    	next(myfile)
    	for line in myfile:
	        slices = re.split(r',',line)
	        
	        for elem in slices:
	        	if re.fullmatch(r'[A-Z]', elem):
	        		genero = elem
	        		break

	        if genero not in dic.keys():
	            dic[genero] = 0
	        dic[genero] += 1

    return dic


def distribuicao_idade():
	dic = {}
	dic["< 35"] = 0
	dic[">= 35"] = 0
	with open("emd.csv", 'r') as myfile:
		next(myfile)
		for line in myfile:
			slices = re.split(r',', line)
			idade = slices[5]

			if int(idade) < 35:
				dic["< 35"] += 1
			else:
				dic[">= 35"] += 1

	return dic


def registos_por_idade_genero():
	lista = []

	with open("emd.csv", 'r') as file:
		next(file)

		for line in file:
			slices = re.split(r',', line)
			nome = slices[3] + " " + slices[4]
			genero = slices[6]
			idade = slices[5]

			lista.append((nome, genero, idade))

	lista.sort(key = lambda x: x[0])
	lista.sort(key = lambda x: x[2])
	lista.sort(key = lambda x: x[1])

	return lista


#dic_genero = distribuicao_genero()
#dic_idade = distribuicao_idade()
#print(dic_idade)
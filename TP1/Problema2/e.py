import re


def percentagem_aptos_naptos():
	dic_aux = {}
	dic = {}

	with open("emd.csv", 'r') as myfile:
		next(myfile)

		for line in myfile:
			slices = re.split(r',', line)
			data = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', line)
			if data:
				ano = re.search(r'[0-9]{4}', data.group())
				ano = ano.group()
			
			matchT = re.search(r'true', slices[12])
			matchF = re.search(r'false', slices[12])

			if ano not in dic_aux.keys():
				dic_aux[ano] = {}
				dic_aux[ano]["aptos"] = 0
				dic_aux[ano]["inaptos"] = 0

			if matchT:
				dic_aux[ano]["aptos"] += 1

			if matchF:
				dic_aux[ano]["inaptos"] += 1


	for ano in dic_aux.keys():
		if ano not in dic.keys():
			dic[ano] = {}
			dic[ano]["aptos"] = 0
			dic[ano]["inaptos"] = 0

		dic[ano]["aptos"] = round(dic_aux[ano]["aptos"] / (dic_aux[ano]["aptos"] + dic_aux[ano]["inaptos"]) * 100, 2)
		dic[ano]["inaptos"] = round(dic_aux[ano]["inaptos"] / (dic_aux[ano]["aptos"] + dic_aux[ano]["inaptos"]) * 100, 2)

	return dic


def registos_aptos_naptos():
	dic = {}

	with open("emd.csv", 'r') as file:
		next(file)

		for line in file:
			match = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', line)
			if match:
				ano = re.match(r'[0-9]{4}', match.group()).group()

			if ano not in dic.keys():
				dic[ano] = []

			slices = re.split(r',', line)
			nome = slices[3] + " " + slices[4]
			modalidade = slices[8]
			
			if re.match(r'(?i:true)', slices[12]):
				dic[ano].append((nome, modalidade, "Apto"))
			elif re.match(r'(?i:false)', slices[12]):
				dic[ano].append((nome, modalidade, "Não Apto"))

	for ano in dic.keys():
		dic[ano].sort(key = lambda x: x[0])
		dic[ano].sort(key = lambda x: x[2])

	return dic


#dic = percetagem_aptos_naptos()
#print(dic)
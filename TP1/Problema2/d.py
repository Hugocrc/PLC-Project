import re


def distribuicao_morada():
	dic = {}

	with open("emd.csv", 'r') as myfile:
		next(myfile)

		for line in myfile:
			slices = re.split(r',', line)
			morada = slices[7]

			if morada not in dic.keys():
				dic[morada] = 0
			dic[morada] += 1

	return dic


def lista_moradas():
	moradas = []

	with open("emd.csv", 'r') as myfile:
		next(myfile)

		for line in myfile:
			slices = re.split(r',', line)
			morada = slices[7]
			if morada not in moradas:
				moradas.append(morada)

	moradas.sort()

	return moradas


def atletas_por_morada(morada):

	with open("emd.csv", 'r') as file:
		next(file)

		string = ""
		for line in file:
			slices = re.split(r',', line)
			if slices[7] == morada:
				string += "(" + slices[3] + " " + slices[4] + ", " + slices[8] + "); "

	return string


#dic_morada = distribuicao_morada()
#print(dic_morada)
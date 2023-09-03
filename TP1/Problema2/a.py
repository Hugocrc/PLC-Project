import re


def data_max(datas):
	ano_max = max(datas, key = lambda x: x[0])
	datas = filter(lambda x: x[0] == ano_max[0], datas)
	datas = list(datas)
	
	mes_max = max(datas, key = lambda x: x[1])
	datas = filter(lambda x: x[1] == mes_max[1], datas)
	datas = list(datas)

	dia_max = max(datas, key = lambda x: x[2])
	datas = filter(lambda x: x[2] == dia_max[2], datas)
	datas = list(datas)

	return datas[0]


def data_min(datas):
	ano_max = min(datas, key = lambda x: x[0])
	datas = filter(lambda x: x[0] == ano_max[0], datas)
	datas = list(datas)
	
	mes_max = min(datas, key = lambda x: x[1])
	datas = filter(lambda x: x[1] == mes_max[1], datas)
	datas = list(datas)

	dia_max = min(datas, key = lambda x: x[2])
	datas = filter(lambda x: x[2] == dia_max[2], datas)
	datas = list(datas)

	return datas[0]


def datas_extremas():
	datas = []

	with open("emd.csv", "r") as file:
		for line in file:
			match = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', line)

			if match:
				slices = re.split(r'-', match.group())
				data = (int(slices[0]), int(slices[1]), int(slices[2]))
				datas.append(data)

		data_mais_recente = data_max(datas)
		data_mais_antiga = data_min(datas)	

		dic = {}
		dic["data_mais_antiga"] = data_mais_antiga
		dic["data_mais_recente"] = data_mais_recente

		return dic


def ordena_datas_crescente(datas):

	datas.sort(key = lambda x: x[2])
	datas.sort(key = lambda x: x[1])
	datas.sort(key = lambda x: x[0])


def lista_datas():
	datas = []

	with open("emd.csv", 'r') as file:
		for line in file:
			match = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', line)

			if match:
				slices = re.split(r'-', match.group())
				data = (int(slices[0]), int(slices[1]), int(slices[2]))
				datas.append(data)

	ordena_datas_crescente(datas)

	return datas

import a
import b
import c
import d
import e
import json
import re


def list_to_string(x):
	string = "<p>"

	for elem in x:
		string += elem + "; "
	string += """</p><br></br>"""

	return string


def generate_pagina_indicador(char):
	with open("pagina_indicador_"+char+".html", "w") as file:
		content = ""

		if char == 'a':
			content ="""<!DOCTYPE html>
						<html>
						<h1>Página do indicador</h1>
						<body>
						<li><a href="index.html">Página principal</a></li>
						-datas-
						</body>
						</html>"""

			string = "<h3>Datas existentes nos registos (ordenadas por ordem crescente):</h3>"
			datas = a.lista_datas()
			
			for data in datas:
				string += "<p>" + str(data[0]) + "-" + str(data[1]) + "-" + str(data[2]) + "</p>"

			content = re.sub(r'-datas-', string, content)

		elif char == 'b':
			content ="""<!DOCTYPE html>
						<html>
						<h1>Página do indicador</h1>
						<body>
						<li><a href="index.html">Página principal</a></li>
						-modalidade-
						</body>
						</html>"""

			dic = b.lista_anos_modalidades()
			string = "<h3>Atletas de cada modalidade ordenados por ano:</h3>"

			for ano in sorted(dic.keys()):
				string += "<p>" + ano + "</p><br>"
				for modalidade in sorted(dic[ano].keys()):
					string += "<p>" + modalidade + ": {"
					for atleta in sorted(dic[ano][modalidade]):
						string += atleta  + "; "
					string += "}</p>"
				string += "<br></br>"

			content = re.sub(r'-modalidade-', string, content)


		elif char == 'c':
			content ="""<!DOCTYPE html>
						<html>
						<h1>Página do indicador</h1>
						<body>
						<li><a href="index.html">Página principal</a></li>
						-info-
						</body>
						</html>"""

			info = c.registos_por_idade_genero()
			string = "<h3>Registos dos atletas ordenados por idade e por género:</h3><br>"

			for elem in info:
				string += "<p>Nome: " + elem[0] + "; Género: " + elem[1] + "; Idade: " + elem[2] + ";</p>"

			content = re.sub(r'-info-', string, content)

		elif char == 'd':
			content ="""<!DOCTYPE html>
						<html>
						<h1>Página do indicador</h1>
						<body>
						<li><a href="index.html">Página principal</a></li>
						-moradas-
						</body>
						</html>"""

			string = """<h3>Moradas existentes e respetivos moradores (nome, modalidade que pratica):</h3>"""
			moradas = d.lista_moradas()

			for morada in moradas:
				string += "<p>" + morada + ": " + d.atletas_por_morada(morada) + "</p>"
				string += "<br>"

			content = re.sub(r'-moradas-', string, content)


		elif char == 'e':
			content ="""<!DOCTYPE html>
						<html>
						<h1>Página do indicador</h1>
						<body>
						<li><a href="index.html">Página principal</a></li>
						-info-
						</body>
						</html>"""

			string = "<h3>Registos de aptos e não aptos por ano:</h3><br>"
			dic = e.registos_aptos_naptos()

			for ano in sorted(dic.keys()):
				string += "<p>" + ano + "</p>"
				for elem in dic[ano]:
					string += "<p>Nome: " + elem[0] + "; " + "Modalidade: " + elem[1] + "; " + elem[2] + ";</p>"
				string += "<br></br>"

			content = re.sub(r'-info-', string, content)

		file.write(content)


def html_a():
	generate_pagina_indicador("a")

	content = """<h3>A - Datas extremas:</h3>
				<li><a href="pagina_indicador_a.html">Página do Indicador</a></li>
				<p>datas</p>
				<br></br>"""
	dic = a.datas_extremas()
	string = "<p>"

	for key in dic.keys():
		if key == "data_mais_antiga":
			string += "<p>Data mais antiga: " + str(dic[key][0]) + "-" + str(dic[key][1]) + "-" + str(dic[key][2]) + "</p>"
		elif key == "data_mais_recente":
			string += "<p>Data mais recente: " + str(dic[key][0]) + "-" + str(dic[key][1]) + "-" + str(dic[key][2]) + "</p>"

	content = re.sub(r'datas', string, content)

	return content


def html_b():
	generate_pagina_indicador("b")

	content = """<h3>B - Distribuição por modalidade em cada ano e no total:</h3>
				<li><a href="pagina_indicador_b.html">Página do Indicador</a></li>
				<p>-ano-</p>
				<p>-total-</p>
				<br></br>"""

	dic_por_ano = b.distribuicao_modalidade_ano()
	dic_total = b.distribuicao_modalidade_total()
	

	dic_por_ano_str = ""
	for ano in sorted(dic_por_ano.keys()):
		dic_por_ano_str += str(ano) + ":<br>"
		for modalidade in sorted(dic_por_ano[ano].keys()):
			dic_por_ano_str += modalidade + ": " + str(dic_por_ano[ano][modalidade]) + "; "
		dic_por_ano_str += "<br></br>"

	dic_total_str = "Total:<br>"
	for modalidade in sorted(dic_total.keys()):
		dic_total_str += modalidade + ": " + str(dic_total[modalidade]) + "; "

	content = re.sub(r'-ano-', dic_por_ano_str, content)
	content = re.sub(r'-total-', dic_total_str, content)

	return content


def html_c():
	generate_pagina_indicador("c")

	content = """<h3>C - Distribuição por idade e género (para a idade, considera apenas 2 escalões: < 35 anos e >= 35):</h3>
				<li><a href="pagina_indicador_c.html">Página do Indicador</a></li>
				-info-
				<br></br>"""

	dic_genero = c.distribuicao_genero()
	dic_idade = c.distribuicao_idade()

	string = ""
	for key in dic_genero.keys():
		string += "<p>" + key + ": " + str(dic_genero[key]) + "</p>"

	for key in dic_idade.keys():
		string += "<p>" + key + ": " + str(dic_idade[key]) + "</p>"

	content = re.sub(r'-info-', string, content)

	return content


def html_d():
	generate_pagina_indicador("d")

	content = """<h3>D - Distribuição por morada:</h3>
				<li><a href="pagina_indicador_d.html">Página do Indicador</a></li>
				-info-
				<br></br>"""

	dic_morada = d.distribuicao_morada()

	string = "<p>"
	for morada in sorted(dic_morada.keys()):
		string += morada + ": " + str(dic_morada[morada]) + "; "
	string += "</p>"

	content = re.sub(r'-info-', string, content)

	return content


def html_e():
	generate_pagina_indicador("e")

	content = """<h3>E - Percentagem de aptos e não aptos por ano:</h3>
				<li><a href="pagina_indicador_e.html">Página do Indicador</a></li>
				-info-
				<br></br>"""

	dic = e.percentagem_aptos_naptos()
	
	string = ""
	for ano in sorted(dic.keys()):
		string += "<p>" + ano + "</p>"
		for estado in dic[ano].keys():
			if estado == "aptos":
				string += "<p>Aptos: " + str(dic[ano][estado]) + "%</p>"
			elif estado == "inaptos":
				string += "<p>Não aptos: " + str(dic[ano][estado]) + "%</p>"
		string += "<br>"


	content = re.sub(r'-info-', string, content)

	return content



def generate_html():

	with open("index.html", 'w') as file:
		content = """<!DOCTYPE html>
					<html>
					<h1>Página principal</h1>
					<body>
					-a-
					-b-
					-c-
					-d-
					-e-
					</body>
					</html>"""

		content = re.sub(r'-a-', html_a(), content)
		content = re.sub(r'-b-', html_b(), content)
		content = re.sub(r'-c-', html_c(), content)
		content = re.sub(r'-d-', html_d(), content)
		content = re.sub(r'-e-', html_e(), content)

		file.write(content)


generate_html()
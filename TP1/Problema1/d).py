import re
import json
import os


path = os.getcwd()

def first_20_lines(file):
	output_file = open("output.json", "w")

	with file as myfile:
		for x in range(20):
			line = next(myfile)
			mom = ""
			dad = ""
			obs = ""

			match_dir = re.search(r'[0-9]+', line)
			if match_dir:
				line = re.sub(match_dir.group(), "#", line)

			match_date = re.search(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', line)
			if match_date:
				line = re.sub(match_date.group(), "#", line)

			match_name = re.search(r'([A-Z][a-z]+|\s)+', line)
			if match_name:
				line = re.sub(match_name.group(), "#", line)

			match_dad = re.search(r':{2}([A-Z][a-z]+|\s)*:{2}', line)
			if match_dad:
				line = re.sub(match_dad.group(), "::#::", line)
				dad = match_dad.group().lstrip("::")
				dad = dad.rstrip("::")

			match_mom = re.search(r':{2}([A-Z][a-z]+|\s)*:{2}', line)
			if match_mom:
				line = re.sub(match_mom.group(), "::#::", line)
				mom = match_mom.group().lstrip("::")
				mom = mom.rstrip("::")

			match_obs = re.search(r':{2}(,|\.|\w|\d| )*:{2}', line)
			if match_obs:
				line = re.sub(match_obs.group(), "::#::", line)
				obs = match_obs.group().lstrip("::")
				obs = obs.rstrip("::")

			dic = {}
			dic["Pasta"] = match_dir.group()
			dic["Data"] = match_date.group()
			dic["Name"] = match_name.group()
			dic["Pai"] = dad
			dic["Mae"] = mom
			dic["Obs"] = obs

			json_object = json.dumps(dic)
			output_file.write(json_object)


file = open("processos.txt", "r")
first_20_lines(file)


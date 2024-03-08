from datascience 

data: dict[str, Table] = {}

for dir_name, _, file_names in os.walk("./Music"):
	for file in file_names:
		if file.endswith(".csv"):
			file_name = file[:-4]
			data[file_name] = Table.read_table(f"{dir_name}/{file}")

print(data)

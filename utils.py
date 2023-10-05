import os


def inputf(file_name: str = '.input.txt', editor_name: str = 'nano') -> str:
	if os.path.isfile(file_name):
		os.remove(file_name)

	os.system(f"{editor_name} {file_name}")
	file_content = ''
	if os.path.isfile(file_name):
		with open(file_name, 'r', encoding='UTF-8') as f:
			file_content = f.read()

		os.remove(file_name)

	return file_content

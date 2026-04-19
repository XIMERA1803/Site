import os
def check_file(name):
	return "png" in name or "jpeg" in name or "jpg" in name
def del_file(filename):
	filepath = os.path.join('./static/images', filename)
	os.remove(filepath)
#del_file('png')
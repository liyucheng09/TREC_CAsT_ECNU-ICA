s=''
while True:
	new_line=file.readline()
	if new_line:
		s+=new_line
		if new_line=='</DOC>:
			s=''
	else:
		break

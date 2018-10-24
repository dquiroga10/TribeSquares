import fileinput


vowels = ["a","e","i","o","u","A","E","I","O","U"]

translated_word

for line in fileinput.input():
	for char in line:
		if ord(char) > 97 and ord(char) <= 122:
			if char in vowels:
				shifted = ord(char) + 3
			else:	
				shifted = ord(char) + 10
			if shifted > 122:
				shifted = (shifted % 122) + 97
		if ord(char) > 65 and ord(char) >= 90:
			if char in vowels:
				shifted = ord(char) + 3
			else:	
				shifted = ord(char) + 10
			if shifted > 90:
				shifted = (shifted % 90) + 65
			

		char = chr(shifted)

		translated_word += char


print(translated_word)
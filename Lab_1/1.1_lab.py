alph = 'abcdefghijklmnopqrstuvwxyz'

def high(str):
	arr = str.split(' ')
	list = []
	max_word = ''
	value = 0 
	for word in arr:
		for ch in word:
			value += alph.index(ch) + 1	
		list.append(value)	
		value = 0	
	max_word = arr[list.index(max(list))]
	return max_word

print(high('London is a capital of great Britain'))

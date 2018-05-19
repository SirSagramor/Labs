import math 

class RomanNumerals():
	@staticmethod
	def to_roman(value):
		dict = {
			'1000': 'M',
			'900':  'MC',
			'500':  'D',
			'400':  'DC',
			'100':  'C',
			'90':   'CX',
			'50':   'L',
			'40':   'LX',
			'10':   'X',
			'9':	'XI',
			'5':    'V',
			'4':	'VI',
			'1':    'I',
			'0':    ''
		}
		numlist = list(str(value))[::-1]
		answer = ''
		for i in range(len(numlist)):
			zero = '0' * i
			if int(numlist[i]) < 4:
				answer += dict['1' + zero] * int(numlist[i]) 
				continue
			if int(numlist[i]) == 4 or int(numlist[i]) == 9: 
				answer += dict[numlist[i] + zero] 
				continue
			if int(numlist[i]) > 5:
				answer += dict['1' + zero] * (int(numlist[i]) - 5)
				answer += dict['5' + zero]	
		answer = answer[::-1]
		return answer 
					
	@staticmethod
	def from_roman(string):
		dict = {
		'M': 1000,
		'D': 500,
		'C': 100,
		'L': 50,
		'X': 10,
		'V': 5,
		'I': 1
    }
		last, total = 0, 0
		for c in list(string)[::-1]:
			if last == 0: 
				total += dict[c]
			elif last > dict[c]:
				total -= dict[c]
			else:
				total += dict[c]
			last = dict[c]
		return total

print (RomanNumerals.to_roman(1999))
print (RomanNumerals.from_roman('MCMXC')) 



# def to_roman(value):
# 		numlist = list(str(value))
# 		string = ''
# 		count = int('1' + ('0' * (len(numlist) - 1)))
# 		for i in range(1, len(numlist) + 1):
# 			s = int(int(numlist[i - 1]) * count)
# 			string = string+Nums[str(s)]
# 			count = math.floor(count / 10)
# 		return string
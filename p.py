def fib():
	arr = [0, 1]
	
	for i in range(11):
		arr.append(arr[i] + arr[i + 1])
	return sum(arr)

print(fib())

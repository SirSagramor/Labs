matrix =[[1, 2, 3, 10],
		 [4, 5, 6, 12],
		 [7, 8, 9, 17],
		 [1, 2, 5, 16]]

def snail(array):
	out = []
	if array == [[]]:
		return out
	dx, dy = 0, 1
	x, y = 0, 0
	for i in range(1, len(array)**2 + 1):
		out.append(array[x][y])
		array[x][y] = None
		nx, ny = x+dx, y+dy
		if 0 <= nx < len(array) and 0 <= ny < len(array) and array[nx][ny]:
			x, y = nx, ny
		else:
			dx, dy = dy, -dx
			x, y = x+dx, y+dy
	return out



print(snail(matrix))

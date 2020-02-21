import argparse

def aux(pizzas, max_, counter = 0, slices = 0, result = []):
	if not pizzas:
		return slices, result
	pizza, pizzas = pizzas[0], pizzas[1:]
	if slices+pizza <= max_:
		slices2, result2 = aux(pizzas, max_, counter+1, slices, result)
		slices1, result1 = aux(pizzas, max_, counter+1, slices+pizza, result+[counter])
		if slices1 > slices2:
			return slices1, result1
		else:
			return slices2, result2
	else:
		return slices, result
	
def aux2(slices, k):
	n = len(slices)
	x = n-1
	max_ = 0
	ocurrences = []
	actual = []
	while x > 0:
		tot = slices[x]
		actual = []
		actual.append(x)
		y = x-1
		while y >= 0:
			if slices[y]+tot < k:
				tot += slices[y]
				actual.append(y)
				y-=1
			elif slices[y]+tot == k:
				actual.append(y)
				return actual
			else:
				y-=1
		x-=1
		if tot > max_:
			max_ = tot
			ocurrences = actual
			
	return ocurrences

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('input_path', type=str,
						help='Path for the input file.')
	args = parser.parse_args()


	with open(args.input_path, 'r') as input_file:
		string = input_file.read()
		lines = string.split('\n')
		specs = [int(spec) for  spec in lines[0].split(' ')]
		slices = [int(slice_) for  slice_ in lines[1].split(' ')]
	
	if False:
		_, pos = aux(slices, specs[0])
		pos = [str(position) for position in pos]
		with open(args.input_path.split(".")[0]+".out", "w") as output_file:
			output_file.write('{specs}\n{slices}'.format(specs=len(pos), slices=" ".join(pos)))

	pos = aux2(slices, specs[0])
	pos = [str(posi) for posi in pos]
	pos.reverse()
	with open(args.input_path.split(".")[0]+".out", "w") as output_file:
		output_file.write('{specs}\n{slices}'.format(specs=len(pos), slices=" ".join(pos)))
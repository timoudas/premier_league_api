def some_func():
	return f'arg -p'

def some_fun1():
	return f'arg -t'

dispatch = {
	'-p': some_func,
	'-t': some_func,
}

map = ['-p', '-t']

for i in map:
	func = dispatch.get(i)
	print(func())
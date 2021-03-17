def read_file():
	path=input("enter file path")
	lines=[]
	with open(path) as f:
		lines=f.readlines()
	count=0 
	for line in lines:
		count+=1
		print(f'line {count}:{line}')
read_file()
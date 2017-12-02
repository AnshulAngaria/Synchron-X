input_file = open("main.sx",'r')

current_variables = []
current_functions = []

def parse_line(tokens):
	instruction = tokens[0]
	if instruction == "[" and tokens[-1]=="]":
		# it is comment instruction; ignore it
		# (i m nopping here just to show how it works)
		print "\tnop"
		pass
	elif instruction == "int":
		# declare memory in stack ...
		print "\tsub\trsp,1"
		current_variables.append(tokens[1])
		pass
	elif instruction in current_variables:
		# modify variable's value ....
		if len(tokens)==3:
			# constant value
			print "\tmov\tbyte [rsp-%d],%s"%(current_variables.index(tokens[0]),tokens[2])
		pass
	elif instruction == "{" and tokens[-1]=="}":
		# function call ....
		pass
	elif instruction[0]=="-":
		# code block end instruction
		pass
	elif instruction == "print":
		# print value of the int variable as ASCII [0-256]
		print "\tmov\trax,1"
		print "\tmov\trdi,1"
		print "\tlea\trsi,[rsp-%d]"%(current_variables.index(tokens[1]))
		print "\tmov\trdx,1"
		print "\tsyscall"
		pass
	elif instruction == "display":
		# display value of integer
		pass

def mode(char):
	if char.isalpha():
		return 1
	elif char.isdigit():
		return 2
	elif char.isspace():
		return 3
	else:
		return 4

def tokenize(line):
	line += "\n"
	symbol = ""
	tokens = []
	cur_mode = mode(line[0])
	i = 0
	while i<len(line):
		char = line[i]
		if mode(char) == cur_mode:
			symbol += char
			i += 1
		else:
			symbol = symbol.strip()
			if symbol!='':
				tokens.append(symbol)
			symbol = ""
		cur_mode = mode(char)
	return tokens

################################################################

# start instructions
print "\tglobal _start"
print "\tsection .text"
print "_start:"

for line in input_file:
	line = line.strip()
	tokens = tokenize(line)
	parse_line(tokens)

print "\tmov\teax, 60"
print "\tmov\trdx, 0"
print "\tsyscall"

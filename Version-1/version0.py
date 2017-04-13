## Bracket Expressions are not supported

import re
def flatten(container):
	for i in container:
		if isinstance(i, (list,tuple)):
			for j in flatten(i):
				yield j
		else:
			yield i
def loop_checker(string):
	if (string=="if" or string=="while" or string=="for"):
		return True
	else:
		return False

class Program:
	def __init__(self,string):
		self.comp_statement=CompoundStatement(string)

	def eval(self,state):
		self.comp_statement.eval(state)

class CompoundStatement:
	def __init__(self,string):
		self.statements=string.strip().split("\n")
		enumerator=0
		for i in self.statements:
			if_count=0
			while_count=0
			for_count=0
			i=i.strip()
			words=i.split()
			if words[0]=="if":
				if_count=1
			elif words[0]=="while":
				while_count=1
			elif words[0]=="for":
				for_count=1
			all_count=if_count|while_count|for_count
			temp_count=enumerator+1
			while(all_count):
				if temp_count<len(self.statements):
					word=self.statements[temp_count].strip().split()
					if word[0]=="if":
						if_count+=1
					elif word[0]=="while":
						while_count+=1
					elif word[0]=="for":
						for_count+=1
					elif word[0]=="done;":
						while_count-=1
					elif word[0]=="fi;":
						if_count-=1
					all_count=if_count|while_count|for_count
					self.statements[enumerator]=self.statements[enumerator]+"\n"+self.statements[temp_count]
					del self.statements[temp_count]
			enumerator+=1
#		for i,j in enumerate(self.statements):
#			self.statements[i]=self.statements
		for i,j in enumerate(self.statements):
			self.statements[i]=re.split(';(?!\n)', self.statements[i])
			del self.statements[i][-1]
		self.statements=list(flatten(self.statements))		
#		print(self.statements)
		for i,j in enumerate(self.statements):
			self.statements[i]=Statement.build(j.strip())

	def eval(self,state):
		for i in self.statements:
			i.eval(state)

class Statement:
	def build(string):
		word=string.strip().split()
		if word[0]=="if":
			return IfElseStatement(string)
		elif word[0]=="while":
			return WhileStatement(string)
		elif word[0][0:7]=="println":
			return PrintlnStatement()	
		elif word[0][0:5]=="print":
			return PrintStatement(string) 
		else:
			return AssignmentStatement(string)

class IfElseStatement:
	def __init__(self,string):
		self.condExpr=ConditionExpression.build(re.findall(r'if (.*?) then',string,re.DOTALL)[0].strip())
		word=string.split()
		temp=word.count("if")
		then_index=string.find("then")
		index=0
		while(temp):
			temp-=1
			index=string.find("else\n",index)
			index+=1
		iftrue=string[then_index+4:index-1]
		temp=word.count("if")
		index1=0
		while(temp):
			temp-=1
			index1=string.find("fi\n",index1)
			index1+=1
		iffalse=string[index+3:index1-2]
#		iftrue=re.findall(r'then(.*?)else',string,re.DOTALL)[0].strip()
#		iffalse=re.findall(r'else(.*?)fi',string,re.DOTALL)[0].strip()
		self.left_comp_statement=CompoundStatement(iftrue)
		self.right_comp_statement=CompoundStatement(iffalse)
	def eval(self,state):
		if self.condExpr.eval(state)==True:
			self.left_comp_statement.eval(state)
		else:
			self.right_comp_statement.eval(state)

class WhileStatement:
	def __init__(self,string):
		self.condExpr=ConditionExpression.build(re.findall(r'while (.*?) do',string,re.DOTALL)[0].strip())
		word=string.split()
		temp=word.count("while")
		do_index=string.find("do")
		index=0
		while(temp):
			temp-=1
			index=string.find("done\n",index)
			index+=1
		statements=string[do_index+2:index-1]
#		statements=re.findall(r'do(.*?)done',string,re.DOTALL)[0].strip()
		self.comp_statement=CompoundStatement(statements)
	def eval(self,state):
		while(self.condExpr.eval(state)):
			self.comp_statement.eval(state)

class AssignmentStatement:
	def __init__(self,string):
		variable,expression=string.split(":=")
		self.var=variable.strip()
		self.expr=Expression.build(expression)

	def eval(self,state):
		state[self.var]=self.expr.eval(state)

class ConditionExpression:
	def build(string):
		if string.find("==")>=0:
			return EqualExpression(string)
		elif string.find("!=")>=0:
			return NotEqualExpression(string)
		elif string.find(">=")>=0:
			return GreaterEqualExpression(string)
		elif string.find("<=")>=0:
			return LesserEqualExpression(string)
		elif string.find(">")>=0:
			return GreaterExpression(string)
		elif string.find("<")>=0:
			return LesserExpression(string)
		elif string[0].isalpha():
			return Variable(string)
		else:
			return ConstantExpression(string)

class Expression:
	def build(string):
		string=string.strip()
		if string.find("-")>=0:
			return SubtractionExpression(string)
		elif string.find("+")>=0:
			return PlusExpression(string)
		elif string.find("*")>=0:
			return MultiplicationExpression(string)
		elif string.find("/")>=0:
			return DivideExpression(string)
		elif string[0]=="\"":
			return StringExpression(string)
		elif string[0].isalpha():
			return Variable(string)
		else: 
			return ConstantExpression(string)

class StringExpression:
	def __init__(self,string):
		self.string=re.findall(r'\"(.*?)\"',string,re.DOTALL)[0]

	def eval(self,state):
		return self.string

class ConstantExpression:
	def __init__(self,string):
		self.value=int(string)

	def eval(self,state):
		return self.value

class Variable:
	def __init__(self,string):
		self.var=string.strip()

	def eval(self,state):
		return state[self.var]

class EqualExpression():
	def __init__(self,string):
		l,r=string.split("==")
		self.left=Expression.build(l)
		self.right=Expression.build(r)

	def eval(self,state):
		return self.left.eval(state)==self.right.eval(state)

class NotEqualExpression():
	def __init__(self,string):
		l,r=string.split("!=")
		self.left=Expression.build(l)
		self.right=Expression.build(r)

	def eval(self,state):
		return self.left.eval(state)!=self.right.eval(state)
		
class GreaterEqualExpression():
	def __init__(self,string):
		l,r=string.split(">=")
		self.left=Expression.build(l)
		self.right=Expression.build(r)

	def eval(self,state):
		return self.left.eval(state)>=self.right.eval(state)
		

class LesserEqualExpression():
	def __init__(self,string):
		l,r=string.split("<=")
		self.left=Expression.build(l)
		self.right=Expression.build(r)

	def eval(self,state):
		return self.left.eval(state)<=self.right.eval(state)

class GreaterExpression():
	def __init__(self,string):
		l,r=string.split(">")
		self.left=Expression.build(l)
		self.right=Expression.build(r)

	def eval(self,state):
		return self.left.eval(state)>self.right.eval(state)

class LesserExpression():
	def __init__(self,string):
		l,r=string.split("<")
		self.left=Expression.build(l)
		self.right=Expression.build(r)

	def eval(self,state):
		return self.left.eval(state)<self.right.eval(state)

class DivideExpression:
	def __init__(self,string):
		l,r=string.split("/",1)
		self.left=Expression.build(l)
		self.right=Expression.build(r)

	def eval(self,state):
		try:
			return self.left.eval(state)/self.right.eval(state)
		except:
			raise ZeroDivisionError("Can't divide by zero !!")

class MultiplicationExpression:
	def __init__(self,string):
		l,r=string.split("*",1)
		self.left=Expression.build(l)
		self.right=Expression.build(r)

	def eval(self,state):
		return self.left.eval(state)*self.right.eval(state)

class PlusExpression:
	def __init__(self,string):
		l,r=string.split("+",1)
		self.left=Expression.build(l)
		self.right=Expression.build(r)

	def eval(self,state):
		return self.left.eval(state)+self.right.eval(state)

class SubtractionExpression:
	def __init__(self,string):
		l,r=string.split("-",1)
		self.left=Expression.build(l)
		self.right=Expression.build(r)

	def eval(self,state):
		return self.left.eval(state)-self.right.eval(state)


class PrintStatement:
	def __init__(self,string):
		self.expr=list(map(str.strip,re.findall(r'\((.*?)\)',string,re.DOTALL)[0].split(",")))
		self.expressions=[]
		for i in self.expr:
			self.expressions.append(Expression.build(i))

	def eval(self,state):
		for i in self.expressions:
			print(i.eval(state),end=" ")
		print()

class PrintlnStatement:
	def eval(self,state):
		print()

if __name__ == '__main__':
	file=open("code.txt")
	state={}
	content=file.read()
	print(content,"\n")
	p=Program(content)
	p.eval(state)
	print(state)

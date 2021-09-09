

class Variable(dict):
	def __init__(self, required=False, prompt=None, helpinfo=None, ID=None, **kwargs):
		super().__init__(required=required, prompt=prompt, helpinfo=helpinfo, ID=ID, **kwargs)
		self.__dict__ = self
	
	
	# def draw(self):
	# 	raise NotImplementedError
	
	
	
class Select(Variable):
	def __init__(self, choices=None, num=1, **kwargs):
		if choices is None:
			choices = []
		super().__init__(choices=choices, num=num, **kwargs)
		

	def new(self, *vals):
		for val in vals:
			if val not in self.choices:
				self.choices.append(val)



class Binary(Select):
	def __init__(self, choices=None, num=None, **kwargs):
		if choices is not None:
			choices = ['yes', 'no']
		super().__init__(choices=choices, num=1, **kwargs)
	


class Date(Variable):
	def __init__(self, date=None, **kwargs):
		super().__init__(date=date, **kwargs)



class Text(Variable):
	def __init__(self, val=None, **kwargs):
		super().__init__(val=val, **kwargs)



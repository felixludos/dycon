from argparse import Namespace
from datetime import datetime
from pathlib import Path
import markdown
from IPython.core.display import HTML

from omnibelt import save_txt, save_yaml, get_now, load_yaml

from .variables import Select, Binary, Date, Text

DRAW_HEADER = '''# {title}
{desc}
*by {sponsor}* -- ID: **{ID}**

{long_desc}

Variables: {vars}
Required variables: {required}
'''


class Query(dict):
	def __init__(self, path, proposal=None):
		if proposal is None:
			ppath = path / 'proposal.yml'
			proposal = load_yaml(ppath) if ppath.exists() else {}
		super().__init__(**proposal)
		self.__dict__ = self
		self._path = path
		
		
	@staticmethod
	def generate_ID(root):
		prefix = get_now('%y%m')
		
		offset = 0
		num = len(list(root.glob(f'{prefix}*')))
		name = f'{prefix}q{str(num).zfill(5)}'
		path = root / name
		while path.exists():
			offset += 1
			name = f'{prefix}q{str(num + offset).zfill(5)}'
			path = root / name
		path.mkdir(exist_ok=True)
		return name
	
	
	@classmethod
	def create_query(cls, root, ID=None, proposal=None, template=None,
	                 template_filename='template.txt'):
		root = Path(root)
		
		if proposal is None:
			proposal = {}
		if ID is None:
			ID = cls.generate_ID(root)
			proposal['ID'] = ID
		
		path = root / ID
		
		if template is not None:
			save_txt(template, path / template_filename)
			proposal['template-path'] = template_filename
		
		q = cls(path, proposal=proposal)
		
		save_yaml(proposal, path / 'proposal.yml')
		save_txt(q.generate_readme(), path / 'README.md')
		
		return proposal
		
		
	def generate_readme(self):
		if 'title' not in self:
			return 'This is the readme for the proposal {ID}.'.format(ID=self.ID)
		return 'This is the readme for the proposal {title} ({ID}).'.format(ID=self.ID, title=self.title)
	
	
	def _load_variable(self, variable):
		typ = variable['type']
		
		if typ == 'select':
			return Select(**variable)
		if typ == 'binary':
			return Binary(**variable)
		if typ == 'date':
			return Date(**variable)
		if typ == 'text':
			return Text(**variable)
		raise Exception(f'Unknown type: {typ}')
	
	
	def load_variables(self, variables=None):
		if variables is None:
			variables = self.get('variables', [])
		self._variables = [self._load_variable(v) for v in variables]
	
	
	def get_variables(self):
		if '_variables' not in self:
			self.load_variables()
		return self._variables
	
	
	def draw(self):
		header = DRAW_HEADER.format(
			title = self.get('title', '[no-title]'),
			desc = self.get('desc', '[no-desc]'),
			sponsor = self.get('sponsor', '[no-sponsor]'),
			ID = self.get('ID'),
			long_desc = self.get('long-desc', '- no description -'),
			vars = '[ {} ]'.format(', '.join(self.get('variables', {}).keys())),
			required = '[ {} ]'.format(', '.join(self.get('required', []))),
		)
		header = markdown.markdown(header)
		return HTML(header)
	
		
	@classmethod
	def load(cls, root, ID=None):
		return cls.create_query(root) if ID is None else cls(root / ID)

	






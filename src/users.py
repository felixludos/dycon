import random
from omnibelt import save_txt, save_yaml, get_now, load_yaml

from .query import Query



EXAMPLE_USERNAMES = ['shaquille.oatmeal', 'hanging_with_my_gnomies', 'hoosier-daddy', 'fast_and_the_curious', 'averagestudent', 'BadKarma', 'google_was_my_idea', 'cute.as.ducks', 'casanova', 'real_name_hidden', 'HairyPoppins', 'fedora_the_explorer ', 'OP_rah', 'YellowSnowman', 'Joe Not Exotic', 'username_copied', 'whos_ur_buddha', 'unfinished_sentenc', 'AllGoodNamesRGone', 'Something', 'me_for_president', 'tinfoilhat', 'oprahwindfury', 'anonymouse', 'Definitely_not_an_athlete', 'HeartTicker ', 'YESIMFUNNY', 'BenAfleckIsAnOkActor', 'magicschoolbusdropout', 'Everybody', 'regina_phalange', 'PawneeGoddess ', 'pluralizes_everythings', 'chickenriceandbeans', 'test_name_please_ignore', 'IYELLALOT', 'heyyou', 'laugh_till_u_pee', 'aDistraction', 'crazy_cat_lady', 'banana_hammock', 'thegodfatherpart4', 'unfriendme', 'babydoodles', 'fluffycookie', 'buh-buh-bacon', 'ashley_said_what', 'LactoseTheIntolerant', 'ManEatsPants', 'Twentyfourhourpharmacy', 'applebottomjeans', 'Babushka', 'toastedbagelwithcreamcheese', 'baeconandeggz', 'FartinLutherKing ', 'coolshirtbra', 'kentuckycriedfricken', 'REVERANDTOAST', 'kim_chi', 'idrinkchocolatemilk', 'SaintBroseph', 'chin_chillin', 'ghostfacegangsta', 'bigfootisreal', 'santas_number1_elf', 'thehornoftheunicorn', 'iNeed2p', 'abductedbyaliens', 'actuallynotchrishemsworth', 'nachocheesefries', 'personallyvictimizedbyreginageorge', 'just-a-harmless-potato', 'FrostedCupcake', 'Avocadorable', 'fatBatman', 'quailandduckeggs', 'PaniniHead', 'mandymooressingingvoice', 'catsordogs', 'FartnRoses', 'RedMonkeyButt', 'FreddyMercurysCat', 'MasterCheif', 'FreeHugz', 'ima.robot', 'actuallythedog', 'notthetigerking', 'pixie_dust', 'ChopSuey', 'turkey_sandwich', 'B.Juice', 'Chris_P_Bacon', 'LtDansLegs', '95.WookiesrPpl2', 'hogwartsfailure', 'CourtesyFlush', 'MomsSpaghetti', 'spongebobspineapple', 'garythesnail', 'nothisispatrick', 'CountSwagula', 'SweetP', 'PNUT', 'Snax', 'Nuggetz', 'colonel_mustards_rope', 'baby_bugga_boo', 'joancrawfordfanclub', 'fartoolong', 'loliateyourcat', 'rawr_means_iloveyou', 'ihavethingstodo.jpg', 'heresWonderwall ', 'UFO_believer', 'ihazquestion', 'SuperMagnificentExtreme', 'It’s_A _Political_ Statement ', 'TheAverageForumUser', 'just_a_teen', 'OmnipotentBeing', 'GawdOfROFLS', 'loveandpoprockz', '2_lft_feet', 'Bread Pitt']
EXAMPLE_TAGS = ['love', 'instagood', 'fashion', 'photooftheday', 'beautiful', 'art', 'photography', 'happy', 'picoftheday', 'cute', 'follow', 'tbt', 'followme', 'nature', 'like4like', 'travel', 'instagram', 'style', 'repost', 'summer', 'instadaily', 'selfie', 'me', 'friends', 'fitness', 'girl', 'food', 'fun', 'beauty', 'instalike', 'smile', 'family', 'photo', 'life', 'likeforlike', 'music', 'ootd', 'follow4follow', 'makeup', 'amazing', 'igers', 'nofilter', 'dog', 'model', 'sunset', 'beach', 'instamood', 'foodporn', 'motivation', 'followforfollow', 'design', 'lifestyle', 'sky', 'l4l', 'f4f', '일상', 'cat', 'handmade', 'hair', 'vscocam', 'bestoftheday', 'vsco', 'funny', 'dogsofinstagram', 'drawing', 'artist', 'gym', 'flowers', 'baby', 'wedding', 'girls', 'instapic', 'pretty', 'likeforlikes', 'photographer', 'instafood', 'party', 'inspiration', 'lol', 'cool', 'workout', 'likeforfollow', 'swag', 'fit', 'healthy', 'yummy', 'blackandwhite', 'foodie', 'moda', 'home', 'christmas', 'black', 'memes', 'holiday', 'pink', 'sea', 'landscape', 'blue', 'london', 'winter']



class User(dict):
	def __init__(self, ID, name=None, tags=None, support=None, **kwargs):
		if tags is None:
			tags = []
		if name is None:
			name = f'u/{ID}'
		if support is None:
			support = {}
		super().__init__(ID=ID, name=name, tags=tags, support=support, **kwargs)
		self.__dict__ = self
	
	
	
class UserSpace:
	def __init__(self, path, users=None):
		self.path = path
		if users is None:
			users = {}
		self.users = users
		if self.path.exists():
			self.users = load_yaml(self.path)
		else:
			self.save()
		self._usernames = {u['name']:u['ID'] for u in self.users.values()}
		
	
	def __str__(self):
		return 'UserSpace({})'.format(', '.join(self._usernames))
		
		
	def __repr__(self):
		return str(self)
		
		
	def export(self):
		return {ID:dict(user) for ID, user in self.users.items()}
		
		
	def find(self, key):
		if isinstance(key, User):
			assert key.ID in self.users, f'Unknown user: {key.ID}'
			return key
		elif key in self.users:
			return self.users[key]
		elif key in self._usernames:
			return self.users[self._usernames[key]]
		raise Exception(f'User not found: {key}')
		
		
	def generate_ID(self):
		offset = 0
		ID = hex(len(self.users))[2:]
		while ID in self.users:
			offset += 1
			ID = hex(len(self.users))[2:]
		return ID
		
		
	def new(self, name=None):
		ID = self.generate_ID()
		if name is None:
			while name is None or name in self._usernames:
				name = random.choice(EXAMPLE_USERNAMES)
		new = User(ID, name)
		self.users[ID] = new
		self._usernames[new.name] = ID
		return new
		
		
	def save(self, path=None):
		if path is None:
			path = self.path
		return save_yaml(self.export(), path)
		


class Client:
	def __init__(self, root):
		self.root = root
		self.users = UserSpace(root/'users.yml')
		self.user = None
		
	
	def load_query(self, ID):
		return Query(self.root/ID)
		
		
	def create_user(self, name=None):
		return self.users.new(name)
		
		
	def login(self, name=None):
		try:
			self.user = self.users.find(name)
		except:
			print('Creating a new user')
			self.user = self.create_user(name)
		return self.user







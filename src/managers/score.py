from src.utils.helpers import Data

class Score(Data):
	def __init__(self):
		# Note: Store score values as zero-padded strings for display.
		self.__score = "00000"
		self.__highscore = "00000"

	@property
	def score(self):
		# Note: Current score shown during a run.
		return self.__score
	
	@score.setter
	def score(self,score):
		# Note: Allow other code to update the current score.
		self.__score = score

	@property
	def highscore(self):
		# Note: Best score stored for the session or loaded data.
		return self.__highscore
	
	@highscore.setter
	def highscore(self,highscore):
		# Note: Allow other code to update the best score.
		self.__highscore = highscore

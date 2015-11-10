'''
Farming Optimization Project
Authors: Amanda Sutherland, Mimi Kome, Ziyu (Selina) Wang
Current Function: Takes user input intuitively
'''

# Construct a nested list from user input
# turn it into a dictionary

def collectingData():
	print 'Hello there! Welcome to FarmOpt!\nWould you like to continue? (y/n)'
	openSoftware = raw_input()
	if openSoftware == 'n':
		print 'Bye!'
	elif openSoftware == 'y':
		print 'How many kinds of crops are you planning on planting?'
		numCrops = raw_input()
		crops = []
		print 'How many weeks are you planning on planting all of these crops?'
		numWeeks = raw_input()
		weeks = []

		for crop in range(int(numCrops)):
			individualcrop = []
			weeks.append(individualcrop)
			print 'What is the name of the', str(crop+1), 'st crop?'
			crops.append(raw_input())
			for week in range(int(numWeeks)):
				print 'How much of', crops[crop], 'would you like to plant in week', str(week+1), '?'
				weeks[crop].append(raw_input())
		print 'Here is all the data we received!'
		for crop in range(int(numCrops)):
			print crops[crop], ':', str(weeks[crop])
			


if __name__ == '__main__':
	collectingData()
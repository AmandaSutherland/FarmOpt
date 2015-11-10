'''
Farming Optimization Project
Authors: Amanda Sutherland, Mimi Kome, Ziyu (Selina) Wang
Current Function: Takes user input intuitively
'''

# Construct a nested list from user input
# turn it into a dictionary

def collectingData():
	print('Hello there! Welcome to FarmOpt!\nWould you like to continue? (y/n)')
	openSoftware = raw_input()
	if openSoftware == 'n':
		print('Bye!')
	elif openSoftware == 'y':
		print('How many kinds of crops are you planning on planting?')
		numPlants == raw_input()
		print('How many weeks are you planning on planting all of these crops?')
		numWeeks == raw_input()
		for week in range(numWeeks):
			


if __name__ == '__main__':
	collectingData()
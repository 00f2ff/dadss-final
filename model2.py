import json, csv, itertools

info = {
	"assumptions": {
		"Natural Light": {
			"Basement": 0,
			"First": 0.95,
			"Second": 0.15,
			"Third": 0.9,
			"Fourth": 0.25
		},
		"Close to Outlet": {
			"Basement": 0.3,
			"First": 0.35,
			"Second": 0.45,
			"Third": 0.95,
			"Fourth": 0.6
		},
		"Quietness": {
			"Basement": 0.05,
			"First": 0.05,
			"Second": 0.15,
			"Third": 1,
			"Fourth": 0.4
		},
		"Close to Food": {
			"Basement": 0.7,
			"First": 1,
			"Second": 0.7,
			"Third": 0.35,
			"Fourth": 0
		},
		"Working Alone": {
			"Basement": 0.1,
			"First": 0.1,
			"Second": 0.15,
			"Third": 1,
			"Fourth": 0.45
		},
		"Total Chairs": {
			"Basement": 33.0,
			"First": 70.0,
			"Second": 72.0,
			"Third": 146.0,
			"Fourth": 76.0
		}
	},
	"availability": {
		"Monday": {
			"10:30 AM": {
				"Basement": 24,
				"First": 41,
				"Second": 29,
				"Third": 51,
				"Fourth": 32
			},
			"1:30 PM": {
				"Basement": 18,
				"First": 38,
				"Second": 28,
				"Third": 43,
				"Fourth": 20
			},
			"4:30 PM": {
				"Basement": 8,
				"First": 21,
				"Second": 18,
				"Third": 14,
				"Fourth": 17
			},
			"7:30 PM": {
				"Basement": 16,
				"First": 30,
				"Second": 20,
				"Third": 30,
				"Fourth": 21
			},
			"10:30 PM": {
				"Basement": 23,
				"First": 13,
				"Second": 13,
				"Third": 9,
				"Fourth": 14
			}
		},
		"Tuesday": {
			"10:30 AM": {
				"Basement": 19,
				"First": 45,
				"Second": 21,
				"Third": 42,
				"Fourth": 23
			},
			"1:30 PM": {
				"Basement": 15,
				"First": 30,
				"Second": 16,
				"Third": 30,
				"Fourth": 15
			},
			"4:30 PM": {
				"Basement": 14,
				"First": 16,
				"Second": 17,
				"Third": 18,
				"Fourth": 13
			},
			"7:30 PM": {
				"Basement": 18,
				"First": 13,
				"Second": 15,
				"Third": 20,
				"Fourth": 18
			},
			"10:30 PM": {
				"Basement": 17,
				"First": 33,
				"Second": 19,
				"Third": 39,
				"Fourth": 17
			}
		},
		"Wednesday": {
			"10:30 AM": {
				"Basement": 28,
				"First": 25,
				"Second": 41,
				"Third": 64,
				"Fourth": 43
			},
			"1:30 PM": {
				"Basement": 14,
				"First": 32,
				"Second": 11,
				"Third": 38,
				"Fourth": 15
			},
			"4:30 PM": {
				"Basement": 17,
				"First": 17,
				"Second": 11,
				"Third": 21,
				"Fourth": 13
			},
			"7:30 PM": {
				"Basement": 14,
				"First": 16,
				"Second": 29,
				"Third": 42,
				"Fourth": 12
			},
			"10:30 PM": {
				"Basement": 18,
				"First": 22,
				"Second": 24,
				"Third": 44,
				"Fourth": 16
			}
		},
		"Thursday": {
			"10:30 AM": {
				"Basement": 21,
				"First": 39,
				"Second": 26,
				"Third": 55,
				"Fourth": 27
			},
			"1:30 PM": {
				"Basement": 15,
				"First": 20,
				"Second": 16,
				"Third": 38,
				"Fourth": 18
			},
			"4:30 PM": {
				"Basement": 17,
				"First": 14,
				"Second": 15,
				"Third": 24,
				"Fourth": 14
			},
			"7:30 PM": {
				"Basement": 17,
				"First": 51,
				"Second": 30,
				"Third": 61,
				"Fourth": 28
			},
			"10:30 PM": {
				"Basement": 21,
				"First": 30,
				"Second": 20,
				"Third": 49,
				"Fourth": 24
			}
		},
		"Friday": {
			"10:30 AM": {
				"Basement": 18,
				"First": 25,
				"Second": 37,
				"Third": 44,
				"Fourth": 32
			},
			"1:30 PM": {
				"Basement": 22,
				"First": 41,
				"Second": 41,
				"Third": 42,
				"Fourth": 27
			},
			"4:30 PM": {
				"Basement": 20,
				"First": 20,
				"Second": 34,
				"Third": 37,
				"Fourth": 31
			},
			"7:30 PM": {
				"Basement": 28,
				"First": 38,
				"Second": 39,
				"Third": 42,
				"Fourth": 20
			},
			"10:30 PM": {
				"Basement": 30,
				"First": 43,
				"Second": 40,
				"Third": 44,
				"Fourth": 34
			}
		}
	}
}

class Simulation(object):
	def __init__(self, info, weight, rank, day, time):
		self.assumptions = info["assumptions"]
		self.total_chairs = info["assumptions"]["Total Chairs"]
		self.availability = info["availability"][day][time]
		self.day = day
		self.time = time
		self.weight = weight
		self.rank = rank
		self.preferences = ['Close to Outlet','Working Alone','Natural Light','Close to Food','Quietness']
		self.floors = ['Basement','First','Second','Third','Fourth']
		self.initial_calculations()
		self.define_options()
		self.calculate_options()
		self.find_best_results()

	# Converts all initial values into what our multipliers rely on
	def initial_calculations(self):
		# Adjust weight to scoring standard (opposite scale than rank)
		self.adjusted_weight = {}
		for p in self.preferences:
			if self.weight[p] == 5: # least important
				self.adjusted_weight[p] = 1
			elif self.weight[p] == 4:
				self.adjusted_weight[p] = 0.75
			elif self.weight[p] == 3:
				self.adjusted_weight[p] = 0.5
			elif self.weight[p] == 2:
				self.adjusted_weight[p] = 0.25
			elif self.weight[p] == 1: # most important
				self.adjusted_weight[p] = 0

		# Adjust rank to scoring standard
		self.adjusted_rank = {}
		# add adjusted ranks
		for r in self.rank.keys():
			self.adjusted_rank[r] = 6 - self.rank[r] # 5 turns into multiplier of 1; 1 turns into multiplier of 5

		# Turn availabilities into probabilities
		for t in self.total_chairs:
			self.availability[t] /= self.total_chairs[t]

	# Reads a default options file to create a starter dict
	def define_options(self):
		with open('tree2.json','r') as f:
			tree = f.read()
		tree = json.loads(tree)
		self.options = tree['paths']

	# Find utility given a assumption, rank, weight, availability, and if a 'no' path is followed
	def utility(self, p, r, w, a, invert):
		if invert: return (1-p)*r*(1-w)*a
		else: return p*r*w*a

	# Calculates all utilities in decision tree and writes new options to disk
	def calculate_options(self):
		# iterate through options
		for o in self.options:
			# iterate through choice node indexes
			for c in xrange(len(o['path'])):
				# see if inverse is needed
				if o['path'][c] == "no": i = True
				else: i = False
				# iterate through preferences in adjusted_rank dict
				for p in self.adjusted_rank.keys():
					# check that rank apself.plies to correct node
					if 5 - self.adjusted_rank[p] == c: # ex. c = 0 means first node; assign multiplier then
						r_mult = self.adjusted_rank[p]
						w_mult = self.adjusted_weight[p]
						# iterate through floors
						for f in self.floors:
							# calculate utility
							u = self.utility(self.assumptions[p][f], r_mult, w_mult, self.availability[f], i)
							# add utility to this option's floor's utility
							o[f] += u

		with open("tree_results.json","w") as f:
		    f.write(str(json.dumps(self.options, indent=2)))

	# Returns a list of the best path(s) and floor(s) in the entire tree. If more than one floor has the same utility, both will be listed.
	def find_best_overall(self):
		# calculate best option(s)
		self.best_paths = []
		self.best_floors = []
		self.best_utility = 0
		# iterate through options
		for o in self.options:
			# iterate through floors
			for f in self.floors:
				# if utility is highest, change values
				if o[f] > self.best_utility: 
					self.best_utility = o[f]
					self.best_paths = [o['path']]
					self.best_floors = [f]
				# if utility is tied, add floor to values
				elif o[f] == self.best_utility:
					self.best_paths.append(o['path'])
					self.best_floors.append(f)

	# Finds the best four results for users per our Excel model
	def find_best_results(self):
		# Initialize variables with [path, floor, utility]
		self.forgo_none = [['yes','yes','yes','yes','yes'], '', 0]
		self.forgo_5 = [['yes','yes','yes','yes','no'], '', 0]
		self.forgo_45 = [['yes','yes','yes','no','no'], '', 0]
		self.forgo_345 = [['yes','yes','no','no','no'], '', 0]
		endings = [self.forgo_none, self.forgo_5, self.forgo_45, self.forgo_345]
		# Iterate through options
		for o in self.options:
			# Iterate through endings
			for e in endings:
				# Check if path matches
				if e[0] == o['path']:
					best_utility = 0
					best_floor = ''
					# Iterate through floors
					for f in self.floors: # For the sake of time I'm avoiding duplicates
						# Find best utility
						if o[f] > best_utility:
							best_utility = o[f]
							best_floor = f
					e[1] = best_floor
					e[2] = round(best_utility, 3)


# These will change according to simulations
weight = {'Close to Outlet': 4, 'Working Alone': 1, 'Natural Light': 4, 'Close to Food': 4, 'Quietness': 1}
# rank = {'Close to Outlet': 1, 'Working Alone': 2, 'Natural Light': 5, 'Close to Food': 3, 'Quietness': 4} # 1 is most important, so rank * of 5
rank = {'Close to Food': 4, 'Quietness': 2, 'Natural Light': 5, 'Close to Outlet': 1, 'Working Alone': 3}
day = 'Monday'
time = '10:30 AM'
# a = Simulation(info, weight, rank, day, time)
# print a.forgo_345


# This generates the 5! different rank permutations available
def rank_combos():
	ranks = []
	# Create a list of all possible permutations
	permutations = list(itertools.permutations([1,2,3,4,5]))
	# Append a rank dict for each permutation to ranks
	for p in permutations:
		rank = {'Close to Outlet': p[0], 'Working Alone': p[1], 'Natural Light': p[2], 'Close to Food': p[3], 'Quietness': p[4]}
		ranks.append(rank)
	return ranks

# This generates 3! * 2 different rank permutations based on survey data for what students find important
def informed_ranks():	
	ranks = []
	permutations = list(itertools.permutations([1,2,3]))
	# Append a rank dict for each permutation to ranks
	for p in permutations:
		rank = {'Close to Outlet': p[0], 'Working Alone': p[1], 'Natural Light': 0, 'Close to Food': 0, 'Quietness': p[2]}
		ranks.append(rank)
	# Go through ranks and add 4 or 5 to the remaining preferences
	for i in xrange(len(ranks)):
		if i % 2 == 0:
			ranks[i]['Natural Light'] = 4
			ranks[i]['Close to Food'] = 5
		else:
			ranks[i]['Natural Light'] = 5
			ranks[i]['Close to Food'] = 4
	return ranks

# This simulates all possible days and times given weights and ranks
def simulate_datetime(info, weight):
	# Basic input options
	days = ['Monday', 'Tuesday','Wednesday', 'Thursday', 'Friday']
	times = ['10:30 AM', '1:30 PM', '4:30 PM', '7:30 PM', '10:30 PM']
	# Advanced input options
	
	ranks = informed_ranks()
	# aaa = Simulation(info, weight, ranks[1], 'Monday', '10:30 AM')
	# print aaa.forgo_none
	sim = []
	for d in days:
		for t in times:
			for r in ranks:
				si = Simulation(info, weight, r, d, t)
				# print s.forgo_none
				sim.append(si)
				del si
				# si = ''
	

	# Write the data to a CSV file
	# Keep rank unadjusted for presentation purposes
	headers = ['day', 'time', 'rank', 'forgo none floor', 'forgo none u', 'forgo one floor', 'forgo one u', 'forgo two floor', 'forgo two u', 'forgo three floor', 'forgo three u']
	with open('results.csv','w') as f:
		writer = csv.writer(f)
		writer.writerow(headers)
		for s in sim:
			data = [s.day, s.time, s.rank, s.forgo_none[1], s.forgo_none[2], s.forgo_5[1], s.forgo_5[2], s.forgo_45[1], s.forgo_45[2], s.forgo_345[1], s.forgo_345[2]]
			writer.writerow(data)


simulate_datetime(info, weight)

"""
Next:
It would be cool if I could simulate every single possible rank, weight, day and time.
This might be too computationally intensive, so why don't I start out with:
1. Refactor code into functions within a class and test
2. Given the current ranks and weights, generate a file with the results for all possible days and times
3. Do 2 but go through all possible ranks
4. Do 3 but go through all possible weights
5. Figure out how to analyze this data


"""



"""
Notes:
Although it may be too early to tell if there are common results since this isn't integrating the proper data yet, we may want to consider a function governing option for alternative solutions based on user rankings. For example, although we ask for 5 preferences, we can assume the first three are the most important, and later ones are less so (We should analyze user surveys to see the probability of each preference being in the top 3). Based on this assumption, students will be seeking out those things specifically, so we can eliminate the alternatives in those cases (i.e. get rid of the "no" branch). That leaves alternatives ("no" branch) for the remaining two preferences. This may be a good approach because it reduces the overall complexity of the tree, as well as alternatives students may not care for.
A different way to do this would be to analyze the following alternatives: yyyyn, yyyny, yynyy, ynyyy, nyyyy

"""
	
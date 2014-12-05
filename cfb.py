import sys
import os
import random
import math

conference_size = 10
number_of_simulations = 50000
home_teams = True
lowest_rating = 1000
highest_rating = 1800
home_advantage = 250

def elo_win_chance(my_rating, opp_rating):
	return 1.0 / (1.0 + pow(10, (opp_rating - my_rating) / 400.0))

def naive_ranking(team1, team2):
	if len(team2["win"]) != len(team1["win"]):
		return len(team2["win"]) - len(team1["win"])
	# random sorting
	return team2["sort"] - team1["sort"]

def head_to_head_ranking(team1, team2):
	if len(team2["win"]) != len(team1["win"]):
		return naive_ranking(team1, team2)
	if team1["name"] in team2["win"]:
		return 1
	if team2["name"] in team1["win"]:
		return -1

def rating_ranking(team1, team2):
	if team2["rating"] != team1["rating"]:
		return team2["rating"] - team1["rating"]
	# have to use a different random sorting to break ratings ties so teams that were created first are not advantaged
	return team2["sort2"] - team1["sort2"]

teams = {}
good_naive = 0.0
bad_naive = 0.0
good_head = 0.0
bad_head = 0.0
teams_tied = 0.0
#ratings = [0,0,0,0,0,0,0,0,0,0,0]
#diff = 0.0

for run in range(0, number_of_simulations):
	for i in range(0, conference_size):
		teams[i] = {"rating" : random.randrange(lowest_rating,highest_rating,1), "win": [], "loss" : [], "name" : i, "sort" : random.randrange(0,100000,1), "sort2" : random.randrange(0, 100000, 1)}
	for i in range(0, conference_size):
		for j in range(i+1, conference_size):
			rating1 = teams[i]["rating"]
			rating2 = teams[j]["rating"]
			if home_teams:
				if j-i <= (conference_size / 2.0):
					rating1 += home_advantage
				else:
					rating2 += home_advantage
			#diff += abs(rating2 - rating1)
			win_prob = elo_win_chance(rating1, rating2)
			result = random.uniform(0,1)
			if result < win_prob:
				teams[i]["win"].append(teams[j]["name"])
				teams[j]["loss"].append(teams[i]["name"])
			else:
				teams[i]["loss"].append(teams[j]["name"])
				teams[j]["win"].append(teams[i]["name"])

	teams_sorted_wins = sorted(teams.values(), naive_ranking)
	teams_sorted_head_to_head = sorted(teams.values(), head_to_head_ranking)
	teams_sorted_rating = sorted(teams.values(), rating_ranking)

	# ratings average to check the random values are actually random
	#for team in teams.values():
	#	ratings[team["name"]] += team["rating"]

	if teams_sorted_rating[0] == teams_sorted_wins[0]:
		good_naive += 1
	else:
		bad_naive += 1
	if teams_sorted_head_to_head[0] == teams_sorted_rating[0]:
		good_head += 1
	else:
		bad_head += 1
	if len(teams_sorted_wins[0]["win"]) == len(teams_sorted_wins[1]["win"]):
		teams_tied += 1


chance_naive =  good_naive / (good_naive + bad_naive)
chance_head = good_head / (good_head + bad_head)
chance_tied = teams_tied / (good_naive + bad_naive)

print "In " + str(number_of_simulations) + " conference winners tied " + str(chance_tied) + "% of the time"
print "Random ranking matched the best team " + str(chance_naive) + "% of the time"
print "Head to head ranking matched the best team " + str(chance_head) + "% of the time"
z_score_significance_test = abs((chance_head - chance_naive) / (math.sqrt(((chance_naive) * (1.0 - chance_naive)) / number_of_simulations)))
print "z-score significance test value is " + str(z_score_significance_test)

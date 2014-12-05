import sys
import os
import random
import math

def elo_win_chance(my_rating, opp_rating):
	return 1.0 / (1.0 + pow(10, (opp_rating - my_rating) / 400.0))

def naive_ranking(team1, team2):
	if len(team2["win"]) != len(team1["win"]):
		return len(team2["win"]) - len(team1["win"])
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
	return team2["name"] - team1["name"]

conference_size = 2
number_of_simulations = 500000
teams = {}
home_teams = True

good_naive = 0.0
bad_naive = 0.0
good_head = 0.0
bad_head = 0.0
teams_tied = 0.0
ratings = [0,0,0,0,0,0,0,0,0,0,0]
diff = 0.0
win_avg = 0.0

for run in range(0, number_of_simulations):
	for i in range(0, conference_size):
		teams[i] = {"rating" : random.randrange(1700,1800,1), "win": [], "loss" : [], "name" : i, "sort" : random.randrange(0,100000,1)}
	for i in range(0, conference_size):
		for j in range(i+1, conference_size):
			rating1 = teams[i]["rating"]
			rating2 = teams[j]["rating"]
			if home_teams:
				rating2 += 0
				#rating2 += 200
				#if j-i <= (conference_size / 2.0):
				#	rating1 += 50
				#else:
				#	rating2 += 500
			diff += abs(rating2 - rating1)
			win_prob = elo_win_chance(rating1, rating2)
			#print elo_win_chance(rating1, rating2) + elo_win_chance(rating2, rating1)
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

	#print teams_sorted_rating

	#print "--"
	#for team in teams_sorted_wins:
	#	print team["rating"], len(team["win"]), len(team["loss"])

	for team in teams.values():
		ratings[team["name"]] += team["rating"]

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
		#print "--"
		#for team in teams_sorted_wins:
		#	print team["name"], team["rating"], team["win"], team["loss"]


chance_naive =  good_naive / (good_naive + bad_naive)
chance_head = good_head / (good_head + bad_head)
chance_tied = teams_tied / (good_naive + bad_naive)

print chance_naive, chance_head, number_of_simulations, chance_tied
z_score_significance_test = abs((chance_head - chance_naive) / (math.sqrt(((chance_naive) * (1.0 - chance_naive)) / number_of_simulations)))
print z_score_significance_test
print diff / number_of_simulations
#print win_avg / number_of_simulations
#for rating in ratings:
#	print rating / float(number_of_simulations)
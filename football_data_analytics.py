import numpy as np 
import pandas as pd
import math
import sys
import inquirer

''' Models the poisson distribution (finding the probability of goals scored 0-10) for each team '''
def poisson_distribution(mode, homeTeamData, awayTeamData): 
    poisson = lambda lam, k: ((lam**k)*(math.e**(-lam)))/math.factorial(k)

    goal_probabilities = []
    l = 0

    ''' The mode decides whether expected goals are used or average goals '''
    if mode == 2:
        l = float(homeTeamData['xG']) * float(awayTeamData['xGA'])
    else:
        #TODO: create offensive/defensive strenght measurement
        l = float(homeTeamData['xG']) * float(awayTeamData['xGA'])

    for i in range(10):
        goal_probabilities.append(poisson(lam=l, k=i))


    return goal_probabilities

''' Helper function to get team stats from the data '''
def get_team_stats(homeTeam, awayTeam):
    homeDataFrame, awayDataFrame = parse() 

    homeTeamData = {
        'Team': "",
        'Goals': "",
        "Shots pg": "", 
        "Possession%": "", 
        "Pass%": "", 
        "AerialsWon": "", 
        "Rating": "", 
        "xG": "", 
        "xGA": "",
    }

    for i in range(len(homeDataFrame['Team'])):
        if homeTeam == homeDataFrame['Team'][i]:
            homeTeamData['Team'] = homeDataFrame['Team'][i]
            homeTeamData['Goals'] = homeDataFrame['Goals'][i]
            homeTeamData['Shots pg'] = homeDataFrame['Shots pg'][i]
            homeTeamData["Possession%"] = homeDataFrame['Possession%'][i]
            homeTeamData["Pass%"] = homeDataFrame['Pass%'][i]
            homeTeamData["AerialsWon"] = homeDataFrame['AerialsWon'][i]
            homeTeamData["Rating"] = homeDataFrame['Rating'][i]
            homeTeamData["xG"] = homeDataFrame['xG'][i]
            homeTeamData["xGA"] = homeDataFrame['xGA'][i]
            break

    awayTeamData = {
        'Team': "",
        'Goals': "",
        "Shots pg": "", 
        "Possession%": "", 
        "Pass%": "", 
        "AerialsWon": "", 
        "Rating": "", 
        "xG": "", 
        "xGA": "",
    }

    for i in range(len(awayDataFrame['Team'])):
        if awayTeam == awayDataFrame['Team'][i]:
            awayTeamData['Team'] = awayDataFrame['Team'][i]
            awayTeamData['Goals'] = awayDataFrame['Goals'][i]
            awayTeamData['Shots pg'] = awayDataFrame['Shots pg'][i]
            awayTeamData["Possession%"] = awayDataFrame['Possession%'][i]
            awayTeamData["Pass%"] = awayDataFrame['Pass%'][i]
            awayTeamData["AerialsWon"] = awayDataFrame['AerialsWon'][i]
            awayTeamData["Rating"] = awayDataFrame['Rating'][i]
            awayTeamData["xG"] = awayDataFrame['xG'][i]
            awayTeamData["xGA"] = awayDataFrame['xGA'][i]
            break

    return homeTeamData, awayTeamData

''' Uses the match_predictor function and compares the results against actual premier league results to find how accurate the predictor is '''
def parse_result_fixtures(mode):
    f = open("results.txt", "r")

    score_predictions = []
    result_predictions = []
    differences_predictions = []
    perfect_predictions = []

    index = 0

    for i in range(214):
        homeTeam = f.readline().rstrip("\n")
        score = f.readline().split("-")
        score[0] = int(score[0])
        score[1] = int(score[1].rstrip(" \n"))
        awayTeam = f.readline().rstrip("\n")

        result = ""
        if score[0] > score[1]:
            result = "{0} win".format(homeTeam)
        elif score[1] > score[0]:
            result = "{0} win".format(awayTeam)
        else:
            result = "Draw"

        difference = abs(score[0] - score[1])

        homeTeamPrediction, awayTeamPrediction = match_predicitor(mode, homeTeam, awayTeam)

        differencePrediction = abs(homeTeamPrediction - awayTeamPrediction)

        resultPrediction = ""
        if homeTeamPrediction > awayTeamPrediction:
            resultPrediction = "{0} win".format(homeTeam)
        elif awayTeamPrediction > homeTeamPrediction:
            resultPrediction = "{0} win".format(awayTeam)
        else:
            resultPrediction = "Draw"

        if resultPrediction == result:
            result_predictions.append(1)
        else:
            result_predictions.append(0)

        if homeTeamPrediction == score[0] and awayTeamPrediction == score[1]:
            score_predictions.append(1)
        else:
            score_predictions.append(0)

        if resultPrediction == result and homeTeamPrediction == score[0] and awayTeamPrediction == score[1]:
            perfect_predictions.append(1)
        else:
            perfect_predictions.append(0)

        if differencePrediction == difference:
            differences_predictions.append(1)
        else:
            differences_predictions.append(0)

        print("Actual result: {0} {1}:{2} {3} | Predicted Result: {4} {5}:{6} {7}".format(homeTeam, score[0], score[1], awayTeam, homeTeam, homeTeamPrediction, awayTeamPrediction, awayTeam))

    results_percent = sum(result_predictions)/len(result_predictions)*100
    scores_percent = sum(score_predictions)/len(score_predictions)*100
    perfect_percent = sum(perfect_predictions)/len(perfect_predictions)*100
    differences_percent = sum(differences_predictions)/len(differences_predictions)*100

    print("\n-----------------------------------------------")
    print("Results predicted:\t\t\t{0:.2f}%".format(results_percent))
    print("Scores predicted:\t\t\t{0:.2f}%".format(scores_percent))
    print("Score line differences predicted:\t{0:.2f}%".format(differences_percent))
    print("Perfect results predicted:\t\t{0:.2f}%".format(perfect_percent))
    print("-----------------------------------------------\n")

    return 0

''' Parse the data into data frames for later use '''
def parse():
    home_txt = open("stats_home.txt", "r")
    away_txt = open("stats_away.txt", "r")

    columns = ["Team", "Goals", "Shots pg", "Discipline", "Possession%", "Pass%", "AerialsWon", "Rating", "xG", "xGA"]

    home_lines = []
    away_lines = []

    ''' Read in the lines from the home stats file '''
    for line in home_txt:
        home_lines.append(line.split("\t"))

    ''' Read in the lines from the away stats file '''
    for line in away_txt:
        away_lines.append(line.split("\t"))

    homeDataFrame = pd.DataFrame(home_lines, columns = columns)
    homeDataFrame = homeDataFrame.replace(r'\n',' ', regex=True) 
    homeDataFrame.drop(['Discipline'], axis=1)

    awayDataFrame = pd.DataFrame(away_lines, columns = columns)
    awayDataFrame = awayDataFrame.replace(r'\n',' ', regex=True) 
    awayDataFrame.drop(['Discipline'], axis=1)

    home_txt.close()
    away_txt.close()

    return homeDataFrame, awayDataFrame

''' Match predictor based on the data '''
def match_predicitor(mode, homeTeam, awayTeam):
    homeTeamData, awayTeamData = get_team_stats(homeTeam, awayTeam)

    homeTeamGoalProbabilities = poisson_distribution(mode, homeTeamData, awayTeamData)
    awayTeamGoalProbabilities = poisson_distribution(mode, awayTeamData, homeTeamData)

    maxHomeTeamGoals = 0
    maxHomeTeamGoalsProbabilities = 0
    maxAwayTeamGoals = 0
    maxAwayTeamGoalsProbabilities = 0

    ''' Finds the maximum probability of the number of goals scored by both teams, then calculates the probability of that outcome '''
    for i in range(len(homeTeamGoalProbabilities)):
        if homeTeamGoalProbabilities[i] > maxHomeTeamGoalsProbabilities:
            maxHomeTeamGoalsProbabilities = homeTeamGoalProbabilities[i]
            maxHomeTeamGoals = i
        if awayTeamGoalProbabilities[i] > maxAwayTeamGoalsProbabilities:
            maxAwayTeamGoalsProbabilities = awayTeamGoalProbabilities[i]
            maxAwayTeamGoals = i

    matchOutcomeProbability = (maxHomeTeamGoalsProbabilities * maxAwayTeamGoalsProbabilities) * 100

    if mode == 1:
        print("\n-------------- Game prediction -------------")
        print("{0} {1} : {2} {3} with probability {4:.2f}%".format(homeTeam, maxHomeTeamGoals, maxAwayTeamGoals, awayTeam, matchOutcomeProbability))
        print("--------------------------------------------\n")

    return maxHomeTeamGoals, maxAwayTeamGoals

if __name__ == '__main__':
    print("\n--------------------------------------------")
    print("Welcome to Damon's football match predictor!")
    print("--------------------------------------------")
    mode = int(input("Please choose mode:\n1 = match predictor,\n2 = results comparison (expected goals),\n3 = results comparison (average goals),\nInput : "))
    if mode == 1:
        homeTeam = input("Please enter the home team: ")
        awayTeam = input("Please enter the away team: ")
        match_predicitor(mode, homeTeam, awayTeam)
    elif mode == 2 or mode == 3:
        parse_result_fixtures(mode)
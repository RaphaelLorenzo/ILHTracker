# -*- coding: utf-8 -*-
"""
Created on Sat May 20 15:36:22 2023

@author: rapha
"""
from raylib import *
from pyray import *
import time
from time import strftime
from time import gmtime

import pandas as pd

AZERTY_MAP_PD = pd.read_csv("azertymap.csv", sep = ";")
AZERTY_MAP = {}
for (char, code) in zip(AZERTY_MAP_PD["character"], AZERTY_MAP_PD["code"]):
    AZERTY_MAP[code] = char
AZERTY_MAP[32] = " "
AZERTY_MAP[59] = "m"

import numpy as np

from ihm_hockeytrack_data import *

SCREEN_HEIGHT = 1900
SCREEN_WIDTH = 2900

# SCREEN_HEIGHT = 1080
# SCREEN_WIDTH = 1920

#### GLOBAL VARIABLES #####

# SCREEN_HEIGHT = GetScreenHeight()
# SCREEN_WIDTH = GetScreenWidth()
WIDTH_RATIO = (SCREEN_WIDTH / 1920)
HEIGHT_RATIO = (SCREEN_HEIGHT / 1080)

input_touch_screen = False # For Windows Surface use another kind of click detection

# Time management
is_paused = True
is_team_a_possess = False
is_team_b_possess = False

time_start = time.time()
time_absolute = 0
time_game = 0 # Add in game_data and set at loading

time_team_a = 0 # Add in game_data and set at loading
time_team_b = 0 # Add in game_data and set at loading

period_counter = 1

# Side management
are_goalies_switched = True # Default to first period where goalies are switched, regarding the team bench sides

# Menu management
is_field_touch_menu_on = False
is_field_touch_menu_to_close = False
last_shot_touch_relative_x = 0
last_shot_touch_relative_y = 0
last_shot_relative_x = 0
last_shot_relative_y = 0

# Score management
goals_A = 0
goals_B = 0

# Goalie managment
current_goalie_num_a = -1
swap_goalies_a = False
current_goalie_num_b = -1
swap_goalies_b = False

# Player stats managment
time_shots_stats_switch = True #true = time, false = shots

# Shot managment
is_any_shooter_a = False
is_any_shooter_b = False
shot_types = ["wrist", "slap", "snap", "backh", "tip", "other"]
is_shot_type = [False for i in shot_types]
shot_results = ["goal", "missed", "blocked", "covered", "rebound"]
is_shot_result = [False for i in shot_results]

DUMMY_PLAYER = {"licence": 999999, "name":"dummy", "num": -1, "poste":"def", "is_on_field":False,   "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False}
DUMMY_PLAYER["stick_side"] = "right"
DUMMY_PLAYER["is_current_blocker_of_shoot"] = False
#add other attributes

# duel management
duel_win_by_team_A = False
duel_win_by_team_B = False

# Faceoff management
faceoff_win_by_team_A = False
faceoff_win_by_team_B = False
is_faceoff_in_center = False

IS_GAME_STARTED = False

def set_timers(tG, tA, tB):
    global time_game
    global time_team_a
    global time_team_b

    time_game = tG
    time_team_a = tA
    time_team_b = tB

# Game data loading
# GAME_DATA = pd.from_csv()
def load_game_data_default():
    GAME_DATA = {}
    # Load players of team A
    players_a_list = [{"licence": 300101, "name":"paul", "num": 18, "poste":"def", "is_on_field":False,   "time_on_field":0, "time_on_field_total":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300102, "name":"momo", "num": 53, "poste":"for", "is_on_field":False,   "time_on_field":0, "time_on_field_total":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300103, "name":"axel", "num": 35, "poste":"for", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300104, "name":"alexis", "num": 21, "poste":"def", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300105, "name":"arthur", "num": 71, "poste":"for", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300999, "name":"pierre", "num": 87, "poste":"def", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300010, "name":"obeid", "num": 31, "poste":"def", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300011, "name":"matteo", "num": 32, "poste":"for", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300012, "name":"mael", "num": 96, "poste":"for", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300013, "name":"lucas", "num": 93, "poste":"def", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300014, "name":"jaime", "num": 30, "poste":"def", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300015, "name":"theo", "num": 19, "poste":"def", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300016, "name":"gaetan", "num": 8, "poste":"goalie", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300017, "name":"julien", "num": 9, "poste":"goalie", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300018, "name":"xxx", "num": 45, "poste":"for", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      {"licence": 300019, "name":"uyyyy", "num": 46, "poste":"for", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                      ]
    # Sort by num
    players_a_num = [player["num"] for player in players_a_list]
    sort_by_num_index = np.argsort(players_a_num)
    players_a_list = [players_a_list[i] for i in sort_by_num_index]
    
    # Load players of team B
    players_b_list = [{"licence": 300106, "name":"pierre", "num": 11, "poste":"def", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                    {"licence": 300107, "name":"paul", "num": 12, "poste":"for", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                    {"licence": 300108, "name":"jacques", "num": 13, "poste":"for", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                    {"licence": 300109, "name":"angus", "num": 14, "poste":"def", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                    {"licence": 300110, "name":"glenn", "num": 15, "poste":"for", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                    {"licence": 300111, "name":"faust", "num": 16, "poste":"def", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False},
                    {"licence": 300199, "name":"garance", "num": 2, "poste":"goalie", "is_on_field":False,  "time_on_field":0, "time_on_field_total":0, "is_current_shooter":False, "is_current_passer":False, "is_involved_in_duel":False, "is_involved_in_faceoff":False}
                    ]
    
    # Add other default value...
    for player in players_a_list + players_b_list:
        player["stick_side"] = "right"
        player["is_current_blocker_of_shoot"] = False
    
    # Sort by num
    players_b_num = [player["num"] for player in players_b_list]
    sort_by_num_index = np.argsort(players_b_num)
    players_b_list = [players_b_list[i] for i in sort_by_num_index]
    
    shots_A = []
    shots_B = []
    GAME_DATA = {
                "team_name_A":b"Ligue IDF",
                "team_name_B":b"Ligue AURA",
                "team_short_name_A":b"IDF",
                "team_short_name_B":b"AURA",
                "team_color_A":GOLD,
                "team_color_B":VIOLET,
                "time_game" : 0,
                "time_team_A": 0,
                "time_team_B": 0,
                "Players_A":players_a_list,
                "Players_B":players_b_list,
                "shots_A":shots_A,
                "shots_B":shots_B,
                "duels":[],
                "faceoffs":[]
                }
    
    #Extend game_data

    print(GAME_DATA)
    return(GAME_DATA)


def get_team_short_name(team, GAME_DATA):
    if not (team == "A" or team == "B"):
        print("[ERROR] Invalid team name : %s (expecting 'A' or 'B'!"%team)
        return -1
    else:
        sname_str = "team_short_name_" + team
        short_name = GAME_DATA[sname_str]

        return short_name

def get_team_name(team, GAME_DATA):
    if not (team == "A" or team == "B"):
        print("[ERROR] Invalid team name : %s (expecting 'A' or 'B'!"%team)
        return -1
    else:
        name_str = "team_name_" + team
        name = GAME_DATA[name_str]

        return name

def get_team_color(team, GAME_DATA):
    if not (team == "A" or team == "B"):
        print("[ERROR] Invalid team name : %s (expecting 'A' or 'B'!"%team)
        return -1
    else:
        color_str = "team_color_" + team
        color = GAME_DATA[color_str]

        return color
    

def get_current_goalkeeper(team, GAME_DATA):
    """
    Get the current present goalkeeper for a team ('A' or 'B') using the global GAME_DATA
    Returns a player object (dict with attributes)
    """
    if not (team == "A" or team == "B"):
        print("[ERROR] Invalid team name : %s (expecting 'A' or 'B'!"%team)
        return DUMMY_PLAYER
    else:
        players_str = "Players" + "_" + team
        players = GAME_DATA[players_str]
        for player in players:
            if (player["poste"]=="goalie") and (player["is_on_field"]==True):
                return player
            
        return DUMMY_PLAYER

def get_current_present_players(team, GAME_DATA):
    """
    Get the current present players for a team ('A' or 'B') using the global GAME_DATA
    Returns a list player objects (dict with attributes)
    """
    if not (team == "A" or team == "B"):
        print("[ERROR] Invalid team name : %s (expecting 'A' or 'B'!"%team)
        return -1
    else:
        players_present = []
        players_str = "Players" + "_" + team
        players = GAME_DATA[players_str]
        for player in players:
            if (player["is_on_field"]==True):
                players_present.append(player)

        return players_present

def get_goal_count(team, GAME_DATA):
    if not (team == "A" or team == "B"):
        print("[ERROR] Invalid team name : %s (expecting 'A' or 'B'!"%team)
        return -1
    else:
        count_goals = 0
        shots_str = "shots" + "_" + team
        for shot in GAME_DATA[shots_str]:
            if shot["result_of_shot"] == "goal":
                count_goals+=1

        return(count_goals)

def DrawTextCenteredInRoundedRectangle(text, fontsize, textcolor, x, y, width, height, roundness, color, border_width, border_color):
    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)
    text_width = MeasureText(text, fontsize)
    if border_width >= 1:
        DrawRectangleRounded(Rectangle(x - border_width, y - border_width, width + 2 * border_width, height + 2 * border_width), roundness, -1, border_color)
    
    DrawRectangleRounded(Rectangle(x, y, width, height), roundness, -1, color)
    y_text = int(y + (height - fontsize) / 2)
    DrawText(text, int(x + (width - text_width)/2),y_text, fontsize, textcolor)


def make_stackbar_graph(x, y, width, height, value_a, value_b, value_none, GAME_DATA):
    """
    Use value_none = None if nothing to put
    """
    if value_none is not None:
        total_vals = value_a + value_b + value_none
        if total_vals == 0:
            prop_none = 0.34
            prop_a = 0.33
            prop_b = 0.33
        else:
            prop_none = value_none / total_vals
            prop_a = value_a / total_vals
            prop_b = value_b / total_vals
    else:
        total_vals = value_a + value_b
        prop_none = 0    
        if total_vals == 0:
            prop_a = 0.5
            prop_b = 0.5
        else:
            prop_a = value_a / total_vals
            prop_b = value_b / total_vals

    height_a = int(height * prop_a)
    height_b = int(height * prop_b)
    height_none = int(height * prop_none)

    DrawTextCenteredInRoundedRectangle(b"%d"%(int(prop_a*100)), 20, BLACK, x, y, width, height_a, 0, get_team_color("A", GAME_DATA), 0, WHITE)
    DrawRectangleRec(Rectangle(x, y + height_a, width, height_none), GRAY)
    DrawTextCenteredInRoundedRectangle(b"%d"%(int(prop_b*100)), 20, BLACK, x, y + height_a + height_none, width, height_b, 0, get_team_color("B", GAME_DATA), 0, WHITE)

def is_touch_input_intersecting_with_rectangle(touch_x, touch_y, x, y, width, height):
    if (touch_x > x) and (touch_x < x + width) and (touch_y > y) and (touch_y < y + height):
        return True
    else:
        return False

def get_touch_relative_rectangle_position(touch_x, touch_y, x, y, width, height):
    if (touch_x > x) and (touch_x < x + width) and (touch_y > y) and (touch_y < y + height):
        relative_x = (touch_x - x) / width
        relative_y = (touch_y - y) / height
        return relative_x, relative_y
    else:
        return 0, 0
    
def make_color_toggle(x, y, width, height, value, frame_width, frame_color, text, text_size_relative = 0.8, color_false = WHITE, color_true = GREEN):
    rec_frame = Rectangle(x-frame_width, y-frame_width, width+frame_width*2, height+frame_width*2)
    text = text #.encode('ascii')
    DrawRectangleRec(rec_frame, Fade(frame_color, 0.9))
    # value = GuiToggle(Rectangle(x, y, width, height), b"", value)
    if (value):
        DrawRectangleRec(Rectangle(x, y, width, height), color_true)
    else:
        DrawRectangleRec(Rectangle(x, y, width, height), color_false)

    text_height = int(height * text_size_relative)
    text_width = MeasureText(text, text_height)
    DrawText(text, int(x + int((width - text_width)/2)), int(y + int((height - text_height) / 2)), text_height, BLACK)
    return value


def click_color_toggle(touch_input, touch_x, touch_y, x, y, width, height, value, frame_width = 0):
    if touch_input and is_touch_input_intersecting_with_rectangle(touch_x, touch_y, x - frame_width, y - frame_width, width + frame_width * 2, height + frame_width * 2):
        value = not value

    return value


def DrawCircleLinesFat(center_x, center_y, radius, color, thickness):
    """
    Draw multiple circles to give thickness
    """
    half_thickness = int(thickness/2)
    for off in range(-half_thickness, half_thickness):
        DrawCircleLines(center_x, center_y, radius + off, color)


DUMMY_SHOT =  {
            "time_absolute":0, 
            "time_game":0, 
            "period":1,
            "team_shooter" : "TEAM A",
            "team_shooter_id": 0,
            "pos_x": 0.5,
            "pos_y": 0.5,
            "pos_on_cage_x": 0.5,
            "pos_on_cage_y": 0.5,
            "pos_on_shooting_frame_x": 0.5, # wider shooting frame to indicates pos of missed shots
            "pos_on_shooting_frame_y": 0.5, # wider shooting frame to indicates pos of missed shots
            "shot_from_zone": "off", #shot_from_zone is either "off" or "def" and indicates whether the player was in its own offensive or defensive zone / side of the field, so pos_x and pos_y can make sense for both sides on afterwards analysis
            "shooter": -1,
            "assits": [-1, -1],
            "opponent_goalkeeper": -1,
            "present_players_shooter": [-1, -1, -1],
            "present_players_opponent": [-1, -1, -1],
            "type_of_shot": "wrist",
            "result_of_shot": "missed",
            "numeric_strength":"equal", #either equal, inf or sup
            "blocker_of_shot":-1
            }

def get_shot_dict(time_absolute, time_game, period, pos_x, pos_y, pos_on_cage_x, pos_on_cage_y, pos_on_shooting_frame_x, pos_on_shooting_frame_y, shot_from_zone, shooter, assists, team_shooter, type_of_shot, result_of_shot, numeric_strength, GAME_DATA):
    if team_shooter == "A":
        team_id = 0
        team_opponent = "B"
    elif team_shooter == "B":
        team_id = 1
        team_opponent = "A"
    else:
        team_id = -1
        print("TEAM %s is not supported ['A' or 'B']"%team_shooter)

    opponent_goalkeeper = get_current_goalkeeper(team_opponent, GAME_DATA)["num"]
    present_players_shooter = [player["num"] for player in get_current_present_players(team_shooter, GAME_DATA)]
    present_players_opponent = [player["num"] for player in get_current_present_players(team_opponent, GAME_DATA)]

    blocker_of_shot = -1
    for player in get_current_present_players(team_opponent, GAME_DATA):
        if player["is_current_blocker_of_shoot"]:
            blocker_of_shot = player["num"]
            break

    shot = {
            "time_absolute":time_absolute, 
            "time_game":time_game, 
            "period":period,
            "team_shooter" : get_team_name(team_shooter, GAME_DATA),
            "team_shooter_id": team_id,
            "pos_x":pos_x,
            "pos_y":pos_y,
            "pos_on_cage_x": pos_on_cage_x,
            "pos_on_cage_y": pos_on_cage_y,
            "pos_on_shooting_frame_x": pos_on_shooting_frame_x, # wider shooting frame to indicates pos of missed shots
            "pos_on_shooting_frame_y": pos_on_shooting_frame_y, # wider shooting frame to indicates pos of missed shots
            "shot_from_zone":shot_from_zone, #shot_from_zone is either "off" or "def" and indicates whether the player was in its own offensive or defensive zone / side of the field, so pos_x and pos_y can make sense for both sides on afterwards analysis
            "shooter":shooter,
            "assits": assists,
            "opponent_goalkeeper": opponent_goalkeeper,
            "present_players_shooter": present_players_shooter,
            "present_players_opponent": present_players_opponent,
            "type_of_shot": type_of_shot,
            "result_of_shot": result_of_shot,
            "numeric_strength":numeric_strength, #either equal, inf or sup
            "blocker_of_shot": blocker_of_shot
            }
    
    return shot

def get_shots_on_goal_by_player_team_and_num(team, num, GAME_DATA):
    # Différencier tirs bloqués des tirs cadrés
    team_shots_str = "shots_" + team
    count_shots = 0
    count_shots_on_goal = 0
    count_goals = 0
    for shot in GAME_DATA[team_shots_str]:
        if shot["shooter"] == num:
            count_shots += 1
            if shot["result_of_shot"] != "missed":
                count_shots_on_goal += 1
                if shot["result_of_shot"] == "goal":
                    count_goals += 1

    return count_shots, count_shots_on_goal, count_goals

def get_shots_on_goal_by_team(team, GAME_DATA):
    shots_count = len(GAME_DATA["shots_"+team])
    shots_on_goal = [shot for shot in GAME_DATA["shots_"+team] if shot["result_of_shot"]!="missed"]
    shots_on_goal_count = len(shots_on_goal)
    return shots_count, shots_on_goal_count

def get_faceoffs_win_by_team(team, GAME_DATA):
    count = 0
    faceoffs = GAME_DATA["faceoffs"]
    for fo in faceoffs:
        if fo["winning_team"] == team:
            count+=1
    return count

DUMMY_DUEL = {
            "time_absolute":0, 
            "time_game":0, 
            "period":1,
            "winning_team" : "A",
            "pos_x":0.5,
            "pos_y":0.5,
            "is_in_offensive_zone":False, # to make sense for afterward analysis
            "involved_players_A": [0,1],
            "involved_players_B": [3,5],
            "present_players_A": [0,1,2,6],
            "present_players_B": [3,5,7,8],
            "numeric_strength":"equal" #either equal, inf or sup
            }

def get_duel_dict(time_absolute, time_game, period, pos_x, pos_y, involved_players_A, involved_players_B, winning_team, is_in_offensive_zone, GAME_DATA):
    if winning_team == "A":
        team_opponent = "B"
    elif winning_team == "B":
        team_opponent = "A"
    else:
        print("TEAM %s is not supported ['A' or 'B']"%winning_team)

    present_players_team_A = [player["num"] for player in get_current_present_players("A", GAME_DATA)]
    present_players_team_B = [player["num"] for player in get_current_present_players("B", GAME_DATA)]

    numeric_strength = "equal"
    if len(get_current_present_players(winning_team, GAME_DATA)) > len(get_current_present_players(team_opponent, GAME_DATA)): 
        numeric_strength = "sup"
    elif len(get_current_present_players(winning_team, GAME_DATA)) < len(get_current_present_players(team_opponent, GAME_DATA)): 
        numeric_strength = "inf"

    duel = {
            "time_absolute":time_absolute, 
            "time_game":time_game, 
            "period":period,
            "winning_team" : winning_team,
            "pos_x":pos_x,
            "pos_y":pos_y,
            "is_in_offensive_zone":is_in_offensive_zone, # to make sense for afterward analysis
            "involved_players_A":involved_players_A,
            "involved_players_B": involved_players_B,
            "present_players_A": present_players_team_A,
            "present_players_B": present_players_team_B,
            "numeric_strength":numeric_strength #either equal, inf or sup
            }
    
    return duel


DUMMY_FACEOFF = {
            "time_absolute":0, 
            "time_game":0, 
            "period":1,
            "winning_team" : "A",
            "pos_x":0.5,
            "pos_y":0.5,
            "is_in_offensive_zone":True, # to make sense for afterwards analysis
            "is_faceoff_in_center":True,
            "involved_players_A":[2],
            "involved_players_B": [4],
            "present_players_A": [2,8,7,6],
            "present_players_B": [2,9,19,87],
            "numeric_strength":"equal" #either equal, inf or sup
            }

def get_faceoff_dict(time_absolute, time_game, period, pos_x, pos_y, involved_players_A, involved_players_B, winning_team, is_in_offensive_zone, is_faceoff_in_center, GAME_DATA):
    if winning_team == "A":
        team_opponent = "B"
    elif winning_team == "B":
        team_opponent = "A"
    else:
        print("TEAM %s is not supported ['A' or 'B']"%winning_team)

    present_players_team_A = [player["num"] for player in get_current_present_players("A", GAME_DATA)]
    present_players_team_B = [player["num"] for player in get_current_present_players("B", GAME_DATA)]

    numeric_strength = "equal"
    if len(get_current_present_players(winning_team, GAME_DATA)) > len(get_current_present_players(team_opponent, GAME_DATA)): 
        numeric_strength = "sup"
    elif len(get_current_present_players(winning_team, GAME_DATA)) < len(get_current_present_players(team_opponent, GAME_DATA)): 
        numeric_strength = "inf"

    faceoff = {
            "time_absolute":time_absolute, 
            "time_game":time_game, 
            "period":period,
            "winning_team" : winning_team,
            "pos_x":pos_x,
            "pos_y":pos_y,
            "is_in_offensive_zone":is_in_offensive_zone, # to make sense for afterwards analysis
            "is_faceoff_in_center":is_faceoff_in_center,
            "involved_players_A":involved_players_A,
            "involved_players_B": involved_players_B,
            "present_players_A": present_players_team_A,
            "present_players_B": present_players_team_B,
            "numeric_strength":numeric_strength #either equal, inf or sup
            }
    
    return faceoff

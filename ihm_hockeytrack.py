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
import numpy as np

from ihm_hockeytrack_utils import *
from ihm_hockeytrack_startmenu import *

GAME_DATA = load_game_data()

def make_time_pannel(x, y, width, height, touch_input, touch_input_x, touch_input_y):
    global is_team_a_possess
    global is_team_b_possess
    global is_paused
    global time_absolute
    global time_game

    DrawRectangleRec(Rectangle(x, y, width, height), GRAY)

    make_color_toggle(x + int(WIDTH_RATIO * 50), y + int(HEIGHT_RATIO * 50), int(WIDTH_RATIO * 200), int(HEIGHT_RATIO * 100), is_team_a_possess, 10, get_team_color("A", GAME_DATA), get_team_short_name("A", GAME_DATA), 0.5)
    is_team_a_possess = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 50), y + int(HEIGHT_RATIO * 50), int(WIDTH_RATIO * 200), int(HEIGHT_RATIO * 100), is_team_a_possess, 10)
    
    if is_key_pressed(KEY_P):
        # P in azerty
        is_team_a_possess = not is_team_a_possess
        if is_team_a_possess:
            is_team_b_possess = False
            is_paused = False

    if is_team_a_possess:
        is_paused = False
        is_team_b_possess = False

    make_color_toggle(x + int(WIDTH_RATIO * 50), y + int(HEIGHT_RATIO * 200), int(WIDTH_RATIO * 200), int(HEIGHT_RATIO * 100), is_team_b_possess, 10, get_team_color("B", GAME_DATA), get_team_short_name("B", GAME_DATA), 0.5)
    is_team_b_possess = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 50), y + int(HEIGHT_RATIO * 200), int(WIDTH_RATIO * 200), int(HEIGHT_RATIO * 100), is_team_b_possess, 10)

    if is_key_pressed(KEY_L):
        is_team_b_possess = not is_team_b_possess
        if is_team_b_possess:
            is_team_a_possess = False
            is_paused = False

    if is_team_b_possess:
        is_paused = False
        is_team_a_possess = False

    if (not is_team_a_possess) and (not is_team_b_possess):
        is_paused = True
    
    time_since_start_iters_str = strftime("%M:%S", gmtime(time_game)).encode('ascii')
    time_since_start_str = strftime("%M:%S", gmtime(time_absolute)).encode('ascii')
    time_team_a_str = strftime("%M:%S", gmtime(time_team_a)).encode('ascii')
    time_team_b_str = strftime("%M:%S", gmtime(time_team_b)).encode('ascii')


    DrawText(b"Time played %s"%(time_since_start_iters_str), x + int(WIDTH_RATIO * 50), y + int(HEIGHT_RATIO * 350), 20, BLACK)
    DrawText(b"Time absolute %s"%(time_since_start_str), x + int(WIDTH_RATIO * 50), y + int(HEIGHT_RATIO * 380), 20, BLACK)
    DrawText(b"Time TEAM A %s"%(time_team_a_str), x + int(WIDTH_RATIO * 50), y + int(HEIGHT_RATIO * 410), 20, BLACK)
    DrawText(b"Time TEAM B %s"%(time_team_b_str), x + int(WIDTH_RATIO * 50), y + int(HEIGHT_RATIO * 440), 20, BLACK)

    return is_team_a_possess, is_team_b_possess, is_paused

def make_inline_hockey_terrain(x, y, width, height, faceoff_zone = None):
    global are_goalies_switched

    DrawRectangleRounded(Rectangle(x - 3, y - 3, width + 6, height + 6), 0.33, -1, BLUE)
    DrawRectangleRounded(Rectangle(x, y, width, height), 0.33, -1, SKYBLUE)

    # compute size in pixels from size in meters
    pixel_per_m = height / 25
    circle_radius = int(3 * pixel_per_m)
    line_dist_from_end = int(3.8 * pixel_per_m)
    circle_center_x = int((6.1 + 3.8) * pixel_per_m)
    circle_center_y = int((2.8 + 3) * pixel_per_m)
    
    cage_zone_width = int(2.5 * pixel_per_m)
    cage_zone_depth = int(1.2 * pixel_per_m)
    cage_depth = int(1.3 * pixel_per_m)
    cage_width = int(1.8 * pixel_per_m)

    # draw cages
    DrawRectangleRounded(Rectangle(x + line_dist_from_end - cage_depth - 2, y + int(height / 2) - int(cage_width / 2) - 2, cage_depth + int(cage_depth/2) + 4, cage_width + 4), 0.6, -1, RED)
    DrawRectangleRounded(Rectangle(x + line_dist_from_end - cage_depth, y + int(height / 2) - int(cage_width / 2), cage_depth + int(cage_depth/2), cage_width), 0.6, -1, WHITE)

    DrawRectangleRounded(Rectangle(x + width - line_dist_from_end - int(cage_depth/2) - 2, y + int(height / 2) - int(cage_width / 2) - 2, cage_depth + int(cage_depth/2) + 4, cage_width + 4), 0.6, -1, RED)
    DrawRectangleRounded(Rectangle(x + width - line_dist_from_end - int(cage_depth/2), y + int(height / 2) - int(cage_width / 2), cage_depth + int(cage_depth/2), cage_width), 0.6, -1, WHITE)

    # draw goal zones
    goalie_a = get_current_goalkeeper("A", GAME_DATA)["num"]
    goalie_b = get_current_goalkeeper("B", GAME_DATA)["num"]

    if are_goalies_switched:
        #left
        DrawTextCenteredInRoundedRectangle(b"%d"%goalie_b, int(cage_zone_width/2), BLACK, x + line_dist_from_end + 2, y + int(height / 2) - int(cage_zone_width / 2), cage_zone_depth, cage_zone_width, 0.0, get_team_color("B", GAME_DATA), 0, BLACK)
        #right
        DrawTextCenteredInRoundedRectangle(b"%d"%goalie_a, int(cage_zone_width/2), BLACK, x + width - line_dist_from_end - 2 - cage_zone_depth, y + int(height / 2) - int(cage_zone_width / 2), cage_zone_depth, cage_zone_width, 0.0, get_team_color("A", GAME_DATA), 0, BLACK)
    else:
        #left
        DrawTextCenteredInRoundedRectangle(b"%d"%goalie_a, int(cage_zone_width/2), BLACK, x + line_dist_from_end + 2, y + int(height / 2) - int(cage_zone_width / 2), cage_zone_depth, cage_zone_width, 0.0, get_team_color("A", GAME_DATA), 0, BLACK)
        #right
        DrawTextCenteredInRoundedRectangle(b"%d"%goalie_b, int(cage_zone_width/2), BLACK, x + width - line_dist_from_end - 2 - cage_zone_depth, y + int(height / 2) - int(cage_zone_width / 2), cage_zone_depth, cage_zone_width, 0.0, get_team_color("B", GAME_DATA), 0, BLACK)

    # draw lines
    DrawRectangleRec(Rectangle(x + line_dist_from_end - 2, y, 4, height), RED)
    DrawRectangleRec(Rectangle(x + width - line_dist_from_end - 2, y, 4, height), RED)
    DrawRectangleRec(Rectangle(x + int(width/2) - 5, y, 10, height), RED)

    # draw circles
    DrawCircleLinesFat(x + circle_center_x, y + circle_center_y, circle_radius, RED, 4)
    DrawCircleLinesFat(x + width - circle_center_x, y + circle_center_y, circle_radius, RED, 4)
    DrawCircleLinesFat(x + circle_center_x, y + height - circle_center_y, circle_radius, RED, 4)
    DrawCircleLinesFat(x + width - circle_center_x, y + height - circle_center_y, circle_radius, RED, 4)
    DrawCircleLinesFat(int(x + width / 2), int(y + height / 2), circle_radius, RED, 4)
    if faceoff_zone is not None:
        if faceoff_zone == "bottom_left":
            DrawCircle(x + circle_center_x, y + circle_center_y, circle_radius, GREEN)
        elif faceoff_zone == "top_left":
            DrawCircle(x + circle_center_x, y + height - circle_center_y, circle_radius, GREEN)
        elif faceoff_zone == "center":
            DrawCircle(int(x + width / 2), int(y + height / 2), circle_radius, GREEN)
        elif faceoff_zone == "bottom_right":
            DrawCircle(x + width - circle_center_x, y + circle_center_y, circle_radius, GREEN)
        elif faceoff_zone == "top_right":
            DrawCircle(x + width - circle_center_x, y + height - circle_center_y, circle_radius, GREEN)




def make_score_board(x, y, width, height):    
    DrawRectangleRec(Rectangle(x,y,width, height), GRAY)

    # Time counters
    time_since_start_iters_str = strftime("%M:%S", gmtime(time_game)).encode('ascii')
    DrawTextCenteredInRoundedRectangle(time_since_start_iters_str, 40, BLACK, x + int(WIDTH_RATIO * 50), y + int(HEIGHT_RATIO * 40), width - int(WIDTH_RATIO * 100), int(HEIGHT_RATIO * 40), 1.0, WHITE, 5, BLACK)

    time_since_start_str = strftime("%M:%S", gmtime(time_absolute)).encode('ascii')
    DrawTextCenteredInRoundedRectangle(time_since_start_str, 20, BLACK, x + int(WIDTH_RATIO * 50), y + int(HEIGHT_RATIO * 10), width - int(WIDTH_RATIO * 100), int(HEIGHT_RATIO * 20), 1.0, WHITE, 0, BLACK)

    # Team names/colors and scores
    DrawTextCenteredInRoundedRectangle(b"%d"%get_goal_count("A", GAME_DATA), 50, BLACK, x + int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 100), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 50), 0.0, WHITE, 0, BLACK)
    DrawTextCenteredInRoundedRectangle(b"%d"%get_goal_count("B", GAME_DATA), 50, BLACK, x + width - int(WIDTH_RATIO * 70) - int(WIDTH_RATIO * 50), y + int(HEIGHT_RATIO * 100), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 50), 0.0, WHITE, 0, BLACK)

    DrawRectangleRec(Rectangle(x + int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 100) + int(HEIGHT_RATIO * 50), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 20)), get_team_color("A", GAME_DATA))
    DrawRectangleRec(Rectangle(x + width - int(WIDTH_RATIO * 70) - int(WIDTH_RATIO * 50), y + int(HEIGHT_RATIO * 100) + int(HEIGHT_RATIO * 50), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 20)), get_team_color("B", GAME_DATA))

    # Period counter
    DrawTextCenteredInRoundedRectangle(b"%d"%period_counter, 40, BLACK, x + int(WIDTH_RATIO * 70) + int(WIDTH_RATIO * 60), y + int(HEIGHT_RATIO * 100), int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 40), 0.0, WHITE, 0, BLACK)

def make_time_poss_graph_tracker(x, y, width, height):
    DrawRectangleRec(Rectangle(x, y, width, height), DARKGRAY)
    make_stackbar_graph(x + int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 150), time_team_a, time_team_b, (time_game - time_team_a - time_team_b), GAME_DATA)
    
    time_team_a_str = strftime("%M:%S", gmtime(time_team_a)).encode('ascii')
    time_team_b_str = strftime("%M:%S", gmtime(time_team_b)).encode('ascii')

    DrawTextCenteredInRoundedRectangle(time_team_a_str, 30, BLACK, x + int(WIDTH_RATIO * 90), y + int(HEIGHT_RATIO * 40), int(WIDTH_RATIO * 90), int(HEIGHT_RATIO * 40), 0, WHITE, 3, BLACK)
    DrawTextCenteredInRoundedRectangle(time_team_b_str, 30, BLACK, x + int(WIDTH_RATIO * 90), y + int(HEIGHT_RATIO * 110), int(WIDTH_RATIO * 90), int(HEIGHT_RATIO * 40), 0, WHITE, 3, BLACK)

def make_shots_graph_tracker(x, y, width, height):
    DrawRectangleRec(Rectangle(x, y, width, height), DARKGRAY)

    shots_team_a, shots_on_goal_team_a = get_shots_on_goal_by_team("A", GAME_DATA)
    shots_team_b, shots_on_goal_team_b = get_shots_on_goal_by_team("B", GAME_DATA)

    make_stackbar_graph(x + int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 150), shots_team_a, shots_team_b, 0, GAME_DATA)
    
    DrawTextCenteredInRoundedRectangle(b"%d"%shots_team_a, 30, BLACK, x + int(WIDTH_RATIO * 90), y + int(HEIGHT_RATIO * 40), int(WIDTH_RATIO * 60), int(HEIGHT_RATIO * 40), 0, WHITE, 3, BLACK)
    DrawTextCenteredInRoundedRectangle(b"%d"%shots_team_b, 30, BLACK, x + int(WIDTH_RATIO * 90), y + int(HEIGHT_RATIO * 110), int(WIDTH_RATIO * 60), int(HEIGHT_RATIO * 40), 0, WHITE, 3, BLACK)

    DrawTextCenteredInRoundedRectangle(b"%d"%shots_on_goal_team_a, 30, BLACK, x + int(WIDTH_RATIO * 200), y + int(HEIGHT_RATIO * 40), int(WIDTH_RATIO * 60), int(HEIGHT_RATIO * 40), 0, WHITE, 3, BLACK)
    DrawTextCenteredInRoundedRectangle(b"%d"%shots_on_goal_team_b, 30, BLACK, x + int(WIDTH_RATIO * 200), y + int(HEIGHT_RATIO * 110), int(WIDTH_RATIO * 60), int(HEIGHT_RATIO * 40), 0, WHITE, 3, BLACK)

    make_stackbar_graph(x + int(WIDTH_RATIO * 280), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 150), shots_on_goal_team_a, shots_on_goal_team_b, 0, GAME_DATA)


def make_faceoffs_graph_tracker(x, y, width, height):
    DrawRectangleRec(Rectangle(x, y, width, height), DARKGRAY)

    faceoffs_team_a = get_faceoffs_win_by_team("A", GAME_DATA)
    faceoffs_team_b = get_faceoffs_win_by_team("B", GAME_DATA)

    make_stackbar_graph(x + int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 150), faceoffs_team_a, faceoffs_team_b, 0, GAME_DATA)
    
    DrawTextCenteredInRoundedRectangle(b"%d"%faceoffs_team_a, 30, BLACK, x + int(WIDTH_RATIO * 90), y + int(HEIGHT_RATIO * 40), int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 40), 0, WHITE, 3, BLACK)
    DrawTextCenteredInRoundedRectangle(b"%d"%faceoffs_team_b, 30, BLACK, x + int(WIDTH_RATIO * 90), y + int(HEIGHT_RATIO * 110), int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 40), 0, WHITE, 3, BLACK)

def make_current_players_pannel(x, y, width, height, touch_input, touch_input_x, touch_input_y):
    global swap_goalies_a
    global current_goalie_num_a
    global swap_goalies_b
    global current_goalie_num_b
    global time_shots_stats_switch

    DrawRectangleRec(Rectangle(x, y, width, height), LIGHTGRAY)
    # TEAM A
    y_pl = int(HEIGHT_RATIO * 20)
    y_goalie = 0
    u = False
    n_goalie = 0
    for i,player in enumerate(GAME_DATA["Players_A"]):
        num = player["num"]
        if player["poste"] == "goalie":
            
            make_color_toggle(x + int(WIDTH_RATIO * 20), y + height - int(HEIGHT_RATIO * 150) + y_goalie, int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 30), GAME_DATA["Players_A"][i]["is_on_field"], 5, get_team_color("A", GAME_DATA), b"%d"%num)
            GAME_DATA["Players_A"][i]["is_on_field"] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20), y + height - int(HEIGHT_RATIO * 150) + y_goalie, int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 30), GAME_DATA["Players_A"][i]["is_on_field"], 5)

            DrawTextCenteredInRoundedRectangle(b"ANY", 22, BLACK, x + int(WIDTH_RATIO * 20) + int(WIDTH_RATIO * 40) + int(WIDTH_RATIO * 10), y + height - int(HEIGHT_RATIO * 150) + y_goalie, int(WIDTH_RATIO * 70), int(HEIGHT_RATIO * 30), 0.0, WHITE, 0, BLACK)  # shots and goals
            y_goalie += int(HEIGHT_RATIO * 50)

            if GAME_DATA["Players_A"][i]["is_on_field"]:
                n_goalie += 1
       
            if n_goalie > 1:
                swap_goalies_a = True

        else:

            make_color_toggle(x + int(WIDTH_RATIO * 20), y + y_pl, int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 30), GAME_DATA["Players_A"][i]["is_on_field"], 5, get_team_color("A", GAME_DATA), b"%d"%num)
            GAME_DATA["Players_A"][i]["is_on_field"] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20), y + y_pl, int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 30), GAME_DATA["Players_A"][i]["is_on_field"], 5)

            time_on_field = strftime("%M:%S", gmtime(player["time_on_field"])).encode('ascii')
            
            if time_shots_stats_switch :
                #show time
                DrawTextCenteredInRoundedRectangle(time_on_field, 22, BLACK, x + int(WIDTH_RATIO * 20) + int(WIDTH_RATIO * 40) + int(WIDTH_RATIO * 10), y + y_pl, int(WIDTH_RATIO * 70), int(HEIGHT_RATIO * 30), 0.0, WHITE, 0, BLACK)  # shots
            else:
                shots, shots_on_goal, goals = get_shots_on_goal_by_player_team_and_num("A", num, GAME_DATA)
                if shots>0:
                    on_goal_perc = 100*(shots_on_goal/shots)
                else:
                    on_goal_perc = 0
                DrawTextCenteredInRoundedRectangle(b"%d"%(shots), 22, BLACK, x + int(WIDTH_RATIO * 20) + int(WIDTH_RATIO * 40) + int(WIDTH_RATIO * 10), y + y_pl, int(WIDTH_RATIO * 20), int(HEIGHT_RATIO * 30), 0.0, WHITE, 0, BLACK)  # blocked / rebound                        
                DrawTextCenteredInRoundedRectangle(b"%d"%(shots_on_goal), 22, BLACK, x + int(WIDTH_RATIO * 20) + int(WIDTH_RATIO * 40) + int(WIDTH_RATIO * 10) + int(WIDTH_RATIO * 20), y + y_pl, int(WIDTH_RATIO * 20), int(HEIGHT_RATIO * 30), 0.0, LIME, 0, BLACK)  # blocked / rebound                        
                DrawTextCenteredInRoundedRectangle(b"%.0f%%"%(on_goal_perc), 22, BLACK, x + int(WIDTH_RATIO * 20) + int(WIDTH_RATIO * 40) + int(WIDTH_RATIO * 10) + int(WIDTH_RATIO * 40), y + y_pl, int(WIDTH_RATIO * 30), int(HEIGHT_RATIO * 30), 0.0, LIME, 2, BLACK)  # blocked / rebound                        

            y_pl += int(HEIGHT_RATIO * 50)
    
    # A bit of a mindfuck by using the toggles but works to change goalies, could use bullet box...
    if (n_goalie == 1):
        for j,playerj in enumerate(GAME_DATA["Players_A"]):
            if (playerj["poste"] == "goalie") and (playerj["is_on_field"]):
                current_goalie_num_a = playerj["num"]    
    elif (swap_goalies_a):
        swap_goalies_a = False
        for j,playerj in enumerate(GAME_DATA["Players_A"]):
            if (playerj["poste"] == "goalie"):
                if (playerj["num"] == current_goalie_num_a):
                    GAME_DATA["Players_A"][j]["is_on_field"] = False
                else:
                    GAME_DATA["Players_A"][j]["is_on_field"] = True
                    current_goalie_num_to_set_a = playerj["num"]   
        current_goalie_num_a = current_goalie_num_to_set_a 

    # TEAM B
    y_pl = int(HEIGHT_RATIO * 20)
    u = False
    y_goalie = 0
    n_goalie = 0
    for i, player in enumerate(GAME_DATA["Players_B"]):
        num = player["num"]
        if player["poste"] == "goalie":

            make_color_toggle(x + int(WIDTH_RATIO * 150), y + height - int(HEIGHT_RATIO * 150) + y_goalie, int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 30), GAME_DATA["Players_B"][i]["is_on_field"], 5, get_team_color("B", GAME_DATA), b"%d"%num)
            GAME_DATA["Players_B"][i]["is_on_field"] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 150), y + height - int(HEIGHT_RATIO * 150) + y_goalie, int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 30), GAME_DATA["Players_B"][i]["is_on_field"], 5)

            DrawTextCenteredInRoundedRectangle(b"ANY", 22, BLACK, x + int(WIDTH_RATIO * 150) + int(WIDTH_RATIO * 40) + int(WIDTH_RATIO * 10), y + height - int(HEIGHT_RATIO * 150) + y_goalie, int(WIDTH_RATIO * 70), int(HEIGHT_RATIO * 30), 0.0, WHITE, 0, BLACK)     
            y_goalie += int(HEIGHT_RATIO * 50)    

            if GAME_DATA["Players_B"][i]["is_on_field"]:
                n_goalie += 1
                
            if n_goalie > 1:
                swap_goalies_b = True
   
        else:
            make_color_toggle(x + int(WIDTH_RATIO * 150), y + y_pl, int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 30), GAME_DATA["Players_B"][i]["is_on_field"], 5, get_team_color("B", GAME_DATA), b"%d"%num)
            GAME_DATA["Players_B"][i]["is_on_field"] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 150), y + y_pl, int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 30), GAME_DATA["Players_B"][i]["is_on_field"], 5)
            
            time_on_field = strftime("%M:%S", gmtime(player["time_on_field"])).encode('ascii')
            if time_shots_stats_switch :
                #show time
                DrawTextCenteredInRoundedRectangle(time_on_field, 22, BLACK, x + int(WIDTH_RATIO * 150) + int(WIDTH_RATIO * 40) + int(WIDTH_RATIO * 10), y + y_pl, int(WIDTH_RATIO * 70), int(HEIGHT_RATIO * 30), 0.0, WHITE, 0, BLACK)     
            else:
                shots, shots_on_goal, goals = get_shots_on_goal_by_player_team_and_num("B", num, GAME_DATA)
                DrawTextCenteredInRoundedRectangle(b"%d"%(shots), 22, BLACK, x + int(WIDTH_RATIO * 150) + int(WIDTH_RATIO * 40) + int(WIDTH_RATIO * 10), y + y_pl, int(WIDTH_RATIO * 20), int(HEIGHT_RATIO * 30), 0.0, WHITE, 0, BLACK)  # blocked / rebound                        
                DrawTextCenteredInRoundedRectangle(b"%d"%(shots_on_goal), 22, BLACK, x + int(WIDTH_RATIO * 150) + int(WIDTH_RATIO * 40) + int(WIDTH_RATIO * 10) + int(WIDTH_RATIO * 20), y + y_pl, int(WIDTH_RATIO * 20), int(HEIGHT_RATIO * 30), 0.0, LIME, 0, BLACK)  # blocked / rebound                        
                DrawTextCenteredInRoundedRectangle(b"%.0f%%"%(on_goal_perc), 22, BLACK, x + int(WIDTH_RATIO * 150) + int(WIDTH_RATIO * 40) + int(WIDTH_RATIO * 10) + int(WIDTH_RATIO * 40), y + y_pl, int(WIDTH_RATIO * 30), int(HEIGHT_RATIO * 30), 0.0, LIME, 2, BLACK)  # blocked / rebound                        

            y_pl += int(HEIGHT_RATIO * 50)
    
    # A bit of a mindfuck by using the toggles but works to change goalies, could use bullet box...
    if (n_goalie == 1):
        for j,playerj in enumerate(GAME_DATA["Players_B"]):
            if (playerj["poste"] == "goalie") and (playerj["is_on_field"]):
                current_goalie_num_b = playerj["num"]    
    elif (swap_goalies_b):
        swap_goalies_b = False
        for j,playerj in enumerate(GAME_DATA["Players_B"]):
            if (playerj["poste"] == "goalie"):
                if (playerj["num"] == current_goalie_num_b):
                    GAME_DATA["Players_B"][j]["is_on_field"] = False
                else:
                    GAME_DATA["Players_B"][j]["is_on_field"] = True
                    current_goalie_num_to_set_b = playerj["num"]   
        current_goalie_num_b = current_goalie_num_to_set_b
    
    if time_shots_stats_switch:
        make_color_toggle(x + int(WIDTH_RATIO * 20), y + height - int(HEIGHT_RATIO * 200), width - int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 30), time_shots_stats_switch, 0, BLACK, b"TIME SHIFT", 0.8, WHITE, GRAY)
    else:
        make_color_toggle(x + int(WIDTH_RATIO * 20), y + height - int(HEIGHT_RATIO * 200), width - int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 30), time_shots_stats_switch, 0, BLACK, b"SHOT STATS", 0.8, WHITE, GRAY)

    time_shots_stats_switch = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20), y + height - int(HEIGHT_RATIO * 200), width - int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 30), time_shots_stats_switch, 0)

    if len(get_current_present_players("A", GAME_DATA)) == len(get_current_present_players("B", GAME_DATA)):
        DrawTextCenteredInRoundedRectangle(b"EQUAL", 22, BLACK, x + int(WIDTH_RATIO * 20), y + height - int(HEIGHT_RATIO * 50), int(WIDTH_RATIO * 120), int(HEIGHT_RATIO * 30), 0.0, WHITE, 2, get_team_color("A", GAME_DATA)) 
        DrawTextCenteredInRoundedRectangle(b"EQUAL", 22, BLACK, x + int(WIDTH_RATIO * 150), y + height - int(HEIGHT_RATIO * 50), int(WIDTH_RATIO * 120), int(HEIGHT_RATIO * 30), 0.0, WHITE, 2, get_team_color("B", GAME_DATA)) 
    elif len(get_current_present_players("A", GAME_DATA)) > len(get_current_present_players("B", GAME_DATA)):
        DrawTextCenteredInRoundedRectangle(b"PP", 22, BLACK, x + int(WIDTH_RATIO * 20), y + height - int(HEIGHT_RATIO * 50), int(WIDTH_RATIO * 120), int(HEIGHT_RATIO * 30), 0.0, GREEN, 2, get_team_color("A", GAME_DATA)) 
        DrawTextCenteredInRoundedRectangle(b"PK", 22, BLACK, x + int(WIDTH_RATIO * 150), y + height - int(HEIGHT_RATIO * 50), int(WIDTH_RATIO * 120), int(HEIGHT_RATIO * 30), 0.0, RED, 2, get_team_color("B", GAME_DATA)) 
    else:
        DrawTextCenteredInRoundedRectangle(b"PK", 22, BLACK, x + int(WIDTH_RATIO * 20), y + height - int(HEIGHT_RATIO * 50), int(WIDTH_RATIO * 120), int(HEIGHT_RATIO * 30), 0.0, RED, 2, get_team_color("A", GAME_DATA)) 
        DrawTextCenteredInRoundedRectangle(b"PP", 22, BLACK, x + int(WIDTH_RATIO * 150), y + height - int(HEIGHT_RATIO * 50), int(WIDTH_RATIO * 120), int(HEIGHT_RATIO * 30), 0.0, GREEN, 2, get_team_color("B", GAME_DATA)) 

def draw_goal_circle(x, y, size, color, fill, text, border_width, border_color, text_color = BLACK):
    if fill:
        DrawCircle(x, y, size + border_width, border_color)
        DrawCircle(x, y, size, color)
    else:
        DrawCircleLinesFat(x, y, size, color, border_width)
    
    text_width = MeasureText(text, int(2 * size * 0.8))
    text_x = x - int(text_width / 2)
    text_y = y - int((2 * size * 0.8)/2)
    DrawText(text, text_x, text_y, int(2 * size * 0.8), text_color)
    DrawText(text, text_x - 1, text_y - 1, int(2 * size * 0.8), text_color)
    DrawText(text, text_x + 1, text_y + 1, int(2 * size * 0.8), text_color)

def make_goals_drawing(x, y, width, height):
    """
    Draw the goals and shots form GAME_DATA using the coordinates of the field
    """
    for shot in GAME_DATA["shots_A"]:
        pos_x_abs = int(x + shot["pos_x"] * width)
        pos_y_abs = int(y + shot["pos_y"] * height)

        if (shot["result_of_shot"] == "goal"):
            draw_goal_circle(pos_x_abs, pos_y_abs, 15, get_team_color("A", GAME_DATA), True, b"%d"%shot["shooter"], 3, BLACK)
        elif (shot["result_of_shot"] == "missed"):
            draw_goal_circle(pos_x_abs, pos_y_abs, 15, get_team_color("A", GAME_DATA), False, b"", 3, BLACK)
        elif (shot["result_of_shot"] == "blocked"):
            draw_goal_circle(pos_x_abs, pos_y_abs, 15, get_team_color("A", GAME_DATA), True, b"-", 0, BLACK, WHITE)
        elif (shot["result_of_shot"] == "rebound"):
            draw_goal_circle(pos_x_abs, pos_y_abs, 15, get_team_color("A", GAME_DATA), True, b"", 0, BLACK)
        elif (shot["result_of_shot"] == "covered"):
            draw_goal_circle(pos_x_abs, pos_y_abs, 15, get_team_color("A", GAME_DATA), True, b"o", 0, BLACK, WHITE)
            
    for shot in GAME_DATA["shots_B"]:
        pos_x_abs = int(x + shot["pos_x"] * width)
        pos_y_abs = int(y + shot["pos_y"] * height)
        
        if (shot["result_of_shot"] == "goal"):
            draw_goal_circle(pos_x_abs, pos_y_abs, 15, get_team_color("B", GAME_DATA), True, b"%d"%shot["shooter"], 3, BLACK)
        elif (shot["result_of_shot"] == "missed"):
            draw_goal_circle(pos_x_abs, pos_y_abs, 15, get_team_color("B", GAME_DATA), False, b"", 3, BLACK)
        elif (shot["result_of_shot"] == "blocked"):
            draw_goal_circle(pos_x_abs, pos_y_abs, 15, get_team_color("B", GAME_DATA), True, b"-", 0, BLACK, WHITE)
        elif (shot["result_of_shot"] == "rebound"):
            draw_goal_circle(pos_x_abs, pos_y_abs, 15, get_team_color("B", GAME_DATA), True, b"", 0, BLACK)
        elif (shot["result_of_shot"] == "covered"):
            draw_goal_circle(pos_x_abs, pos_y_abs, 15, get_team_color("B", GAME_DATA), True, b"o", 0, BLACK, WHITE)


def draw_duel_cross(x, y, size, color, thickness = 5):
    top_left = [x - int(size/2), y + int(size/2)]
    top_right = [x + int(size/2), y + int(size/2)]
    bottom_left = [x - int(size/2), y - int(size/2)]
    bottom_right = [x + int(size/2), y - int(size/2)]

    for t in range(-int(thickness/2), int(thickness/2)):
        DrawLine(top_left[0] + t, top_left[1], bottom_right[0] + t, bottom_right[1], color)
        DrawLine(top_right[0] + t, top_right[1], bottom_left[0] + t, bottom_left[1], color)


def make_duels_drawing(x, y, width, height):
    """
    Draw the duels from GAME_DATA 
    """
    for duel in GAME_DATA["duels"]:
        pos_x_abs = int(x + duel["pos_x"] * width)
        pos_y_abs = int(y + duel["pos_y"] * height)

        draw_duel_cross(pos_x_abs, pos_y_abs, 20, get_team_color(duel["winning_team"], GAME_DATA))
      
def make_shot_touch_menu(x, y, width, height, touch_input, touch_x, touch_y):
    # global is_field_touch_menu_to_close
    global is_field_touch_menu_on
    global GAME_DATA
    global is_any_shooter_a
    global is_any_shooter_b
    global last_shot_touch_relative_x #only to handle auto team detection not shot placement
    global last_shot_touch_relative_y #only to handle auto team detection not shot placement
    global is_shot_type
    global is_shot_result
    global is_paused
    global is_team_b_possess
    global is_team_a_possess
    
    DrawRectangleRec(Rectangle(x - 4, y - 4, width + 8, height + 8), BLACK)
    DrawRectangleRec(Rectangle(x, y, width, height), DARKGRAY)

    current_present_players_a = get_current_present_players("A", GAME_DATA)
    current_present_players_b = get_current_present_players("B", GAME_DATA)
    shooting_team = "U"

    # Shot type and result
    for i, result in enumerate(shot_results):
        size_rel = 0.5
        width_button = int(WIDTH_RATIO * 80)
        # if result == "rebound":
        #     width_button += int(WIDTH_RATIO * 10)
        
        if is_shot_result[i]:
            DrawTextCenteredInRoundedRectangle(result.encode('ascii'), 25, BLACK, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 100), y + int(HEIGHT_RATIO * 20), width_button, int(HEIGHT_RATIO * 50), 0, GREEN, 5, BLACK)        
        else:
            DrawTextCenteredInRoundedRectangle(result.encode('ascii'), 25, BLACK, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 100), y + int(HEIGHT_RATIO * 20), width_button, int(HEIGHT_RATIO * 50), 0, WHITE, 5, BLACK)
        if touch_input and is_touch_input_intersecting_with_rectangle(touch_x, touch_y, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 100), y + int(HEIGHT_RATIO * 20), width_button, int(HEIGHT_RATIO * 50)):
            is_shot_result[i] = not is_shot_result[i] #invert truth state
            for j in range(len(is_shot_result)):
                if j!=i:
                    is_shot_result[j] = False

    for i, type in enumerate(shot_types):
        width_button = int(WIDTH_RATIO * 63)
        
        #83 spacing for aligning
        if is_shot_type[i]:
            DrawTextCenteredInRoundedRectangle(type.encode('ascii'), 20, BLACK, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 83), y + int(HEIGHT_RATIO * 90), width_button, int(HEIGHT_RATIO * 50), 0, GREEN, 5, BLACK)        
        else:
            DrawTextCenteredInRoundedRectangle(type.encode('ascii'), 20, BLACK, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 83), y + int(HEIGHT_RATIO * 90), width_button, int(HEIGHT_RATIO * 50), 0, WHITE, 5, BLACK)
        if touch_input and is_touch_input_intersecting_with_rectangle(touch_x, touch_y, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 83), y + int(HEIGHT_RATIO * 90), width_button, int(HEIGHT_RATIO * 50)):
            is_shot_type[i] = not is_shot_type[i] #invert truth state
            for j in range(len(is_shot_type)):
                if j!=i:
                    is_shot_type[j] = False
        

    # Any shooter auto detection
    if are_goalies_switched:
        if (last_shot_touch_relative_x > 0) and (last_shot_touch_relative_x < 0.5):
            is_any_shooter_a = True
            is_any_shooter_b = False
        elif (last_shot_touch_relative_x >= 0.5):
            is_any_shooter_a = False
            is_any_shooter_b = True
    else:
        if (last_shot_touch_relative_x > 0) and (last_shot_touch_relative_x < 0.5):
            is_any_shooter_a = False
            is_any_shooter_b = True
        elif (last_shot_touch_relative_x >= 0.5):
            is_any_shooter_a = True
            is_any_shooter_b = False
    
    make_color_toggle(x + width - int(WIDTH_RATIO * 150) - int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 150), int(HEIGHT_RATIO * 50), is_any_shooter_a, 5, get_team_color("A", GAME_DATA), b"ANY", 0.8)    
    is_any_shooter_a = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + width - int(WIDTH_RATIO * 150) - int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 150), int(HEIGHT_RATIO * 50), is_any_shooter_a, 5)
    if is_any_shooter_a:
        shooting_team = "A"
        is_any_shooter_b = False
        last_shot_touch_relative_x = 0
        last_shot_touch_relative_y = 0

    make_color_toggle(x + width - int(WIDTH_RATIO * 150) - int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 90), int(WIDTH_RATIO * 150), int(HEIGHT_RATIO * 50), is_any_shooter_b, 5, get_team_color("B", GAME_DATA), b"ANY", 0.8)
    is_any_shooter_b = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + width - int(WIDTH_RATIO * 150) - int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 90), int(WIDTH_RATIO * 150), int(HEIGHT_RATIO * 50), is_any_shooter_b, 5)
    if is_any_shooter_b:
        shooting_team = "B"
        is_any_shooter_a = False
        last_shot_touch_relative_x = 0
        last_shot_touch_relative_y = 0

    if (is_any_shooter_a) or (is_any_shooter_b):
        for player in current_present_players_a:
            player["is_current_shooter"] = False
            player["is_current_passer"] = False
        for player in current_present_players_b:
            player["is_current_shooter"] = False
            player["is_current_passer"] = False

    # Detailed selection
    i = 0
    for player in (current_present_players_a):
        if player["poste"] != "goalie" and player["is_on_field"] == True:
            make_color_toggle(x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 170), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 50), player["is_current_shooter"], 5, get_team_color("A", GAME_DATA), b"%d"%player["num"], 0.8)
            player["is_current_shooter"] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 170), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 50), player["is_current_shooter"], 5)
            i+=1
        else:
            player["is_current_shooter"] = False # to avoid hidden shooters
    
    i = 0
    for player in (current_present_players_b):
        if player["poste"] != "goalie" and player["is_on_field"] == True:
            make_color_toggle(x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 240), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 50), player["is_current_shooter"], 5, get_team_color("B", GAME_DATA), b"%d"%player["num"], 0.8)
            player["is_current_shooter"] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 240), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 50), player["is_current_shooter"], 5)
            i+=1
        else:
            player["is_current_shooter"] = False # to avoid hidden shooters
    
    n_shooters = sum([player["is_current_shooter"] for player in current_present_players_a] + [player["is_current_shooter"] for player in current_present_players_b])
    if n_shooters > 1:
        #invalid number of shooters reset everyone
        for player in (current_present_players_a):
            player["is_current_shooter"] = False
            player["is_current_passer"] = False
        for player in (current_present_players_b):
            player["is_current_shooter"] = False
            player["is_current_passer"] = False
    elif n_shooters == 1:
        is_any_shooter_a = False
        is_any_shooter_b = False
        last_shot_touch_relative_x = 0
        last_shot_touch_relative_y = 0
        shooting_team = "U"
        if sum([player["is_current_shooter"] for player in current_present_players_a]) == 1:
            shooting_team = "A"
            i = 0
            for player in (current_present_players_a):
                if player["poste"] != "goalie" and player["is_on_field"] and not player["is_current_shooter"]:
                    make_color_toggle(x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 60) + int(WIDTH_RATIO * 350) + int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 170), int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 40), player["is_current_passer"], 5, get_team_color("A", GAME_DATA), b"%d"%player["num"], 0.8)
                    player["is_current_passer"] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 60) + int(WIDTH_RATIO * 350) + int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 170), int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 40), player["is_current_passer"], 5)
                    i+=1
                else:
                    player["is_current_passer"] = False # to avoid hidden passers
                    
        elif sum([player["is_current_shooter"] for player in current_present_players_b]) == 1:
            shooting_team = "B"
            i = 0
            for player in (current_present_players_b):
                if player["poste"] != "goalie" and player["is_on_field"] and not player["is_current_shooter"]:
                    make_color_toggle(x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 60) + int(WIDTH_RATIO * 350) + int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 240), int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 40), player["is_current_passer"], 5, get_team_color("B", GAME_DATA), b"%d"%player["num"], 0.8)
                    player["is_current_passer"] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 60) + int(WIDTH_RATIO * 350) + int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 240), int(WIDTH_RATIO * 40), int(HEIGHT_RATIO * 40), player["is_current_passer"], 5)
                    i+=1
                else:
                    player["is_current_passer"] = False # to avoid hidden passers
                    
        else:
            print("[ERROR] One and only one shooter should be on")
    elif n_shooters == 0:
        # Remove hidden shooters / passers
        for player in (current_present_players_a):
            player["is_current_shooter"] = False
            player["is_current_passer"] = False
        for player in (current_present_players_b):
            player["is_current_shooter"] = False
            player["is_current_passer"] = False
        
    if (shooting_team != "U"):
        # Draw the cage for results
        # Goal tap zone
        DrawRectangleRec(Rectangle(x, y + int(HEIGHT_RATIO * 320), width, height - int(HEIGHT_RATIO * 320)), GRAY)
        
        # Cage
        cage_pos_x = x + int(WIDTH_RATIO * 110)    
        cage_pos_y = y + int(HEIGHT_RATIO * 370)   
        cage_width = width - int(WIDTH_RATIO * 240)
        cage_height = height - int(HEIGHT_RATIO * 380)
        DrawRectangleRec(Rectangle(cage_pos_x - 10, cage_pos_y - 10, cage_width + 20, cage_height + 20), RED)
        DrawRectangleRec(Rectangle(cage_pos_x, cage_pos_y, cage_width, cage_height), WHITE)

        # Fake "goalie"
        if shooting_team == "A":
            opponent_team = "B"
        elif shooting_team == "B":
            opponent_team = "A"

        current_goalie = get_current_goalkeeper(opponent_team, GAME_DATA)
        goal_width = int(cage_width/3)
        goal_height = int(cage_height * 0.7)
        DrawTextCenteredInRoundedRectangle(b"%d"%current_goalie["num"], 30, BLACK, int(cage_pos_x + cage_width / 2 - goal_width / 2), int(cage_pos_y + (cage_height - goal_height)), goal_width, goal_height, 0.2, get_team_color(opponent_team, GAME_DATA), 5, BLACK)
        
        type_of_shot = "U"
        for val, shot in zip(is_shot_type, shot_types):
            if val:
                type_of_shot = shot

        result_of_shot = "U"
        for val, result in zip(is_shot_result, shot_results):
            if val:
                result_of_shot = result

        if result_of_shot == "blocked":
            # Add selector for player who blocked
            blocker_y_boxes = 0

            for player in get_current_present_players(opponent_team, GAME_DATA):
                if player["poste"] != "goalie":
                    make_color_toggle(cage_pos_x + cage_width + 25 * WIDTH_RATIO, cage_pos_y + blocker_y_boxes, int(40 * WIDTH_RATIO), int(40 * HEIGHT_RATIO), player["is_current_blocker_of_shoot"], 5, get_team_color(opponent_team, GAME_DATA), b"%d"%player["num"])
                    player["is_current_blocker_of_shoot"] = click_color_toggle(touch_input, touch_input_x, touch_input_y, cage_pos_x + cage_width + 10 * WIDTH_RATIO, cage_pos_y + blocker_y_boxes, int(40 * WIDTH_RATIO), int(40 * HEIGHT_RATIO), player["is_current_blocker_of_shoot"], 5)
                    blocker_y_boxes += int(60 * HEIGHT_RATIO)

        shot_from_zone = "U"

        if result_of_shot != "blocked":
            is_input_valid = is_touch_input_intersecting_with_rectangle(touch_input_x, touch_input_y, x, y + int(HEIGHT_RATIO * 320), width, height - int(HEIGHT_RATIO * 320))
        else:
            is_input_valid = is_touch_input_intersecting_with_rectangle(touch_input_x, touch_input_y, cage_pos_x - 10, cage_pos_y - 10, cage_width + 20, cage_height + 20)

        if touch_input and is_input_valid:
            on_rec_x, on_rec_y = get_touch_relative_rectangle_position(touch_input_x, touch_input_y, x, y + int(HEIGHT_RATIO * 320), width, height - int(HEIGHT_RATIO * 320))
            
            if are_goalies_switched:
                if (last_shot_relative_x > 0) and (last_shot_relative_x < 0.5):
                    if (shooting_team == "A"):
                        shot_from_zone = "off"
                    elif (shooting_team == "B"):
                        shot_from_zone = "def"
                elif (last_shot_relative_x >= 0.5):
                    if (shooting_team == "B"):
                        shot_from_zone = "off"
                    elif (shooting_team == "A"):
                        shot_from_zone = "def"
            else:
                if (last_shot_relative_x > 0) and (last_shot_relative_x < 0.5):
                    if (shooting_team == "B"):
                        shot_from_zone = "off"
                    elif (shooting_team == "A"):
                        shot_from_zone = "def"
                elif (last_shot_relative_x >= 0.5):
                    if (shooting_team == "A"):
                        shot_from_zone = "off"
                    elif (shooting_team == "B"):
                        shot_from_zone = "def"

            shooter = -1
            if is_any_shooter_a or is_any_shooter_b:
                shooter = -1
            else:
                if shooting_team == "A":
                    for player in current_present_players_a:
                        if player["is_current_shooter"]:
                            shooter = player["num"]
                else:
                    for player in current_present_players_b:
                        if player["is_current_shooter"]:
                            shooter = player["num"]

            numeric_strength = "equal"
            if (len(get_current_present_players(shooting_team, GAME_DATA)) > len(get_current_present_players(opponent_team, GAME_DATA))):
                numeric_strength = "sup"
            elif (len(get_current_present_players(shooting_team, GAME_DATA)) < len(get_current_present_players(opponent_team, GAME_DATA))):
                numeric_strength = "inf"

            shot_str = "shots_" + shooting_team
            assists = []
            for player in get_current_present_players(shooting_team, GAME_DATA):
                if player["is_current_passer"]:
                    assists.append(player["num"])

            if is_touch_input_intersecting_with_rectangle(touch_input_x, touch_input_y, cage_pos_x - 10, cage_pos_y - 10, cage_width + 20, cage_height + 20):
                print("SHOT ON NET")
                on_net_x, on_net_y = get_touch_relative_rectangle_position(touch_input_x, touch_input_y,  cage_pos_x - 10, cage_pos_y - 10, cage_width + 20, cage_height + 20)
                shot = get_shot_dict(time_absolute, time_game, period_counter, last_shot_relative_x, last_shot_relative_y, on_net_x, on_net_y, on_rec_x, on_rec_y, shot_from_zone, shooter, assists, shooting_team, type_of_shot, result_of_shot, numeric_strength, GAME_DATA)
                
                GAME_DATA[shot_str].append(shot)
                is_field_touch_menu_on = False
            else:
                if (result_of_shot == "rebound"):
                    #only use auto missed shot detection if default
                    result_of_shot = "missed"
                on_net_x = -1
                on_net_y = -1
                print("MISSED")
                shot = get_shot_dict(time_absolute, time_game, period_counter, last_shot_relative_x, last_shot_relative_y, on_net_x, on_net_y, on_rec_x, on_rec_y, shot_from_zone, shooter, assists, shooting_team, type_of_shot, result_of_shot, numeric_strength, GAME_DATA)
                GAME_DATA[shot_str].append(shot)
                is_field_touch_menu_on = False

            if (result_of_shot == "goal") or (result_of_shot == "covered"):
                # Stop the time if goal or covered selected
                is_paused = True
                is_team_a_possess = False
                is_team_b_possess= False

            if (result_of_shot == "blocked"):
                for player in get_current_present_players(opponent_team, GAME_DATA):
                    player["is_current_blocker_of_shoot"] = False


            print(shot)

def make_duel_touch_menu(x, y, width, height):
    DrawRectangleRec(Rectangle(x - 4, y - 4, width + 8, height + 8), BLACK)
    DrawRectangleRec(Rectangle(x, y, width, height), DARKGRAY)

    global duel_win_by_team_A
    global duel_win_by_team_B
    global is_field_touch_menu_on

    current_present_players_a = get_current_present_players("A", GAME_DATA)
    current_present_players_b = get_current_present_players("B", GAME_DATA)
    i = 0
    u = False
    for player in (current_present_players_a):
        if player["poste"] != "goalie" and player["is_on_field"] == True:
            make_color_toggle(x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 50), player["is_involved_in_duel"], 5, get_team_color("A", GAME_DATA), b"%d"%player["num"], 0.8)
            player["is_involved_in_duel"] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 50), player["is_involved_in_duel"], 5)
            i+=1
        else:
            player["is_involved_in_duel"] = False # to avoid hidden duels
    
    i = 0
    for player in (current_present_players_b):
        if player["poste"] != "goalie" and player["is_on_field"] == True:
            make_color_toggle(x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 90), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 50), player["is_involved_in_duel"], 5, get_team_color("B", GAME_DATA), b"%d"%player["num"], 0.8)
            player["is_involved_in_duel"] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 90), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 50), player["is_involved_in_duel"], 5)
            i+=1
        else:
            player["is_involved_in_duel"] = False # to avoid hidden duels

    make_color_toggle(x + int(WIDTH_RATIO * 20) + 5 * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 100), int(HEIGHT_RATIO * 50), duel_win_by_team_A, 5, get_team_color("A", GAME_DATA), b"WIN", 0.8)
    duel_win_by_team_A = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20) + 5 * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 100), int(HEIGHT_RATIO * 50), duel_win_by_team_A, 5)

    winning_team = "U"

    if duel_win_by_team_A:
        duel_win_by_team_B = False
        winning_team = "A"

    make_color_toggle(x + int(WIDTH_RATIO * 20) + 5 * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 90), int(WIDTH_RATIO * 100), int(HEIGHT_RATIO * 50), duel_win_by_team_B, 5, get_team_color("B", GAME_DATA), b"WIN", 0.8)
    duel_win_by_team_B = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20) + 5 * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 90), int(WIDTH_RATIO * 100), int(HEIGHT_RATIO * 50), duel_win_by_team_B, 5)

    if duel_win_by_team_B:
        duel_win_by_team_A = False
        winning_team = "B"
    
    if (duel_win_by_team_A) or (duel_win_by_team_B):
        involved_players_A = [player["num"] for player in get_current_present_players("A",GAME_DATA) if player["is_involved_in_duel"]]
        involved_players_B = [player["num"] for player in get_current_present_players("B",GAME_DATA) if player["is_involved_in_duel"]]
        is_in_offensive_zone = False
        if are_goalies_switched:
            if (last_shot_relative_x > 0) and (last_shot_relative_x < 0.5):
                if (winning_team == "A"):
                    is_in_offensive_zone = True
                elif (winning_team == "B"):
                    is_in_offensive_zone = False
            elif (last_shot_relative_x >= 0.5):
                if (winning_team == "B"):
                    is_in_offensive_zone = True
                elif (winning_team == "A"):
                    is_in_offensive_zone = False
        else:
            if (last_shot_relative_x > 0) and (last_shot_relative_x < 0.5):
                if (winning_team == "B"):
                    is_in_offensive_zone = True
                elif (winning_team == "A"):
                    is_in_offensive_zone = False
            elif (last_shot_relative_x >= 0.5):
                if (winning_team == "A"):
                    is_in_offensive_zone = True
                elif (winning_team == "B"):
                    is_in_offensive_zone = False

        duel = get_duel_dict(time_absolute, time_game, period_counter, last_shot_relative_x, last_shot_relative_y, involved_players_A, involved_players_B, winning_team, is_in_offensive_zone, GAME_DATA)
        print(duel)
        GAME_DATA["duels"].append(duel)

        is_field_touch_menu_on = False
        duel_win_by_team_B = False
        duel_win_by_team_A = False

        for player in (current_present_players_a):
            player["is_involved_in_duel"] = False # to avoid hidden duels
        
        for player in (current_present_players_b):
            player["is_involved_in_duel"] = False # to avoid hidden duels

def make_faceoff_touch_menu(x, y, width, height):
    #500 * 360 (with ratios at 1)
    DrawRectangleRec(Rectangle(x - 4, y - 4, width + 8, height + 8), BLACK)
    DrawRectangleRec(Rectangle(x, y, width, height), DARKGRAY)

    global faceoff_win_by_team_A
    global faceoff_win_by_team_B
    global is_field_touch_menu_on
    global is_faceoff_in_center

    faceoff_hockey_terrain_width = width - int(WIDTH_RATIO * 80)
    faceoff_hockey_terrain_height = height - int(160 * HEIGHT_RATIO)

    print(last_shot_relative_x, last_shot_relative_y)

    if (last_shot_relative_x > 0.1 and last_shot_relative_x < 0.33):
        if (last_shot_relative_y < 0.5):
            make_inline_hockey_terrain(x + int(WIDTH_RATIO * 40), y + int(20 * HEIGHT_RATIO), faceoff_hockey_terrain_width, faceoff_hockey_terrain_height, "bottom_left")
        else:
            make_inline_hockey_terrain(x + int(WIDTH_RATIO * 40), y + int(20 * HEIGHT_RATIO), faceoff_hockey_terrain_width, faceoff_hockey_terrain_height, "top_left")
    elif (last_shot_relative_x > 0.33 and last_shot_relative_x < 0.66):
        make_inline_hockey_terrain(x + int(WIDTH_RATIO * 40), y + int(20 * HEIGHT_RATIO), faceoff_hockey_terrain_width, faceoff_hockey_terrain_height, "center")
        is_faceoff_in_center = True
    elif (last_shot_relative_x > 0.66 and last_shot_relative_x < 0.9):
        if (last_shot_relative_y < 0.5):
            make_inline_hockey_terrain(x + int(WIDTH_RATIO * 40), y + int(20 * HEIGHT_RATIO), faceoff_hockey_terrain_width, faceoff_hockey_terrain_height, "bottom_right")
        else:
            make_inline_hockey_terrain(x + int(WIDTH_RATIO * 40), y + int(20 * HEIGHT_RATIO), faceoff_hockey_terrain_width, faceoff_hockey_terrain_height, "top_right")

    current_present_players_a = get_current_present_players("A", GAME_DATA)
    current_present_players_b = get_current_present_players("B", GAME_DATA)
    i = 0
    u = False

    for player in (current_present_players_a):
        if player["poste"] != "goalie" and player["is_on_field"] == True:
            make_color_toggle(x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 20) + (faceoff_hockey_terrain_height) + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 40), player["is_involved_in_faceoff"], 5, get_team_color("A", GAME_DATA), b"%d"%player["num"], 0.8)
            player["is_involved_in_faceoff"] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 20) + (faceoff_hockey_terrain_height) + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 40), player["is_involved_in_faceoff"], 5)
            i+=1
        else:
            player["is_involved_in_faceoff"] = False # to avoid hidden faceoffists
    
    i = 0
    for player in (current_present_players_b):
        if player["poste"] != "goalie" and player["is_on_field"] == True:
            make_color_toggle(x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 20) + (faceoff_hockey_terrain_height) + int(HEIGHT_RATIO * 80), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 40), player["is_involved_in_faceoff"], 5, get_team_color("B", GAME_DATA), b"%d"%player["num"], 0.8)
            player["is_involved_in_faceoff"] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20) + i * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 20) + (faceoff_hockey_terrain_height) + int(HEIGHT_RATIO * 80), int(WIDTH_RATIO * 50), int(HEIGHT_RATIO * 40), player["is_involved_in_faceoff"], 5)
            i+=1
        else:
            player["is_involved_in_faceoff"] = False # to avoid hidden faceoffists

    make_color_toggle(x + int(WIDTH_RATIO * 20) + 5 * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 20) + (faceoff_hockey_terrain_height) + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 110), int(HEIGHT_RATIO * 40), faceoff_win_by_team_A, 5, get_team_color("A", GAME_DATA), b"WIN", 0.8)
    faceoff_win_by_team_A = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20) + 5 * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 20) + (faceoff_hockey_terrain_height) + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 110), int(HEIGHT_RATIO * 40), faceoff_win_by_team_A, 5)

    winning_team = "U"

    if faceoff_win_by_team_A:
        faceoff_win_by_team_B = False
        winning_team = "A"

    make_color_toggle(x + int(WIDTH_RATIO * 20) + 5 * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 20) + (faceoff_hockey_terrain_height) + int(HEIGHT_RATIO * 80), int(WIDTH_RATIO * 110), int(HEIGHT_RATIO * 40), faceoff_win_by_team_B, 5, get_team_color("B", GAME_DATA), b"WIN", 0.8)
    faceoff_win_by_team_B = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + int(WIDTH_RATIO * 20) + 5 * int(WIDTH_RATIO * 70), y + int(HEIGHT_RATIO * 20) + (faceoff_hockey_terrain_height) + int(HEIGHT_RATIO * 80), int(WIDTH_RATIO * 110), int(HEIGHT_RATIO * 40), faceoff_win_by_team_B, 5)

    if faceoff_win_by_team_B:
        faceoff_win_by_team_A = False
        winning_team = "B"
    
    if (faceoff_win_by_team_A) or (faceoff_win_by_team_B):
        involved_players_A = [player["num"] for player in get_current_present_players("A",GAME_DATA) if player["is_involved_in_faceoff"]]
        involved_players_B = [player["num"] for player in get_current_present_players("B",GAME_DATA) if player["is_involved_in_faceoff"]]
        is_in_offensive_zone = False
        if are_goalies_switched:
            if (last_shot_relative_x > 0) and (last_shot_relative_x < 0.5):
                if (winning_team == "A"):
                    is_in_offensive_zone = True
                elif (winning_team == "B"):
                    is_in_offensive_zone = False
            elif (last_shot_relative_x >= 0.5):
                if (winning_team == "B"):
                    is_in_offensive_zone = True
                elif (winning_team == "A"):
                    is_in_offensive_zone = False
        else:
            if (last_shot_relative_x > 0) and (last_shot_relative_x < 0.5):
                if (winning_team == "B"):
                    is_in_offensive_zone = True
                elif (winning_team == "A"):
                    is_in_offensive_zone = False
            elif (last_shot_relative_x >= 0.5):
                if (winning_team == "A"):
                    is_in_offensive_zone = True
                elif (winning_team == "B"):
                    is_in_offensive_zone = False
    
        faceoff = get_faceoff_dict(time_absolute, time_game, period_counter, last_shot_relative_x, last_shot_relative_y, involved_players_A, involved_players_B, winning_team, is_in_offensive_zone, is_faceoff_in_center, GAME_DATA)
        print(faceoff)
        GAME_DATA["faceoffs"].append(faceoff)

        is_field_touch_menu_on = False
        faceoff_win_by_team_B = False
        faceoff_win_by_team_A = False
        is_faceoff_in_center = False

        for player in (current_present_players_a):
            player["is_involved_in_faceoff"] = False # to avoid hidden faceoffs
        
        for player in (current_present_players_b):
            player["is_involved_in_faceoff"] = False # to avoid hidden faceoffs

def make_field_touch_menu(x, y, width, height, touch_input, touch_x, touch_y):
    global is_field_touch_menu_on
    DrawRectangleRec(Rectangle(x - 4, y - 4, width + 8, height + 8), BLACK)
    DrawRectangleRec(Rectangle(x, y, width, height), Fade(GRAY, 0.99))

    DrawTextCenteredInRoundedRectangle(b"ANNULER", 50, WHITE, x + width - int(WIDTH_RATIO * 500) - int(WIDTH_RATIO * 20), y + height - int(HEIGHT_RATIO * 100) - int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 500), int(HEIGHT_RATIO * 100), 0, RED, 4, WHITE)
    make_shot_touch_menu(x + int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 690), int(HEIGHT_RATIO * 660), touch_input, touch_input_x, touch_input_y)
    make_duel_touch_menu(x + int(WIDTH_RATIO * 20) + int(WIDTH_RATIO * 690) + int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 500), int(HEIGHT_RATIO * 160))
    make_faceoff_touch_menu(x + int(WIDTH_RATIO * 20) + int(WIDTH_RATIO * 690) + int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 20) + int(HEIGHT_RATIO * 160) + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 500), int(HEIGHT_RATIO *360))

    if touch_input:
        if is_touch_input_intersecting_with_rectangle(touch_x, touch_y, x + width - int(WIDTH_RATIO * 500) - int(WIDTH_RATIO * 20), y + height - int(HEIGHT_RATIO * 100) - int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 500), int(HEIGHT_RATIO * 100)):
            is_field_touch_menu_on = False
        elif is_touch_input_intersecting_with_rectangle(touch_x, touch_y, x + int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 690), int(HEIGHT_RATIO * 660)):
            print("shot")
        elif is_touch_input_intersecting_with_rectangle(touch_x, touch_y, x + int(WIDTH_RATIO * 20) + int(WIDTH_RATIO * 690) + int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 500), int(HEIGHT_RATIO * 260)):
            print("duel")
        elif is_touch_input_intersecting_with_rectangle(touch_x, touch_y, x + int(WIDTH_RATIO * 20) + int(WIDTH_RATIO * 690) + int(WIDTH_RATIO * 20), y + int(HEIGHT_RATIO * 20) + int(HEIGHT_RATIO * 260) + int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 500), int(HEIGHT_RATIO * 260)):
            print("faceoff")

# GuiLoadStyle(b"C:\Users\rapha\projects\raygui\styles\dark\dark.rgs")
InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, b"PROTOTYPE OF HOCKEY TRACKER")
SetTargetFPS(30)

last_iter_time = time.time()


while not WindowShouldClose():

    # iter_time_start = time.time()

    if is_game_ready_to_start():
        # do not export while beginning
        export_game_data(GAME_DATA, override_time_limit = False) # export every two seconds

    BeginDrawing()
    ClearBackground(RAYWHITE)
    
    input_touch_screen = GuiCheckBox(Rectangle(int(WIDTH_RATIO * 20), int(HEIGHT_RATIO * 20), int(WIDTH_RATIO * 100), int(HEIGHT_RATIO * 50)), b"TOUCH", input_touch_screen)

    # HANDLE INPUT

    # if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)) or (IsMouseButtonDown(MOUSE_BUTTON_LEFT)) or (IsMouseButtonReleased(MOUSE_BUTTON_LEFT)):
    #     print("IsMouseButtonPressed(MOUSE_BUTTON_LEFT):", IsMouseButtonPressed(MOUSE_BUTTON_LEFT))
    #     # print("IsMouseButtonPressed(MOUSE_BUTTON_RIGHT):", IsMouseButtonPressed(MOUSE_BUTTON_RIGHT))
    #     print("IsMouseButtonDown(MOUSE_BUTTON_LEFT):", IsMouseButtonDown(MOUSE_BUTTON_LEFT))
    #     print("IsMouseButtonReleased(MOUSE_BUTTON_LEFT):", IsMouseButtonReleased(MOUSE_BUTTON_LEFT))
    
    touch_input = False
    touch_input_x = 0
    touch_input_y = 0
    if (IsMouseButtonPressed(MOUSE_BUTTON_LEFT)):
        touch_input = True
        touch_input_x = GetMouseX()
        touch_input_y = GetMouseY()

    # For tactile screens, to test later
    if (GetTouchPointCount() == 1):
        touch_input = True
        touch_input_x = GetTouchX()
        touch_input_y = GetTouchY()
    
    # For surface tactile screen
    if input_touch_screen:
        move = Vector2()
        move = GetMouseDelta()
        if (move.x != 0) or (move.y != 0):
            touch_input = True
            touch_input_x = GetMouseX()
            touch_input_y = GetMouseY()

    if IS_GAME_STARTED:

        make_inline_hockey_terrain(int(WIDTH_RATIO * 335), int(HEIGHT_RATIO * 190), int(WIDTH_RATIO * 1250), int(HEIGHT_RATIO * 700))
        make_goals_drawing(int(WIDTH_RATIO * 335), int(HEIGHT_RATIO * 190), int(WIDTH_RATIO * 1250), int(HEIGHT_RATIO * 700))
        make_duels_drawing(int(WIDTH_RATIO * 335), int(HEIGHT_RATIO * 190), int(WIDTH_RATIO * 1250), int(HEIGHT_RATIO * 700))
        make_score_board(int(int(WIDTH_RATIO * 1920) / 2 - int(WIDTH_RATIO * 300) / 2), int(HEIGHT_RATIO * 0), int(WIDTH_RATIO * 300), int(HEIGHT_RATIO * 190))
        make_time_poss_graph_tracker(int(int(WIDTH_RATIO * 1920) / 2 + int(WIDTH_RATIO * 300) / 2), int(HEIGHT_RATIO * 0), int(WIDTH_RATIO * 200), int(HEIGHT_RATIO * 190))
        make_shots_graph_tracker(int(int(WIDTH_RATIO * 1920) / 2 - int(WIDTH_RATIO * 300) / 2 - int(WIDTH_RATIO * 350)), int(HEIGHT_RATIO * 0), int(WIDTH_RATIO * 350), int(HEIGHT_RATIO * 190))
        make_faceoffs_graph_tracker(int(int(WIDTH_RATIO * 1920) / 2 + int(WIDTH_RATIO * 300) / 2) +  int(WIDTH_RATIO * 200), int(HEIGHT_RATIO * 0), int(WIDTH_RATIO * 150), int(HEIGHT_RATIO * 190))
        
        make_current_players_pannel(int(WIDTH_RATIO * 20), int(HEIGHT_RATIO * 100), int(WIDTH_RATIO * 300), int(HEIGHT_RATIO * 920), touch_input, touch_input_x, touch_input_y)

        is_team_a_possess, is_team_b_possess, is_paused = make_time_pannel(int(WIDTH_RATIO * 1605), int(HEIGHT_RATIO * 260), int(WIDTH_RATIO * 300), int(HEIGHT_RATIO * 550), touch_input, touch_input_x, touch_input_y)

        # Make the touch terrain menu if activated
        if touch_input:
            if is_touch_input_intersecting_with_rectangle(touch_input_x, touch_input_y, int(WIDTH_RATIO * 335), int(HEIGHT_RATIO * 190), int(WIDTH_RATIO * 1250), int(HEIGHT_RATIO * 700)):
                relative_x, relative_y = get_touch_relative_rectangle_position(touch_input_x, touch_input_y, int(WIDTH_RATIO * 335), int(HEIGHT_RATIO * 190), int(WIDTH_RATIO * 1250), int(HEIGHT_RATIO * 700))
                print("TOUCH TERRAIN", relative_x, relative_y, last_shot_touch_relative_x, last_shot_touch_relative_y)
                if not is_field_touch_menu_on:
                    last_shot_touch_relative_x = relative_x
                    last_shot_touch_relative_y = relative_y
                    last_shot_relative_x = relative_x
                    last_shot_relative_y = relative_y
                    touch_input_x = 0
                    touch_input_y = 0
                    # Reset shot types and results to default (rebound and wrist)
                    is_shot_type = [False for k in shot_types]
                    is_shot_type[0] = True #wrist
                    is_shot_result = [False for k in shot_results]
                    is_shot_result[-1] = True #rebound

                #start the menu
                is_field_touch_menu_on = True
        
        if is_field_touch_menu_on:
            make_field_touch_menu(int(WIDTH_RATIO * 335), int(HEIGHT_RATIO * 190), int(WIDTH_RATIO * 1250), int(HEIGHT_RATIO * 700), touch_input, touch_input_x, touch_input_y)
        
        # Add 

    else:
        width_start_menu = 1720 * WIDTH_RATIO
        height_start_menu = 880 * HEIGHT_RATIO
        x_start_menu = 100 * WIDTH_RATIO
        y_start_menu = 100 * HEIGHT_RATIO

        if is_teams_ready():
            make_players_menu(int(x_start_menu), int(y_start_menu), int(width_start_menu), int(height_start_menu), touch_input, touch_input_x, touch_input_y)
        else:
            make_start_menu(int(x_start_menu), int(y_start_menu), int(width_start_menu), int(height_start_menu), touch_input, touch_input_x, touch_input_y)

        if is_game_ready_to_start():
            for box in INPUT_TEXT_BOXES:
                # Disable input text boxes
                if box["id_str"].startswith("start") or box["id_str"].startswith("players"):
                    box["is_active"] = False
                    box["is_selecte"] = False

            IS_GAME_STARTED = True
            GAME_DATA = load_game_data()
            set_timers(GAME_DATA["time_game"], GAME_DATA["time_team_A"], GAME_DATA["time_team_B"])
            time_start = time.time()
        
        time_game = GAME_DATA["time_game"] # bizarre que set_timers() n'agisse pas... set la variable directement
        time_team_a = GAME_DATA["time_team_A"] # bizarre que set_timers() n'agisse pas... set la variable directement
        time_team_b = GAME_DATA["time_team_B"] # bizarre que set_timers() n'agisse pas... set la variable directement

    set_selected_box(touch_input_x, touch_input_y)
    write_in_selected_box(GetKeyPressed())
    draw_text_input_boxes()

    if IsKeyPressed(KEY_TAB):
        go_to_next_box()

    if not is_paused:
        iter_time_end = time.time()
        time_game += (iter_time_end - last_iter_time)
        if is_team_b_possess:
            time_team_b += (iter_time_end - last_iter_time)
        if is_team_a_possess:
            time_team_a += (iter_time_end - last_iter_time)

        # print("ITER LASTED ", iter_time_end - last_iter_time, "teama", time_team_a, "teamb", time_team_b, "game : ", time_game)

        #Increment counters of shift time for present players, reset to 0 for other
        for player in GAME_DATA["Players_A"]:
            if player["is_on_field"]:
                player["time_on_field"] += (iter_time_end - last_iter_time)
            else:
                player["time_on_field"] = 0
        for player in GAME_DATA["Players_B"]:
            if player["is_on_field"]:
                player["time_on_field"] += (iter_time_end - last_iter_time)
            else:
                player["time_on_field"] = 0

    GAME_DATA["time_game"] = time_game
    GAME_DATA["time_team_B"] = time_team_a
    GAME_DATA["time_team_A"] = time_team_b


    last_iter_time = time.time()
    time_absolute = time.time() - time_start

    EndDrawing()

CloseWindow()
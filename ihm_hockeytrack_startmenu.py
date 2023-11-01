from ihm_hockeytrack_utils import *
import os
from datetime import datetime
import json

# Name game
# Add automatic date and time
# Create folder
# Create a team a file (or tab)
# Create a team b file (or tab)
# Create a players a file (or tab)
# Create a players b file (or tab)
# Create a shots a file (or tab)
# Create a shots b file (or tab)
# Create a duel file (or tab)
# Create a faceoffs file (or tab)

# Add team names and short names and colors
# Add players one by one with fields (and options) (licence, name, num, poste)

# Add in GAME_DATA then export game data
# Then reload game_data

IS_TEAMS_READY = False
IS_GAME_READY_TO_START = False
GAME_DATA = load_game_data_default()

DEFAULT_MAX_CHAR = 1024

INPUT_TEXT_BOXES = []

FLAG_TXT_DEFAULT = 0
FLAG_TXT_NUMER_ONLY = 1
FLAG_TXT_TEXT_ONLY = 2

LOAD_GAME_DATA_DIRECTORY = os.path.join(os.curdir, "games_data")
SAVE_GAME_DATA_DIRECTORY = os.path.join(os.curdir, "games_data", datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
if not os.path.exists(SAVE_GAME_DATA_DIRECTORY):
    os.makedirs(SAVE_GAME_DATA_DIRECTORY)

LAST_EXPORT_GAME_DATA = time.time()
EXPORT_EVERY_S = 2

def get_valid_input_dir_list():
    subfolders = [ f.path for f in os.scandir(LOAD_GAME_DATA_DIRECTORY) if f.is_dir() ]
    valid_subfolders = []

    required = ["teams.xlsx", "players.xlsx", "shots.xlsx", "duels.xlsx", "faceoffs.xlsx"]
    for folder in subfolders:
        is_folder_valid = True
        for req in required:
            if not os.path.exists(os.path.join(folder, req)):
                is_folder_valid = False

        if is_folder_valid:
            valid_subfolders.append(folder)
    
    return valid_subfolders

def export_game_data(game_data, override_time_limit = True):
    global LAST_EXPORT_GAME_DATA
    # a_file = open(os.path.join(SAVE_GAME_DATA_DIRECTORY,"game_data.json"), "w")
    # json.dump(game_data, a_file)
    # a_file.close()

    if (time.time() - LAST_EXPORT_GAME_DATA > EXPORT_EVERY_S) or override_time_limit:

        print("EXPORTING game_data !")

        teams = {"Team_A":[game_data["team_name_A"].decode(), 
                           game_data["team_short_name_A"].decode(), 
                           game_data["time_team_A"],
                           game_data["time_game"],
                           game_data["team_color_A"][0], 
                           game_data["team_color_A"][1], 
                           game_data["team_color_A"][2], 
                           game_data["team_color_A"][3]],
                "Team_B":[game_data["team_name_B"].decode(), 
                          game_data["team_short_name_B"].decode(), 
                          game_data["time_team_B"],
                          game_data["time_game"],
                          game_data["team_color_B"][0], 
                          game_data["team_color_B"][1], 
                          game_data["team_color_B"][2], 
                          game_data["team_color_B"][3]]}
        
        df_teams = pd.DataFrame(teams)
        print(df_teams)
        df_teams.to_excel(os.path.join(SAVE_GAME_DATA_DIRECTORY,"teams.xlsx"))

        # To add : 
        # n_duels, n_win duels, n_loss_duels (functions getters), 
        # n_faceoff, n_faceoff win, n_faceoff_loose, n_faceoff_neutral (ajouter neutral, functions getters), 
        # shots_blocked (ajouter au getter en plus de shots, shots_on_goal, shots_missed), 
        # shots, shots_on_goal, shots_missed, shots_blocked when in powerplay (add distinction and in getter)
        # [puck_loss, puck_win --> in duels]
        # goal for when on field, goal against when on field (save and make a getter)
        # block_shot -> add a selector for who blocked when the "blocked" type of shot is selected then a getter

        # TO ADD IN MENU --> bottom bar, select from available players then proposal
        # decisive pass, masking goalie, 
        # occasion, mistake_occasion, anihilate_adv_occasion



        players = {"team_id":[], "team" : [], "licence":[], "name":[], "num":[], "poste":[], "stick_side":[], "time_on_field":[], "time_on_field_total":[], "shots":[], "shots_on_goal":[], "goals":[]}
        for player in game_data["Players_A"]:
            players["team_id"].append(0)
            players["team"].append(game_data["team_name_A"].decode())
            players["licence"].append(int(player["licence"]))
            players["name"].append(player["name"])
            players["num"].append(player["num"])
            players["poste"].append(player["poste"])
            players["stick_side"].append(player["stick_side"])
            players["time_on_field"].append(player["time_on_field_total"])
            players["time_on_field_total"].append(player["time_on_field_total"])
            count_shots, count_shots_on_goal, count_goals = get_shots_on_goal_by_player_team_and_num("A", player["num"], game_data)
            players["shots"].append(count_shots)
            players["shots_on_goal"].append(count_shots_on_goal)
            players["goals"].append(count_goals)


        for player in game_data["Players_B"]:
            players["team_id"].append(1)
            players["team"].append(game_data["team_name_B"].decode())
            players["licence"].append(int(player["licence"]))
            players["name"].append(player["name"])
            players["num"].append(player["num"])
            players["poste"].append(player["poste"])
            players["stick_side"].append(player["stick_side"])
            players["time_on_field"].append(player["time_on_field"])
            players["time_on_field_total"].append(player["time_on_field_total"])
            count_shots, count_shots_on_goal, count_goals = get_shots_on_goal_by_player_team_and_num("B", player["num"], game_data)
            players["shots"].append(count_shots)
            players["shots_on_goal"].append(count_shots_on_goal)
            players["goals"].append(count_goals)

        for key in players.keys():
            print(key, len(players[key]))

        print(players)

        df_players = pd.DataFrame(players)
        print(df_players)
        df_players.to_excel(os.path.join(SAVE_GAME_DATA_DIRECTORY,"players.xlsx"))

        shot_dict = {}
        
        for key in DUMMY_SHOT.keys():
            shot_dict[key] = []

        for shot in game_data["shots_A"]:
            for key in DUMMY_SHOT.keys():
                if key in shot.keys():
                    print(key, shot[key])
                    shot_dict[key].append(shot[key])
                else:
                    shot_dict[key].append(DUMMY_SHOT[key])

        for shot in game_data["shots_B"]:
            for key in DUMMY_SHOT.keys():
                if key in shot.keys():
                    print(key, shot[key])
                    shot_dict[key].append(shot[key])
                else:
                    shot_dict[key].append(DUMMY_SHOT[key])
                    
        shot_df = pd.DataFrame(shot_dict)
        shot_df.to_excel(os.path.join(SAVE_GAME_DATA_DIRECTORY,"shots.xlsx"))

        # To add :
        # shots.xlsx with shots data (time, position etc)
        # Add option "is goalie masked"
        
        duels_dict = {}

        for key in DUMMY_DUEL.keys():
            duels_dict[key] = []

        for duel in game_data["duels"]:
            for key in duel.keys():
                duels_dict[key].append(duel[key])

        duel_df = pd.DataFrame(duels_dict)

        print(duel_df)
        duel_df.to_excel(os.path.join(SAVE_GAME_DATA_DIRECTORY,"duels.xlsx"))

        # Faceoffs
        faceoffs_dict = {}

        for key in DUMMY_FACEOFF.keys():
            faceoffs_dict[key] = []

        for faceoff in game_data["faceoffs"]:
            for key in faceoff.keys():
                faceoffs_dict[key].append(faceoff[key])

        faceoffs_df = pd.DataFrame(faceoffs_dict)

        print(faceoffs_df)
        faceoffs_df.to_excel(os.path.join(SAVE_GAME_DATA_DIRECTORY,"faceoffs.xlsx"))


        LAST_EXPORT_GAME_DATA = time.time()
        
        # To add :
        # line.xlsx with occasions and other stats by line, add a line selector near the time pannel (L1, L2, L3, PP1, PP2, PK1, PK2)

    else:
        # print("NOT EXPORTING game_data (done less than 2 sec ago) !")
        # do not export if it has been exported less than 2 seconds ago
        pass

def load_game_data(data_dir = SAVE_GAME_DATA_DIRECTORY):
    #  reload GAME_DATA from files everytime it has been exported and set cached one, else just send cached one
    # make a set_game_data() to update cache with current game_data of ihm_hockey_track.py
    if os.path.exists(os.path.join(data_dir,"teams.xlsx")):
        df_teams = pd.read_excel(os.path.join(data_dir,"teams.xlsx"))

        team_A_data = df_teams["Team_A"]
        GAME_DATA["team_name_A"] = team_A_data[0].encode('ascii')
        GAME_DATA["team_short_name_A"] = team_A_data[1].encode('ascii')
        team_A_color = (team_A_data[4],team_A_data[5],team_A_data[6],team_A_data[7])
        GAME_DATA["team_color_A"] = team_A_color
        GAME_DATA["time_team_A"] = team_A_data[2]

        team_B_data = df_teams["Team_B"]
        GAME_DATA["team_name_B"] = team_B_data[0].encode('ascii')
        GAME_DATA["team_short_name_B"] = team_B_data[1].encode('ascii')
        team_B_color = (team_B_data[6],team_B_data[5],team_B_data[6],team_B_data[7])
        GAME_DATA["team_color_B"] = team_B_color
        GAME_DATA["time_team_B"] = team_B_data[2]

        GAME_DATA["time_game"] = team_B_data[3] #use this one because info is duplicate

        set_timers(GAME_DATA["time_game"], GAME_DATA["time_team_A"], GAME_DATA["time_team_B"])

        print(GAME_DATA)
    
    if os.path.exists(os.path.join(data_dir,"players.xlsx")):
        players_A = []
        players_B = []

        df_players = pd.read_excel(os.path.join(data_dir,"players.xlsx"))
        players_keys = GAME_DATA["Players_A"][0].keys()

        for i in range(len(df_players)):
            if df_players.loc[i, "team_id"] == 0:
                player = {}
                for key in players_keys:
                    if key in df_players.columns:
                        player[key] = df_players.loc[i, key]
                    else:
                        player[key] = DUMMY_PLAYER[key]

                players_A.append(player)
            elif df_players.loc[i, "team_id"] == 1:
                player = {}
                for key in players_keys:
                    if key in df_players.columns:
                        player[key] = df_players.loc[i, key]
                    else:
                        player[key] = DUMMY_PLAYER[key]

                players_B.append(player)


        GAME_DATA["Players_A"] = players_A
        GAME_DATA["Players_B"] = players_B

    if os.path.exists(os.path.join(data_dir,"shots.xlsx")):
        shots_A = []
        shots_B = []

        df_shots = pd.read_excel(os.path.join(data_dir,"shots.xlsx"))
        shot_keys = DUMMY_SHOT.keys()

        print(df_shots.columns)

        for i in range(len(df_shots)):
            if df_shots.loc[i, "team_shooter_id"] == 0:
                shot = {}
                for key in shot_keys:
                    if key in df_shots.columns:
                        shot[key] = df_shots.loc[i, key]
                    else:
                        player[key] = DUMMY_SHOT[key]

                shots_A.append(shot)
            elif df_shots.loc[i, "team_shooter_id"] == 1:
                shot = {}
                for key in shot_keys:
                    if key in df_shots.columns:
                        shot[key] = df_shots.loc[i, key]
                    else:
                        player[key] = DUMMY_SHOT[key]

                shots_B.append(shot)


        GAME_DATA["shots_A"] = shots_A
        GAME_DATA["shots_B"] = shots_B

    if os.path.exists(os.path.join(data_dir,"duels.xlsx")):
        duels = []

        df_duels = pd.read_excel(os.path.join(data_dir,"duels.xlsx"))
        duel_keys = DUMMY_DUEL.keys()

        print(df_duels.columns)

        for i in range(len(df_duels)):
            duel = {}
            for key in duel_keys:
                if key in df_duels.columns:
                    duel[key] = df_duels.loc[i, key]
                else:
                    duel[key] = DUMMY_DUEL[key]

            duels.append(duel)

        GAME_DATA["duels"] = duels

    if os.path.exists(os.path.join(data_dir,"faceoffs.xlsx")):
        faceoffs = []

        df_faceoffs = pd.read_excel(os.path.join(data_dir,"faceoffs.xlsx"))
        faceoff_keys = DUMMY_FACEOFF.keys()

        print(df_faceoffs.columns)

        for i in range(len(df_faceoffs)):
            faceoff = {}
            for key in faceoff_keys:
                if key in df_faceoffs.columns:
                    faceoff[key] = df_faceoffs.loc[i, key]
                else:
                    faceoff[key] = DUMMY_FACEOFF[key]

            faceoffs.append(faceoff)

        GAME_DATA["faceoffs"] = faceoffs

    return GAME_DATA



def go_to_next_box():
    print("GO TO NEXT BOX !!!!!")
    gotonextbox = False
    for box in INPUT_TEXT_BOXES:
        if box["is_active"]:
            if gotonextbox:
                box["is_selected"] = True
                break
            else:
                if box["is_selected"]:
                    box["is_selected"] = False
                    gotonextbox = True
            

def write_in_selected_box(key):
    if key >= 32 and key <= 125:
        print(key)
        char = AZERTY_MAP[key]
        char = str(char).upper()

        for box in INPUT_TEXT_BOXES:
            if box["is_selected"] and box["is_active"]:
                print(box["current_text"], char.encode('ascii'))
                if (box["flag"] == FLAG_TXT_NUMER_ONLY) and (char not in '0123456789'):
                    char = ''
                elif (box["flag"] == FLAG_TXT_TEXT_ONLY) and (char in '0123456789'):
                    char = ''
                
                if (len(box["current_text"]) < box["max_char"]):
                    box["current_text"] += char.encode('ascii')

    elif key == KEY_BACKSPACE:
        for box in INPUT_TEXT_BOXES:
            if box["is_selected"] and box["is_active"]:
                 box["current_text"] = box["current_text"][:-1]


def set_selected_box(touch_input_x, touch_input_y):

    if touch_input_x != 0 or touch_input_y != 0:
        # A click has been done, start by putting everyone to false
        for i,box in enumerate(INPUT_TEXT_BOXES):
            box["is_selected"] = False
    
    for box in INPUT_TEXT_BOXES:
        if is_touch_input_intersecting_with_rectangle(touch_input_x, touch_input_y, box["x"], box["y"], box["width"], box["height"]):
            box["is_selected"] = True
            break
    

def draw_text_input_boxes():
    for box in INPUT_TEXT_BOXES:
        if box["is_active"]:
            if box["is_selected"]:
                DrawTextCenteredInRoundedRectangle(box["current_text"], int(box["text_size"]), box["text_color"], int(box["x"]), int(box["y"]), int(box["width"]), int(box["height"]), 0, LIGHTGRAY, 5, box["line_color"])
            else:
                DrawTextCenteredInRoundedRectangle(box["current_text"], int(box["text_size"]), box["text_color"], int(box["x"]), int(box["y"]), int(box["width"]), int(box["height"]), 0, WHITE, 5, box["line_color"])

def add_input_text_box(x, y, width, height, text_size, idstr, is_active, is_selected, current_text, textcolor = BLACK, linecolor = BLACK, max_char = DEFAULT_MAX_CHAR, flag = FLAG_TXT_DEFAULT):
    global INPUT_TEXT_BOXES

    # Check if box already exists then if so modify the values
    is_box_existing = any([box["id_str"] == idstr for box in INPUT_TEXT_BOXES])

    if not is_box_existing:
        current_text_box = {"id_str" :  idstr, "x" : x, "y" : y, "width" : width, "height" : height, "text_size" : text_size, "is_active" : is_active, "is_selected" : False,  "current_text" : current_text, "max_char" : max_char, "text_color": textcolor, "line_color": linecolor, "flag": flag}
        INPUT_TEXT_BOXES.append(current_text_box)
        print("Added box to list : ", current_text_box)

def get_box_attribute(id_str, attribute):
    for box in INPUT_TEXT_BOXES:
        if box["id_str"] == id_str:
            return box[attribute]
    return 0
        
def set_box_attribute(id_str, attribute, value):
    for box in INPUT_TEXT_BOXES:
        if box["id_str"] == id_str:
            box[attribute] = value
            return 0
    return -1


team_colors = [GOLD, BLUE, DARKBLUE, DARKBROWN, PURPLE, RED, PINK, GREEN, LIME, VIOLET, MAGENTA, BEIGE]
is_color_selected_A = [False for i in team_colors]
is_color_selected_B = [False for i in team_colors]

def get_team_A_selected_color():
    color = WHITE
    for i, c in enumerate(team_colors):
        if is_color_selected_A[i]:
            return c
    return color

def get_team_B_selected_color():
    color = WHITE
    for i, c in enumerate(team_colors):
        if is_color_selected_B[i]:
            return c
    return color

def is_teams_ready():
    return IS_TEAMS_READY

def is_game_ready_to_start():
    return IS_GAME_READY_TO_START

def make_start_menu(x, y, width, height, touch_input, touch_input_x, touch_input_y):
    global is_color_selected_A
    global is_color_selected_B
    global IS_TEAMS_READY
    global IS_GAME_READY_TO_START
    global GAME_DATA

    # Creer le dossier si il n'existe pas

    DrawRectangle(x, y, width, height, LIGHTGRAY)
    
    # Faire un système custom :
    # Creer une boite et ajouter à un dict de boites (identifiant -str, activee - bool, selectionee - bool, texte courant - str)
    # Dessiner toutes les boites active à chaque iteration, couleur spécifique pour la sélectionnée
    # Ajouter du texte dans la boite selectionne si il y en a une et qu'il y a des inputs de touches


    add_input_text_box(x + 100 * WIDTH_RATIO, y + 100 * HEIGHT_RATIO, width - 500 * WIDTH_RATIO, 50 * HEIGHT_RATIO, 40 * HEIGHT_RATIO, "start_team_name_a_box", True, False, b"TEAM A")
    add_input_text_box(x + 100 * WIDTH_RATIO, y + 300 * HEIGHT_RATIO, width - 500 * WIDTH_RATIO, 50 * HEIGHT_RATIO, 40 * HEIGHT_RATIO, "start_team_name_b_box", True, False, b"TEAM B")

    add_input_text_box(x + 100 * WIDTH_RATIO + width - 500 * WIDTH_RATIO + 20, y + 100 * HEIGHT_RATIO, 280 * WIDTH_RATIO, 50 * HEIGHT_RATIO, 40 * HEIGHT_RATIO, "start_team_shortname_a_box", True, False, b"TA")
    add_input_text_box(x + 100 * WIDTH_RATIO + width - 500 * WIDTH_RATIO + 20, y + 300 * HEIGHT_RATIO, 280 * WIDTH_RATIO, 50 * HEIGHT_RATIO, 40 * HEIGHT_RATIO, "start_team_shortname_b_box", True, False, b"TB")

    n_colors = len(team_colors)
    color_spacing = 10 * WIDTH_RATIO
    color_width_total = width - 200 * WIDTH_RATIO - (n_colors - 1) * color_spacing
    color_width = color_width_total / n_colors

    for i,color in enumerate(team_colors):

        if touch_input:
            if is_touch_input_intersecting_with_rectangle(touch_input_x, touch_input_y,  x + 100 * WIDTH_RATIO + i * color_width + i * color_spacing, y + 170 * HEIGHT_RATIO, color_width, 50 * HEIGHT_RATIO):
                is_color_selected_A[i] = not is_color_selected_A[i]
                if is_color_selected_A[i]:
                    for j, c in enumerate(team_colors): 
                        if j != i:
                            is_color_selected_A[j] = False

            if is_touch_input_intersecting_with_rectangle(touch_input_x, touch_input_y,  x + 100 * WIDTH_RATIO + i * color_width + i * color_spacing, y + 370 * HEIGHT_RATIO, color_width, 50 * HEIGHT_RATIO):
                is_color_selected_B[i] = not is_color_selected_B[i]
                if is_color_selected_B[i]:
                    for j, c in enumerate(team_colors): 
                        if j != i:
                            is_color_selected_B[j] = False

        if is_color_selected_A[i]:
            border_width_a = 5
        else:
            border_width_a = 0
        
        if is_color_selected_B[i]:
            border_width_b = 5
        else:
            border_width_b = 0

        DrawTextCenteredInRoundedRectangle(b"", 25, color, x + 100 * WIDTH_RATIO + i * color_width + i * color_spacing, y + 170 * HEIGHT_RATIO, color_width, 50 * HEIGHT_RATIO, 0, color, border_width_a, BLACK)
        DrawTextCenteredInRoundedRectangle(b"", 25, color, x + 100 * WIDTH_RATIO + i * color_width + i * color_spacing, y + 370 * HEIGHT_RATIO, color_width, 50 * HEIGHT_RATIO, 0, color, border_width_b, BLACK)


    name_a = get_box_attribute("start_team_name_a_box", "current_text")
    name_b = get_box_attribute("start_team_name_b_box", "current_text")
    short_name_a = get_box_attribute("start_team_shortname_a_box", "current_text")
    short_name_b = get_box_attribute("start_team_shortname_b_box", "current_text")

    if get_team_A_selected_color() != WHITE and get_team_B_selected_color() != WHITE:
        if len(name_a) >= 4 and len(name_a) < 256 and len(name_b) >= 4 and len(name_b) < 256:
            if len(short_name_a) >= 2 and len(short_name_a) <= 4 and len(short_name_b) >= 2 and len(short_name_b) <= 4:
                DrawTextCenteredInRoundedRectangle(b"OK", 25, GREEN, x + 100 * WIDTH_RATIO, y + 500 * HEIGHT_RATIO, width - 200 * WIDTH_RATIO, 50 * HEIGHT_RATIO, 2, WHITE, 5, GREEN)
                if is_touch_input_intersecting_with_rectangle(touch_input_x, touch_input_y,  x + 100 * WIDTH_RATIO, y + 500 * HEIGHT_RATIO, width - 200 * WIDTH_RATIO, 50 * HEIGHT_RATIO):
                    IS_TEAMS_READY = True
                    for box in INPUT_TEXT_BOXES:
                        # Disable input text boxes
                        if box["id_str"].startswith("start"):
                            box["is_active"] = False
                            box["is_selecte"] = False
                    GAME_DATA["team_name_A"] = name_a
                    GAME_DATA["team_name_B"] = name_b
                    GAME_DATA["team_short_name_A"] = short_name_a
                    GAME_DATA["team_short_name_B"] = short_name_b
                    GAME_DATA["team_color_A"] = get_team_A_selected_color()
                    GAME_DATA["team_color_B"] = get_team_B_selected_color()
                    export_game_data(GAME_DATA)
            else:
                DrawTextCenteredInRoundedRectangle(b"Short name must be 2 to 4 char long", 25, RED, x + 100 * WIDTH_RATIO, y + 500 * HEIGHT_RATIO, width - 200 * WIDTH_RATIO, 50 * HEIGHT_RATIO, 0, LIGHTGRAY, 0, RED)
        else:
            DrawTextCenteredInRoundedRectangle(b"Name must be 4 to 256 char long", 25, RED, x + 100 * WIDTH_RATIO, y + 500 * HEIGHT_RATIO, width - 200 * WIDTH_RATIO, 50 * HEIGHT_RATIO, 0, LIGHTGRAY, 0, RED)
    else:   
        DrawTextCenteredInRoundedRectangle(b"Please select a color for each team", 25, RED, x + 100 * WIDTH_RATIO, y + 500 * HEIGHT_RATIO, width - 200 * WIDTH_RATIO, 50 * HEIGHT_RATIO, 0, LIGHTGRAY, 0, RED)

    # DrawTextCenteredInRoundedRectangle(b"OK", 25, BLACK, x + int(WIDTH_RATIO * 100 + width - 300 * WIDTH_RATIO) + 20 * WIDTH_RATIO, y + int(HEIGHT_RATIO * 300), int(60 * WIDTH_RATIO), int(HEIGHT_RATIO * 50), 0, WHITE, 5, BLACK)
    # DrawTextCenteredInRoundedRectangle(b"OK", 25, BLACK, x + int(WIDTH_RATIO * 100 + width - 300 * WIDTH_RATIO) + 20 * WIDTH_RATIO, y + int(HEIGHT_RATIO * 500), int(60 * WIDTH_RATIO), int(HEIGHT_RATIO * 50), 0, WHITE, 5, BLACK)

    # Ajouter un bouton de sélection de la couleur
    # Ajouter un bouton pour valider et ajouter à GAME_DATA

    valid_directories_list = get_valid_input_dir_list()

    y_folders = 20 + 50
    for directory in valid_directories_list:
        DrawTextCenteredInRoundedRectangle(directory.encode('ascii'), 20, BLACK, x + 100 * WIDTH_RATIO, y + 500 * HEIGHT_RATIO + y_folders * HEIGHT_RATIO, width - 200 * WIDTH_RATIO, 25 * HEIGHT_RATIO, 0, WHITE, 2, BLACK)
        if is_touch_input_intersecting_with_rectangle(touch_input_x, touch_input_y, x + 100 * WIDTH_RATIO, y + 500 * HEIGHT_RATIO + y_folders * HEIGHT_RATIO, width - 200 * WIDTH_RATIO, 25 * HEIGHT_RATIO):
            GAME_DATA = load_game_data(directory)
            export_game_data(GAME_DATA)
            IS_GAME_READY_TO_START = True

        y_folders += 30


    #select a valid directory
    #load data (from directory)
    #export data (in current save directory)
    #set IS_GAME_READY_TO_START to true


    # Exporter GAME_DATA

    if IS_GAME_READY_TO_START:
        DrawTextCenteredInRoundedRectangle(b"START GAME", int(20 * HEIGHT_RATIO), BLACK, int(x + 50 * WIDTH_RATIO), int(y + height - 120 * HEIGHT_RATIO), int(width - 100 * WIDTH_RATIO), int(100 * HEIGHT_RATIO), 5, SKYBLUE, 5, BLACK)


max_players = 16
players_a_active = [False for i in range(max_players)]
players_a_goal = [False for i in range(max_players)]
players_a_for = [False for i in range(max_players)]
players_a_def = [False for i in range(max_players)]
players_a_stick_left = [False for i in range(max_players)]

players_b_active = [False for i in range(max_players)]
players_b_goal = [False for i in range(max_players)]
players_b_for = [False for i in range(max_players)]
players_b_def = [False for i in range(max_players)]
players_b_stick_left = [False for i in range(max_players)]

def make_players_menu(x, y, width, height, touch_input, touch_input_x, touch_input_y):
    global players_a_active
    global players_a_goal
    global players_a_for
    global players_a_def
    global players_b_active
    global players_b_goal
    global players_b_for
    global players_b_def
    global IS_GAME_READY_TO_START
    global GAME_DATA

    DrawRectangle(x, y, width, height, DARKGRAY)

    text_box_margin = 10 * HEIGHT_RATIO
    text_box_height = (height - 200 * HEIGHT_RATIO - text_box_margin * max_players) / max_players
    text_box_height_tot = text_box_height + text_box_margin

    width_div = width / 32
    # ################################
    # ||lllnnnnn°°ppp||lllnnnnn°°ppp||
    for i in range(max_players):
        if players_a_active[i] == True:
            input_box_line_color = get_team_color("A", GAME_DATA)
        else:
            input_box_line_color = BLACK
        
        add_input_text_box(x + 2 * width_div, y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 2 * width_div, text_box_height, int(text_box_height * 0.6), "players_licence_a_%d"%i, True, False, b"%05d"%np.random.randint(0,100000), BLACK, input_box_line_color, max_char = 6, flag = FLAG_TXT_NUMER_ONLY)
        set_box_attribute("players_licence_a_%d"%i, "line_color", input_box_line_color)

        add_input_text_box(x + 4 * width_div, y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 5 * width_div, text_box_height, int(text_box_height * 0.6), "players_name_a_%d"%i, True, False, b"PLAYER %d"%i, BLACK, input_box_line_color)
        set_box_attribute("players_name_a_%d"%i, "line_color", input_box_line_color)

        add_input_text_box(x + 9 * width_div, y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, int(text_box_height * 0.9), "players_num_a_%d"%i, True, False, b"%02d"%i, BLACK, input_box_line_color, max_char = 2, flag = FLAG_TXT_NUMER_ONLY)
        set_box_attribute("players_num_a_%d"%i, "line_color", input_box_line_color)

        make_color_toggle(x + 10 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, players_a_goal[i], 5, input_box_line_color, b"G")
        players_a_goal[i] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + 10 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, players_a_goal[i], 5)
        
        make_color_toggle(x + 11 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, players_a_for[i], 5, input_box_line_color, b"F")
        players_a_for[i] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + 11 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, players_a_for[i], 5)
        
        make_color_toggle(x + 12 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, players_a_def[i], 5, input_box_line_color, b"D")
        players_a_def[i] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + 12 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, players_a_def[i], 5)

        if players_a_stick_left[i]:
            make_color_toggle(x + 13 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 2 * width_div, text_box_height, players_a_stick_left[i], 5, input_box_line_color, b"Left", color_true = WHITE, color_false = WHITE)
        else:
            make_color_toggle(x + 13 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 2 * width_div, text_box_height, players_a_stick_left[i], 5, input_box_line_color, b"Right", color_true = WHITE, color_false = WHITE)

        players_a_stick_left[i] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + 13 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 2 * width_div, text_box_height, players_a_stick_left[i], 5)

        n_active = players_a_goal[i] + players_a_for[i] + players_a_def[i]
        if n_active == 0:
            players_a_active[i] = False
        elif n_active == 1:
            players_a_active[i] = True
        else:
            players_a_active[i] = False
            players_a_goal[i] = False
            players_a_for[i] = False
            players_a_def[i] = False


    for i in range(max_players):
        if players_b_active[i] == True:
            input_box_line_color = get_team_color("B", GAME_DATA)
        else:
            input_box_line_color = BLACK

        add_input_text_box(x + 17 * width_div, y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 2 * width_div, text_box_height, int(text_box_height * 0.6), "players_licence_b_%d"%i, True, False, b"%05d"%np.random.randint(0,100000), BLACK, input_box_line_color, max_char = 6, flag = FLAG_TXT_NUMER_ONLY)
        set_box_attribute("players_licence_b_%d"%i, "line_color", input_box_line_color)

        add_input_text_box(x + 19 * width_div, y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 5 * width_div, text_box_height, int(text_box_height * 0.6), "players_name_b_%d"%i, True, False, b"PLAYER %d"%i, BLACK, input_box_line_color)
        set_box_attribute("players_name_b_%d"%i, "line_color", input_box_line_color)

        add_input_text_box(x + 24 * width_div, y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, int(text_box_height * 0.9), "players_num_b_%d"%i, True, False, b"%02d"%i, BLACK, input_box_line_color, max_char = 2, flag = FLAG_TXT_NUMER_ONLY)
        set_box_attribute("players_num_b_%d"%i, "line_color", input_box_line_color)

        make_color_toggle(x + 25 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, players_b_goal[i], 5, input_box_line_color, b"G")
        players_b_goal[i] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + 25 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, players_b_goal[i], 5)
        
        make_color_toggle(x + 26 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, players_b_for[i], 5, input_box_line_color, b"F")
        players_b_for[i] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + 26 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, players_b_for[i], 5)
        
        make_color_toggle(x + 27 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, players_b_def[i], 5, input_box_line_color, b"D")
        players_b_def[i] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + 27 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 1 * width_div, text_box_height, players_b_def[i], 5)

        if players_b_stick_left[i]:
            make_color_toggle(x + 28 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 2 * width_div, text_box_height, players_b_stick_left[i], 5, input_box_line_color, b"Left", color_true = WHITE, color_false = WHITE)
        else:
            make_color_toggle(x + 28 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 2 * width_div, text_box_height, players_b_stick_left[i], 5, input_box_line_color, b"Right", color_true = WHITE, color_false = WHITE)

        players_b_stick_left[i] = click_color_toggle(touch_input, touch_input_x, touch_input_y, x + 28 * width_div,  y + 50 * HEIGHT_RATIO + i * text_box_height_tot, 2 * width_div, text_box_height, players_b_stick_left[i], 5)

        n_active = players_b_goal[i] + players_b_for[i] + players_b_def[i]
        if n_active == 0:
            players_b_active[i] = False
        elif n_active == 1:
            players_b_active[i] = True
        else:
            players_b_active[i] = False
            players_b_goal[i] = False
            players_b_for[i] = False
            players_b_def[i] = False
    
    nb_valid_a = 0
    nb_valid_b = 0
    nb_goal_a = 0
    nb_goal_b = 0
    display_text = "Error missing name or num at players :"
    has_invalid_input = False
    display_ready_to_start_button = False

    for i in range(max_players):
        if players_a_active[i]:
            name = get_box_attribute("players_name_a_%d"%i, "current_text")
            num = get_box_attribute("players_num_a_%d"%i, "current_text")
            if len(num) == 0 or len(name) < 4:
                display_text += " A-%d,"%i
                has_invalid_input = True
            else:
                nb_valid_a += 1
        if players_a_goal[i]:
            nb_goal_a += 1

    for i in range(max_players):
        if players_b_active[i]:
            name = get_box_attribute("players_name_b_%d"%i, "current_text")
            num = get_box_attribute("players_num_b_%d"%i, "current_text")
            if len(num) == 0 or len(name) < 4:
                display_text += " B-%d,"%i
                has_invalid_input = True
            else:
                nb_valid_b += 1

        if players_b_goal[i]:
            nb_goal_b += 1

    if not has_invalid_input:
        if (nb_goal_a < 1) or (nb_goal_b < 1) or (nb_goal_a > 2) or (nb_goal_b > 2):
            display_text = "1 or 2 goals required per team (%d A and %d B)"%(nb_goal_a, nb_goal_b)
            display_ready_to_start_button = False
        
        print(nb_valid_a - nb_goal_a, nb_valid_b - nb_goal_b, ((nb_valid_a - nb_goal_a) < 6), ((nb_valid_b - nb_goal_b) < 6))
        if (nb_valid_a < 7) or (nb_valid_b < 7) or ((nb_valid_a - nb_goal_a) < 6) or ((nb_valid_b - nb_goal_b) < 6):
            if ( (nb_goal_a > 2) or (nb_goal_b > 2)):
                display_text = "1 or 2 goals required per team (%d A and %d B)"%(nb_goal_a, nb_goal_b)
                display_ready_to_start_button = False
            else:
                display_text = "Minimum 6 + 1 players required (%d A and %d B)"%(nb_valid_a, nb_valid_b)
                display_ready_to_start_button = False
        
    if not ( (nb_valid_a < 7) or (nb_valid_b < 7) or (nb_goal_a < 1) or (nb_goal_b < 1) or (nb_goal_a > 2) or (nb_goal_b > 2) or ((nb_valid_a - nb_goal_a) < 6) or ((nb_valid_b - nb_goal_b) < 6)):
        display_ready_to_start_button = True
    
    if has_invalid_input:
        display_ready_to_start_button = False

    if display_ready_to_start_button:
        DrawTextCenteredInRoundedRectangle(b"START GAME", int(20 * HEIGHT_RATIO), BLACK, int(x + 50 * WIDTH_RATIO), int(y + height - 120 * HEIGHT_RATIO), int(width - 100 * WIDTH_RATIO), int(100 * HEIGHT_RATIO), 5, SKYBLUE, 5, BLACK)
    else:
        DrawTextCenteredInRoundedRectangle(display_text.encode('ascii'), int(20 * HEIGHT_RATIO), RED, int(x + 50 * WIDTH_RATIO), int(y + height - 120 * HEIGHT_RATIO), int(width - 100 * WIDTH_RATIO), int(100 * HEIGHT_RATIO), 5, WHITE, 0, BLACK)
    
    if is_touch_input_intersecting_with_rectangle(touch_input_x, touch_input_y,  int(x + 50 * WIDTH_RATIO), int(y + height - 120 * HEIGHT_RATIO), int(width - 100 * WIDTH_RATIO), int(100 * HEIGHT_RATIO)):
        players_a_list = []
        for i in range(max_players):
            if players_a_active[i]:
                name = get_box_attribute("players_name_a_%d"%i, "current_text")
                num = int(get_box_attribute("players_num_a_%d"%i, "current_text"))
                poste = "none"
                if players_a_goal[i]:
                    poste="goalie"
                elif players_a_def[i]:
                    poste = "def"
                elif players_a_for[i]:
                    poste = "for"
                
                stick_side = "right"
                if players_a_stick_left[i]:
                    stick_side = "left"

                licence = int(get_box_attribute("players_licence_a_%d"%i, "current_text"))
                player = {"licence": licence, 
                          "name":name, 
                          "num": num, 
                          "poste":poste, 
                          "stick_side":stick_side, 
                          "is_on_field":False, 
                          "time_on_field":0, 
                          "time_on_field_total":0, 
                          "is_current_shooter":False, 
                          "is_current_passer":False, 
                          "is_involved_in_duel":False, 
                          "is_involved_in_faceoff":False,
                          "is_current_blocker_of_shoot":False}
                
                players_a_list.append(player)

        players_a_num = [player["num"] for player in players_a_list]
        sort_by_num_index = np.argsort(players_a_num)
        players_a_list = [players_a_list[i] for i in sort_by_num_index]

        players_b_list = []
        for i in range(max_players):
            if players_b_active[i]:
                name = get_box_attribute("players_name_b_%d"%i, "current_text")
                num = int(get_box_attribute("players_num_b_%d"%i, "current_text"))
                poste = "none"
                if players_b_goal[i]:
                    poste="goalie"
                elif players_b_def[i]:
                    poste = "def"
                elif players_b_for[i]:
                    poste = "for"
                
                stick_side = "right"
                if players_b_stick_left[i]:
                    stick_side = "left"

                licence = int(get_box_attribute("players_licence_b_%d"%i, "current_text"))
                player = {"licence": licence, 
                          "name":name, 
                          "num": num, 
                          "poste":poste, 
                          "stick_side":stick_side, 
                          "is_on_field":False, 
                          "time_on_field":0, 
                          "time_on_field_total":0, 
                          "is_current_shooter":False, 
                          "is_current_passer":False, 
                          "is_involved_in_duel":False, 
                          "is_involved_in_faceoff":False,
                          "is_current_blocker_of_shoot":False}
                players_b_list.append(player)
                
        players_b_num = [player["num"] for player in players_b_list]
        sort_by_num_index = np.argsort(players_b_num)
        players_b_list = [players_b_list[i] for i in sort_by_num_index]

        GAME_DATA["Players_A"] = players_a_list
        GAME_DATA["Players_B"] = players_b_list
        export_game_data(GAME_DATA)

        IS_GAME_READY_TO_START = True

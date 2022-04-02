import sys

#pandas 
import numpy as np 
import pandas as pd




#api 

from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import PlayerOrTeamAbbreviation, LeagueIDNullable, LeagueID, Season, SeasonTypeAllStar
from nba_api.stats.endpoints import cumestatsplayer


#matplotlib 
import matplotlib.pyplot as plt
import seaborn as sns
from importlib.resources import read_binary

from matplotlib import cm
from matplotlib.patches import Circle, Rectangle, Arc, ConnectionPatch

# cursor hover library 

import mplcursors as mpc


p_name = input("Enter Player Name: ")
fig1 = plt.figure(p_name + "'s game stats")

hooper = players.find_players_by_full_name(p_name)


print(hooper)


p_id = input("Enter Player ID: ")

season_id = input("Enter Season: ")
    

    
   

player_info1 = commonplayerinfo.CommonPlayerInfo(player_id=p_id)


game_finder = leaguegamefinder.LeagueGameFinder(player_or_team_abbreviation=PlayerOrTeamAbbreviation.default, league_id_nullable=LeagueIDNullable.default, player_id_nullable=p_id, season_nullable=season_id)


matchup_abrev = game_finder.get_data_frames()[0]['MATCHUP']
game_id = game_finder.get_data_frames()[0]['GAME_ID']

game_mu_id = pd.concat([matchup_abrev, game_id], axis=1)



print(game_mu_id)

g_id = input("Enter Game ID: ")



player_info2 = cumestatsplayer.CumeStatsPlayer(game_ids=g_id, league_id=LeagueID.default, player_id=p_id, season=season_id, season_type_all_star=SeasonTypeAllStar.default)

pts = player_info2.get_data_frames()[0]['PTS']
ast = player_info2.get_data_frames()[0]['AST']
reb = player_info2.get_data_frames()[0]['TOT_REB']
blk = player_info2.get_data_frames()[0]['BLK']
stl = player_info2.get_data_frames()[0]['STL']
to_s = player_info2.get_data_frames()[0]['TURNOVERS']
fg_pct = player_info2.get_data_frames()[0]['FG_PCT']
fg3_pct = player_info2.get_data_frames()[0]['FG3_PCT']

player_game_stats = pd.concat([pts, ast, reb, blk, stl, to_s, fg_pct, fg3_pct], axis = 1)



plt.bar(np.array(["PTS", "AST", "REB", "BLK", "STL", "TO", "FG-PCT", "3PT-PCT"]), np.array(list(map(float, np.array([pts, ast, reb, blk, stl, to_s, fg_pct, fg3_pct])))))


plt.xlabel = ("GAME STATS")
plt.ylabel = ("NUMBERS")
plt.title = (p_name + " GAME STATS")



def player_shotchart():
    
    player_name = input("Enter Player Name: ")
    
    hooper_hooper = players.find_players_by_full_name(player_name)

    print(hooper_hooper)

    hooper_id = input("Enter Player id: ")

    season_id = input("Enter Season: ")

    game_id_finder = leaguegamefinder.LeagueGameFinder(player_or_team_abbreviation=PlayerOrTeamAbbreviation.default, league_id_nullable=LeagueIDNullable.default, player_id_nullable=hooper_id, season_nullable=season_id)

    matchup_abrev = game_id_finder.get_data_frames()[0]['MATCHUP']
    get_game_ids = game_id_finder.get_data_frames()[0]['GAME_ID']

    game_mu_id = pd.concat([matchup_abrev, get_game_ids], axis=1)    

    
    with pd.option_context('display.max_rows', None,
                       'display.max_columns',None, 
                       'display.precision', 3):


        print(game_mu_id)
    
    
    game_ids = input("Enter Game id: ")




    
    
    
    # player avg's career or current year
    hooper_hooper_info = commonplayerinfo.CommonPlayerInfo(player_id=hooper_id)
    print(hooper_hooper_info.get_data_frames()[1])
    

    hoopers_career = playercareerstats.PlayerCareerStats(player_id=hooper_id)
    hoopers_info = hoopers_career.get_data_frames()[0]

    # the team player played during specific year

    team_id = hoopers_info[hoopers_info['SEASON_ID'] == season_id]['TEAM_ID']
    

    hoopestshotlist = shotchartdetail.ShotChartDetail(game_id_nullable=game_ids,team_id=int(team_id),
                                              player_id=hooper_id,
                                              season_type_all_star='Regular Season',
                                              season_nullable=season_id,
                                              context_measure_simple="FGA").get_data_frames()

        


    return hoopestshotlist[0], hoopestshotlist[1]



#leprint(player_game_stats)





# court display 

def show_court(ax = None, color = "black", lw = 1, outer_lines = False):
    if ax is None:
        plt.figure(2)   
        ax = plt.gca()

    # Hoop 
    bball_hoop = Circle((0,0), radius = 7.5, linewidth = lw, color=color, fill = False)

    # Backboard
    bball_backboard = Rectangle((-30, -12.5), 60, 0, linewidth=lw, color=color)

    # Paint
    o_box = Rectangle((-80, -47.5), 160, 190, linewidth = lw, color = color, fill = False)
    i_box = Rectangle((-60, -47.5), 120, 190, linewidth = lw, color=color, fill = False)

    # Free Throw Arch
    topft_arch = Arc((0, 142.5), 120, 120, theta1 = 0, theta2= 180, linewidth = lw, color = color)
    bottomft_arch = Arc((0, 142.5), 120, 120, theta1 = 180, theta2 = 0, linewidth = lw, color = color)

    # Restricted Area
    restricted = Arc((0, 0), 80, 80, theta1 = 0, theta2 = 180, linewidth = lw, color = color)

    # 3PT ARCH "BOOOOOOOOOOOOOOOOOOOM"
    cornerth_1 = Rectangle((-220, -47.5), 0, 140, linewidth = lw, color = color)
    cornerth_2 = Rectangle((220, -47.5), 0, 140, linewidth = lw, color = color)
    threeee = Arc((0,0), 475,475, theta1=22, theta2=158, linewidth = lw, color = color)


    # Half Court
    half_court_o = Arc((0,422.5), 120, 120, theta1 = 180, theta2 = 0, linewidth = lw, color = color)
    hafl_court_i = Arc((0, 422.5), 40, 40, theta1 = 180, theta2= 0, linewidth = lw, color = color)

    # list of all of court shapes
    court_shapes = [bball_hoop, bball_backboard, o_box, i_box, topft_arch, bottomft_arch, restricted, cornerth_1, cornerth_2, threeee, half_court_o, hafl_court_i]

    # If outer_lines = True

    if outer_lines: 
        outer_lines = Rectangle((-250, -47.5), 500, 470, linewidth = lw, color = color, fill = False)
        court_shapes.append(outer_lines)

    for shape in court_shapes:
        ax.add_patch(shape)

    

def shot_chart(data, title="", color = "b", xlim=(-250,250), ylim=(422.5, -47.5), line_color="black", court_color="white", court_lw=2, outer_lines=False, flip_court=False, gridsize=None, ax=None, despine=False):

    if ax is None:
        plt.figure(2)
        ax = plt.gca()

    if not flip_court: 
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    else: 
        ax.set_xlim(xlim[::-1])
        ax.set_ylim(ylim[::-1])

    ax.tick_params(labelbottom = "off", labelleft= "off")
    ax.set_title(title, fontsize = 18)


    # displays court using show function up above
    show_court(ax, color = line_color, lw = court_lw, outer_lines = outer_lines)

    # X - Red = Miss --> O - Green = Make
    x_miss = data[data['EVENT_TYPE'] == 'Missed Shot']['LOC_X']
    y_miss = data[data['EVENT_TYPE'] ==  'Missed Shot']['LOC_Y']

    x_make = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_X']
    y_make = data[data['EVENT_TYPE'] == 'Made Shot']['LOC_Y']


    # plotting misses 
    ax.scatter(x_miss, y_miss, c = 'r', marker="x", s=300, linewidths=3)

    #plotting makes
    ax.scatter(x_make, y_make, facecolors='none', edgecolors='g', marker='o', s=100, linewidths=3)


    # setting the spines == courtlines

    for spine in ax.spines:
        ax.spines[spine].set_lw(court_lw)
        ax.spines[spine].set_color(line_color)

    if despine: 
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)


    return ax










player_shotchart_show, league_avg = player_shotchart()



    
shot_chart(player_shotchart_show)
plt.rcParams['figure.figsize'] = (12,11)




    
mpc.cursor(hover=True)

plt.show()

        







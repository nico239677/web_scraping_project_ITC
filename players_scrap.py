from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)
from parser_file import *
import pandas as pd
from tqdm import tqdm
from functions import *
from variables import *
from api_nba import get_info_draft_api


with open('database_config.py', "rb") as source_file:
    code = compile(source_file.read(), 'database_config.py', "exec")
exec(code)

cur = connection.cursor()

# Scrap all players whose last name starts with a letter between FIRST_LETTER and LAST_LETTER
player_list = []
for char in range_alphabet:
    logger.info(f'Scraping all players whose last name starts with {char} ...')
    link_players_alphabet = main_link + 'players/' + char
    alphabet_letter = read_link(link_players_alphabet)
    draft_table = alphabet_letter.find(class_="overthrow table_container")
    try:
        body = draft_table.find("tbody").find_all("th")
    except AttributeError:
        print('Link not valid')
        continue
    for player in tqdm(body):
        # add_player_and_stats(player, player_list)
        name_player = player.find('a')['href']
        link_player = main_link + name_player
        player_page = read_link(link_player)
        player_name = player_page.find('div', attrs={'itemtype': 'https://schema.org/Person'}).find('h1').text[1:-1]
        # print('player is ', player_name)
        year_draft = int(find_year_draft(player_page))
        # print('player is ', player_name, 'year draft is ', year_draft)
        player_stats = player_page.find('div', attrs={'class': 'stats_pullout'})
        player_stats_p1 = player_stats.find('div', attrs={'class': 'p1'}).find_all('p')
        try:
            total_games = float(player_stats_p1[1].text)
        except:
            total_games = 0
        try:
            total_points = float(player_stats_p1[3].text)
        except:
            total_points = 0
        try:
            total_rebounds = float(player_stats_p1[5].text)
        except:
            total_rebounds = 0
        try:
            total_assists = float(player_stats_p1[7].text)
        except:
            total_assists = 0

        # Inserting into PLAYERS table
        cur.execute("INSERT INTO players ("
                       "name_player, year_draft, number_of_games_career, total_points_career, "
                       "total_rebounds_career, total_assists_career) "
                       "VALUES (%(name)s, %(year_d)s, %(nb_games)s, %(nb_points)s, %(nb_rebounds)s, %(nb_assists)s)",
                    {'name': player_name,
                        'nb_games': total_games,
                        'year_d': year_draft,
                        'nb_points': total_points,
                        'nb_rebounds': total_rebounds,
                        'nb_assists': total_assists})
        connection.commit()

        cur.execute('select last_insert_id()')
        id_player = cur.fetchone()['last_insert_id()']

        arr_per_game = player_page.find('div', attrs={'class': "overthrow table_container", 'id': 'div_per_game'})
        body_per_game = arr_per_game.find('tbody').find_all('tr')
        for row in body_per_game:
            try:
                year = int(row.find('a').text[:-3])
                # print('year is ', year)
                team = row.find('td', attrs={'data-stat': 'team_id'})
                try:
                    name_team = team.find('a').text
                except:
                    name_team = team.text
                cur.execute('SELECT team_name FROM teams WHERE team_name = %(teams)s', {'teams': name_team})
                team_exists = cur.fetchone()
                if team_exists is None:
                    # Inserting into TEAMS table only if team is not already in TEAMS table
                    cur.execute("INSERT INTO teams (team_name) VALUES (%(teams)s)", {'teams': name_team})
                    connection.commit()

                cur.execute('SELECT id_team FROM teams WHERE team_name = %(teams)s', {'teams': name_team})
                id_team = cur.fetchone()['id_team']
                # print(id_team, id_player, year)
                # print(type(id_team), type(id_player), type(year))

                # Inserting into TEAMS_TO_PLAYERS table
                cur.execute("INSERT INTO teams_to_players (id_team, id_player, year) "
                            "VALUES (%(id_team_fk)s, %(id_player_fk)s, %(year_play)s)",
                            {'id_team_fk': id_team,
                             'id_player_fk': id_player,
                             'year_play': year})

                connection.commit()

            except Exception as err:
                warning_logger.info(err)
                pass
        # print(player_name, year_draft)
        try:
            # Inserting into DRAFTS table the values we got from the API
            info_draft = get_info_draft_api(player_name, year_draft)
            cur.execute("INSERT INTO drafts_api ("
                        "id_player,"
                        "PLAYER_NAME,"
                        "POSITION,"
                        "HEIGHT_WO_SHOES,"
                        "WEIGHT,"
                        "WINGSPAN) "
                        "VALUES (%(id)s, %(name)s, %(pos)s, %(height)s, %(weight)s, %(wing)s)",
                        {'id': str(id_player),
                         'name': str(info_draft[0]),
                         'pos': str(info_draft[1]),
                         'height': str(info_draft[2]),
                         'weight': str(info_draft[3]),
                         'wing': str(info_draft[4])})
            connection.commit()
        except Exception as err:
            warning_logger.info(err)
            pass



# ----------------------------------------------------------------------------




 # cur.execute("INSERT IGNORE INTO players ( " + cols + ") VALUES (" + "%s," * (len(row) - 1) + "%s)", tuple(row))

# NUMBER_SCRAPED_COLUMNS = 7

# Turning the list into list of lists
# updated_player_list = [player_list[x:x + NUMBER_SCRAPED_COLUMNS]
#                        for x in range(0, len(player_list), NUMBER_SCRAPED_COLUMNS)]
#
# # Storing the data in dataframe and exporting it to database
# player_df = pd.DataFrame(updated_player_list, columns=['name_player',
#                                                        'number_of_games_career',
#                                                        'total_points_career',
#                                                        'total_rebounds_career',
#                                                        'total_assists_career'
#                                                        ])

#  Filling tables line by line
# cur = connection.cur()
#
# cols = ", ".join([str(i) for i in player_df.columns.tolist()])
# print('cols are ', cols)
# for i, row in player_df.iterrows():
#     cur.execute("INSERT IGNORE INTO players ( " + cols + ") VALUES (" + "%s," * (len(row) - 1) + "%s)", tuple(row))


# Deleting duplicates
# cur.execute("DROP TABLE IF EXISTS players_no_duplicates")
# cur.execute("CREATE TABLE players_no_duplicates SELECT DISTINCT name_player,"
#                "number_of_games_career,"
#                "total_points_career,"
#                "total_rebounds_career,"
#                "total_assists_career "
#                "FROM players")
# cur.execute("DROP TABLE players")
# cur.execute("ALTER TABLE players_no_duplicates RENAME TO players")
#
# connection.commit()

# engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
#                        .format(user="root",
#                                pw="pwdmysql",
#                                db="basketball"))
# player_df.to_sql('players', con=engine, if_exists='append', chunksize=1000, index=False)


import pymysql.cursors
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='pwdmysql',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cur:
    # Create database
    print("\nCreating database basketball if it does not already exists\n")
    cur.execute('CREATE DATABASE IF NOT EXISTS basketball')

    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='pwdmysql',
                                 db='basketball',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    cur.execute('use basketball')

    # cur.execute("DROP TABLE IF EXISTS players")
    # cur.execute("DROP TABLE IF EXISTS drafts")
    # cur.execute("DROP TABLE IF EXISTS teams")

    # Create table players
    print("\nCreating table players if it does not already exists...\n")
    cur.execute("CREATE TABLE IF NOT EXISTS players ("
                "id INT NOT NULL AUTO_INCREMENT,"
                "name_player VARCHAR(30),"
                "number_of_games_career INT,"
                "total_points_career INT,"
                "total_rebounds_career VARCHAR(5),"
                "total_assists_career INT,"
                "PRIMARY KEY (id)"
                ")")

    # Create table teams
    print("\nCreating table teams if it does not already exists...\n")
    cur.execute("CREATE TABLE IF NOT EXISTS teams ("
                "idteam INT NOT NULL AUTO_INCREMENT,"
                "year INT,"
                "team_name VARCHAR(30),"
                "team_player VARCHAR(30),"
                "PRIMARY KEY (idteam)"
                ")")

    # Create table drafts
    print("\nCreating table drafts if it does not already exists...\n")
    cur.execute("CREATE TABLE IF NOT EXISTS drafts ("
                "id INT NOT NULL AUTO_INCREMENT,"
                "year INT,"
                "number_draft INT,"
                "name VARCHAR(30),"
                "number_of_games INT,"
                "total_minutes_played INT,"
                "total_points INT,"
                "total_rebounds INT,"
                "total_assists INT,"
                "minutes_per_game INT,"
                "points_per_game INT,"
                "rebounds_per_game INT,"
                "assists_per_game INT,"
                "PRIMARY KEY (id)"
                # "FOREIGN KEY (name) REFERENCES players (name_player)"
                ")")
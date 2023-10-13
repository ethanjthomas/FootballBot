from mysql.connector import MySQLConnection, Error, errorcode
import secret
import sys

# Credentials to connect to database
HOST = secret.host
PASSWORD = secret.password
USER = secret.user

TABLES = ['Leagues', 'LeagueTeams', 'LeagueTables', 'LeagueMathces']

# Tells whether tables have already been initialized so as to not drop already created tables
INITIALIZED = True

def connect_to_db():
    """Establish a connetion to database"""
    try:
        print('Connecting to MySQL Database...')
        conn = MySQLConnection(host=HOST, password=PASSWORD, user=USER)
 
        if conn.is_connected():
            print('Connection Established.')
            return conn
        else:
            print('Connection Failed.')
    except Error as err:
        print('Connection Failed.')
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("Unexpected error")
            print(err)
            sys.exit(1)


def initialize_db_tables(curs):
    initialize_query = '''
        -- Exported from QuickDBD: https://www.quickdatabasediagrams.com/
        -- Link to schema: https://app.quickdatabasediagrams.com/#/d/196LiO
        -- NOTE! If you have used non-SQL datatypes in your design, you will have to change these here.

        DROP TABLE IF EXISTS `Leagues`;
        DROP TABLE IF EXISTS `LeagueTeams`;
        DROP TABLE IF EXISTS `LeagueTables`;
        DROP TABLE IF EXISTS `LeagueMatches`;

        CREATE TABLE `Leagues` (
            `LeagueID` int  NOT NULL ,
            `LeagueName` varchar(20)  NOT NULL ,
            PRIMARY KEY (
                `LeagueID`
            )
        );

        CREATE TABLE `LeagueTeams` (
            `TeamID` int  NOT NULL ,
            `LeagueID` int  NOT NULL ,
            `TeamName` varchar(45)  NOT NULL ,
            PRIMARY KEY (
                `TeamID`
            )
        );

        CREATE TABLE `LeagueTables` (
            `LeagueID` int  NOT NULL ,
            `TeamID` int  NOT NULL ,
            `TeamName` varchar(45)  NOT NULL ,
            `GamesPlayed` int  NOT NULL ,
            `GamesWon` int  NOT NULL ,
            `GamesDrawn` int  NOT NULL ,
            `GamesLost` int  NOT NULL ,
            `GoalsFor` int  NOT NULL ,
            `GoalsAgainst` int  NOT NULL ,
            `GoalDiff` int  NOT NULL ,
            `Points` int  NOT NULL ,
            PRIMARY KEY (
                `LeagueID`,`TeamID`
            )
        );

        CREATE TABLE `LeagueMatches` (
            `Team1ID` int  NOT NULL ,
            `Team2ID` int  NOT NULL ,
            `LeagueID` int  NOT NULL ,
            `StartTime` datetime  NOT NULL ,
            PRIMARY KEY (
                `Team1ID`,`Team2ID`
            )
        );

        ALTER TABLE `LeagueTeams` ADD CONSTRAINT `fk_LeagueTeams_LeagueID` FOREIGN KEY(`LeagueID`)
        REFERENCES `Leagues` (`LeagueID`);

        ALTER TABLE `LeagueTables` ADD CONSTRAINT `fk_LeagueTables_LeagueID` FOREIGN KEY(`LeagueID`)
        REFERENCES `Leagues` (`LeagueID`);

        ALTER TABLE `LeagueTables` ADD CONSTRAINT `fk_LeagueTables_TeamID_TeamName` FOREIGN KEY(`TeamID`, `TeamName`)
        REFERENCES `LeagueTeams` (`TeamID`, `TeamName`);

        ALTER TABLE `LeagueMatches` ADD CONSTRAINT `fk_LeagueMatches_Team1ID` FOREIGN KEY(`Team1ID`)
        REFERENCES `LeagueTeams` (`TeamID`);

        ALTER TABLE `LeagueMatches` ADD CONSTRAINT `fk_LeagueMatches_Team2ID` FOREIGN KEY(`Team2ID`)
        REFERENCES `LeagueTeams` (`TeamID`);

        ALTER TABLE `LeagueMatches` ADD CONSTRAINT `fk_LeagueMatches_LeagueID` FOREIGN KEY(`LeagueID`)
        REFERENCES `Leagues` (`LeagueID`);
    '''

    try:
        print('Initializing Database Tables...')
        curs.execute(initialize_query, multi=True)
    except Error as err:
        print('Failed to Initialize Database.')
        print(err)
        sys.exit(1)

def pres(curs):
    """Print the result of the previous query"""
    res = curs.fetchall()
    for row in res:
        print(row)

if __name__ == "__main__":
    conn = connect_to_db()
    mycursor = conn.cursor(buffered=True)
    use_query = "USE football;"
    mycursor.execute(use_query)

    if not INITIALIZED:
        initialize_db_tables(mycursor)

    mycursor.execute("SHOW TABLES;")
    pres(mycursor)

    conn.close()
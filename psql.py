import psycopg2


class PSQL:
    def __init__(self, database: str, username: str, password: str, hostname: str, port: int):
        self.connection = psycopg2.connect(database=database, user=username, password=password,
                                      host=hostname, port=port)
        self.cursor = self.connection.cursor()


    def get_summoner_matches(self, summoner_name):
        self.cursor.execute("SELECT * FROM match_history")
        records = cursor.fetchall()
        print(records)
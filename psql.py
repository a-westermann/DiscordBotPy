import psycopg2

database="league"
username="andweste"
password="apostria1"
hostname="localhost"
port=5432
from psycopg2.extras import RealDictCursor


class PSQL:
    def open_connection(self):
        self.connection = psycopg2.connect(database=database, user=username, password=password,
                                      host=hostname, port=port, cursor_factory=RealDictCursor)
        self.cursor = self.connection.cursor()


    def insert_match(self, match_id, summoner_name, kills, deaths, assists, doubles,
                     triples, quadras, pentas, date_created):
        self.open_connection()
        sql_text = "INSERT INTO match_history VALUES('{0}', '{1}', {2}, {3}, {4}, {5}, {6}, {7}, {8}, '{9}')"
        sql_text = sql_text.format(match_id, summoner_name, str(kills), str(deaths), str(assists), str(doubles),
                                   str(triples), str(quadras), str(pentas), str(date_created))
        self.cursor.execute(sql_text)
        self.connection.commit()
        self.connection.close()



    def get_summoner_matches(self, summoner_name):
        self.open_connection()
        self.cursor.execute("SELECT * FROM match_history WHERE summoner_name = '{0}' \
                             ORDER BY date_created LIMIT 100;".format(summoner_name))
        records = self.cursor.fetchall()
        self.connection.close()
        return records


    # ensure only grab matches 3+ were in
    def get_recent_100_matches(self, summoner_name):
        self.open_connection()
        self.cursor.execute("SELECT * FROM match_history WHERE "
                            "COUNT(select  \
                             ORDER BY date_created LIMIT 100;")
        records = self.cursor.fetchall()
        self.connection.close()
        return records


    def get_specific_match(self, match_id, summoner_name):
        self.open_connection()
        self.cursor.execute("SELECT * FROM match_history WHERE match_id = '{0}' \
                            AND summoner_name = '{1}';".format(match_id, summoner_name))
        records = self.cursor.fetchall()
        self.connection.close()
        return records
import psycopg2

database="league"
username="andweste"
password="apostria1"
hostname="localhost"
port=5432


class PSQL:
    def open_connection(self):
        self.connection = psycopg2.connect(database=database, user=username, password=password,
                                      host=hostname, port=port)
        self.cursor = self.connection.cursor()


    def insert_match(self, match_id, summoner_name, kills, deaths, assists, doubles,
                     triples, quadras, pentas, date_created):
        self.open_connection()
        sql_text = "INSERT INTO match_history VALUES({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9})"
        sql_text = sql_text.format(match_id, summoner_name, str(kills), str(deaths), str(assists), str(doubles),
                                   str(triples), str(quadras), str(pentas), str(date_created))
        self.cursor.execute(sql_text)
        self.connection.commit()
        self.connection.close()



    def get_summoner_matches(self, summoner_name):
        self.open_connection()
        self.cursor.execute("SELECT * FROM match_history WHERE summoner_name = " + summoner_name)
        records = self.cursor.fetchall()
        print(records)
        self.connection.close()
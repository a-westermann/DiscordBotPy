import psycopg2
import urllib3 as u3
import base64
from requests.auth import HTTPBasicAuth as auths
import requests
import cassiopeia

database="league"
username="andweste"
password="apostria1"
hostname="localhost"
port=5432

# http = u3.PoolManager()
db_url = open("/home/andweste/Tokens/secret_creds_repo/supabase_host.txt").read()

remote_database="league"
remote_user="Vierce1"
remote_key=open("/home/andweste/Tokens/secret_creds_repo/supabase_api_key.txt").read()
# remote_key=open("/home/andweste/Tokens/secret_creds_repo/supabase_access_token.txt").read()
remote_host=open("/home/andweste/Tokens/secret_creds_repo/supabase_host.txt").read()
remote_port=3333


from psycopg2.extras import RealDictCursor


class PSQL:
    def open_connection(self):
        self.connection = psycopg2.connect(database=database, user=username, password=password,
                                      host=hostname, port=port, cursor_factory=RealDictCursor)
        self.cursor = self.connection.cursor()

    def open_remote_connection(self, table_name: str)-> (str, dict[str, str]):
        headers = {'apikey': f"{remote_key}", 'Authorization' : f"Bearer {remote_key}"}
        url, headers = f"{db_url}/rest/v1/{table_name}", headers
        return url, headers



    def update_remote(self):
        url, headers = self.open_remote_connection(table_name='match_history')
        params = {'query' : "Insert into match_history (match_id, summoner_name) VALUES ('test', 'testy');"}
        json_response = requests.post(url=url, headers=headers,params=params)
        print(json_response)



    def test_remote(self):
        url, headers = self.open_remote_connection(table_name='match_history')
        query = "SELECT * FROM match_history;"
        json_response = requests.get(url=url, headers=headers, params={'match_id' : 'test'})
        print(json_response)
        json_response = json_response.json()
        print(json_response)
        return json_response







    def query(self, query: str):
        self.open_connection()
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        self.connection.close()
        return results

    def command(self, statement: str):
        self.open_connection()
        self.cursor.execute(statement)
        success = False
        if self.cursor.rowcount > 0:
            success = True
        self.connection.commit()
        self.connection.close()
        return success


    def insert_match(self, match_id, summoner_name, kills, deaths, assists, doubles,
                     triples, quadras, pentas, date_created, item_0, item_1, item_2, item_3, item_4, item_5,
                     champion_id):
        self.open_connection()
        sql_text = f"INSERT INTO match_history VALUES('{match_id}', '{summoner_name}', {kills}, {deaths}, {assists}, " \
                   f"{doubles}, {triples}, {quadras}, {pentas}, '{date_created}', {item_0}, {item_1}, {item_2}, " \
                   f"{item_3}, {item_4}, {item_5}, {champion_id})"
        self.cursor.execute(sql_text)
        self.connection.commit()
        self.connection.close()



    def get_summoner_matches(self, summoner_name):
        self.open_connection()
        self.cursor.execute("SELECT * FROM match_history WHERE summoner_name = '{0}' \
                             ORDER BY date_created DESC LIMIT 110;".format(summoner_name))
        records = self.cursor.fetchall()[::-1] # reverse the results
        self.connection.close()
        return records


#TODO: ensure only grab matches 3+ were in
    def get_recent_100_matches(self):
        self.open_connection()
        # first get the top 100 where 3+ members were in game
        self.cursor.execute("select match_id FROM match_history "
                            "GROUP BY match_id, date_created "
                            " HAVING COUNT(match_id)>2 ORDER BY date_created DESC LIMIT 110")
        records = self.cursor.fetchall()[::-1] # reverse the results
        print("found " + str(len(records)) + "  records w/ 3+ summoners.")
        list_records = ""
        for row in records:
            list_records += "'" + str(row["match_id"]) + "',"
        list_records = list_records[0:len(list_records) - 1] # remove last comma
        self.connection.close()
        # now pull all rows for each member that match those match_id's
        self.open_connection()
        # gives the matches in chronological order
        self.cursor.execute("SELECT * FROM match_history WHERE match_id IN (" + list_records + ") "
                                                                    " ORDER BY date_created;")
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


    def get_champ_history(self, summoner_name: str, champion: cassiopeia.Champion):
        self.open_connection()
        # first get average of all scores
        self.cursor.execute(f"SELECT SUM(kills) kills, SUM(deaths) deaths, SUM(assists) assists, SUM(doubles) doubles, "
                            f"SUM(triples) triples, SUM(quadras) quadras, SUM(pentas) pentas, "
                            f"COUNT(match_id) match_count "
                            f"FROM match_history "
                            f"WHERE summoner_name = '{summoner_name}' AND champion_id = {champion.id} "
                            f"GROUP BY champion_id;")
        records = self.cursor.fetchall()
        self.connection.close()
        return records


    def get_best_match(self, summoner_name: str, champion: cassiopeia.Champion):
        self.open_connection()
        self.cursor.execute(f"SELECT kills, deaths, assists, doubles, triples, quadras, pentas, date_created, "
                            f"item_0, item_1, item_2, item_3, item_4, item_5 "
                            f"FROM match_history "
                            f"WHERE summoner_name = '{summoner_name}' AND champion_id = {champion.id} "
                            f"ORDER BY (kills + assists) / "
                            f" (CASE WHEN deaths = 0 THEN 1 ELSE deaths END) DESC LIMIT 1;")
        records = self.cursor.fetchall()
        self.connection.close()
        return records

    def percent_played_champ(self, summoner_name: str, champion: cassiopeia.Champion):
        self.open_connection()
        self.cursor.execute(f"SELECT ROUND((ROUND((SELECT COUNT(match_id) count from match_history "
                            f"WHERE summoner_name = '{summoner_name}' AND champion_id = {champion.id}), 4)) / "
                            f"ROUND((SELECT COUNT(match_id) count from match_history "
                            f"WHERE summoner_name = '{summoner_name}'), 4), 41"
                            f") AS play_percent")
        records = self.cursor.fetchall()
        self.connection.close()
        return records[0]  # only return 1 row

from random import randint
from gtl.models import PlayedGame, Person, Location
import json
import datetime

from gtl import create_app, db

app = create_app()
app.app_context().push()

# List of users/admins/whatever (person-table)
persons = [
  { "email": "thisismy@email.com", "password": "exampleofastrongpasswordthisisnt"},
  { "email": "thisisnotmy@email.com", "password": "exampleofanevenstrongerpasswordthisisnt"},
  { "email": "thisusedtobemy@email.com", "password": "exampleofthestrongestpasswordintheworldthisisnt"},
]
# List names
names = ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III", "JJJ"]
# List of played games
games = []
# Generate list of games from names
for name in names:
  games.append(
    {
      "player_name": name,
      "score": randint(0, 10000),
      "timestamp": datetime.datetime.utcnow(),
      "game_type": randint(0, 3)
    }
  )

# Add persons to db session
for person in persons:
  pers = Person(
      email = person["email"],
      password = person["password"],
    )

  db.session.add(pers)

# Add locations to db session
with open('images/locationdata.json') as json_file:
    data = json.load(json_file)

    for location in data["locations"]:
      loc = Location(
        image_path = location["image_path"],
        country_name = location["country_name"],
        town_name = location["town_name"],
        person_id = location["person_id"]
      )
      
      db.session.add(loc)

# Add played games to db session
for game in games:
  pg = PlayedGame(
      player_name = game["player_name"],
      score = game["score"],
      timestamp = game["timestamp"],
      game_type = game["game_type"],
    )

  db.session.add(pg)


# Commit persons, locations and games
db.session.commit()

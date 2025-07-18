import os
from time import time

from dotenv import load_dotenv
import sqlalchemy as sa
import sqlalchemy.orm as orm

from app.tables import Movie, Episode, Serie, Genre

load_dotenv()
db_url = os.getenv("DB_URL")
ENGINE = sa.create_engine(db_url)


def Star_Wars():
    # Genres
    sci_fi = Genre(name="Science Fiction")
    fantasy = Genre(name="Fantasy")
    animation = Genre(name="Animation")
    western = Genre(name="Western")
    spies = Genre(name="Spies")
    politics = Genre(name="Politics")
    psy_horror = Genre(name="Psychological Horror")
    
    # Movies
    ep1 = Movie(name="Episode 1: The Phantom Menace", duration=136)
    ep2 = Movie(name="Episode 2: Attack of the Clones", duration=142)
    ep3 = Movie(name="Episode 3: Revenge of the Sith", duration=140) 
        # How is III shorter than II
    solo = Movie(name="Solo: A Star Wars Story", duration=135) 
    rouge_one = Movie(name="Rouge One", duration=133)
    ep4 = Movie(name="Episode 4: A New Hope", duration=125)
    ep5 = Movie(name="Episode 5: The Empire strikes back", duration=127)
    ep6= Movie(name="Episode 6: The Return of the Jedi", duration=127)
    
    # Series
    andor = Serie(name="&|")
    mandalorian = Serie(name="The Mandalorian")
    bad_batch = Serie(name="The Bad Batch")
    
    # Add Episodes to Series
        # Andor
            # Season 1
    andor.episodes.append(Episode(name="Kassa", duration=41, season=1))
    andor.episodes.append(Episode(name="That would be me", duration=38, season=1))
    andor.episodes.append(Episode(name="Reckoning", duration=38, season=1))
    andor.episodes.append(Episode(name="Aldhani", duration=47, season=1))
    andor.episodes.append(Episode(name="The Axe Forgets", duration=46, season=1))
    andor.episodes.append(Episode(name="The Eye", duration=50, season=1))
    andor.episodes.append(Episode(name="Announcement", duration=50, season=1))
    andor.episodes.append(Episode(name="Narkina 5", duration=53, season=1, genres=[psy_horror]))
    andor.episodes.append(Episode(name="Nobody's Listening", duration=47, season=1))
    andor.episodes.append(Episode(name="One way out", duration=43, season=1))
    andor.episodes.append(Episode(name="Daughter of Ferrix", duration=43, season=1))
    andor.episodes.append(Episode(name="Rix Road", duration=57, season=1))
            # Season 2
    andor.episodes.append(Episode(name="One Year Later", duration=51, season=2))
    andor.episodes.append(Episode(name="Sagrona Teema", duration=44, season=2))
    andor.episodes.append(Episode(name="Harvest", duration=53, season=2))
    andor.episodes.append(Episode(name="Ever Been to Ghorman?", duration=54, season=2))
    andor.episodes.append(Episode(name="I have friends everywhere", duration=54, season=2))
    andor.episodes.append(Episode(name="What a Festive Evening", duration=55, season=2))
    andor.episodes.append(Episode(name="Messenger", duration=44, season=2))
    andor.episodes.append(Episode(name="Who are you?", duration=44, season=2))
    andor.episodes.append(Episode(name="Welcome to the Rebllion", duration=58, season=2))
    andor.episodes.append(Episode(name="Make it Stop", duration=44, season=2))
    andor.episodes.append(Episode(name="Who else knows?", duration=42, season=2))
    andor.episodes.append(Episode(name="Jedha, Kyber, Erson", duration=46, season=2))
    
        # Mando
            # Season 1
    mandalorian.episodes.append(Episode(name="The Mandalorian", duration=37, season=1))
    mandalorian.episodes.append(Episode(name="The Child", duration=30, season=1))
    mandalorian.episodes.append(Episode(name="The Sin", duration=34, season=1))
    mandalorian.episodes.append(Episode(name="Sanctuary", duration=38, season=1))
    mandalorian.episodes.append(Episode(name="The Gunslinger", duration=32, season=1))
    mandalorian.episodes.append(Episode(name="The Prisoner", duration=41, season=1))
    mandalorian.episodes.append(Episode(name="The Reckoning", duration=37, season=1))
    mandalorian.episodes.append(Episode(name="Redemption", duration=45, season=1))
            # Season 2
    mandalorian.episodes.append(Episode(name="The Marshal", duration=50, season=2))
    mandalorian.episodes.append(Episode(name="The Passenger", duration=38, season=2))
    mandalorian.episodes.append(Episode(name="The Heiress", duration=32, season=2))
    mandalorian.episodes.append(Episode(name="The Siege", duration=36, season=2))
    mandalorian.episodes.append(Episode(name="The Jedi", duration=43, season=2))
    mandalorian.episodes.append(Episode(name="The Tragedy", duration=30, season=2))
    mandalorian.episodes.append(Episode(name="The Beliver", duration=35, season=2))
    mandalorian.episodes.append(Episode(name="The Rescue", duration=44, season=2))
        
        # Bad Batch
            # Season 1
    bad_batch.episodes.append(Episode(name="Aftermath", duration=70, season=1))
    bad_batch.episodes.append(Episode(name="Cut and Run", duration=31, season=1))
    bad_batch.episodes.append(Episode(name="Replacements", duration=28, season=1))
    bad_batch.episodes.append(Episode(name="Cornered", duration=26, season=1))
    bad_batch.episodes.append(Episode(name="Rampage", duration=23, season=1))
    bad_batch.episodes.append(Episode(name="Decommissioned", duration=21, season=1))
    bad_batch.episodes.append(Episode(name="Battle Scars", duration=27, season=1))
    bad_batch.episodes.append(Episode(name="Reunion", duration=24, season=1))
    bad_batch.episodes.append(Episode(name="Bounty Lost", duration=25, season=1))
    bad_batch.episodes.append(Episode(name="Common Ground", duration=25, season=1))
    bad_batch.episodes.append(Episode(name="Devil's Deal", duration=26, season=1))
    bad_batch.episodes.append(Episode(name="Rescue on Ryloth", duration=26, season=1))
    bad_batch.episodes.append(Episode(name="Infested", duration=25, season=1))
    bad_batch.episodes.append(Episode(name="War-Mantle", duration=28, season=1))
    bad_batch.episodes.append(Episode(name="Return to Kamino", duration=26, season=1))
    bad_batch.episodes.append(Episode(name="Lost Road", duration=26, season=1))
            # Season 2
    bad_batch.episodes.append(Episode(name="Spoils of War", duration=23, season=2))
    bad_batch.episodes.append(Episode(name="Ruins of War", duration=27, season=2))
    bad_batch.episodes.append(Episode(name="The Solitary Clone", duration=29, season=2))
    bad_batch.episodes.append(Episode(name="Faster", duration=23, season=2))
    bad_batch.episodes.append(Episode(name="Enotomble", duration=27, season=2))
    bad_batch.episodes.append(Episode(name="Tribe", duration=26, season=2))
    bad_batch.episodes.append(Episode(name="The Clone Conspiracy", duration=28, season=2))
    bad_batch.episodes.append(Episode(name="Truth and Consequences", duration=30, season=2))
    bad_batch.episodes.append(Episode(name="The Crossing", duration=27, season=2))
    bad_batch.episodes.append(Episode(name="Retrieval", duration=27, season=2))
    bad_batch.episodes.append(Episode(name="Metamorphosis", duration=27, season=2))
    bad_batch.episodes.append(Episode(name="The Outpost", duration=29, season=2))
    bad_batch.episodes.append(Episode(name="Pabu", duration=25, season=2))
    bad_batch.episodes.append(Episode(name="Tipping Point", duration=26, season=2))
    bad_batch.episodes.append(Episode(name="The Summit", duration=24, season=2))
    bad_batch.episodes.append(Episode(name="Plan 99", duration=25, season=2))
            # Season 3
    bad_batch.episodes.append(Episode(name="Confined", duration=31, season=3))
    bad_batch.episodes.append(Episode(name="Paths Unknown", duration=25, season=3))
    bad_batch.episodes.append(Episode(name="Shadows of Tantiss", duration=25, season=3))
    bad_batch.episodes.append(Episode(name="A different approach", duration=25, season=3))
    bad_batch.episodes.append(Episode(name="The Return", duration=26, season=3))
    bad_batch.episodes.append(Episode(name="Infiltration", duration=26, season=3))
    bad_batch.episodes.append(Episode(name="Extraction", duration=23, season=3))
    bad_batch.episodes.append(Episode(name="Bad Territory", duration=26, season=3))
    bad_batch.episodes.append(Episode(name="The Canonbreaker", duration=25, season=3))
    bad_batch.episodes.append(Episode(name="Identity Crisis", duration=23, season=3))
    bad_batch.episodes.append(Episode(name="Point of No Return", duration=22, season=3))
    bad_batch.episodes.append(Episode(name="Juggernaut", duration=21, season=3))
    bad_batch.episodes.append(Episode(name="Into the Breach", duration=24, season=3))
    bad_batch.episodes.append(Episode(name="Flash Strike", duration=22, season=3))
    bad_batch.episodes.append(Episode(name="The Cavalry Has Arrived", duration=50, season=3))
    
    
    # Add genres
    ep1.genres.extend([sci_fi, fantasy]) 
    ep2.genres.extend([sci_fi, fantasy]) 
    ep3.genres.extend([sci_fi, fantasy])
    solo.genres.extend([sci_fi, fantasy])
    rouge_one.genres.extend([sci_fi, fantasy])
    ep4.genres.extend([sci_fi, fantasy])
    ep5.genres.extend([sci_fi, fantasy])
    ep6.genres.extend([sci_fi, fantasy])
    
    andor.genres.extend([sci_fi, spies, politics])
    for ep in andor.episodes:
        ep.genres.extend([sci_fi, politics, spies])
        
    mandalorian.genres.extend([sci_fi, fantasy, western])
    for ep in mandalorian.episodes:
        ep.genres.extend([sci_fi, fantasy, western])
        
    bad_batch.genres.extend([sci_fi, fantasy, animation])
    for ep in bad_batch.episodes:
        ep.genres.extend([sci_fi, fantasy, animation])
        
    # Add it to the DB
    with orm.Session(ENGINE) as session:
        session.add(ep1)
        session.add(ep2)
        session.add(ep3)
        session.add(solo)
        session.add(rouge_one)
        session.add(ep4)
        session.add(ep5)
        session.add(ep6)
        
        session.add(andor)
        session.add(mandalorian)
        session.add(bad_batch)
        
        session.commit()
    

if __name__ == "__main__":
    t1 = time()
    Star_Wars()
    t2 = time()
    
    print(f"{t2 - t1} seconds")
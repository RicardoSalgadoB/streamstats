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
    ep1 = Movie(name="Episode 1: The Phantom Menace", length=136)
    ep2 = Movie(name="Episode 2: Attack of the Clones", length=142)
    ep3 = Movie(name="Episode 3: Revenge of the Sith", length=140) 
        # How is III shorter than II
    solo = Movie(name="Solo: A Star Wars Story", length=135) 
    rouge_one = Movie(name="Rouge One", length=133)
    ep4 = Movie(name="Episode 4: A New Hope", length=125)
    ep5 = Movie(name="Episode 5: The Empire strikes back", length=127)
    ep6= Movie(name="Episode 6: The Return of the Jedi", length=127)
    
    # Series
    andor = Serie(name="&|")
    mandalorian = Serie(name="The Mandalorian")
    bad_batch = Serie(name="The Bad Batch")
    
    # Add Episodes to Series
        # Andor
            # Season 1
    andor.episodes.append(Episode(name="Kassa", length=41, season=1))
    andor.episodes.append(Episode(name="That would be me", length=38, season=1))
    andor.episodes.append(Episode(name="Reckoning", length=38, season=1))
    andor.episodes.append(Episode(name="Aldhani", length=47, season=1))
    andor.episodes.append(Episode(name="The Axe Forgets", length=46, season=1))
    andor.episodes.append(Episode(name="The Eye", length=50, season=1))
    andor.episodes.append(Episode(name="Announcement", length=50, season=1))
    andor.episodes.append(Episode(name="Narkina 5", length=53, season=1, genres=[psy_horror]))
    andor.episodes.append(Episode(name="Nobody's Listening", length=47, season=1))
    andor.episodes.append(Episode(name="One way out", length=43, season=1))
    andor.episodes.append(Episode(name="Daughter of Ferrix", length=43, season=1))
    andor.episodes.append(Episode(name="Rix Road", length=57, season=1))
            # Season 2
    andor.episodes.append(Episode(name="One Year Later", length=51, season=2))
    andor.episodes.append(Episode(name="Sagrona Teema", length=44, season=2))
    andor.episodes.append(Episode(name="Harvest", length=53, season=2))
    andor.episodes.append(Episode(name="Ever Been to Ghorman?", length=54, season=2))
    andor.episodes.append(Episode(name="I have friends everywhere", length=54, season=2))
    andor.episodes.append(Episode(name="What a Festive Evening", length=55, season=2))
    andor.episodes.append(Episode(name="Messenger", length=44, season=2))
    andor.episodes.append(Episode(name="Who are you?", length=44, season=2))
    andor.episodes.append(Episode(name="Welcome to the Rebllion", length=58, season=2))
    andor.episodes.append(Episode(name="Make it Stop", length=44, season=2))
    andor.episodes.append(Episode(name="Who else knows?", length=42, season=2))
    andor.episodes.append(Episode(name="Jedha, Kyber, Erson", length=46, season=2))
    
        # Mando
            # Season 1
    mandalorian.episodes.append(Episode(name="The Mandalorian", length=37, season=1))
    mandalorian.episodes.append(Episode(name="The Child", length=30, season=1))
    mandalorian.episodes.append(Episode(name="The Sin", length=34, season=1))
    mandalorian.episodes.append(Episode(name="Sanctuary", length=38, season=1))
    mandalorian.episodes.append(Episode(name="The Gunslinger", length=32, season=1))
    mandalorian.episodes.append(Episode(name="The Prisoner", length=41, season=1))
    mandalorian.episodes.append(Episode(name="The Reckoning", length=37, season=1))
    mandalorian.episodes.append(Episode(name="Redemption", length=45, season=1))
            # Season 2
    mandalorian.episodes.append(Episode(name="The Marshal", length=50, season=2))
    mandalorian.episodes.append(Episode(name="The Passenger", length=38, season=2))
    mandalorian.episodes.append(Episode(name="The Heiress", length=32, season=2))
    mandalorian.episodes.append(Episode(name="The Siege", length=36, season=2))
    mandalorian.episodes.append(Episode(name="The Jedi", length=43, season=2))
    mandalorian.episodes.append(Episode(name="The Tragedy", length=30, season=2))
    mandalorian.episodes.append(Episode(name="The Beliver", length=35, season=2))
    mandalorian.episodes.append(Episode(name="The Rescue", length=44, season=2))
        
        # Bad Batch
            # Season 1
    bad_batch.episodes.append(Episode(name="Aftermath", length=70, season=1))
    bad_batch.episodes.append(Episode(name="Cut and Run", length=31, season=1))
    bad_batch.episodes.append(Episode(name="Replacements", length=28, season=1))
    bad_batch.episodes.append(Episode(name="Cornered", length=26, season=1))
    bad_batch.episodes.append(Episode(name="Rampage", length=23, season=1))
    bad_batch.episodes.append(Episode(name="Decommissioned", length=21, season=1))
    bad_batch.episodes.append(Episode(name="Battle Scars", length=27, season=1))
    bad_batch.episodes.append(Episode(name="Reunion", length=24, season=1))
    bad_batch.episodes.append(Episode(name="Bounty Lost", length=25, season=1))
    bad_batch.episodes.append(Episode(name="Common Ground", length=25, season=1))
    bad_batch.episodes.append(Episode(name="Devil's Deal", length=26, season=1))
    bad_batch.episodes.append(Episode(name="Rescue on Ryloth", length=26, season=1))
    bad_batch.episodes.append(Episode(name="Infested", length=25, season=1))
    bad_batch.episodes.append(Episode(name="War-Mantle", length=28, season=1))
    bad_batch.episodes.append(Episode(name="Return to Kamino", length=26, season=1))
    bad_batch.episodes.append(Episode(name="Lost Road", length=26, season=1))
            # Season 2
    bad_batch.episodes.append(Episode(name="Spoils of War", length=23, season=2))
    bad_batch.episodes.append(Episode(name="Ruins of War", length=27, season=2))
    bad_batch.episodes.append(Episode(name="The Solitary Clone", length=29, season=2))
    bad_batch.episodes.append(Episode(name="Faster", length=23, season=2))
    bad_batch.episodes.append(Episode(name="Enotomble", length=27, season=2))
    bad_batch.episodes.append(Episode(name="Tribe", length=26, season=2))
    bad_batch.episodes.append(Episode(name="The Clone Conspiracy", length=28, season=2))
    bad_batch.episodes.append(Episode(name="Truth and Consequences", length=30, season=2))
    bad_batch.episodes.append(Episode(name="The Crossing", length=27, season=2))
    bad_batch.episodes.append(Episode(name="Retrieval", length=27, season=2))
    bad_batch.episodes.append(Episode(name="Metamorphosis", length=27, season=2))
    bad_batch.episodes.append(Episode(name="The Outpost", length=29, season=2))
    bad_batch.episodes.append(Episode(name="Pabu", length=25, season=2))
    bad_batch.episodes.append(Episode(name="Tipping Point", length=26, season=2))
    bad_batch.episodes.append(Episode(name="The Summit", length=24, season=2))
    bad_batch.episodes.append(Episode(name="Plan 99", length=25, season=2))
            # Season 3
    bad_batch.episodes.append(Episode(name="Confined", length=31, season=3))
    bad_batch.episodes.append(Episode(name="Paths Unknown", length=25, season=3))
    bad_batch.episodes.append(Episode(name="Shadows of Tantiss", length=25, season=3))
    bad_batch.episodes.append(Episode(name="A different approach", length=25, season=3))
    bad_batch.episodes.append(Episode(name="The Return", length=26, season=3))
    bad_batch.episodes.append(Episode(name="Infiltration", length=26, season=3))
    bad_batch.episodes.append(Episode(name="Extraction", length=23, season=3))
    bad_batch.episodes.append(Episode(name="Bad Territory", length=26, season=3))
    bad_batch.episodes.append(Episode(name="The Canonbreaker", length=25, season=3))
    bad_batch.episodes.append(Episode(name="Identity Crisis", length=23, season=3))
    bad_batch.episodes.append(Episode(name="Point of No Return", length=22, season=3))
    bad_batch.episodes.append(Episode(name="Juggernaut", length=21, season=3))
    bad_batch.episodes.append(Episode(name="Into the Breach", length=24, season=3))
    bad_batch.episodes.append(Episode(name="Flash Strike", length=22, season=3))
    bad_batch.episodes.append(Episode(name="The Cavalry Has Arrived", length=50, season=3))
    
    
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
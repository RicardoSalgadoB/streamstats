# Function to populate the catalog with fake content

import os
import random
from typing import List
import json

from dotenv import load_dotenv
from faker import Faker
import sqlalchemy as sa
import sqlalchemy.orm as orm

from app.models import Movie, Episode, Series, Genre

from examples.fake_generator import generate_fake_title

fake = Faker()

places = [
    "Monterrey",
    "San Pedro",
    "Guadalupe",
    "Apodaca",
    "Guadlajara",
    "Tenochtitlan",
    "Fallout",
    "New Vegas",
    "Old Vegas",
    "Chilangolandia",
    "Gringoland",
    "Ferghana",
    "Indo Kush",
    "Bolsonaria",
    "Colombia",
    "Maracaibo",
    "Easter Island",
    "Luzern",
    "Zurich",
    "the Alps",
    "Powhatan",
    "Anderson Island",
    "Colinas del Sabio",
    "California",
    "Utapau",
    "a gerrymandered state",
    "federal district",
    "Mérida",
    "Milwakke",
    "Daytona",
    "Henderson Field",
    "Munchen",
    "Osterreich",
    "Munich",
    "Boston",
    "Harvard",
    "MIT",
    "CMU",
    "Toronto",
    "Ottawa",
    "Taum Sauk",
    "the Lower Reservoir",
    "Los Angeles",
    "Capri"
]

animals = [
    "Cow",
    "Fish",
    "Antilope",
    "Eagle",
    "Lion",
    "Seabird",
    "Xenomorph",
    "Seacow",
    "Seapig",
    "Monkey",
    "Hawk",
    "Panda",
    "Polar Bear",
    "Ant",
    "Grasshooper",
    "Wolf",
    "Panther",
    "Leopard"
]

criminal_adjectives = [
    "Fast",
    "Furious",
    "Peaky",
    "Bourbon",
    "Pedagogic",
    "Cruel",
    "Inglorious",
    "Blazing"
]

criminals = [
    "Blinders",
    "Killers",
    "Murders",
    "Scorpions",
    "Psychopaths",
    "Bastards",
    "Drug Addicts",
    "Blazers",
    "Arsonists"
]

heist_organizers = [
    "Ocean",
    "Sky",
    "Earth",
    "Hell",
    "Heaven"
]

superhero_names = [
    "Cowman",
    "Enderman",
    "Fishman",
    "Sealman",
    "Tungstenman",
    "Diamondwoman",
    "Captain Oceania",
    "Captain Europe",
    "Captain Antartica",
    "Purple Son",
    "Titan",
    "Metroman",
    "Busman",
    "Borg",
    "Nicoooooooo Huuuuuuuuuulkenberg",
    "Dudududu",
    "Dodo",
    "Raindeerman",
    "Friendly Werewolf",
    "Carolus Rex",
    "Pooman",
    "Doctor Salvation",
    "Santa Monica",
    "Blue Daughter",
    "Red Velvet",
    "Curiouos George",
    "Captain Gold",
    "Trebala",
    "Harpy",
    "Godess of Antioch"
]

body_parts = [
    "back",
    "eye",
    "foot",
    "tooth",
    "nose",
    "ear",
    "knee",
    "belly",
    "arm",
    "head",
    "neck",
    "crotch"
]

weapons = [
    "Blade",
    "Knife",
    "Rifle",
    "Gun",
    "Pistol",
    "Axe",
    "Slate",
    "Arch",
    "Bow",
    "Crossbow"
]

persons_doing = [
    "Runners",
    "Twisters",
    "Kneedlers",
    "Tricksters",
    "Roamers",
    "Sleepers",
    "Creepers",
    "Raiders",
    "Goers",
    "Jailers",
    "Brushers",
    "Hummers",
    "Drimmers"
]

things1 = [
    "Frying pans",
    "Ketchup",
    "Mayonnaise",
    "Swords",
    "Lands",
    "Bracelets",
    "Octopuses",
    "Night",
    "Twilight",
    "Dead",
    "Hells",
    "Heaven",
    "Long Table",
    "Crimson Tide",
    "Yellow Horde"
]

# Load secret variables
load_dotenv()
db_url = os.getenv("DB_URL")

# Create an sql alchemy engine
ENGINE = sa.create_engine(db_url)


# Class for weighted selection
class WeightedChoice:
    def __init__(self, choice: dict[str, float], k:int = 1):
        self.items = list(choice.keys())
        self.weights = list(choice.values())
        self.k = k

    def choose(self):
        if self.k == 1:
            return random.choices(self.items, weights=self.weights, k=self.k)[0]
        else:
            return random.choices(self.items, weights=self.weights, k=self.k)


class ContentGenerator:
    def __init__(self) -> None:
        self.domains = WeightedChoice({
            "Scripted": 0.9,
            "Unscripted": 0.1
        })
        
        self.scripted_genres = WeightedChoice({
            "Anthology": 0.018, # 1000/1000
            "Art film": 0.003,
            "Crime": 0.073,
            "Experimental": 0.001,
            "Exploitation": 0.012,
            "Gothic": 0.001,
            "Fantasy": 0.007,   # 892/100
            "Musical":  0.006,
            "Police": 0.003,
            "Romance": 0.078,
            "Serial": 0.005,    # 798/1000
            "Cereal": 0.001,
            "Social Problem": 0.001,
            "Social": 0.064,
            "Sports": 0.013,
            "Telenovela": 0.048,    # 714/1000
            "Téléroman": 0.028,
            " THriller": 0.002,
            "Action": 0.128,
            "Adventure:": 0.078, 
            "Animation": 0.100, # 430/1000
            "Traditional Animation": 0.030,
            "3D Animation": 0.013,
            "CGI Animation": 0.018,
            "Stop Motion": 0.001,
            "Puppetry": 0.001,
            "Comedy": 0.085,
            "Mockumentary": 0.001,
            "Parody": 0.008,    # 238/1000
            "Satire": 0.003,
            "Devotional": 0.028,
            "Drama": 0.068,
            "Docudrama": 0.003,
            "Legal drama": 0.010,
            "Medical Drama": 0.006, # 118/1000
            "Melodrama": 0.016,
            "Military": 0.014,
            "Philosophical drama": 0.001,
            "Psychological drama": 0.002,
            "Political drama": 0.001,
            "Teen drama": 0.001,    # 78/1000
            "Alternate History": 0.001,
            "Biopic": 0.001,
            "Historical EPIC": 0.001,
            "Historical event": 0.001,
            "Historical fiction": 0.010,
            "Period drama": 0.001,
            "Period piece": 0.001,
            "Horror": 0.006,
            "Kaiju": 0.001,
            "Mecha": 0.001,
            "Giallo": 0.001,   # 43/1000
            "Science Fiction": 0.025,
            "Science Fantasy": 0.023,
            "Fantastique": 0.001,
            "Western": 0.002,
            "": 0.001
        })
        
        self.unscripted_genres = WeightedChoice({
            "Amateur": 0.01,
            "Documentary": 0.20,
            "Educacional": 0.03,
            "Infomertial": 0.02,
            "Talk show": 0.05,
            "Variety": 0.03,
            "Cocert": 0.01,
            "Cooking show": 0.10,
            "Game show": 0.10,
            "Home renovation": 0.06,
            "News": 0.05,
            "Politcal Commentary": 0.01,
            "Religious": 0.01,
            "Stand-up Comedy": 0.02,
            "Sports": 0.30,
        })
        
        self.additional_genres = max(random.randint(0, 10) - random.randint(0, 6), 0)

        self.crime_subgenres = WeightedChoice({
            "Detective": 0.15,
            "Noir": 0.05,
            "Gangster": 0.30,
            "Heist": 0.20,
            "Hood": 0.10,
            "Mystery": 0.15,
            "Vigilante": 0.05,
        })
            
        self.scifi_subgenres = WeightedChoice({
            "Cyberpunk": 0.30,
            "Dystopian": 0.01,
            "Utopian": 0.09,
            "Military": 0.20,
            "Post Apocalyptic": 0.01,
            "Space Opera": 0.05,
            "Tech Noir": 0.02,
            "Utopian": 0.18,
            "Fantastique": 0.01,
            "Gothic Sci-Fi": 0.01,
            "New Wave": 0.05,
            "Alien": 0.01,
            "SciFi Horror": 0.05,
            "Parallel universe": 0.01,
        })
            
        self.anthology = {
            "name": random.choice([
                f"The stories of {random.choice(places)}",
                f"The year of {random.randint(1, 2100)}",
                f"The month of the {random.choice(animals)}"
            ]),
            "secondary genres": WeightedChoice({
                "Crime": 0.20,
                "Mafia": 0.10,
                "Detective": 0.20,
                "Romance": 0.03,
                "Adventure": 0.03,
                "Fiction": 0.01,
                "Political drama": 0.10,
                "Military": 0.20,
                "Science Fiction": 0.05,
                "Western": 0.05,
                "Cyberpunk": 0.03 
            }, k=self.additional_genres)
        }
        
        self.art_film= {
            "name": random.choice([
                "Water",
                "Fire",
                "Earth",
                "Air",
                "Uranium",
                "Baguette",
                "Croissant",
                "Animals",
                "Places",
                random.choice(animals)
            ])
        }
        
        self.detective = {
            "name": random.choice([
                fake.name(),
                fake.place_name(),
                fake.administrative_unit(),
                f"{fake.color()} Falcon",
                f"{fake.color()} Phoenix"
            ]),
            "secondary genres": WeightedChoice({
                "Gong'an": 0.05,
                "Romance": 0.20,
                "Action": 0.35,
                "Fantasy": 0.10,
                "Science Fiction": 0.15,
                str(self.scifi_subgenres.choose()): 0.15
            }, k=self.additional_genres//3)
        }
        
        self.noir = {
            "name": random.choice([
                fake.name(),
                fake.place_name(),
                fake.administrative_unit(),
                f"{fake.color()} Falcon",
                f"{fake.color()} Phoenix",
                "Knives Out",
                "Rush"
            ]),
            "secondary genres": WeightedChoice({
                "Gothic": 0.95,
                "Romance": 0.01,
                "Science Fiction": 0.01,
                "Exploitation film": 0.01,
                "Dark Fantasy": 0.01,
                "Science Fantasy": 0.01
            }, k=self.additional_genres//4)
        }
        
        self.gangster = {
            "name": random.choice([
                f"The Ballad of {fake.full_name()}",
                f"The {fake.last_name}",
                f"{random.choice(criminal_adjectives)} {random.choice(criminals)}"
            ]),
            "secondary genres": WeightedChoice({
                "Irish Mafia": 0.20,
                "Romani Mafia": 0.10,
                "Italian Mafia": 0.40,
                "Jewish Mafia": 0.05,
                "Mumbai": 0.15,
                "Yakuza": 0.10,
                "Comedy": 0.10
            }, k=self.additional_genres//2)
        }
        
        self.heist = {
            "name": random.choice([
                f"{random.choice(heist_organizers)}' {random.randint(2, 100)}",
                f"The {fake.color} {random.choice(animals)}",
                f"A {fake.color} {random.choice(animals)}",
            ]),
            "secondary genres": WeightedChoice({
                "Pirate": 0.10,
                "Swashbuckler": 0.15,
                "Science Fiction": 0.20,
                "Distopian": 0.20,
                "Romance": 0.30,
                "Superhero": 0.05
            }, k=self.additional_genres//3)
        }
        
        self.hood = {
            "name": random.choice([
                "The Animals",
                "Los Animales",
                "Las Ojivas Místicas",
                f"The {random.choice(animals)}s"
            ]),
            "secondary genres": WeightedChoice({
                "Romance": 0.2,
                "Social Problem": 0.8,
            }, k=self.additional_genres//5)
        }
        
        self.mystery = {
            "name": random.choice([
                f"{fake.name()}: The Angels roar",
                f"{fake.name()}: The Demons weep",
                f"The Son of Mrs.{fake.name_female()}",
                f"The Daughter of Mrs.{fake.name_female()}",
            ]),
            "secondary genres": WeightedChoice({
                "Sports": 0.02,
                "SciFi": 0.02,
                "Fantasy": 0.02,
                "Religious": 0.01,
                "Comedy": 0.03,
                "Romance": 0.10,
                "Detective": 0.75,
                "Social Problem": 0.05
            })
        }
        
        self.vigilante = {
            "name": random.choice([
                f"The Hero of {random.choice(places)}",
                f"The Man in the Hood",
                f"The Woman in the Hood",
                f"The {random.choice(superhero_names)}",
                f"Corporate Socalism"
            ]),
            "secondary genres": WeightedChoice({
                "Superhero": 0.60,
                "Absurdist": 0.02,
                "Social Problem": 0.03,
                "Religious": 0.01,
                "Gothic": 0.30,
                "Gangster": 0.04,
                "Cyberpunk": 0.01
            }, k=self.additional_genres)
        }
        
        self.exploitation = {
            "name": random.choice([
                f"The body of {fake.name()}",
                f"The Culture of {random.choice(places)}",
                f"Sweet sweet{random.choice(body_parts)}",
                f"The Van of {fake.name()}",
                "Ahhh... Zombie",
                "Por unos pesos más",
                "For a few weights more",
            ]),
            "secondary genres": WeightedChoice({
                "Social Problem": 0.05,
                "Historical drama": 0.10,
                "Western": 0.10,
                "Zombie": 0.50,
                "Blaxploitation": 0.02,
                "Sexploitation": 0.02,
                "Slasher": 0.06,
                "Vansploitation": 0.05,
                "Adult Comedy": 0.10
            }, k=self.additional_genres//2)
        }
        
        self.gothic = {
            "name": random.choice([
                f"{fake.first_name()}stein",
                f"{random.choice(list('DFSTYBCZL'))}cula",
                f"{random.choice(weapons)} {random.choice(persons_doing)}"
            ]),
            "secondary genres": WeightedChoice({
                "Gothic Horror": 0.50,
                "Gothic Romance": 0.25,
                "Gothic Science Fiction": 0.05,
                "Urban Gothic": 0.07,
                "Suburban Gothic": 0.05,
                "Rural Gothic": 0.05,
                "Religious": 0.03
            }, k=self.additional_genres//2) 
        }
        
        self.fantasy = {
            "name": random.choice([
                str(fake.name()),
                f"The Chroncles of {random.choice(places)}",
                f"The Lord of the {random.choice(things1)}",
                f"The Lord of the Castle in {fake.plant_name()}",
                "Kobols",
                "Dwarven Cities",
                "The Prince",
                "The Princes",
                "The Princess",
                "The Princesses",
                "The Hammerhead"
                f"The whimsical origin of {animals}",
                f"The ancient past of {places}",
                f"The Kingdom of the {fake.last_name()}"
                f"The Nibelungians",
                "The Descendants of Achilles",
                f"{fake.file_name()} the Zombie slayer",
                f"{fake.file_name()} the Vampire slayer",
                f"{fake.file_name()} the Werewolf slayer",
                f"{fake.file_name()} the Demon slayer",
                "Not so natural",
                f"Game of {animals}"
            ]),
            "secondary genres": WeightedChoice({
                "Contemporary fantasy": 0.10,
                "Urban fantasy": 0.05,
                "Dark fantasy": 0.10,
                "High fantasy": 0.15,
                "Fantasy comedy": 0.05,
                "Fairy tale": 0.10,
                "Animation": 0.10,
                "Historical fantasy": 0.05,
                "Romance": 0.20,
                "Adventure": 0.08,
                "Military": 0.02
            }, k=self.additional_genres)
        }


def generate_genres() -> List[Genre]:
    """Generate the genres of the catalog."""
    # Got names from Wikipedia, swapped one (guess which)
    genre_names = [
        "Action",
        "Adventure",
        "Animation",
        "Comedy",
        "Drama",
        "Fantasy",
        "Historical",
        "Horror",
        "Melodrama",
        "Musical",
        "Noir",
        "Romance",
        "Science Fiction",
        "Spies",
        "Thriller",
        "Western"
    ]
    genre_objs = []
    
    # Create each object
    for name in genre_names:
        genre_objs.append(Genre(name=name))
        
    return genre_objs


def generate_movies(num: int = 5000) -> List[Movie]:
    """Generates num fake movies of the catalog."""
    movies = []
    names =[]
    
    for _ in range(num):
        n = generate_fake_title()   # get name
        names.append(n) # add it the names list
            # add the movie object to the list
        movies.append(Movie(
            name=n, 
            duration=random.randint(100, 240)
        ))
            # store the names of the movies in a file for finds during testing. Not needed for Docker.
        #with open('names/movie_names.txt', 'w') as f:
        #    for n in names:
        #        f.write(n + '\n')
    return movies   # return the list of objects


def generate_series(num: int = 2000):
    """Generates num fake series for the catalog."""
    series = []
    series_names: dict[str, List[str]] = {} # dictionary to save series and episodes names
    
    for _ in range(num):
        name = generate_fake_title()
        series.append(Series(name=name))
        series_names[name] = [] # add name to the dict
    return series, series_names # return list and dict
        
        
def generate_episodes(series: List[Series], series_names: dict[str, List[str]], num: int = 20000) -> None:
    """Generate num fake episodes for the catalog."""
    for _ in range(num):
        ep_name = generate_fake_title()
        s = random.choice(series)   # pick a random series
            # append an episode to it
        s.episodes.append(Episode(
            name=ep_name,
            duration=random.randint(5, 100),
            season=random.randint(1, 10)
        ))
        series_names[s.name].append(ep_name)    # Add the episode to the list of its respective entry
    
    # Once the series-episodes dictinary is comlete, store it on a json file for testing purposes. Not needed for Docker.
    #with open("names/series.json", "w") as f:
    #    json.dump(series_names, f)
        
        
def embed_genres(
    genres: List[Genre], 
    movies: List[Movie], 
    series: List[Series]
) -> None:
    """Add genres to the contents of the catalog."""
    for m in movies:
            # Use set to add the same genre twice to the same movie
        gnr_set = {random.choice(genres) for _ in range(random.randint(1, 5))}
        for gnr in list(gnr_set):
            m.genres.append(gnr)
        
    for s in series:
            # Use set to add the same genre twice to the same series and eps
        gnr_set = {random.choice(genres) for _ in range(random.randint(1, 5))}
        for gnr in list(gnr_set):
            s.genres.append(gnr)
            # Add the genres to each episode
            for ep in s.episodes:
                ep.genres.append(gnr)
                
                
if __name__ == '__main__':
    genres = generate_genres()
    movies = generate_movies(num=100000)
    series, series_names = generate_series(num=50000)
    generate_episodes(series, series_names, num=850000)
    embed_genres(genres, movies, series)
    
    # Commit the objects to the database
    with orm.Session(ENGINE) as session:
        for g in genres:
            session.add(g)
        for m in movies:
            session.add(m)
        for s in series:
            session.add(s)
        session.commit()

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

# Load secrets
load_dotenv()
db_url = os.getenv("DB_URL")

# Create a sqlalchemy engine
ENGINE = sa.create_engine(db_url)

# Instantiate Faker Object generator
fake = Faker()

# Dictionary for content translation
TRANSLATIONS = {
    "Adrenaline Rush": ["A tope", "Sobredosis de Adrenalina"],
    "Into the Unknown": ["Hacia lo desconocido"],
    "Comedy Gold": ["Mucha Risa"],
    "Emotional Journey": ["Viaje Emocional", "Dimensión Emocional"],
    "Blood Moon Rising": [
        "El surgimiento de los muertos", 
        "El Acenso de la luna roja",
        "El Ascenso del Mal",
    ],
    "The Final Hour": ["La Hora Final", "La Última Hora"],
    "The Underdog Story": ["La Historia del Perro de Abajo"]
}


# Generate list of random stuff to add complexity
places = [
    "Monterrey", "San Pedro", "Guadalupe", "Apodaca", "Guadalajara", "Tenochtitlan",
    "Fallout", "New Vegas", "Old Vegas", "Chilangolandia", "Gringoland", "Ferghana",
    "Indo Kush", "Bolsonaria", "Colombia", "Maracaibo", "Easter Island", "Luzern",
    "Zurich", "the Alps", "Powhatan", "Anderson Island", "Colinas del Sabio",
    "California", "Utapau", "a gerrymandered state", "federal district", "Mérida",
    "Milwaukee", "Daytona", "Henderson Field", "München", "Österreich", "Munich",
    "Boston", "Harvard", "MIT", "CMU", "Toronto", "Ottawa", "Taum Sauk",
    "the Lower Reservoir", "Los Angeles", "Capri"
]

animals = [
    "Cow", "Fish", "Antelope", "Eagle", "Lion", "Seabird", "Xenomorph", "Seacow",
    "Seapig", "Monkey", "Hawk", "Panda", "Polar Bear", "Ant", "Grasshopper",
    "Wolf", "Panther", "Leopard", "Dragon", "Phoenix", "Griffin", "Unicorn"
]

criminal_adjectives = [
    "Fast", "Furious", "Peaky", "Bourbon", "Pedagogic", "Cruel", "Inglorious",
    "Blazing", "Ruthless", "Deadly", "Silent", "Vengeful", "Notorious"
]

criminals = [
    "Blinders", "Killers", "Murderers", "Scorpions", "Psychopaths", "Bastards",
    "Drug Addicts", "Blazers", "Arsonists", "Syndicate", "Cartel", "Brotherhood"
]

superhero_names = [
    "Cowman", "Enderman", "Fishman", "Sealman", "Tungstenman", "Diamondwoman",
    "Captain Oceania", "Captain Europe", "Captain Antarctica", "Purple Son",
    "Titan", "Metroman", "Busman", "Borg", "Nico Hulkenberg", "Dudududu",
    "Dodo", "Raindeerman", "Friendly Werewolf", "Carolus Rex", "Pooman",
    "Doctor Salvation", "Santa Monica", "Blue Daughter", "Red Velvet",
    "Curious George", "Captain Gold", "Trebala", "Harpy", "Goddess of Antioch"
]

weapons = ["Blade", "Knife", "Rifle", "Gun", "Pistol", "Axe", "Slate", "Arch", "Bow", "Crossbow"]

body_parts = ["back", "eye", "foot", "tooth", "nose", "ear", "knee", "belly", "arm", "head", "neck", "crotch"]

things = ["Frying pans", "Ketchup", "Mayonnaise", "Swords", "Lands", "Bracelets", "Octopuses", "Night", "Twilight", "Dead", "Hells", "Heaven", "Long Table", "Crimson Tide", "Yellow Horde"]


class WeightedChoice:
    """Random Choices wrapper allowing for delayed chosing."""
    def __init__(self, choice: dict[str, float], k: int = 1):
        """
        Constructor...
        Args:
            choice (dict[str, float]): Items as keys and weights as values.
            k (int, optional): Number of choices to be returned.
        """
        self.items = list(choice.keys())
        self.weights = list(choice.values())
        self.k = k

    def choose(self):
        return random.choices(self.items, weights=self.weights, k=self.k)


class ContentGenerator:
    """Abstract Class to generate content."""
    def __init__(self) -> None:
        """
        Initializes the content genenerator with a fixed amount of additional genres and a WeightedChoice for the main genres.
        The additional genres and titles for each main genre are generated through WeightedChoices inside propierties.
        """
        self.additional_genres = max(random.randint(0, 5) - random.randint(0, 3), 0)
        
        # PRIMARY GENRES
        self.genres = WeightedChoice({
            "Action": 0.10,
            "Adventure": 0.10,
            "Animation": 0.10,
            "Comedy":0.05,
            "Crime": 0.05,
            "Drama": 0.05,
            "Fantasy": 0.05,
            "Horror":0.06,
            "Musical": 0.04,
            "Romance": 0.07,
            "Science_Fiction": 0.08,
            "Sci-Fi": 0.01,
            "Thriller": 0.02,
            "Western": 0.11,
            "Sports": 0.02,
            "Documentary": 0.05,
            "Reality": 0.04
        })

    # ACTION GENRE
    @property
    def action(self):
        return {
            "name": random.choice([
                f"{fake.last_name()}: Maximum Velocity",
                f"The {fake.color_name()} Storm",
                f"Operation {fake.military_apo()}",
                f"Code {fake.color_name()}",
                f"The {random.choice(weapons)} of {random.choice(places)}",
                f"Explosive {fake.word()}",
                "Adrenaline Rush",
                f"{fake.first_name()} Protocol"
            ]),
            "secondary_genres": WeightedChoice({
                "Martial Arts": 0.25,
                "Spy": 0.15,
                "Military": 0.20,
                "Superhero": 0.10,
                "Disaster": 0.08,
                "Chase": 0.12,
                "Revenge": 0.10
            }, k=self.additional_genres)
        }

    # ADVENTURE GENRE
    @property
    def adventure(self):
        return {
            "name": random.choice([
                f"Journey to {random.choice(places)}",
                f"The Quest for the {fake.color_name()} {random.choice(things)}",
                f"Treasure of {fake.last_name()} Island",
                f"The {fake.color_name()} Compass",
                f"Expedition {random.randint(1, 100)}",
                f"The Map of {random.choice(places)}",
                "Into the Unknown",
                f"The {random.choice(animals)} Trail"
            ]),
            "secondary_genres": WeightedChoice({
                "Jungle": 0.20,
                "Desert": 0.15,
                "Ocean": 0.10,
                "Mountain": 0.5,
                "Snow": 0.10,
                "Treasure Hunt": 0.10,
                "Pirate": 0.15,
                "Survival": 0.15
            }, k=self.additional_genres)
        }

    # ANIMATION GENRE
    @property
    def animation(self):
        return {
            "name": random.choice([
                f"The Adventures of {fake.first_name()}",
                f"{random.choice(animals)} Tales",
                f"Magic in {random.choice(places)}",
                f"The {fake.color_name()} Kingdom",
                f"Dancing {random.choice(animals)}s",
                f"The Singing {random.choice(things)}",
                "Cartoon Chronicles",
                f"Studio {fake.last_name()}"
            ]),
            "secondary_genres": WeightedChoice({
                "Traditional 2D": 0.30,
                "CGI": 0.15,
                "3D": 0.20,
                "Stop Motion": 0.10,
                "Mixed Media": 0.08,
                "Puppetry": 0.05,
                "Rotoscoping": 0.12
            }, k=self.additional_genres)
        }

    # COMEDY GENRE
    @property
    def comedy(self):
        return {
            "name": random.choice([
                f"The Funny Side of {fake.job()}",
                f"{fake.first_name()}'s Big Mistake",
                f"Chaos in {random.choice(places)}",
                f"The {fake.color_name()} Comedy",
                f"Laughing with {random.choice(animals)}s",
                f"The Misadventures of {fake.name()}",
                "Comedy Gold",
                f"Silly {fake.word()}s"
            ]),
            "secondary_genres": WeightedChoice({
                "Romantic Comedy": 0.25,
                "Slapstick": 0.15,
                "Dark Comedy": 0.20,
                "Screwball": 0.10,
                "Parody": 0.15,
                "Satire": 0.15
            }, k=self.additional_genres)
        }

    # DRAMA GENRE
    @property
    def drama(self):
        return {
            "name": random.choice([
                f"The Heart of {fake.name()}",
                f"Tears in {random.choice(places)}",
                f"The {fake.color_name()} Letter",
                f"Stories from {fake.street_name()}",
                f"The Weight of {fake.word()}",
                f"Memories of {fake.name()}",
                "Emotional Journey",
                f"The Price of {fake.word()}"
            ]),
            "secondary_genres": WeightedChoice({
                "Family Drama": 0.25,
                "Psychological Drama": 0.20,
                "Social Drama": 0.15,
                "Political Drama": 0.10,
                "Criminal Drama": 0.02,
                "Legal Drama": 0.10,
                "Medical Drama": 0.18
            }, k=self.additional_genres)
        }

    # HORROR GENRE
    @property
    def horror(self):
        return {
            "name": random.choice([
                f"The {fake.color_name()} Terror",
                f"Nightmare in {random.choice(places)}",
                f"The Haunting of {fake.street_name()}",
                f"Screams from {fake.building_number()} {fake.street_name()}",
                f"The {random.choice(body_parts)} Collector",
                f"Dark {fake.word()}",
                "Blood Moon Rising",
                f"The {fake.color_name()} Shadow"
            ]),
            "secondary_genres": WeightedChoice({
                "Slasher": 0.20,
                "Supernatural": 0.25,
                "Psychological Horror": 0.20,
                "Zombie": 0.10,
                "Vampire": 0.08,
                "Werewolf": 0.05,
                "Ghost": 0.12
            }, k=self.additional_genres)
        }

    # MUSICAL GENRE
    @property
    def musical(self):
        return {
            "name": random.choice([
                f"Songs from {random.choice(places)}",
                f"The {fake.color_name()} Note",
                f"Dancing in {fake.city()}",
                f"Melody of {fake.name()}",
                f"The Singing {random.choice(animals)}",
                f"Rhythm of {fake.word()}",
                "Broadway Dreams",
                f"The {fake.color_name()} Symphony"
            ]),
            "secondary_genres": WeightedChoice({
                "Broadway": 0.30,
                "Jukebox Musical": 0.20,
                "Rock Opera": 0.15,
                "Dance Musical": 0.20,
                "Biographical Musical": 0.15
            }, k=self.additional_genres)
        }

    # ROMANCE GENRE
    @property
    def romance(self):
        return {
            "name": random.choice([
                f"Love in {random.choice(places)}",
                f"The {fake.color_name()} Rose",
                f"{fake.first_name()} and {fake.first_name()}",
                f"Hearts in {fake.city()}",
                f"The Love of {fake.name()}",
                f"Passion in {fake.month_name()}",
                "Eternal Love",
                f"Quantum {fake.word()}",
                f"The {fake.color_name()} Wedding"
            ]),
            "secondary_genres": WeightedChoice({
                "Romantic Comedy": 0.35,
                "Historical Romance": 0.20,
                "Contemporary Romance": 0.25,
                "Paranormal Romance": 0.10,
                "Erotic Romance": 0.10
            }, k=self.additional_genres)
        }

    # SCIENCE FICTION GENRE
    @property
    def science_fiction(self):
        return {
            "name": random.choice([
                f"2{random.randint(100, 999)}: The Future",
                f"Galaxy {fake.lexify('???-###')}",
                f"The {fake.color_name()} Planet",
                f"Robots of {random.choice(places)}",
                f"The {fake.word()} Station",
                f"Quantum {fake.word()}",
                "Space Odyssey",
                f"The {fake.color_name()} Dimension"
            ]),
            "secondary_genres": WeightedChoice({
                "Space Opera": 0.10,
                "Science Fantasy": 0.15,
                "Cyberpunk": 0.20,
                "Dystopian": 0.20,
                "Time Travel": 0.15,
                "Alien Contact": 0.10,
                "Post-Apocalyptic": 0.10
            }, k=self.additional_genres)
        }

    # THRILLER GENRE
    @property
    def thriller(self):
        return {
            "name": random.choice([
                f"The {fake.color_name()} Conspiracy",
                f"Edge of {fake.word()}",
                f"The {fake.word()} Protocol",
                f"Danger in {random.choice(places)}",
                f"The {fake.color_name()} Files",
                f"Midnight {fake.word()}",
                "The Final Hour",
                f"The {fake.word()} Challenge",
                f"Code {fake.color_name()}"
            ]),
            "secondary_genres": WeightedChoice({
                "Psychological Thriller": 0.25,
                "Political Thriller": 0.15,
                "Techno Thriller": 0.20,
                "Medical Thriller": 0.10,
                "Legal Thriller": 0.15,
                "Conspiracy Thriller": 0.15
            }, k=self.additional_genres)
        }

    # WESTERN GENRE
    @property
    def western(self):
        return {
            "name": random.choice([
                f"The Gunslinger of {random.choice(places)}",
                f"Wild {fake.word()}",
                f"The {fake.color_name()} Sheriff",
                f"Sunset in {fake.city()}",
                f"The {fake.word()} Gang",
                f"Dust and {fake.word()}",
                "High Noon Showdown",
                f"The Ballad of {fake.name()}"
            ]),
            "secondary_genres": WeightedChoice({
                "Spaghetti Western": 0.25,
                "Revisionist Western": 0.20,
                "Comedy Western": 0.15,
                "Acid Western": 0.10,
                "Space Western": 0.15,
                "Contemporary Western": 0.15
            }, k=self.additional_genres)
        }

    # SPORTS GENRE
    @property
    def sports(self):
        return {
            "name": random.choice([
                f"Champions of {random.choice(places)}",
                f"The {fake.color_name()} Team",
                f"Victory in {fake.city()}",
                f"The {fake.word()} League",
                f"Training for {fake.word()}",
                f"Gold Medal {fake.word()}",
                "The Underdog Story",
                f"Game of {fake.word()}s"
            ]),
            "secondary_genres": WeightedChoice({
                "Football": 0.20,
                "Basketball": 0.15,
                "Baseball": 0.15,
                "Boxing": 0.20,
                "Racing": 0.15,
                "Olympics": 0.15
            }, k=self.additional_genres)
        }

    # CRIME GENRE
    @property
    def crime(self):
        return {
            "name": random.choice([
                # Detective-style titles
                f"Detective {fake.last_name()}",
                f"The {fake.color_name()} Case",
                f"Mystery at {random.choice(places)}",
                f"Inspector {fake.last_name()}",
                # Noir-style titles
                f"Dark Night in {fake.city()}",
                f"The {fake.color_name()} Shadow",
                f"Midnight {fake.word()}",
                f"Black {fake.word()}",
                # Gangster-style titles
                f"The Ballad of {fake.name()}",
                f"The {fake.last_name()} Family",
                f"{random.choice(criminal_adjectives)} {random.choice(criminals)}",
                f"King of {random.choice(places)}",
                # Heist-style titles
                f"The {fake.color_name()} Job",
                f"Ocean's {random.randint(2, 20)}",
                f"The {random.choice(places)} Heist",
                f"Stealing {fake.word()}",
                # Hood-style titles
                f"Streets of {random.choice(places)}",
                f"The {random.choice(animals)} Gang",
                f"Blood and {fake.word()}",
                # Mystery-style titles
                f"The {fake.word()} Mystery",
                f"Who Killed {fake.name()}?",
                f"The Missing {fake.word()}",
                # Vigilante-style titles
                f"The {fake.color_name()} Vigilante",
                f"Justice in {random.choice(places)}",
                f"The {random.choice(superhero_names)} Files"
            ]),
            "secondary_genres": WeightedChoice({
                "Detective": 0.15,
                "Film Noir": 0.10,
                "Gangster": 0.20,
                "Heist": 0.15,
                "Hood Film": 0.08,
                "Mystery": 0.12,
                "Vigilante": 0.05,
                "Police Procedural": 0.10,
                "Organized Crime": 0.05
            }, k=self.additional_genres)
        }

    # FANTASY GENRE
    @property
    def fantasy(self):
        return {
            "name": random.choice([
                f"The Chronicles of {random.choice(places)}",
                f"The {fake.color_name()} Kingdom",
                f"Quest for the {fake.color_name()} {random.choice(things)}",
                f"The {fake.color_name()} Throne",
                f"Magic in {random.choice(places)}",
                f"The {random.choice(animals)} Prophecy",
                f"Realm of {fake.word()}",
                f"The {fake.color_name()} Wizard",
                f"Dragons of {random.choice(places)}",
                f"The {fake.word()} Saga",
                f"Legends of {fake.last_name()}",
                f"The {fake.color_name()} Spell",
                f"Empire of {fake.word()}",
                f"The {random.choice(animals)} Wars",
                f"Curse of the {fake.color_name()} {random.choice(things)}",
                f"The {fake.word()} Alliance"
            ]),
            "secondary_genres": WeightedChoice({
                "High Fantasy": 0.25,
                "Urban Fantasy": 0.15,
                "Dark Fantasy": 0.20,
                "Contemporary Fantasy": 0.15,
                "Epic Fantasy": 0.15,
                "Sword and Sorcery": 0.10
            }, k=self.additional_genres)
        }
        
    # DOCUMENTARY GENRE
    @property
    def documentary(self):
        return {
            "name": random.choice([
                f"Inside {random.choice(places)}",
                f"The Secret World of {random.choice(animals)}s",
                f"Uncovering {fake.word()}",
                f"The Story of {fake.name()}",
                f"{fake.word()}: A {fake.word()} Story",
                f"Behind the {fake.color_name()} Curtain",
                f"The Rise and Fall of {fake.company()}",
                f"Voices from {random.choice(places)}",
                f"The {fake.color_name()} Truth",
                f"Exploring {fake.word()}",
                f"Lost Secrets of {random.choice(places)}",
                f"The {fake.word()} Chronicles",
                f"Breaking: The {fake.word()} Investigation",
                f"Journey into {fake.word()}",
                f"The Hidden {fake.word()}"
            ]),
            "secondary_genres": WeightedChoice({
                "Historical": 0.18,
                "Nature": 0.15,
                "Political": 0.12,
                "Social Issues": 0.14,
                "Biography": 0.16,
                "True Crime": 0.13,
                "Science": 0.08,
                "Sports": 0.04
            }, k=self.additional_genres)
        }

    # REALITY TV GENRE
    @property
    def reality(self):
        return {
            "name": random.choice([
                f"Real Life in {random.choice(places)}",
                f"The {fake.word()} Challenge",
                f"Surviving {random.choice(places)}",
                f"The {fake.color_name()} House",
                f"Dating in {fake.city()}",
                f"Big {fake.word()}",
                f"The Ultimate {fake.word()}",
                f"Life with the {fake.last_name()}s",
                f"Keeping Up with {fake.word()}",
                f"The {fake.word()} Wars",
                f"Making {fake.word()}",
                f"The {fake.color_name()} Bachelor",
                f"Island of {fake.word()}",
                f"The Real {fake.job()}s",
                f"Extreme {fake.word()}"
            ]),
            "secondary_genres": WeightedChoice({
                "Competition": 0.25,
                "Dating": 0.18,
                "Lifestyle": 0.15,
                "Survival": 0.12,
                "Family": 0.10,
                "Makeover": 0.08,
                "Travel": 0.07,
                "Drama": 0.05
            }, k=self.additional_genres)
        }
    

class MovieGenerator(ContentGenerator):
    """
    Class for generating movies. Inherits from ContentGenerator.
    Adds duration parameters (µ & sigma) to each main genre property.
    """
    def __init__(self) -> None:
        super().__init__()
        
    @property
    def action(self):
        temp = super().action
        temp["duration_params"] = (110, 20)
        return temp
    
    @property
    def adventure(self):
        temp = super().adventure
        temp["duration_params"] = (115, 18)
        return temp
    
    @property
    def animation(self):
        temp = super().animation
        temp["duration_params"] = (80, 13)
        return temp
    
    @property
    def comedy(self):
        temp = super().comedy
        temp["duration_params"] = (100, 10)
        return temp
    
    @property
    def drama(self):
        temp = super().drama
        temp["duration_params"] = (120, 22)
        return temp
    
    @property
    def horror(self):
        temp = super().horror
        temp["duration_params"] = (90, 24)
        return temp
    
    @property
    def musical(self):
        temp = super().musical
        temp["duration_params"] = (100, 12)
        return temp
    
    @property
    def romance(self):
        temp = super().romance
        temp["duration_params"] = (90, 17)
        return temp
    
    @property
    def science_fiction(self):
        temp = super().science_fiction
        temp["duration_params"] = (140, 16)
        return temp
    
    @property
    def thriller(self):
        temp = super().thriller
        temp["duration_params"] = (95, 13)
        return temp
    
    @property
    def western(self):
        temp = super().western
        temp["duration_params"] = (120, 19)
        return temp
    
    @property
    def sports(self):
        temp = super().sports
        temp["duration_params"] = (90, 20)
        return temp
    
    @property
    def crime(self):
        temp = super().crime
        temp["duration_params"] = (120, 14)
        return temp
    
    @property
    def fantasy(self):
        temp = super().fantasy
        temp["duration_params"] = (110, 23)
        return temp
    
    @property
    def documentary(self):
        temp = super().documentary
        temp["duration_params"] = (90, 9)
        return temp
    
    @property
    def reality(self):
        temp = super().reality
        temp["duration_params"] = (60, 8)
        return temp
        
    def generate_content(self, genres: List[Genre]) -> List[Movie]:
        """Generates a movie based on a random main genre.

        Args:
            genres (List[Genre]): List of all possible genres as objects

        Returns:
            Movie: The generated movie objects in different laguages.
        """
        
        # Dictionary mapping genres (strings) to genre properties
        genre_map = {
            "Action": self.action,
            "Adventure": self.adventure,
            "Animation": self.animation,
            "Comedy": self.comedy,
            "Crime": self.crime,
            "Drama": self.drama,
            "Fantasy": self.fantasy,
            "Horror": self.horror,
            "Musical": self.musical,
            "Romance": self.romance,
            "Science_Fiction": self.science_fiction,
            "Sci-Fi": self.science_fiction,
            "Thriller": self.thriller,
            "Western": self.western,
            "Sports": self.sports,
            "Documentary": self.documentary,
            "Reality": self.reality
        }
        
        genre_type = str(self.genres.choose()[0])   # Generate random genre
        genre_data = genre_map[genre_type.title()]  # Get genre property
        title = genre_data["name"]                  # Get title
        
        # Get genres as combination of main genre and additional genres
        genre_names = [genre_type] + genre_data["secondary_genres"].choose()
        
        # Get the duration of the movie from the duration parameters
        duration = int(random.normalvariate(
            mu=genre_data["duration_params"][0], 
            sigma=genre_data["duration_params"][1]
        ))
        
        # Translate to other languages
        titles = [title]
        if title in TRANSLATIONS:
            titles += TRANSLATIONS[title]
            
        # Mess up with the data
        for t in titles:
            if t[:3] == "The" and random.randint(1,1000) == 1:
                t = t[3:]

            if random.randint(1,1000) == 1:
                t = ' ' + t

            if random.randint(1,1000) == 1:
                t += ' '
            
        if random.randint(1,1000) == 1:
            duration *= 60
        
        # Generate movie object
        movies = []
        for t in titles:
            m = Movie(
                name = t,
                duration = duration
            )
            movies.append(m)
        
        # Add genres and shuffle them (just for more variability)
        for m in movies:
            for g in genres:
                if g.name in genre_names:
                    m.genres.append(g)
            random.shuffle(m.genres)
           
        return movies
    

class EpisodeGenerator(ContentGenerator):
    """A class to generate random episodes. Inherits from ContentGenerator."""
    def __init__(self) -> None:
        super().__init__()
        
    def generate_content(self, main_genre: str, season:int, duration:int) -> List[Episode]:
        """
        Generates the episodes, getting the name from the properties, but the rest from parameters.

        Returns:
            List[Episode]: The generated episodes in english and spanish.
        """
        
        # Dictionary mapping genres (strings) to genre properties
        genre_map = {
            "Action": self.action,
            "Adventure": self.adventure,
            "Animation": self.animation,
            "Comedy": self.comedy,
            "Crime": self.crime,
            "Drama": self.drama,
            "Fantasy": self.fantasy,
            "Horror": self.horror,
            "Musical": self.musical,
            "Romance": self.romance,
            "Science_Fiction": self.science_fiction,
            "Sci-Fi": self.science_fiction,
            "Thriller": self.thriller,
            "Western": self.western,
            "Sports": self.sports,
            "Documentary": self.documentary,
            "Reality": self.reality
        }
        
        # Get properties for genre base on the name passed for the main genre
        genre_data = genre_map[main_genre]
        ep_title = genre_data["name"]       # Get episode title
        
        # Translate to other languages
        titles = [ep_title]
        if ep_title in TRANSLATIONS:
            titles += TRANSLATIONS[ep_title]
        
        # Mess up with the data
        for t in titles:
            if t[:3] == "The" and random.randint(1,1000) == 1:
                t = t[3:]

            if random.randint(1,1000) == 1:
                t = ' ' + t

            if random.randint(1,1000) == 1:
                t += ' '
            
        if random.randint(1,1000) == 1:
            duration *= 60
        
        # Generate episodes in ditinct languages
        eps = []
        for t in titles:
            ep = Episode(
                name = ep_title,
                duration = duration+random.randint(-4, 4),
                season=season
            )
            eps.append(ep)
            
        return eps
        
        
class SeriesGenerator(ContentGenerator):
    """
    Class for generating movies. Inherits from ContentGenerator.
    Adds duration parameters (µ & sigma) and number of episodes to each main genre property.
    """
    def __init__(self) -> None:
        super().__init__()
        
    @property
    def action(self):
        temp = super().action
        temp["duration_params"] = (50, 4)
        temp["num_episodes"] = 20
        return temp
    
    @property
    def adventure(self):
        temp = super().adventure
        temp["duration_params"] = (48, 6)
        temp["num_episodes"] = 16
        return temp
    
    @property
    def animation(self):
        temp = super().animation
        temp["duration_params"] = (18, 10)
        temp["num_episodes"] = 30
        return temp
    
    @property
    def comedy(self):
        temp = super().comedy
        temp["duration_params"] = (28, 4)
        temp["num_episodes"] = 8
        return temp
    
    @property
    def drama(self):
        temp = super().drama
        temp["duration_params"] = (52, 5)
        temp["num_episodes"] = 24
        return temp
    
    @property
    def horror(self):
        temp = super().horror
        temp["duration_params"] = (40, 7)
        temp["num_episodes"] = 12
        return temp
    
    @property
    def musical(self):
        temp = super().musical
        temp["duration_params"] = (20, 2)
        temp["num_episodes"] = 8
        return temp
    
    @property
    def romance(self):
        temp = super().romance
        temp["duration_params"] = (31, 6)
        temp["num_episodes"] = 30
        return temp
    
    @property
    def science_fiction(self):
        temp = super().science_fiction
        temp["duration_params"] = (56, 7)
        temp["num_episodes"] = 16
        return temp
    
    @property
    def thriller(self):
        temp = super().thriller
        temp["duration_params"] = (44, 5)
        temp["num_episodes"] = 20
        return temp
    
    @property
    def western(self):
        temp = super().western
        temp["duration_params"] = (33, 10)
        temp["num_episodes"] = 10
        return temp
    
    @property
    def sports(self):
        temp = super().sports
        temp["duration_params"] = (45, 3)
        temp["num_episodes"] = 12
        return temp
    
    @property
    def crime(self):
        temp = super().crime
        temp["duration_params"] = (40, 6)
        temp["num_episodes"] = 20
        return temp
    
    @property
    def fantasy(self):
        temp = super().fantasy
        temp["duration_params"] = (48, 4)
        temp["num_episodes"] = 16
        return temp
    
    @property
    def documentary(self):
        temp = super().documentary
        temp["duration_params"] = (65, 5)
        temp["num_episodes"] = 20
        return temp
    
    @property
    def reality(self):
        temp = super().reality
        temp["duration_params"] = (47, 4)
        temp["num_episodes"] = 20
        return temp
    
    def generate_content(self, genres: List[Genre]) -> List[Series]:
        """Generates a series WITH episodes.

        Args:
            genres (List[Genre]): List of all posible genres

        Returns:
            List[Series]: Generated Series in different languages
        """
        
        # Dictionary mapping genres (strings) to genre properties
        genre_map = {
            "Action": self.action,
            "Adventure": self.adventure,
            "Animation": self.animation,
            "Comedy": self.comedy,
            "Crime": self.crime,
            "Drama": self.drama,
            "Fantasy": self.fantasy,
            "Horror": self.horror,
            "Musical": self.musical,
            "Romance": self.romance,
            "Science_Fiction": self.science_fiction,
            "Sci-Fi": self.science_fiction,
            "Thriller": self.thriller,
            "Western": self.western,
            "Sports": self.sports,
            "Documentary": self.documentary,
            "Reality": self.reality
        }
        
        genre_type = str(self.genres.choose()[0])   # Generate random genre based on weights
        genre_data = genre_map[genre_type.title()]  # Get genre properties
        title = genre_data["name"]                  # Get title from properties
        
        # Get genres
        genre_names = [genre_type] + genre_data["secondary_genres"].choose()
        
        # Calculate durations for episodes based on duration parameters and normal distribution
        duration = int(random.normalvariate(
            mu=genre_data["duration_params"][0], 
            sigma=genre_data["duration_params"][1]
        ))
        
        # Translate to other languages
        titles = [title]
        if title in TRANSLATIONS:
            titles += TRANSLATIONS[title]
        
        # Mess up with the data
        for t in titles:
            if t[:3] == "The" and random.randint(1,1000) == 1:
                t = t[3:]

            if random.randint(1,1000) == 1:
                t = ' ' + t

            if random.randint(1,1000) == 1:
                t += ' '
        
        # Genrate series
        series: List[Series] = []
        for t in titles:
            s = Series(name=t)
            series.append(s)
        
        # Genetate episodes and append them to the series
        num_episodes = genre_data["num_episodes"]
        for ep_number in range(num_episodes):
            ep_generator = EpisodeGenerator()
            eps = ep_generator.generate_content(
                main_genre=genre_type.title(), 
                season=max(1, ep_number//random.randint(1,4)), 
                duration=duration
            )
            for ep in eps:
                for s in series:
                    s.episodes.append(ep)
        
        # Add each genre to the series
        for g in genres:
            if g.name in genre_names:
                for s in series:
                    s.genres.append(g)
                    for ep in s.episodes:
                        ep.genres.append(g)
                    # Shuffle genres for complexity
                        random.shuffle(ep.genres)
                    random.shuffle(s.genres)
        
        return series
        

def generate_genres() -> List[Genre]:
    """Generate the all the genres of the catalog."""
    genre_names = {
            "Action", "Martial Arts", "Spy", "Military", "Superhero", "Disaster",
                "Chase", "Revenge", "Monster",
            "Adventure", "Jungle", "Desert", "Ocean", "Mountain", "Snow", 
                "Treasure Hunt", "Pirate", "Survival",
            "Animation", "Traditional 2D", "CGI", "3D", "Stop Motion",
                "Mixed Media", "Puppetry", "Rotoscoping",
            "Comedy", "Romanctic Comedy", "Slapstick", "Dark Comedy", "Screwball",
                "Parody", "Satire",
            "Crime", "Detective", "Film Noir", "Gangster", "Heist", "Hood Film",
                "Mystery", "Vigilante", "Police Procedural", "Organized Crime",
            "Drama", "Family Drama", "Psychological Drama", "Social Drama",
                "Political Drama", "Criminal Drama", "Legal Drama", "Medical Drama",
            "Fantasy", "High Fantasy", "Urban Fantasy", "Dark Fantasy",
                "Contemporary Fantasy", "Epic Fantasy", "Sword and Sorcery",
            "Horror", "Slasher", "Supernatural", "Psychological Horror", "Zombie",
                "Vampire", "Werewolf", "Ghost",
            "Musical", "Broadway", "Jukebox Musical", "Rock Opera", "Dance Musical",
                "Biographical Musical",
            "Romance",  "Romantic Comedy", "Historical Romance", 
                "Contemporary Romance", "Paranormal Romance", "Erotic Romance",
            "Science_Fiction", "Space Opera", "Science Fantasy", "Cyberpunk",
                "Dystopian", "Time Travel", "Alien Contact", "Post-Apocalyptic",
            "Sci-Fi",
            "Thriller", "Psychological Thriller", "Political Thriller",
                "Techno Thriller", "Medical Thriller", "Legal Thriller",
                "Conspiracy Thriller",
            "Western", "Spaghetti Western", "Revisionist Western", "Comedy Western",
                "Acid Western", "Space Western", "Contemporary Western",
            "Sports", "Foorball", "Basketball", "Baseball", "Boxing", "Racing",
                "Olympics",
            "Documentary", "Historical", "Nature", "Political", "Social Issues",
                "Biography", "True Crime", "Science", "Sports",
            "Reality", "Competition", "Dating", "Lifestyle", "Family",
                "Makeover", "Travel"
    }
    genre_objs = []
    
    # Create each genre object
    for name in list(genre_names):
        genre_objs.append(Genre(name=name))
        
    return genre_objs


def generate_movies(genres: List[Genre] ,num: int = 5000) -> List[Movie]:
    """Generates `num` fake movies of the catalog."""
    # List to store movies
    movies = []
    
    # Create object to generate movies
    movie_generator = MovieGenerator()
    for _ in range(num):
        translations = movie_generator.generate_content(genres)
        for m in translations:
            movies.append(m)
    return movies   # return the list of movies


def generate_series(genres: List[Genre], num: int = 2000):
    """Generates `num` fake series (with episodes) for the catalog. Episodes included"""
    series = []
   
    # Instantiate object to generate series
    series_generator = SeriesGenerator()
    for _ in range(num):
        translations = series_generator.generate_content(genres) # Generate a series
        for s in translations:
            series.append(s)
    return series # return list of series

                
if __name__ == '__main__':
    # Generate genres, movies and series
    genres = generate_genres()
    movies = generate_movies(genres)
    series = generate_series(genres)
    
    # Commit the objects to the database
    with orm.Session(ENGINE) as session:
        for g in genres:
            session.add(g)
        for m in movies:
            session.add(m)
        for s in series:
            session.add(s)
        session.commit()

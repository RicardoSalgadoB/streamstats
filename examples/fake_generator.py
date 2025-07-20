import random

from faker import Faker

fake = Faker()

adjectives = ["Silent", "Deadly", "Hidden", "Unseen", "Forgotten", "Broken", "Gullible", "Sexy"]
nouns = ["Legacy", "Secret", "Whisper", "Tale", "Journey", "Code", "Shadow", "Pirates"]
verbs = ["Write", "Explore", "Implement", "Cry", "Shout", "Dance", "Take", "Kill", "Pay"]

def generate_fake_title():
    # Combine elements to make a title
    templates = [
        f"The {fake.word().title()} of {fake.name()}",
        f"{fake.word().title()} {fake.word().title()}",
        f"A {random.choice(adjectives)} {random.choice(nouns)}",
        f"{fake.name()}'s {random.choice(nouns)}",
        f"The {random.choice(adjectives)} {random.choice(nouns)} of {fake.country()}",
        f"{random.choice(verbs)} the {random.choice(nouns)}",
        f"{random.choice(adjectives)} {random.choice(nouns)}: The {fake.word().title()} Continues"
    ]
    return random.choice(templates)

if __name__ == '__main__':
    for i in range(3):
        print(generate_fake_title())
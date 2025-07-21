# StreamStats
A RESTful backend for managing streaming catalog, built with Python, FastAPI, and PostgreSQL.

## Summary
A **Python RESTful API** for a streaming service catalog utilizing a peristent **PostgreSQL** database and **SQLAlchemy ORM** for DB-API robust interactions, containerized using **Docker**. It enables efficient management of movies, series, episodes, genres, and user ratings. 

The primary goal was to demonstrate proficiency in modern backend development practices, relational database design, and API development, building upon a foundational understanding of databases.

## Background
Last semester, I had to code a *C++* project to store a catalog of movies and series. While doing so, I couldn't but think that no real company would build a database with pure *C++*, instead, I tought, they would do it using *SQL*.

Since the semester ended, I've not had the chance to work on this project, but using the excuse of vacations (much to the demise of my family) I took the time to learn some of the technologies that I would eventually use here. Once I returned from vacations, I had the momentum and the project was done in less than a week.

## Tech Stack
* ***PostgreSQL***: 
    * **HOW?** Used it to store the information about the movies and series. 
    * **WHY?** The most used Relational Mapping Database (RMDB) because of its capabilities, ACID complience and efficiency. *NoSQL* was another option, but I believe that in my position (I'm data not backend) Postgres would be more useful.
* ***FastAPI***:
    * **HOW?** It creates an API to access and modify the information of the catalog.
    * **WHY?** The other candidates where *Flask* and *Django*. I wanted to use a lightweight backend, so *Django* was out of the question. *FastAPI* is quickly gaining traction in the backend ecosystem and personally prefer its syntax.
* ***SQLAlchemy**:
    * **HOW?** I needed a way to connect the API with the DB and that is what this technology does. It does this with an *Object Relational Mapper (ORM)*, but as I will discuss later it could also be done with the only the *core* features of SQLAlchemy.
    * **WHY?** SQLAlchemy is the most popular. If I had chosen *django*, I would have considered *DjangoORM*, but I didn't.
* ***Alembic***:
    * **HOW?** It manages database migrations, instead of creating schemas with SQLAlchemy.
    * **WHY?** Even though I could have stuck with SQLAlchemy, this technology is standard industry and facilitates management of the database.
* ***Locust***:
    * **HOW?** Its use is for testing the API, its latency and throughput.
* ***Docker***: 
    * **HOW?** Containerization. A *docker-compose* is used to run both the app and the database.
    * **WHY?** Its robustness, adaptability and scalability. Docker is standard in backend development.

## Features
* **Content Management**: CRUD operations for movies, series, episodes and genres.
* **Rating System**: Users dubmit ratings for content and averages are dynamically calculated.
* **Object Relational Mapper (ORM)**: Python classes are automatically mapped to SQL tables. Handy for the migration from *C++* to *SQL*.
* **Joined Table Inheritance**: A feature of SQLAlchemy that preserves Python Inheritance without data redundancies.
* **Indexes**: An index on the name of the contents allows for fast information retrieval.
* **Pagination**: Efficienty recovery of content data in managable chucks.
* **API Documentation**: Automatically generated as feature of *Fast API*.

## Getting Started

### Prerequisites
* Python 3.9+
* Docker
* pip
* venv

### Installation

1. Clone this repo
```bash
git clone [https://github/RicardoSalgadoB/streamstats.git](https://github/RicardoSalgadoB/streamstats.git)
cd streamstats
```

2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

3. Install python dependencies
```bash
pip install -r requirements.txt
```

### Running the application

1. Start the container using Docker Compose:
```bash
docker compose up --build -d
```

2. Access documentation at `http://localhost:8000/docs`.

3. Stop the container (ensuring data persisitency):
```bash
docker compose down
```

## API endpoints
Documentation can also be accessed at `http://localhost:8000/docs`.

**Movie Retrieval Methods**
- `GET  /movies`: Retrieve a paginated list of movies.
- `GET  /movies/{name})`: Get details for a movie with the given name.

**Series Retrieval Methods**
- `GET  /series`: Retrieve a paginated list of series.
- `GET  /series/{name}`: Get details for a specific series.
- `GET  /series/{name}/episodes`: Retrieve a list for the episodes of series.
- `GET  /series/{series_name}/episodes/{name}`: Get a given episode of a given series.

**All Content Retrieval Methods**
- `GET  /content`: Retrieve a paginated list of movies and series.
- `GET  /content/{name}`: Get details for a given movie or series.

**Rating Methods**
- `POST /movies/{name}/rate`: Submit a rating for a movie.
- `POST /series/{name}/rate`: Submit a rating for a series.
- `POST /series/{series_name}/episodes/{name}/rate`: Submit a rating for the given episode of a series.

**Adding Content Methods**
- `POST /movies`: Create a new movie. Accepts a json payload.
- `POST /series`: Create a new series. Accepts a json payload.
- `POST /series/{series_name}/episodes`: Create a new episode of a given series. Accepts a json payload.
- `POST /genres`: Create a new genre. Accepts a json payload.

**Delete Content Methods**
- `DELETE /movies/{name}`: Delete a given movie.
- `DELETE /series/{name}`: Delete a given series.
- `DELETE /series/{series_name}/episodes/{name}`: Delte an episode of a given series.
- `DELETE /genres/{name}`: Delete a given genre.

**Update Content Methods**
- `PATCH /movies/{name}`: Update a movie. Accepts a json payload.
- `PATCH /series/{name}`: Update a series. Accepts a json payload.
- `PATCH /series/{series_name}/episodes/{name}`: Update an episode of a given series. Accepts a json payload.
- `PATCH /genres/{name}`: Update a genre. Accepts a json payload.

## Database Schemas
The application's data is stored in a PostgreSQL 16 Database configured with the following schemas:

- **`content` table**: Stores metadata for attributes shared between movies, series and episodes.
- **`movie` table**: Extends `content` for movie specific information (only its ID in this application).
- **`series` table**: Extends `content` for series specific information.
- **`episode` table**: Extends `content` for episode specific information, linked to `series`.
- **`genre` table**: Store genre category information.
- **`genre_content_junc` table**: Junction table for many-to-many relationship between `genre` and `content`.
- **`rating` table**: Stores user ratings for specific content,

## Testing
The following where carried out:

- **Unit Tests**: Implemented with `pytest`, both for API methods and Database intereactions.
- **Database Migration Tests**: Migrations are tested to ensure schema evolution reliability (even though there is only one version).
- **Load Tests**: Conducted performance tests with *Locust* to evaluate API throughput.

## Performance
Out of testing, the following results came out:

- For common lockups, updates and rate methods, the average API response time of the application is *<20 ms*.
- The application supported a throughput of *240 rps* for a minute before significant latency degradation. However, failures show a rate of *1 fps* with an *75 rps*.
- Database searches are executed in *0.5 ms* accross a *25,000 row database*, even though searches through SQLAlchemy take *50 ms* on average.
- Multiple content lookups (aka. the showing methods) take *400 ms* on average (it depends on the size specified by the request).


### Comparison with previous C++ implementation
The average search takes around 10 microseconds (3 lightkilometers or 1.9 lightmiles on the same hardware, if the Bethesda Terrace exploted, people in the Empire State Building would see that at the same time my search ended).

I know that SQL has its benefits (persistency and sharability) but this is harsh.

### Hardware
The tests were run on a *M4 Macbook Pro* at 30°C (86 °F) and 49% humidity (source: Apple Weather).

## Future
* **Front-end**: No, I won't add a frontend. I'm a *data scientist delving into data engineering delving into backend*, I will not become a *data scientist delving into data engineering delving into backend delving into frontend*. For the conceivable future.
* **Optimization with Core**: I don't believe that any optimization will achieve rates comparable to C++, but it would be interesting to see how much I get (probably not much).
* **Live Deployment**: I would like to deployment in the future as it is cool to have the project online (UNRELATED: my prose is a bit worse this time of the night), but the money constraint is always there.
* **ETL Pipeline**: This would allow me to become a *data scientist that only delves into data engineering* which would be something. Either way I already have an idea of how I might approach this but I need to learn the technology. For now I have to choose if  I do the documentation *breath-first* or *depth-first*.

## Contact
Ricardo Salgado Benítez - [ricardosabe2018@gmail.com] - [https://www.linkedin.com/in/ricardosalgadob/]
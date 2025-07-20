# StreamStats
A RESTful backend for managing video content, built with Python, FastAPI, and PostgreSQL.

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
* ***Locust***:
    * **HOW?** Its use is for testing the API, its latency and throughput.
* ***Docker***: 
    * **HOW?** Containerization. A *docker-compose* is used to run both the app and the database.
    * **WHY?** Its robustness, adaptability and scalability. Docker is standard in backend development.

## Features
* **Content Management**:
* **Rating System**:
* **Object Relational Mapper (ORM)**:
* **Joined Table Inheritnace**:
* **Indexes**:
* **Pagination**: 
* **API Documentation**: 

## Getting Started

## API Endpoints

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

## Performance

AVERAGE RESPONSE FOR SINGLE MOVIE
20 ms

RESPONSE TO SHOW ALL MOVIES
28 s

## Future
* **Front-end**: No, I won't add a frontend. I'm a *data scientist delving into data engineering delving into backend*, I will not become a *data scientist delving into data engineering delving into backend delving into frontend*. For the conceivable future.
* **Alembic**: 
* **Optimization with Core**:
* **

## Contact
Ricardo Salgado Benítez - [ricardosabe2018@gmail.com] - []
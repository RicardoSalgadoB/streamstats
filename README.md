# StreamStats ETL

An ETL pipeline built from API requests with the help of Python, Pandas, Polars, PySpark, Airflow, Docker and MongoDB

## Summary

A **Python ETL Pipeline** that extracts 100K records from an **RESTful API** (a fake streaming catalog that I built). This data is then transformed using three frameworks: **Pandas**, **Polars** and **Apache Spark**. The time performance of these frameworks is stored for future benchmarking. The transformed data is then loaded into **Mongo DB Atlas**. The complete pipeline is run inside various **Docker Containers** orchestrated with **Docker Compose**.

My goal was to show my ability to work with some of the most common data engineering tools and show that I can integrating succesfully to efficiently performa various tasks.

## Description

### Backend enhancements

Before I could begin "data engineering", I needed to make some adjustments to the backend. These changes can be classified into 2 categories: *Changes to the backend logic* and *Changes to the data* stored in the backend.

In the first department, my utmost priority was to make all methods accesible by ID and not only by name as it had been in the original version. This ended up leading to what I like to call the "GREAT QUERY PARAMETER MIGRATION" as it was immeasurably easier to pass the names and ids as query parameters than path parameters. Another improvement in this section was adding reviews to the database, this was as a result of wanting to make the data way more messier, which would remain a constant.

As I said, the main task of the second department was making the data messier. This was achieved with the following:

* Leading/trailing blankspaces
* Redundant genres (e.g. *Sci-Fi* == *Science Fiction*)
* Increasing the amount of genres stored in the database
* Translating some movies to Spanish while also leaving originals (I would then have to rejoin the reviews and ratings)
* Change content length (duration) to sometimes be in seconds instead of minutes
* Remove the "The" from some titles.

### Extracting

After these modifications, the backend was ready to serve data to my ETL and so it did. This was a relatively easy part of the project, the only dependency needed was Python's *Requests*. Further down the line, *PyMongo* was required to compare *last updated time* of the records and *last run time* stored in **Mongo DB** and only do updates to the database.

### Transforming

In a general manner, independently of the individuals tools and approaches used in each framework, the transformations consisted of the following steps:

1. Tranforming the data into the dataframes in the given framework.
2. Cleaning the data.
    1. Removing trailing and leading blankspaces.
    2. Adding back the "The" to the titles that had lost it.
    3. Translating back titles to Spanish (I wanted to use some sort of token comparison, for this but I had kept true to the Spansih tradition of making horrible translations, e.g. 101 Dalmatians $\to$ La noche de las narices frías (The Night of the Cold Noses), so I ended up using a dictionary).
    4. Standarize content length in minutes (this was done with thresholds, check how they were caclucalted in the *notebooks* folder).
3. Eliminate non-fiction genres (I am assuming my "clients" are only interested in ficiton content).
4. Remove redundant genres or split them (for example, *Romantic Comedy* $\to$ *Romance*, *Comedy*).
5. Add episodes to series in a list.
6. Get number of movies, series and episodes in each genre.

Finally, the `_id` column was added for making Mongo's life easier and the dataframes were trasnformed to a list of dictionaries.

I used 3 frameworks for these transformations: **Pandas**, **Polars** and **Apache Spark** (through **PySpark**)

#### Pandas

This was the easiest framework to implement, as I am the most familiarized with it. While it is the standard data transforming package in Python, I need to tell you a secret... IT DIDN'T WORK WITH MY 100K!!! Now... you might say, why are you adding this you \*\*\*\* and my answer is simple: It did work when the data was smaller (both running locally and in docker), therefore my only possible conclusion is that my data was too big to be processed by Pandas, which is amazing, it means that I can build an *scalable* data engineering pipeline (with, dare, I way **big data tools**). Either way, I still probably need to run more tests in order to claim this with absolute rigor.

When the data was smaller *Pandas* achieved roughly x20 faster performance than *Polars* and x100 compared to *Spark*.

#### Polars

I ended up liking a lot the way *Polars* works, from its syntax to its scalability. It certainly a good alternative to *Pandas* especially when the data is not that big as is with this case. The hardest part was ensuring the schema of the data was correct, which is a problem that only appeared when running in Docker. The performance of the framework was around 2 seconds when all the data was needed to be inserted to **Mongo** and right around 300 ms when updating content.

#### Spark

Both locally but very, very, very specially in **Docker**, Spark was one big awful hell to install. Part of these problems came from my "Install latest versions of everythong and don't look at compatibility" approach, which I learned to never again follow. The other part of the problems came from trying to have **Airflow** and **Spark** in one image, but I eventually discovered what is a *microservice*.

As I might have implied above, I do not believe that the scale of the data being ETLed justifies using **Spark**. Its time performance when uploading all entires to **Mongo** was 10 seconds and 7 seconds when updating, which allows me to conclude that there is a lot of overhead from the JVM (Java Virtual Machine). But hey, even if it wasn't jutified *I know how to use Spark + Airflow + Docker!*. Next step learn how to run it in a cluster.

### Loading

Coming up from the hell of data transformations, I was nice to see that *PyMongo* is an amazing library an extremely easy to use. It genuenly allowed me to do what what I wanted to do fast and intuitively so that I could focus on other more pressing problems. Even though I was only using **Mongo DB** to add a NO-SQL database to my resume, I genuinely ended up loving how easy it is to work with.

### Orchestrating

Next comes **Airflow**, which is rather easy to use actually. However, running it with **Docker** was the cause of many of the problems that I've described above, not to mention an awful stomachache and been bitten 8 times by spiders (they are related, I promise). I want to at least some of the choices I followed with my *Airflow* implementation. First, I used decorators, instead of context managers as I feel this the more pythonic approach not to mention more aesthetically pleasing. Second, for syncing up **Spark**, I used Data with Marc's approach as discussed in [his video](https://youtu.be/L3VuPnBQBCM?si=TtGoQKl2bQCP_Fda), which ended up solving all my problems once I managed to sync up versions correcty... so thank you, if you ever read this.

## Getting started

Running the project is relatively easy, just do the following (well, if you are in Linux or Mac. I guess you can figure it out, Window users :):

1. Clone the repo

```bash
git clone [https://github/RicardoSalgadoB/Streamstats-ETL.git](https://github/RicardoSalgadoB/Streamtats-etl.git)
cd streamstats
```

2. Go to the `airflow/dags` and change the strating time of each dag (well just *PySpark* and *Polars*, *Pandas* doesn't work) to whatever you want

3. Make an `.env` file and add a variable called *MONGO_CONN* to connect with **MONGO DB**, as well as the follwing variables to connect the backend database:

```
DB_URL="postgresql+psycopg2://<user>:<password>@backend-db:5432/streamstats"
POSTGRES_DB="streamstats"
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
```

4. Then, make sure you have **Docker** [installed](https://www.docker.com/get-started/) and go to the `streamstats` directory.

5. Build the docker image

```bash
docker-compose build
```

6. Run docker

```bash
docker-compose up -d
```

And that is it the Airflow is running, the dags will execute as the specified time.

To stop docker just do:

```bash
docker-compose down
```

Or, if you wish to restar the content in the backend:

```bash
docker-compose down -v
```

## Future

* **More performance tests**: Besides only time, I would like to mesasure *peak memory usage* for each framework. Also, I would like to show this performance benchmarks in some sort of dashboard (**Tableau** or **Power BI**), this is relatively easy, so proabably I am going to do so in the next week or so (hopefully).

## Contact

Ricardo Salgado Benítez - [ricardosabe2018@gmail.com] - [https://www.linkedin.com/in/ricardosalgadob/]
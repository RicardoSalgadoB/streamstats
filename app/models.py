from __future__ import annotations

import os

from typing import List, Optional
from dotenv import load_dotenv

# Generally gonna use this syntax. Easier than importing everything
import sqlalchemy as sa 
import sqlalchemy.orm as orm

# Load secrete varaibles
load_dotenv()
db_url = os.getenv("DB_URL")

# Create sqlalchemy engine
ENGINE = sa.create_engine(db_url)


# Base to store metadata
class Base(orm.DeclarativeBase):
    pass


# TABLES #

# Junction table for many2many relationships between re
genre_content_junc = sa.Table(
    "genre_content_junc",
    Base.metadata,
    sa.Column("content_id", sa.ForeignKey("content.id"), nullable=False),
    sa.Column("genre_id", sa.ForeignKey("genre.id"), nullable=False),
)


class Genre(Base):
    """A table to store information about genres."""
    __tablename__ = "genre"
    
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(30), 
        nullable=False, 
        unique=True # No real reson to have 2 genres with the same name
    )
    
    # Each genre can be mapped to many contents
    contents: orm.Mapped[List[Content]] = orm.relationship(
        back_populates="genres",
        secondary=genre_content_junc,
    )
    
    def __repr__(self) -> str:
        """Representation of the genre object. Retunrs a string"""
        return f"Genre(name={self.name!r})"
    
    def to_dict(self) -> dict:
        """Return a dict that Fast API can convert to JSON.
        Cannot overridw __dict__ as the SQLAlchemy implementation uses that.
        """
        return {
            "id": self.id,
            "genre": self.name,
        }
    
    
class Rating(Base):
    """Table to store information about user ratings.
    Has a many-to-one relationship with content.
    """
    __tablename__ = "rating"
    
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    score: orm.Mapped[int] = orm.mapped_column(nullable=False)
    review: orm.Mapped[str] = orm.mapped_column(
        sa.String(255), 
        nullable=True
    )
    
    # ID for the many to one relationship
    content_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("content.id"), 
        nullable=False
    )
    
    # Map content with the sqlalchemy orm
    content: orm.Mapped[Content] = orm.relationship(back_populates="ratings")
    
    def __repr__(self):
        return f"Rating(score='{self.score}', content_name={self.content.name!r})"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "score": self.score,
            "review": self.review,
            "content": self.content.name
        }


class Content(Base):
    """Table to store the general information about movies, series and episodes."""
    __tablename__ = "content"
    
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(nullable=False)
    type: orm.Mapped[str] = orm.mapped_column(nullable=False)
    
    # Mapper to allow for inheritance
    __mapper_args__ = {
        "polymorphic_identity": "content",
        "polymorphic_on": "type"
    }
    
    # Declare many-to-many and one-to-many relationships with genres and ratings
    genres: orm.Mapped[List[Genre]] = orm.relationship(
        back_populates="contents",
        secondary=genre_content_junc,
    )
    ratings: orm.Mapped[List[Rating]] = orm.relationship(
        back_populates="content",
        cascade="all, delete"
    )
    
    def __repr__(self) -> str:
        genres = [str(genre.name) for genre in self.genres]
        reviews = [str(rating.review) for rating in self.ratings]
        genres_str = ", ".join(genres)
        return (
            f"{self.__class__.__name__}(id={self.id}, title={self.name!r}, " 
            + f"duration='{self.duration!s} minutes', genre(s)={genres_str!r}, "    
                # duration isn't an attribute of content but of its children
            + f"average_rating={self.average!r}, "
            + f"reviews={reviews})"
        )
        
    def to_dict(self) -> dict:
        reviews = [str(rating.review) for rating in self.ratings]
        return {
            "id": self.id,
            "title": self.name,
            "duration_minutes": self.duration,  # same as above
            "genre(s)": [str(genre.name) for genre in self.genres],
            "average_rating": self.average,
            "reviews": reviews,
        }
        
    @property
    def average(self) -> float:
        """Cannot store the average rating as an attribute as it is dynamical.
        So the property decorator need to be used on a fucntion.
        """
        total = sum([rating.score for rating in self.ratings])  # sum all the ratings
        if len(self.ratings) != 0:  # if not 0
            return total/len(self.ratings)  # divide by the number of them
        return 0    # if 0 ratings; return 0

        
class Movie(Content):
    """Extends content to store movies' metadata."""
    __tablename__ = "movie"
    
    # movie id is mapped to content id
    id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("content.id"), 
        primary_key=True
    )
    duration: orm.Mapped[int] # in minutes
    
    # Mapper to allwo for inheritance
    __mapper_args__ = {
        "polymorphic_identity": "movie"
    }
    
    
class Episode(Content):
    """Store episodes metadata by extending content.
    Has a many to one relationship with series.
    
    On a brief note, a parent class to Episode and Movie (Video) could be consider.
    This could be handy for the addition of video files.
    """
    __tablename__ = "episode"
    
    # episode id is mapped to content id
    id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("content.id"), 
        primary_key=True
    )
    duration: orm.Mapped[int] # in minutes
    season: orm.Mapped[int]  = orm.mapped_column(nullable=False)
    series_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("series.id"))
    series: orm.Mapped[Series] = orm.relationship(
        back_populates="episodes",
        foreign_keys=[series_id]
    )

    # Again the mapper to allow for 
    __mapper_args__ = {
        "polymorphic_identity": "episode"
    }
    
    def __repr__(self) -> str:
        serie_name = self.series.name if self.series else None 
        return super().__repr__()[:-1] + f", series={serie_name!r}, season={self.season})"
    
    def to_dict(self) -> dict:
        return super().to_dict() | {
            "series": self.series.name if self.series else None,
            "season": self.season
        }


class Series(Content):
    """Extends content to store series information.
    One to many relationship to episodes.
    """
    __tablename__ = "series"
    
    # Mapped id
    id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("content.id"), 
        primary_key=True
    )
    episodes: orm.Mapped[List[Episode]] = orm.relationship(
        back_populates="series",
        foreign_keys="[Episode.series_id]",
        cascade="all, delete",  # Episode will be deleted if the series is
        order_by="Episode.id"   # Order for some retireval operations further donw the line
    )
    
    # Mapper to allow for inheritance
    __mapper_args__ = {
        "polymorphic_identity": "serie"
    }
    
    @property
    def duration(self) -> int:
        """Duration depends on the length of the episodes,
        so it needs to be declared as a function wiht the property decorator
        """
        return sum([ep.duration for ep in self.episodes])
            # Dont know if list comprension would be faster, seemingly so

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + f", # of episodes={len(self.episodes)})"
    
    def to_dict(self) -> dict:
        return super().to_dict() | {
            "number_of_episodes": len(self.episodes)
        }


# INDEXES #
    # Add index for performance reasons
content_index = sa.Index("idx_content_name", Content.name)
gender_index = sa.Index("idx_gender_name", Genre.name)


# No reason for this, since I implemented Alembic
#if __name__ == "__main__":
    #Base.metadata.drop_all(ENGINE)
    #Base.metadata.create_all(ENGINE)
    
    #content_index.drop(bind=ENGINE)
    #content_index.create(bind=ENGINE)

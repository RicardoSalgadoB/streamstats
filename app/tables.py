from __future__ import annotations

import os

# Find working with module aliases easier than with individual functions or clasess
from typing import List, Optional
from dotenv import load_dotenv

import sqlalchemy as sa 
import sqlalchemy.orm as orm

load_dotenv()
db_url = os.getenv("DB_URL")
ENGINE = sa.create_engine(db_url)


class Base(orm.DeclarativeBase):
    pass


genre_content_junc = sa.Table(
    "genre_content_junc",
    Base.metadata,
    sa.Column("content_id", sa.ForeignKey("content.id")),
    sa.Column("genre_id", sa.ForeignKey("genre.id")),
)


class Genre(Base):
    __tablename__ = "genre"
    
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(30))
    
    contents: orm.Mapped[List[Content]] = orm.relationship(
        back_populates="genres",
        secondary=genre_content_junc,
    )
    
    def __repr__(self):
        return f"Genre(name={self.name!r})"


class Content(Base):
    __tablename__ = "content"
    
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str]
    type: orm.Mapped[str]
    ratings_total: orm.Mapped[int] = orm.mapped_column(default=0)
    ratings_number: orm.Mapped[int] = orm.mapped_column(default=0)
    
    __mapper_args__ = {
        "polymorphic_identity": "content",
        "polymorphic_on": "type"
    }
    
    genres: orm.Mapped[List[Genre]] = orm.relationship(
        back_populates="contents",
        secondary=genre_content_junc,
    )
    
    def __repr__(self) -> str:
        genres: List[str] = self.get_genres()
        genres_str = ", ".join(genres)
        return (
            f"{self.__class__.__name__}(id={self.id}, name={self.name!r}, " 
            + f"length='{self.length!s} minutes', genre(s)={genres_str!r}, "    
                # length isn't a part of content but of its children
            + f"score average={self.average!r})"
        )
        
    def get_genres(self) -> List[str]:
        genres = [str(genre.name) for genre in self.genres] 
        return genres
    
    @property
    def average(self) -> float:
        if self.ratings_number != 0:
            return self.ratings_total/self.ratings_number
        return 0

        
class Movie(Content):
    __tablename__ = "movie"
    
    id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("content.id"), 
        primary_key=True
    )
    length: orm.Mapped[int] # in minutes
    
    __mapper_args__ = {
        "polymorphic_identity": "movie"
    }
    
    
class Episode(Content):
    __tablename__ = "episode"
    
    id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("content.id"), 
        primary_key=True
    )
    
    # New
    length: orm.Mapped[int] # in minutes
    season: orm.Mapped[int]
    series_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("serie.id"))
    series: orm.Mapped[Serie] = orm.relationship(
        back_populates="episodes",
        foreign_keys=[series_id]
    )

    __mapper_args__ = {
        "polymorphic_identity": "episode"
    }
    
    def __repr__(self) -> str:
        serie_name = self.series.name if self.series else None
            
        return super().__repr__()[:-1] + f", series={serie_name!r}, season={self.season})"


class Serie(Content):
    __tablename__ = "serie"
    
    id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("content.id"), 
        primary_key=True
    )
    
    # New
    episodes: orm.Mapped[List[Episode]] = orm.relationship(
        back_populates="series",
        foreign_keys="[Episode.series_id]",
        cascade="all, delete",
        order_by="Episode.id"
    )
    
    __mapper_args__ = {
        "polymorphic_identity": "serie"
    }
    
    @property
    def length(self) -> int:
        total = 0
        for ep in self.episodes:
            total += ep.length 
        return total

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + f", # of episodes={len(self.episodes)})"


if __name__ == "__main__":
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)

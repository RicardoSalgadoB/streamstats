from __future__ import annotations

import os

from typing import List, Optional
from dotenv import load_dotenv
import sqlalchemy as sa 
import sqlalchemy.orm as orm

load_dotenv()
db_url = os.getenv("DB_URL")
ENGINE = sa.create_engine(db_url)


class Base(orm.DeclarativeBase):
    pass


# TABLES #
genre_content_junc = sa.Table(
    "genre_content_junc",
    Base.metadata,
    sa.Column("content_id", sa.ForeignKey("content.id"), nullable=False),
    sa.Column("genre_id", sa.ForeignKey("genre.id"), nullable=False),
)


class Genre(Base):
    __tablename__ = "genre"
    
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(30), 
        nullable=False, 
        unique=True
    )
    
    contents: orm.Mapped[List[Content]] = orm.relationship(
        back_populates="genres",
        secondary=genre_content_junc,
    )
    
    def __repr__(self) -> str:
        return f"Genre(name={self.name!r})"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "genre": self.name,
        }
    
    
class Rating(Base):
    __tablename__ = "rating"
    
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    score: orm.Mapped[int] = orm.mapped_column(nullable=False)
    content_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("content.id"), 
        nullable=False
    )
    
    content: orm.Mapped[Content] = orm.relationship(back_populates="ratings")
    
    def __repr__(self):
        return f"Rating(score='{self.score}', content_name={self.content.name!r})"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "score": self.score,
            "content": self.content.name
        }


class Content(Base):
    __tablename__ = "content"
    
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(nullable=False)
    type: orm.Mapped[str] = orm.mapped_column(nullable=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "content",
        "polymorphic_on": "type"
    }
    
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
        genres_str = ", ".join(genres)
        return (
            f"{self.__class__.__name__}(id={self.id}, title={self.name!r}, " 
            + f"duration='{self.duration!s} minutes', genre(s)={genres_str!r}, "    
                # length isn't an attribute of content but of its children
            + f"average_rating={self.average!r})"
        )
        
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.name,
            "duration_minutes": self.duration,
            "genre(s)": [str(genre.name) for genre in self.genres],
            "average_rating": self.average
        }
        
    @property
    def average(self) -> float:
        total = sum([rating.score for rating in self.ratings])
        if len(self.ratings) != 0:
            return total/len(self.ratings)
        return 0

        
class Movie(Content):
    __tablename__ = "movie"
    
    id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("content.id"), 
        primary_key=True
    )
    duration: orm.Mapped[int] # in minutes
    
    __mapper_args__ = {
        "polymorphic_identity": "movie"
    }
    
    
class Episode(Content):
    __tablename__ = "episode"
    
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
    __tablename__ = "series"
    
    id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("content.id"), 
        primary_key=True
    )
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
    def duration(self) -> int:
        total = 0
        for ep in self.episodes:
            total += ep.duration 
        return total

    def __repr__(self) -> str:
        return super().__repr__()[:-1] + f", # of episodes={len(self.episodes)})"
    
    def to_dict(self) -> dict:
        return super().to_dict() | {
            "number_of_episodes": len(self.episodes)
        }


# INDEXES #
content_index = sa.Index("idx_content_name", Content.name)


if __name__ == "__main__":
    Base.metadata.drop_all(ENGINE)
    Base.metadata.create_all(ENGINE)
    
    content_index.drop(bind=ENGINE)
    content_index.create(bind=ENGINE)

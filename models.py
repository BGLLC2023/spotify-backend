from typing import Any
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import String, Integer, ForeignKey



class Base(DeclarativeBase):
    pass



class Country(Base):
    __tablename__ = "countries"
    
    country_id: Mapped[int] = mapped_column(Integer, primary_key=True,nullable=False, unique=True, autoincrement=True)
    
    country_name: Mapped[str] = mapped_column(String(255),nullable=False, unique=True)

    spotify_users: Mapped[list["SpotifyUser"]] = relationship(back_populates="country")




class SpotifyUser(Base):
    __tablename__ = "spotify_users"
    
    user_id: Mapped[int] = mapped_column(Integer, primary_key=True,nullable=False, unique=True, autoincrement=True)

    # ondelete cascade means if parent delted then all children are deleted to maintain referential integrity
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("countries.country_id", ondelete="CASCADE"), nullable=True)

    age: Mapped[int] = mapped_column(Integer, nullable=False)
    signup_date: Mapped[str] = mapped_column(String(255), nullable=False)
    subscription_type: Mapped[str] = mapped_column(String(255), nullable=False)
    subscription_status: Mapped[str] = mapped_column(String(255), nullable=False)
    months_inactive: Mapped[int] = mapped_column(Integer, nullable=False)
    inactive_3_months_flag: Mapped[int] = mapped_column(Integer, nullable=False)
    ad_interaction: Mapped[str] = mapped_column(String(3), nullable=False)
    ad_conversion_to_subscription: Mapped[str] = mapped_column(String(3), nullable=False)
    music_suggestion_rating_1_to_5: Mapped[int] = mapped_column(Integer, nullable=False)
    


    avg_listening_hours_per_week: Mapped[float] = mapped_column(nullable=False)
    favorite_genre: Mapped[str] = mapped_column(String(255), nullable=False)

    most_liked_feature: Mapped[str] = mapped_column(String(255), nullable=False)
    desired_future_feature: Mapped[str] = mapped_column(String(255), nullable=False)
    primary_device: Mapped[str] = mapped_column(String(255), nullable=False)
    playlists_created: Mapped[int] = mapped_column(Integer, nullable=False)
    avg_skips_per_day: Mapped[int] = mapped_column(Integer, nullable=False)
    country: Mapped[Country] = relationship("Country", back_populates="spotify_users")






 
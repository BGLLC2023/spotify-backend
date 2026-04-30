from pydantic import BaseModel, EmailStr, Field, ConfigDict





class SpotifyUser(BaseModel):

    country_id: int
    age: int
    signup_date: str
    subscription_type: str
    subscription_status: str
    months_inactive: int
    inactive_3_months_flag: int
    ad_interaction: str
    ad_conversion_to_subscription: str
    music_suggestion_rating_1_to_5: int
    
    avg_listening_hours_per_week: float
    favorite_genre: str

    most_liked_feature: str
    desired_future_feature: str
    primary_device: str
    playlists_created: int
    avg_skips_per_day: int

    model_config = ConfigDict(from_attributes=True)

    


class SpotifyUserCreate(SpotifyUser):
  pass 




class SpotifyUserRead(SpotifyUser):
    user_id: int
    country_id: int
    age: int
    signup_date: str
    subscription_type: str
    subscription_status: str
    months_inactive: int
    inactive_3_months_flag: int
    ad_interaction: str
    ad_conversion_to_subscription: str
    music_suggestion_rating_1_to_5: int
    
    avg_listening_hours_per_week: float
    favorite_genre: str

    most_liked_feature: str
    desired_future_feature: str
    primary_device: str
    playlists_created: int
    avg_skips_per_day: int
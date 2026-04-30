from pydantic import BaseModel, Field,  ConfigDict


class TopGenre(BaseModel):
    country_name: str
    top_genres: dict
    # allows pydantic to read data from sqlalchemy models and convert them to pydantic models
    model_config = ConfigDict(from_attributes=True)



class SubscriptionCount(BaseModel):
    country_name: str
    subscription_counts: dict
    model_config = ConfigDict(from_attributes=True)



class AdConversions(BaseModel):
    country_name: str
    ad_conversion_counts: dict
    model_config = ConfigDict(from_attributes=True)



class DesiredFeatures(BaseModel):
    country_name: str
    desired_features_counts: dict
    model_config = ConfigDict(from_attributes=True)


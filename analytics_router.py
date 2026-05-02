from fastapi import APIRouter, Depends, HTTPException, status
from database import get_async_session
from models import Country, SpotifyUser
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from users_schema.user_schema import SpotifyUserRead, SpotifyUserCreate
from country_schema.country_schema import CountryRead, CountryCreate
from sqlalchemy import func # for aggregate functions like count, sum, avg, etc.
from response_models.response_models import TopGenre, SubscriptionCount, AdConversions, DesiredFeatures



router = APIRouter()

# Decided to make this function to follow the DRY method, I am using the same logic several times
async def get_country(country_id: int, session: AsyncSession):
    country_query = select(Country).where(Country.country_id == country_id)
    country_result = await session.execute(country_query)
    country = country_result.scalar_one_or_none()

    # error handling for if country is not found in db
    if country is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")

    return country


# get top 3 genres based on country search
@router.get("/top-genres/{country_id}", response_model=TopGenre, status_code=status.HTTP_200_OK)
async def top_genres(country_id: int, session: AsyncSession = Depends(get_async_session)):
    # query that returns the country 
    country = await get_country(country_id, session)
    
    # query that returns top 3 genre by country 
    genre_query = select(SpotifyUser.favorite_genre, func.count(SpotifyUser.favorite_genre).label("genre_count")).where(SpotifyUser.country_id == country_id).group_by(SpotifyUser.favorite_genre).order_by(func.count(SpotifyUser.favorite_genre).desc()).limit(3)

    #fetches result by executing the query 
    genre_result = await session.execute(genre_query)
    top_genres = genre_result.all()
    # turns result into a dictionary 
    top_3 = {k: v for k, v in top_genres}
    # returns a dictionary for the response model 
    return {
        "country_name": country.country_name,
        "top_genres": top_3
    }

   # select count(genre) as genre_count, genre from spotify_users where country_id = (select country_id from countries where country_name = 'country_name') group by genre order by genre_count desc limit 3;


@router.get("/subscription-type/{country_id}", response_model=SubscriptionCount, status_code=status.HTTP_200_OK)
async def subscription_count_by_country(country_id: int, session: AsyncSession = Depends(get_async_session)):

    country = await get_country(country_id, session)
    
    query = select(SpotifyUser.subscription_type, func.count(SpotifyUser.subscription_type).label('Subscription_count')).where(SpotifyUser.country_id == country_id).group_by(SpotifyUser.subscription_type).order_by(func.count(SpotifyUser.subscription_type).desc())

    result = await session.execute(query)
    subscription_counts = result.all()

    subscription_counts_dict = {subscription_type: count for subscription_type, count in subscription_counts}

    return {
        "country_name": country.country_name,
        "subscription_counts": subscription_counts_dict
    }





   
# select country_name, count(subscription_type) as subscription_count, subscription_type from spotify_users join countries on spotify_users.country_id = countries.country_id where spotify_users.country_id = 1 group by subscription_type, country_name order by subscription_count desc;

# ad conversion to subscription by country
@router.get("/ad-conversion/{country_id}",response_model=AdConversions, status_code=status.HTTP_200_OK)
async def ad_conversions(country_id: int, session: AsyncSession = Depends(get_async_session)):
    country = await get_country(country_id, session)

    query = select(SpotifyUser.ad_conversion_to_subscription, func.count(SpotifyUser.ad_conversion_to_subscription).label('conversion_count')).where(SpotifyUser.country_id == country_id).group_by(SpotifyUser.ad_conversion_to_subscription).order_by(func.count(SpotifyUser.ad_conversion_to_subscription).desc())
    
    result = await session.execute(query)

    ad_conversion_counts = result.all()

    ad_counversion_dict = {outcome: count for outcome, count in ad_conversion_counts}


    return {
        "country_name": country.country_name,
        "ad_conversion_counts": ad_counversion_dict
    }

# top 3 desired future feature by country

@router.get("/desired-features/{country_id}", response_model=DesiredFeatures, status_code=status.HTTP_200_OK)
async def desired_features(country_id:int, session: AsyncSession = Depends(get_async_session)):
    country = await get_country(country_id, session)

    query = select(SpotifyUser.desired_future_feature, func.count(SpotifyUser.desired_future_feature).label('Desired_feature')).where(SpotifyUser.country_id == country_id).group_by(SpotifyUser.desired_future_feature).order_by(func.count(SpotifyUser.desired_future_feature).desc()).limit(3)

    result = await session.execute(query)

    features = result.all()

    features_dict = {feature: count for feature, count in features}

    return {
        "country_name": country.country_name,
        "desired_features_counts": features_dict
    }




   
# add user -- make sure to do a data check to make sure the countr_id exist 
@router.post("/users", response_model=SpotifyUserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user: SpotifyUserCreate, session: AsyncSession = Depends(get_async_session)):
    new_user = SpotifyUser(**user.model_dump(exclude={"user_id"}))
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user






@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(SpotifyUser).where(SpotifyUser.user_id == user_id)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await session.delete(user)
    await session.commit()





# add country
@router.post("/countries", response_model=CountryRead, status_code=status.HTTP_201_CREATED)
async def create_country(country: CountryCreate, session: AsyncSession =Depends(get_async_session)):
    # country is is excluded because the table auto increments
    new_country = Country(**country.model_dump(exclude={"country_id"}))
    session.add(new_country)
    await session.commit()
    await session.refresh(new_country)

    return new_country










# raw_result = await session.execute(text("SELECT user_id, country_id FROM spotify_users WHERE country_id = 1 LIMIT 5"))
# rows = raw_result.fetchall()
# print(f"Raw SQL result: {rows}")
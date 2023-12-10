import pandas as pd
import psycopg2 as pg
import numpy as np
from datetime import datetime, timezone
from sklearn.model_selection import train_test_split
import random
import pickle
from sklearn.model_selection import KFold
from model_evaluation import *
from xgboost import XGBClassifier


connection_args = {
    'host': 'euw-postgres.onitsoft.com',
    'dbname': 'bot_detector',
    'port': 5432,
    'user': 'postgres',
    'password': 'Os5ef.7Q{8j!?7R'
}

connection = pg.connect(**connection_args)

for i in range(4):
    num_bots = 20 * 1000 * (i + 1)
    print(f"Number of bots {num_bots}")

    bots_df = pd.read_sql(f'SELECT * FROM users where bot = true limit {num_bots}', connection)
    humans_df = pd.read_sql(f'SELECT * FROM users where bot = false limit {2*num_bots}', connection)

    raw_df = pd.concat([bots_df, humans_df])

    raw_df["account_age_days"] = (datetime(year=2022, month=5, day=15, tzinfo=timezone.utc) - raw_df["created_at"]).apply(lambda d: d.days)
    raw_df["average_tweets_per_day"] = raw_df["tweet_count"] / raw_df["account_age_days"]
    raw_df.drop(columns=['id', 'location'], inplace=True)
    raw_df['default_profile_image'] = raw_df['default_profile_image'].astype(int)
    raw_df['pinned_tweet'] = raw_df['pinned_tweet'].astype(int)
    raw_df['protected'] = raw_df['protected'].astype(int)
    raw_df['geo_enabled'] = raw_df['geo_enabled'].astype(int)
    raw_df['verified'] = raw_df['verified'].astype(int)
    raw_df['created_at'] = pd.to_datetime(raw_df['created_at'])
    raw_df['hour_created'] = pd.to_datetime(raw_df['created_at']).dt.hour
    raw_df['bot'] = raw_df['bot'].astype(int)

    df = raw_df[['bot', 'hour_created', 'verified', 'geo_enabled', 'default_profile_image', 'following_count', 'follower_count', 'listed_count', 'pinned_tweet', 'protected', 'description_urls_count', 'description_mentions_count', 'account_age_days', 'average_tweets_per_day']]

    # Interesting features to look at: 
    df['avg_daily_followers'] = np.round(df['follower_count'] / df['account_age_days'])
    df['avg_daily_friends'] = np.round(df['follower_count'] / df['account_age_days'])
    df['avg_daily_favorites'] = np.round(df['follower_count'] / df['account_age_days'])

    # Log transformations for highly skewed data
    df['following_log'] = np.round(np.log(1 + df['following_count']), 3)
    df['follower_log'] = np.round(np.log(1 + df['follower_count']), 3)
    # df['favs_log'] = np.round(np.log(1 + df['favourites_count']), 3)
    df['avg_daily_tweets_log'] = np.round(np.log(1+ df['average_tweets_per_day']), 3)

    # Possible interaction features
    df['network'] = np.round(df['following_log'] * df['follower_log'], 3)
    df['tweet_to_followers'] = np.round(np.log( 1+ df['listed_count']) * np.log(1+ df['follower_count']), 3)

    # Log-transformed daily acquisition metrics for dist. plots
    df['follower_acq_rate'] = np.round(np.log(1 + (df['follower_count'] / df['account_age_days'])), 3)
    df['friends_acq_rate'] = np.round(np.log(1 + (df['following_count'] / df['account_age_days'])), 3)
    df['favs_rate'] = np.round(np.log(1 + (df['following_count'] / df['account_age_days'])), 3)

    features = [
                'verified', 
                'geo_enabled', 
                'protected',
                'pinned_tweet',
                'default_profile_image', 
                'follower_count', 
                'following_count', 
                'listed_count', 
                'average_tweets_per_day',
                'network', 
                'tweet_to_followers', 
                'follower_acq_rate', 
                'friends_acq_rate',
                # 'favs_rate',
                # 'hour_created',
            ]


    X = df[features]
    y = df['bot']

    X, X_test, y, y_test = train_test_split(X, y, test_size=.3, random_state=1234)

    xgb = XGBClassifier(scale_pos_weight=1.8, 
                        tree_method='hist', 
                        learning_rate=0.1,           
                        eta=0.01,                 
                        max_depth=7,                
                        gamma=0.05,
                        n_estimators=200,
                        colsample_bytree=.8
                    )

    model_list = [xgb]

    kf = KFold(n_splits=5, shuffle=True, random_state=33)

    multi_model_eval(model_list, X, y, kf)
    print()
    print()

    with open(f'models/app_detection/xgb_model_{i+6}b.pkl', 'wb') as file:
        pickle.dump(xgb, file)

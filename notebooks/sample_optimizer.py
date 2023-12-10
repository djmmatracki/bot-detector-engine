import numpy as np
import optuna

import sklearn.datasets
import sklearn.metrics
from sklearn.model_selection import train_test_split
import xgboost as xgb
import psycopg2 as pg
from datetime import datetime, timezone
import pandas as pd
import random

connection_args = {
    'host': 'euw-postgres.onitsoft.com',
    'dbname': 'bot_detector',
    'port': 5432,
    'user': 'postgres',
    'password': 'Os5ef.7Q{8j!?7R'
}

connection = pg.connect(**connection_args)  

# bots_df = pd.read_sql(f'SELECT * FROM users where bot = true limit 100000', connection)
# humans_df = pd.read_sql(f'SELECT * FROM users where bot = false limit 200000', connection)

# raw_df = pd.concat([bots_df, humans_df])
raw_df = pd.read_sql(f'SELECT * FROM users', connection)

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
df['avg_daily_followers'] = np.round(df['follower_count'] / df['account_age_days'])
df['avg_daily_friends'] = np.round(df['follower_count'] / df['account_age_days'])
df['avg_daily_favorites'] = np.round(df['follower_count'] / df['account_age_days'])
df['following_log'] = np.round(np.log(1 + df['following_count']), 3)
df['follower_log'] = np.round(np.log(1 + df['follower_count']), 3)
df['avg_daily_tweets_log'] = np.round(np.log(1+ df['average_tweets_per_day']), 3)
df['network'] = np.round(df['following_log'] * df['follower_log'], 3)
df['tweet_to_followers'] = np.round(np.log( 1+ df['listed_count']) * np.log(1+ df['follower_count']), 3)
df['follower_acq_rate'] = np.round(np.log(1 + (df['follower_count'] / df['account_age_days'])), 3)
df['friends_acq_rate'] = np.round(np.log(1 + (df['following_count'] / df['account_age_days'])), 3)
df['favs_rate'] = np.round(np.log(1 + (df['following_count'] / df['account_age_days'])), 3)

print(df.corr()["bot"].abs().sort_values(inplace=False))

features = ['verified', 
            'geo_enabled', 
            'protected',
            'pinned_tweet',
            'default_profile_image', 
            'follower_count', 
            'following_count', 
            'listed_count', 
            'average_tweets_per_day',
            'avg_daily_tweets_log',
            'follower_log',
            'network', 
            'tweet_to_followers', 
            'follower_acq_rate', 
            'following_log', 
            'friends_acq_rate',
            'avg_daily_followers'
            # 'favs_rate',
            # 'hour_created', 
           ]

data = df[features]
target = df['bot']

def objective(trial):
    train_x, valid_x, train_y, valid_y = train_test_split(data, target, test_size=0.25)
    dtrain = xgb.DMatrix(train_x, label=train_y)
    dvalid = xgb.DMatrix(valid_x, label=valid_y)

    param = {
        "verbosity": 0,
        "objective": "binary:logistic",
        # use exact for small dataset.
        "tree_method": "exact",
        # defines booster, gblinear for linear functions.
        "booster": trial.suggest_categorical("booster", ["gbtree", "gblinear", "dart"]),
        # L2 regularization weight.
        "lambda": trial.suggest_float("lambda", 1e-8, 1.0, log=True),
        # L1 regularization weight.
        "alpha": trial.suggest_float("alpha", 1e-8, 1.0, log=True),
        # sampling ratio for training data.
        "subsample": trial.suggest_float("subsample", 0.2, 1.0),
        # sampling according to each tree.
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.2, 1.0),
    }

    if param["booster"] in ["gbtree", "dart"]:
        # maximum depth of the tree, signifies complexity of the tree.
        param["max_depth"] = trial.suggest_int("max_depth", 3, 9, step=2)
        # minimum child weight, larger the term more conservative the tree.
        param["min_child_weight"] = trial.suggest_int("min_child_weight", 2, 10)
        param["eta"] = trial.suggest_float("eta", 1e-8, 1.0, log=True)
        # defines how selective algorithm is.
        param["gamma"] = trial.suggest_float("gamma", 1e-8, 1.0, log=True)
        param["grow_policy"] = trial.suggest_categorical("grow_policy", ["depthwise", "lossguide"])

    if param["booster"] == "dart":
        param["sample_type"] = trial.suggest_categorical("sample_type", ["uniform", "weighted"])
        param["normalize_type"] = trial.suggest_categorical("normalize_type", ["tree", "forest"])
        param["rate_drop"] = trial.suggest_float("rate_drop", 1e-8, 1.0, log=True)
        param["skip_drop"] = trial.suggest_float("skip_drop", 1e-8, 1.0, log=True)

    bst = xgb.train(param, dtrain)
    preds = bst.predict(dvalid)
    pred_labels = np.rint(preds)
    accuracy = sklearn.metrics.accuracy_score(valid_y, pred_labels)
    return accuracy


if __name__ == "__main__":
    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=100, timeout=600)

    print("Number of finished trials: ", len(study.trials))
    print("Best trial:")
    trial = study.best_trial

    print("  Value: {}".format(trial.value))
    print("  Params: ")
    for key, value in trial.params.items():
        print("    {}: {}".format(key, value))

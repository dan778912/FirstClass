import os

import pymongo as pm

LOCAL = "0"
CLOUD = "1"

GAME_DB = 'gamesDB'

client = None

MONGO_ID = '_id'


def connect_db():
    """
    This provides a uniform way to connect to the DB across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    We should probably either return a client OR set a
    client global.
    """
    global client
    if client is None:  # not connected yet!
        print("Setting client because it is None.")
        if os.environ.get("CLOUD_MONGO", LOCAL) == CLOUD:
            username = os.environ.get("GAME_MONGO_USER")
            # username = 'zcd'
            password = os.environ.get("GAME_MONGO_PW")
            # password = 'swefall24'
            cluster_url = os.environ.get("GAME_MONGO_URL")
            # cluster_url = 'swe24.8te4n.mongodb.net'
            if not username or not password or not cluster_url:
                raise ValueError('You must set your credentials '
                                 + 'to use Mongo in the cloud.')
            print("Connecting to Mongo in the cloud.")
            client = pm.MongoClient(f'mongodb+srv://{username}:{password}'
                                    + f'@{cluster_url}'
                                    + '/gamesDB?retryWrites=true&w=majority')
        else:
            print("Connecting to Mongo locally.")
            client = pm.MongoClient()
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected!")
            return client
        except Exception as e:
            print(e)
        return None


def convert_mongo_id(doc: dict):
    if MONGO_ID in doc:
        # Convert mongo ID to a string so it works as JSON
        doc[MONGO_ID] = str(doc[MONGO_ID])


def create(collection, doc, db=GAME_DB):
    """
    Insert a single doc into collection.
    """
    print(f'{db=}')
    result = client[db][collection].insert_one(doc)
    return str(result.inserted_id)


def read_one(collection, filt, db=GAME_DB):
    """
    Find with a filter and return on the first doc found.
    Return None if not found.
    """
    for doc in client[db][collection].find(filt):
        convert_mongo_id(doc)
        return doc


def delete(collection, filt, db=GAME_DB):
    """
    Find with a filter and return on the first doc found.
    """
    print(f'{filt=}')
    del_result = client[db][collection].delete_one(filt)
    return del_result.deleted_count


def update(collection, filters, update_dict, db=GAME_DB):
    """
    Update an entry
    Args:
        collection: collection to update in
        filters: filter for documents to update
        update_dict: update dictionary for the document
        db: database name (default: GAME_DB)
    Returns:
        UpdateResult from MongoDB
    """
    result = client[db][collection].update_one(filters, {'$set': update_dict})
    return result


def fetch_all(collection, db=GAME_DB):
    ret = []
    for doc in client[db][collection].find():
        ret.append(doc)
    return ret


def fetch_all_as_dict(key, collection, db=GAME_DB):
    ret = {}
    for doc in client[db][collection].find():
        del doc[MONGO_ID]
        ret[doc[key]] = doc
    return ret


def read(collection, db=GAME_DB, no_id=True) -> list:
    """
    Return all documents in the collection as a list.
    Optionally remove the `_id` field from each document.
    """
    ret = []
    for doc in client[db][collection].find():
        if no_id:
            del doc[MONGO_ID]
        ret.append(doc)
    return ret


def read_dict(collection, key, db=GAME_DB, no_id=True) -> dict:
    """
    Return all documents in the collection as a dictionary,
    keyed by a specific field.
    Optionally remove the `_id` field from each document.
    """
    recs = read(collection, db=db, no_id=no_id)
    recs_as_dict = {}
    for rec in recs:
        if no_id and MONGO_ID in rec:
            del rec[MONGO_ID]
        recs_as_dict[rec[key]] = rec
    return recs_as_dict


if __name__ == "__main__":
    print(connect_db())
    print("Database connected.")

import sys
import os
from timeit import timeit as timer
import multiprocessing as mp
import pymongo.errors as mongo_error
import pandas as pd
from loguru import logger
from pymongo import MongoClient


"""
Hey Cody,
I put all the relevant code into a single file, so that way you don't have to hop around.
I am attempting an implementation of the producer/consumer design pattern.

In the producer/consumer pattern a producer function puts something in a queue
and a consumer takes it out of the queue.

This is the blog post I am basing my code on:
https://stonesoupprogramming.com/2017/09/11/python-multiprocessing-producer-consumer-pattern/

It looks like my producer is never handing off to my consumer. I have annotated everything.

My if __name__ == '__main__': function is a little weird, but that's because it's built to time the operation.

I have included an alternative implementation that just calls the function.

I am also getting this warning "UserWarning: MongoClient opened before fork. Create MongoClient only after forking. See PyMongo's documentation for details:"
which I have no idea how to resolve (I've read the documentation).
"""


class MongoDBConnection:
    """Class for connecting to a Mongo DB"""
    def __init__(self, host='127.0.0.1', port=27017, maxPoolSize=200):
        """instantiates the connection"""
        self.host = host
        self.port = port
        self.maxPoolSize = maxPoolSize
        self.connection = None # MongoClient(self.host, self.port)

    def __enter__(self):
        """Activates the connection"""
        self.connection = MongoClient(self.host, self.port, maxPoolSize=self.maxPoolSize)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the connection"""
        self.connection.close()


class UserCollection():
    '''
    Contains a collection of Users objects
    '''

    @logger.catch()
    def __init__(self, collection):
        self.database = collection['users']

    @logger.catch()
    def purge_user_collection(self):
        self.database.drop()
        # logger.info('Purged Status Collection')
        return True


    @logger.catch
    def add_csv_in_chunks_producer(self,filename, queue, lock, size=10):
        '''
        I am attempting to use a producer/consumer pattern. This is the producer
        '''
        # chunk_number = 0
        for chunk in pd.read_csv(filename, chunksize=size, iterator=True):
            # print(f"CHUNK {chunk_number}")
            fieldnames = ['_id', 'email', 'user_name', 'user_last_name']
            chunk_list = []
            with lock:
                for index, row in chunk.iterrows():
                    row_dict = {fieldnames[0]: row['USER_ID'], fieldnames[1]: row['EMAIL'], fieldnames[2]: row['NAME'],
                                fieldnames[3]: row['LASTNAME']}
                    chunk_list.append(row_dict)
                    queue.put(chunk_list)
                # print('producer loop complete')
            return True

    @logger.catch
    def bulk_write_consumer(self, queue, lock):
        """I am attempting a producer/consumer design pattern. This is the consumer.
        This is the part that doesn't work
        """
        with lock:
            # while True:
            # try:
            item = queue.get()
            self.database.insert_many(item)
            # print('consumer loop complete')
            return True
            """It throws a mongo_error.AutoReconnect"""
            # except mongo_error.AutoReconnect:
            #     pass


@logger.catch
def multi_process_load_users(user_collection, size):
    """Uses multi-processing to add users"""
    queue = mp.Queue()
    # print('queued')
    lock = mp.Lock()
    # print('locked')
    producers = []
    # print('producers list instantiated')
    consumers = []
    # print('consumer list instantiated')
    for i in range(mp.cpu_count()):
        # this adds producer objects to a list
        producers.append(mp.Process(target=user_collection.add_csv_in_chunks_producer,
                                    args=('accounts.csv', queue, lock, size,)))

    for i in range(mp.cpu_count()):
        #This ads consumer objects to a list
        cons = mp.Process(target=user_collection.bulk_write_consumer, args=(queue, lock,))
        cons.daemon = True
        # print(cons)
        consumers.append(cons)

    for producer in producers:
        # starts our producers
        producer.start()
        print('Producer started')

    for consumer in consumers:
        # starts our consumers
        consumer.start()
        print(consumer)
        print('Consumer started')

    for producer in producers:
        # joins our producers
        producer.join()
        print('Producer joined')


def init_user_collection(collection):
    '''
    Creates and returns a new instance
    of UserCollection
    '''
    return UserCollection(collection)

def load_users_multi_processing_timing():
    """times multiprocessing"""
    user_collection.purge_user_collection()
    multi_process_load_users(user_collection, size=10)

function_list = ['load_users_multi_processing_timing()']
REPETITIONS = 1
if __name__ == '__main__':
    with open('multi-processing-mongo.txt', 'w') as out:
        mongo = MongoDBConnection()
        with mongo:
            database = mongo.connection.social_media
            user_collection = init_user_collection(database)
            user_collection.purge_user_collection()
            original_stdout = sys.stdout
            for function in function_list:
                sys.stdout = out
                print(function[0:-9])
                print(timer(function,
                      globals=globals(),
                      number=REPETITIONS)
                      )
                print('\n')
                sys.stdout = original_stdout
                print(f'{function} completed')
'''
Classes for user information for the
social network project
'''
# pylint: disable=R0903
from loguru import logger
import peewee as pw
import socialnetwork_model as model


class Users:
    '''
    Contains user information
    '''

    @logger.catch()
    def __init__(self, user_id, email, user_name, user_last_name):
        self.user_id = user_id
        self.email = email
        self.user_name = user_name
        self.user_last_name = user_last_name


class UserCollection:
    '''
    Contains a collection of Users objects
    '''

    @logger.catch()
    def __init__(self):
        self.database = model.db
        logger.info(f'User database {self.database} created')

    @logger.catch()
    def add_user(self, user_id, email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        # new_user = Users(user_id, email, user_name, user_last_name)
        with self.database.transaction():
            try:
                new_user_db = model.Users.create(
                    user_id=user_id
                    , email=email
                    , user_name=user_name
                    , user_last_name=user_last_name
                )
                new_user_db.save()
                logger.info(f'User {user_id} added')
                return True
            except pw.IntegrityError:
                logger.info(f'Duplication attempt of {user_id}')
                return False


    @logger.catch()
    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        with self.database.transaction():
            try:
                modify_target = model.User.get(user_id)
                modify_target.user_id = user_id
                modify_target.email = email
                modify_target.username = user_name
                modify_target.user_last_name = user_last_name
                modify_target.save()
                logger.info(f'User {user_id} modified')
                return True
            except pw.DoesNotExist:
                logger.info(f'user id : {user_id} not in database to modify')
                return False

    @logger.catch()
    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        # if user_id not in self.database:
        #     logger.info(f'user id : {user_id} not in database to delete')
        #     return False
        # del self.database[user_id]
        # logger.info(f'User {user_id} deleted')
        # return True
        with self.database.transaction():
            try:
                delete_target = model.Users.get(user_id)
                delete_target.delete()
                delete_target.save()
                logger.info(f'User {user_id} deleted')
                #delete all statuses from that user
                model.Statuses.delete().where(model.Status.user_id == user_id).execute()
                return True
            except pw.DoesNotExist:
                logger.info(f'user id : {user_id} not in database to delete')
                return False

    @logger.catch()
    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        # if user_id not in self.database:
        #     logger.info(f'user id : {user_id} not in database')
        #     return Users(None, None, None, None)
        # logger.info(f'User {user_id} searched for')
        # return self.database[user_id]
        with self.database.transaction():
            try:
                search_target = model.Users.get(user_id)
                logger.info(f'User {user_id} searched for')
                return search_target

            except pw.DoesNotExist:
                logger.info(f'user id : {user_id} not in database')
                return Users(None, None, None, None)

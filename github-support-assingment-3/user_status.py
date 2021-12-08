# pylint: disable=R0903
# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
from loguru import logger
import peewee as pw
import socialnetwork_model as model

#splorf

class UserStatus():
    @logger.catch()
    def __init__(self, status_id, user_id, status_text):
        self.status_id = status_id
        self.user_id = user_id
        self.status_text = status_text


class UserStatusCollection():
    @logger.catch()
    def __init__(self):
        # Needed for the context manager
        self.database = model.db

    @logger.catch()
    def add_status(self, status_id, user_id, status_text):
        new_status = UserStatus(status_id, user_id, status_text)
        with self.database.transaction():
            try:
                new_status_db = model.Status.create(
                    status_id=new_status.status_id
                    , user_id=new_status.user_id
                    , status_text=new_status.status_text
                )
                new_status_db.save()
                logger.info(f'Status {status_id} added')
                return True
            except pw.IntegrityError:
                logger.info(f'status id : {status_id} already in database')
                return False


    @logger.catch()
    def modify_status(self, status_id, user_id, status_text):
        with self.database.transaction():
            try:
                modify_target = model.Status.get(status_id)
                modify_target.user_id = user_id
                modify_target.status_text = status_text
                modify_target.save()
                logger.info(f'Status {status_id} changed')
                return True
            except pw.DoesNotExist:
                logger.info(f'status id : {status_id} not in database to modify')
                return False

    @logger.catch()
    def delete_status(self, status_id):
        with self.database.transaction():
            try:
                delete_target = model.Status.get(status_id)
                delete_target.delete()
                delete_target.save()
                logger.info(f'Status {status_id} deleted')
                return True
            except pw.DoesNotExist:
                logger.info(f'status id : {status_id} not in database to delete')
                return False


    @logger.catch()
    def search_status(self, status_id):
        with self.database.transaction():
            try:
                search_target = model.Status.get(status_id)
                logger.info(f'Status {status_id} searched for')
                return search_target

            except pw.DoesNotExist:
                logger.info(f'status id : {status_id} not in database')
                return UserStatus(None, None, None)


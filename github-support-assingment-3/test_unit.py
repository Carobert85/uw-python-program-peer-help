import pytest
from unittest import mock
from mock import patch
from loguru import logger

import users
from users import Users
from users import UserCollection
from user_status import UserStatus
from user_status import UserStatusCollection
import socialnetwork_model

socialnetwork_model.main()

def test_add_user_success():
    """Tests adding a user"""
    test_user_collection = UserCollection()
    assert test_user_collection.add_user(user_id='007'
                                        , email='Bond@uk.gov'
                                        , user_name='James'
                                        , user_last_name='Bond') is True


def test_add_status_success():
    """Tests adding a status"""
    test_status_collection = UserStatusCollection()
    assert test_status_collection.add_status(status_id='001'
                                             , user_id='007'
                                             , status_text=
                                             'Won a poker tournament') is True

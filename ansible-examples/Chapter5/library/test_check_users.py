from nose.tools import *
import imp
imp.load_source("check_users","./check_users")
from check_users import User

def test_check_user():
    chkusr = User("ec2-user")
    success, ret_msg = chkusr.check_if_user_exists()
    assert_true(success)
    assert_equals('User ec2-user exists', ret_msg)

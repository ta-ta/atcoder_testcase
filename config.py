import os

import termcolor

COOKIE = os.path.join(os.environ['ATCODER_TESTCASE'], '.atcoder_cookie')

LOGGER = 'testcases'

IN = 'in'
OUT = 'out'
RESULT_FILE = 'result.out'

AC_MESSAGE = termcolor.colored('AC', 'green', attrs=['bold'])
WA_MESSAGE = termcolor.colored('WA', 'red', attrs=['bold'])
TLE_MESSAGE = termcolor.colored('TLE', 'yellow', attrs=['bold'])
WJ_MESSAGE = termcolor.colored('Waiting for Judge', 'green', attrs=['bold'])

TEST_TIMEOUT = 10
AC_TIMEOUT = 2

ATCODER = 'https://atcoder.jp'
LOGIN_URL = ATCODER + '/login'
LOGOUT_URL = ATCODER + '/logout'

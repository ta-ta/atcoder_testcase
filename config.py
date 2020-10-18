import os

import termcolor


# dir
TESTCASES = os.path.join(os.environ['HOME'], 'atcoder_testcase', 'testcases')
COOKIE = os.path.join(os.environ['ATCODER_TESTCASE'], '.atcoder_cookie')

# file extension
IN = 'in'
OUT = 'out'
RESULT = 'result'

# status
AC = 'AC'
WA = 'WA'
TLE = 'TLE'

AC_MESSAGE = termcolor.colored(AC, 'green', attrs=['bold'])
WA_MESSAGE = termcolor.colored(WA, 'red', attrs=['bold'])
TLE_MESSAGE = termcolor.colored(TLE, 'yellow', attrs=['bold'])
WJ_MESSAGE = termcolor.colored('Waiting for Judge', 'green', attrs=['bold'])

# execution time
TEST_TIMEOUT = 10
AC_TIMEOUT = 2

# atcoder url
ATCODER = 'https://atcoder.jp'
LOGIN_URL = ATCODER + '/login'
LOGOUT_URL = ATCODER + '/logout'

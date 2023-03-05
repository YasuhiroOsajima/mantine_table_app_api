import sys
from util import get_password_hash


if __name__ == "__main__":
    passwd = sys.argv[1]
    result = get_password_hash(passwd)

    print(result)

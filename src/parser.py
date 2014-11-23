import os
import sys
import loadimpact
import config_manager


def main():
    c = config_manager.config_mgr()
    c.print_config()


if __name__ == '__main__':
    main()
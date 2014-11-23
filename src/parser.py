import os
import sys
import loadimpact
import config_manager
import user_scenario_manager


def main():
    c = config_manager.config_mgr()
    c.print_config()
    path = "%s/target/tmp.txt" % (config_manager.PARENT_DIR)
    usm = user_scenario_manager.usr_scenario_mgr(path, c, 2)
    print usm


if __name__ == '__main__':
    main()
import os
import sys
import loadimpact
import time
import config_manager
import client_manager
import user_scenario_manager


def main():
    c = config_manager.config_mgr()
    c.print_config()
    path = "%s/target/tmp.txt" % (config_manager.PARENT_DIR)
    usm = user_scenario_manager.usr_scenario_mgr(path, c, 2)
    loadscript = open(path, "r").read()
    client = client_manager.get_client('my')
    print client
    name = "Test-%s" % time.time()
    user_scenario = client.create_user_scenario({
        'name' : name,
        'load_script':loadscript
    })
    client_manager.validate_user_scenario(user_scenario)

if __name__ == '__main__':
    main()
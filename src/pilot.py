import time
import config_manager
import client_manager
import user_scenario_manager

def main():
    user = 'my'
    c = config_manager.config_mgr(user) #Can be instantiated with a FilePath.
    c.print_config()
    path = "%s/target/tmp.txt" % (config_manager.PARENT_DIR)
    usm = user_scenario_manager.usr_scenario_mgr(path, c, 2)
    loadscript = open(path, "r").read()
    client = client_manager.get_client(c.token)
    name = "UserScenario-%s" % time.time()
    user_scenario = client.create_user_scenario({
        'name' : name,
        'load_script':loadscript
    })
    print user_scenario
    client_manager.validate_user_scenario(user_scenario)
    code = client_manager.test_scenario_upload(c, client, [user_scenario])
    if code is 201:
        print "Test Scenario Created"

if __name__ == '__main__':
    main()
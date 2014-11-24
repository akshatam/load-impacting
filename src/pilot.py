import time
import config_manager
import client_manager
import user_scenario_manager

def main():
    c = config_manager.config_mgr() #Can be instantiated with a FilePath.
    c.print_config()
    path = "%s/target/tmp.txt" % (config_manager.PARENT_DIR)
    usm = user_scenario_manager.usr_scenario_mgr(path, c, 2)
    loadscript = open(path, "r").read()
    client = client_manager.get_client('my')
    name = "UserScenario-%s" % time.time()
    user_scenario = client.create_user_scenario({
        'name' : name,
        'load_script':loadscript
    })
    print user_scenario
    client_manager.validate_user_scenario(user_scenario)
    tc = client_manager.test_scenario_upload(c, client, [user_scenario])
    if tc is None:
        print "Couldn't Create the Test Scenario.."

if __name__ == '__main__':
    main()
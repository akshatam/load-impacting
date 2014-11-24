__author__ = 'Amar'

import config_manager
import client_manager
import time

SAMPLER_METHODS = ['GET','POST']

def test_config():
    c = config_manager.config_mgr()
    assert (c.num_threads == 50), "ParseError, Incorrect Thread Numbers"
    assert (c.ramp_time == 60), "ParseError, Incorrect Ramp Time"
    assert (c.httpsampler_concurrent_pool == 4), "ParseEror, Incorrect Concurrent Pool"
    for i in c.http_sampler_proxies:
        assert (i.method in SAMPLER_METHODS), "ConfigError, Invalid Method"

def test_usn_creation():
    load_script = """
    local response = http.get("http://example.com')
    log.info("Load time: "..response.total_load_time.."s")
    client.sleep(5)
    """
    client = client_manager.get_client('my')
    name = "TestUserScenario-%s" % time.time()
    user_scenario = client.create_user_scenario({
        'name' : name,
        'load_script': load_script
    })
    assert (user_scenario.id > 0), "UserScenarioCreationError, Invalid ID obtained"
    user_scenario.delete_with_id(client, user_scenario.id)


def main():
    print "Initiating Test Suite..."
    try:
        test_config()
        test_usn_creation()
    except Exception as e:
        print "One of the tests failed " + e.message


if __name__ == '__main__':
    main()
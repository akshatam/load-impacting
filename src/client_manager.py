__author__ = 'Amar'
import config_manager
import user_scenario_manager
import time
import loadimpact
import os

def get_client(name):
    tokfile = "%s/resources/tokens/%s.token" % (config_manager.PARENT_DIR, name)
    if not os.path.isfile(tokfile):
        raise('File Not Found')
    token = open(tokfile, "r").read()
    client = client = loadimpact.ApiTokenClient(api_token=token)
    return client

def validate_user_scenario(user_scenario):
    print "Starting Validation..."
    validation = user_scenario.validate()
    stream = validation.result_stream()
    for result in stream:
        if 'stack_trace' in result:
            print('[%s]: %s @ line %s'
                  % (result['timestamp'], result['message'],
                    result['line_number']))
            print('Stack trace:')
            for filename, line, function in result['stack_trace']:
                print('\t%s:%s in %s' % (function, line, filename))
        else:
            print('[%s]: %s' % (result['timestamp'], result['message']))
        print("Validation completed with status '%s'"
              % (loadimpact.UserScenarioValidation.status_code_to_text(validation.status)))
    print "Validation Ends..."

def test_scenario_upload(config, client, user_scenarios, loadzone=loadimpact.LoadZone.AMAZON_JP_TOKYO):
    name = "TestConfig-%s" % time.time()
    url = "http://%s" % config.master_httpsampler_domain
    load_schedule = [{"users": config.num_threads, "duration": config.ramp_time}]
    usns = []
    for usn in user_scenarios:
        a = {"user_scenario_id":usn.id, "percent":100}
        usns.append(a)

    ldzone = loadimpact.LoadZone.name_to_id(loadzone)
    tracks = [{
        "clips" : usns,
        "loadzone":ldzone,
    }]
    config1 = None
    try:
        config1 = client.create_test_config({
            'name': 'Amartest_configuration',
            'url': 'http://test.loadimpact.com/',
            'config': {
                "load_schedule": [{"users": 10, "duration": 10}],
                "tracks": [{
                    "clips": [{
                        "user_scenario_id": user_scenarios[0].id, "percent": 100
                        }],
                    "loadzone": loadimpact.LoadZone.name_to_id(loadzone)
                    }]
                }
            })
    except loadimpact.exceptions.ClientError as e:
        print e.response, e.message, e.args

    return config1


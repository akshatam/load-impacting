__author__ = 'Amar'
import config_manager
import time
import loadimpact


TESTURL = 'https://api.loadimpact.com/v2/test-configs'

def get_client(token):
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
    usns = []
    for usn in user_scenarios:
        a = {"user_scenario_id":usn.id, "percent":100}
        usns.append(a)

    config1 = None
    config.master_httpsampler_domain = "http://"+config.master_httpsampler_domain + "/"

    data_map = {
        "config": {
            "load_schedule": [
                {
                    "duration": 2,
                    "users": 5
                }
            ],
            "tracks": [
                {
                    "clips": usns,
                    "loadzone": loadzone
                }
            ],
            "user_type": "sbu"
        },
        "name": name,
        "url": url
    }
    import json, requests
    data = json.dumps(data_map)
    r = requests.post(TESTURL, data, auth=(config.token, ''))

    print r.json
    return r.status_code
__author__ = 'Amar'
import config_manager
import user_scenario_manager
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

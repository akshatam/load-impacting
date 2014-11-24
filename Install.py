__author__ = 'Amar'
import os
import platform
import pip
import subprocess
import sys
from zipfile import ZipFile

NUMBER_OF_ESSENTIAL_PKGS = 2
PARENT_DIR = os.getcwd()


def main(argv):
    system = platform.system()
    all_packages = pip.get_installed_distributions()
    req_pkg_found = 0
    for pkg in all_packages:
        if 'loadimpact' in str(pkg) or 'requests' in str(pkg):
            req_pkg_found += 1

    if not os.path.isdir("%s/target" % PARENT_DIR):
        os.makedirs("%s/target" % PARENT_DIR)

    print "Installing Credential File...my.token"
    password = None
    if argv[1] == "--password":
        password = argv[2]

    print password
    if password is None:
        print "Enter the Password.."
        password = raw_input()
    try:
        if os.path.isfile('my.token'):
            os.remove('my.token')
        with ZipFile('my.zip') as zf:
            zf.extractall(pwd=password)
        os.remove("%s/resources/tokens/my.token" % PARENT_DIR)
        os.rename('my.token', "%s/resources/tokens/my.token" % PARENT_DIR)
    except Exception as e:
        print e
        print "Hint: Ask Password."
        sys.exit(-1)
    assert(req_pkg_found == NUMBER_OF_ESSENTIAL_PKGS), "You must have loadimpact SDK and requests."
    assert(os.path.isdir("%s/src" % PARENT_DIR)), "Should be run from Project Root"
    test_config_file = "%s/resources/jmeter_test.xml" % PARENT_DIR
    assert(os.path.isfile(test_config_file)), "Can't Find Test JMETER Config file at %s" % test_config_file
    test_token_file = "%s/resources/tokens/my.token" % PARENT_DIR
    assert(os.path.isfile(test_token_file)), "Can't Find Test Token File at %s" % test_token_file
    print "Now attempting the Test"
    try:
        ret = subprocess.call(["python", "%s/src/test.py" % PARENT_DIR])
        assert(ret == 0), "Tests Failed."
    except Exception as e:
        print "Failure " + e.message
        sys.exit(-1)

    print "ALL Tests PASSED, Feel free to use the system, %s/src/pilot.py can be used as reference..." % PARENT_DIR

if __name__ == '__main__':
    main(sys.argv)
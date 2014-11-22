import os
import sys
import loadimpact
import xml.etree.ElementTree as ET


def main():
    PARENT_DIR = os.getcwd()
    if not os.path.isdir("%s/src" % (PARENT_DIR)):
        print "Run from Project Root."
        os.chdir(os.path.abspath(os.path.join(PARENT_DIR, os.pardir)))
        PARENT_DIR = os.getcwd()

    print "Parent DIR is %s" % (PARENT_DIR)

    RESOURCES_DIR = "%s/resources" % (PARENT_DIR)
    try:
        tree = ET.parse("%s/jmeter_test.xml" % (RESOURCES_DIR))
        root = tree.getroot()
        ele = root.iter('ThreadGroup').next()
        name = ele.attrib['testname']
        print name
        for a in ele.iter('strinProp'):
            print a

        for conf in root.iter('stringProp'):
            a = conf.get('name')
            print a
            print conf.text

    except Exception as e:
        print e


if __name__ == '__main__':
    main()
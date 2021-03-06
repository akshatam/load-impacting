__author__ = 'Amar'

import os
import xml.etree.ElementTree as ET

PARENT_DIR = os.getcwd()
if not os.path.isdir("%s/src" % (PARENT_DIR)):
    print "Run from Project Root."
    os.chdir(os.path.abspath(os.path.join(PARENT_DIR, os.pardir)))
    PARENT_DIR = os.getcwd()

class http_sampler_proxy(object):
    def __init__(self, path, method, domain, map={}):
        self.path = path
        self.method = method
        self.domain = domain
        self.header_map = map

class config_mgr(object):
    def __init__(self, user, filename=None):
        if filename == None:
            print "Using Default config JMX file"
            filename = "%s/resources/jmeter_test.xml" % (PARENT_DIR)

        self.filename = filename

        try:
            tree = ET.parse(self.filename)
            root = tree.getroot()
            ele = root.iter('ThreadGroup').next()
            self.testname = ele.attrib['testname']

            tokfile = "%s/resources/tokens/%s.token" % (PARENT_DIR, user)
            if not os.path.isfile(tokfile):
                raise("%s: File Not Found" % (tokfile))
            token = open(tokfile, "r").read()
            self.token = token

            for conf in root.iter('stringProp'):
                a = conf.get('name')
                txt = conf.text
                if a == 'ThreadGroup.num_threads':
                    self.num_threads = int(txt)
                elif a == 'ThreadGroup.ramp_time':
                    self.ramp_time = int(txt)
                else:
                    pass

            configele = root.iter('ConfigTestElement').next()
            for conf in configele.iter('stringProp'):
                a = conf.get('name')
                txt = conf.text
                if a == 'HTTPSampler.domain':
                    self.master_httpsampler_domain = txt
                elif a == 'HTTPSampler.concurrentPool':
                    self.httpsampler_concurrent_pool = int(txt)
                else:
                    pass

            self.http_sampler_proxies = []
            for conf in root.iter('HTTPSamplerProxy'):
                path = None
                method = None
                domain = None
                for str in conf.iter('stringProp'):
                    if str.get('name') == 'HTTPSampler.path':
                        path = str.text
                    elif str.get('name') == 'HTTPSampler.method':
                        method = str.text
                    if str.get('name') == 'HTTPSampler.domain':
                        domain = str.text

                if domain is None:
                    domain = self.master_httpsampler_domain

                hsp = http_sampler_proxy(path, method, domain)
                self.http_sampler_proxies.append(hsp)

            hdr_count = 0
            for conf in root.iter('HeaderManager'):
                map = {}
                for ele in conf.iter('elementProp'):
                    key = None
                    val = None
                    for str in ele.iter('stringProp'):
                        if str.get('name') == 'Header.name':
                            key = str.text
                        elif str.get('name') == 'Header.value':
                            val = str.text
                        else:
                            pass
                    map[key] = val

                if hdr_count < len(self.http_sampler_proxies):
                    self.http_sampler_proxies[hdr_count].map = map

                hdr_count += 1

        except Exception as e:
            print e

    def print_config(self):
        print "ThreadGroup.num_threads:"    + str(self.num_threads)
        print "ThreadGroup.ramp_time:"      + str(self.ramp_time)
        print "ThreadGroup.domain:"         + str(self.master_httpsampler_domain)
        print "ThreadGroup.concurrent_pool" + str(self.httpsampler_concurrent_pool)

        for i in self.http_sampler_proxies:
            print "HTTP Sampler Path:"   + i.path
            print "HTTP Sampler Method:" + i.method
            print "Header Map " + str(i.map)

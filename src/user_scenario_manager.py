__author__ = 'Amar'

import loadimpact
import os
import config_manager

class usr_scenario_mgr(object):
    def __init__(self, path, configuration, batch_size=2):
        self.file = None
        try:
            self.file = open(path, "w")
            batch_size_counter = 1
            self.file.write("http.request_batch({\n")
            for idx, sp in enumerate(configuration.http_sampler_proxies):
                headers = "{"
                h_count = 0
                for key in sp.map.keys():
                    if h_count != 0:
                        headers = headers + ","

                    headers = headers + "[\"%s\"]=\"%s\"" % (key, sp.map[key])
                    h_count += 1

                headers = headers + "}"

                self.file.write("\t{\"%s\", \"%s/%s\", %s\n" % (sp.method, sp.domain, sp.path, headers))
                if batch_size_counter == batch_size:
                    self.file.write("}),\n")
                    if idx != len(configuration.http_sampler_proxies):
                        self.file.write("http.request_batch({\n")
                    batch_size_counter = 0

                if batch_size_counter != batch_size and idx == len(configuration.http_sampler_proxies) - 1:
                    self.file.write("}),\n")


                batch_size_counter += 1

        except Exception as e:
            print e


    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file != None:
            self.file.close()


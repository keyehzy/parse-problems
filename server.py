#!/usr/bin/env python
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import os
from time import time

sol_name = "a.exe"

class Parse:
    def __init__(self, body):
        self.body = json.loads(body)
        self.name = self.body['name']
        self.memoryLimit = self.body['memoryLimit']
        self.timeLimit = self.body['timeLimit']
        self.tests = Test(self.name)
        for test in self.body['tests']:
            self.tests.add_input_output(test['input'].strip(), test['output'].strip())

    def analyze_result(self):
        results, onTime = self.get_results()
        if not onTime:
            print("Time exceeded limit!")
            return
        for r in results:
            if self.tests.tests[r[0]] == r[1]:
                print(self.tests.tests[r[0]], r[1], "OK")
            else:
                print(self.tests.tests[r[0]], r[1], "WA")
                return
        print("AC")
        return

    def get_results(self):
        results = []
        onTime = True
        if os.path.isfile(sol_name):
            for test in self.tests.tests.keys():
                #print(test)
                process, run_time = self.run(test)
                results.append([test, process.stdout.decode('utf-8').strip()])
                #if run_time > self.timeLimit:
                print(run_time)
        else:
            print("File " + sol_name + " not found")
        return results, onTime

    def run(self, test):
        t = time()
        process = subprocess.run(['a.exe'], stdout=subprocess.PIPE, input=test.encode('utf-8'))
        return process, time() - t

class Test:
    def __init__(self, name):
        self.name = name
        self.tests = {}

    def add_input_output(self, input, output):
        self.tests[input] = output


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        parse = Parse(body)
        parse.analyze_result()


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 4244), Handler)
    httpd.serve_forever()

import sys
import socket
import requests
import platform
import subprocess

class actions(object):
    def __init__(self,):
        self.dists = {'redhat':'rpm -qa','amazon linux':'rpm -qa',
        'ubuntu':"dpkg-query -W -f='${Package} ${Version} ${Architecture}\n'",
        'debian':"dpkg-query -W -f='${Package} ${Version} ${Architecture}\n'",'centos':'rpm -qa',
        'fedora':'rpm -qa','oraclelinux':'rpm -qa'}

    def analyze(self,):
        self.getDist()
        if self.dist in self.dists:
            self.cmd = self.dists[self.dist]
            self.installed()
            self.environment = {'package':self.packages,'os':self.dist,'version':self.dist_version}
            #self.environment = {'package':self.packages,'os':'debian','version':'8'} #REMOVER REMOVER REMOVER
            return self.getVulns()
        else:
            return False

    def getDist(self,):
        self.dist,self.dist_version,codename = platform.linux_distribution()
        #self.dist = 'debian' #REMOVER REMOVER REMOVER

    def installed(self,):
        self.packages = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, shell=True).communicate()[0].split('\n')
        self.packages = [package for package in self.packages if package]

    def getVulns(self,):
        url = 'https://vulners.com/api/v3/audit/audit/'
        r = requests.post(url,json=self.environment)
        return r.json()

    def register(self,server):
        self.getDist()
        self.getServer()
        serverInfos = {'ip':self.ip,'hostname':self.hostname,'dist':self.dist,'dist_version':self.dist_version}
        r = requests.post('http://%s:8000/register' % server,json=serverInfos)
        if 'ok' in r.json()['status']:
            print 'Register Sucess!'
            return True

    def getServer(self,):
        self.ip = socket.gethostbyname(socket.gethostname())
        self.hostname = socket.gethostname()

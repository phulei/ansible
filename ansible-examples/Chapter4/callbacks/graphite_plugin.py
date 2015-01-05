
import socket
import time

class CallbackModule(object):

  def __init__(self):
     self.UNREACHABLE_RUN = 0
     self.FAILED_RUN = 25
     self.SUCCESSFUL_RUN = 50
     self.CARBON_SERVER = '192.168.1.3'
     self.CARBON_PORT = 2003
     self.playbook = ''

  #Process the run result for each host
  def process_result(self,res):
     status = self.SUCCESSFUL_RUN
     changed_tasks, tasks = 0,0
     if type(res) == type(dict()):
        for key in res:
           host = key
           if res[host]['unreachable'] == 1:
              status = self.UNREACHABLE_RUN
           elif res[host]['failures'] != 0:
              status = self.FAILED_RUN
           else:
              tasks = res[host]['ok'] + res[host]['changed']
              changed_tasks = res[host]['changed']
        host = host.replace('.','-')
        self.send_data_to_graphite(host,status,tasks,changed_tasks)

 
  def send_data_to_graphite(self, host, status, tasks, changed_tasks):
     prefix = "ansible.run.%s.%s" % (self.playbook,host)
     tasks_metric = "%s.number_of_tasks %d %d\n" % (prefix,tasks,int(time.time()))
     status_metric = "%s.status %d %d\n" % (prefix,status,int(time.time()))
     changed_tasks_metric = "%s.changed_tasks %d %d\n" % (prefix,changed_tasks,int(time.time()))
     print "Prefix", prefix
     print "Tasks: %d, status: %d, changed_tasks: %s" % (tasks,status,changed_tasks)

     sock = socket.socket()
     sock.connect((self.CARBON_SERVER, self.CARBON_PORT))
     sock.sendall(status_metric)
     sock.sendall(tasks_metric)
     sock.sendall(changed_tasks_metric)
     sock.close()

 ## Other methods in the plugin do not change  ##

  def playbook_on_play_start(self, pattern): 
     self.playbook = pattern

  def playbook_on_stats(self, stats):
     results = dict([(h, stats.summarize(h)) for h in stats.processed])
     self.process_result(results)


import subprocess

class CallbackModule(object):  
  def __init__(self):
    self.play_name = ""

  def nagios_passive_check(self, host, return_code, status):
    subprocess.call("echo -e '%s\t%s\t%d\t%s' | sudo /usr/sbin/send_nsca -H 10.47.137.69  -c  /etc/nagios/send_nsca.cfg" % (host, self.play_name, return_code, status),  shell=True)

  def runner_on_failed(self, host, res, ignore_errors=False):
    self.nagios_passive_check(host, 2, "Critical: %s" % res)

  def runner_on_unreachable(self, host, res):
    self.nagios_passive_check(host, 2, "Critical: %s" % res)

  def playbook_on_play_start(self, pattern):
    self.play_name = self.play.name

  def playbook_on_stats(self, stats):
    if not stats.dark and not stats.failures:
      self.nagios_passive_check(stats.ok.keys()[0], 0, "Ok: Successful")


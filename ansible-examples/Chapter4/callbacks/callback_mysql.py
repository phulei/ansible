import getpass
import MySQLdb as mdb
import os

class CallbackModule(object):

  def __init__(self):
    self.dbhost = os.getenv('DBHOST')
    self.dbuser = os.getenv('DBUSER')
    self.dbpassword = os.getenv('DBPASSWORD')
    self.dbname = os.getenv('DBNAME')
    self.action = ""
    self.user = ""

  def update_stats(self, host, result, task=None, message=None):
    con = mdb.connect(self.dbhost, self.dbuser, self.dbpassword, self.dbname)
    cur=con.cursor()
    cur.execute('insert into ansible_run_stats(user,host,result,task,message) values("%s","%s","%s","%s","%s")' %(self.user,host,result,task,message))
    con.commit()
    con.close()

  def on_any(self, *args, **kwargs):
    pass
 
  def runner_on_failed(self, host, res, ignore_errors=False):
      self.update_stats(self.task.play.hosts, "unsuccessful", task=self.task.name, message=res)
 
  def runner_on_ok(self, host, res):
    pass
 
  def runner_on_error(self, host, msg):
    pass
 
  def runner_on_skipped(self, host, item=None):
    pass
 
  def runner_on_unreachable(self, host, res):
      self.update_stats(self.task.play.hosts, "unsuccessful", task=self.task.name, message=res)

  def runner_on_no_hosts(self):
    pass
 
  def runner_on_async_poll(self, host, res, jid, clock):
    pass
 
  def runner_on_async_ok(self, host, res, jid):
    pass
 
  def runner_on_async_failed(self, host, res, jid):
    pass
 
  def playbook_on_start(self):
    pass
 
  def playbook_on_notify(self, host, handler):
    pass
 
  def playbook_on_no_hosts_matched(self):
    pass
 
  def playbook_on_no_hosts_remaining(self):
    pass
 
  def playbook_on_task_start(self, name, is_conditional):
    pass
 
  def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
    pass
 
  def playbook_on_setup(self):
    pass
 
  def playbook_on_import_for_host(self, host, imported_file):
    pass
 
  def playbook_on_not_import_for_host(self, host, missing_file):
    pass
 
  def playbook_on_play_start(self, pattern):
    if not self.user:
      self.user = getpass.getuser()
 
  def playbook_on_stats(self, stats):
    if not stats.dark and not stats.failures:
      self.update_stats(stats.ok.keys()[0], "successful")


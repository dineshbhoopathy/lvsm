import unittest
import os
import sys
import StringIO

path = os.path.abspath(os.path.dirname(__file__))
from lvsm import shell


class Configure(unittest.TestCase):
    """Verify correct functionality in configure"""
    config = {'ipvsadm': path + '/scripts/ipvsadm',
              'iptables': path + '/scripts/iptables',
              'pager': 'none',
              'cache_dir': path + '/cache',
              'director_config': path + '/etc/ldirectord.conf',
              'firewall_config': path + '/etc/iptables.rules',
              'director': 'ldirectord',
              'director_cmd': '',
              'director_bin': '',
              'firewall_cmd': '',
              'nodes':'',
              'version_control': '',
              'keepalived-mib': 'KEEPALIVED-MIB',
              'snmp_community': '',
              'snmp_host': '',
              'snmp_user': '',
              'snmp_password': ''            
              }
    shell = shell.ConfigurePrompt(config)

    def test_showdirector1(self):
        output = StringIO.StringIO()
        sys.stdout = output
        expected_result = "# director config\nmaintenancedir = tests/maintenance\n"
        self.shell.onecmd(' show director')
        result = output.getvalue()
        self.assertEqual(result, expected_result)

    def test_showdirector2(self):
        # verify error checking
        self.assertTrue(True)

    def test_showfirewall1(self):
        output = StringIO.StringIO()
        sys.stdout = output
        expected_result = "# iptables\n"
        self.shell.onecmd(' show firewall')
        result = output.getvalue()
        self.assertEqual(result, expected_result)

    def test_showfirewall2(self):
        # verify error checking
        self.assertTrue(True)


class Virtual(unittest.TestCase):
    config = {'ipvsadm': path + '/scripts/ipvsadm',
              'iptables': path + '/scripts/iptables',
              'pager': 'none',
              'cache_dir': path + '/cache',
              'director_config': path + '/etc/ldirectord.conf',
              'firewall_config': path + '/etc/iptables.rules',
              'director': 'ldirectord',
              'director_cmd': '',
              'director_bin': '',
              'firewall_cmd': '',
              'nodes':'',
              'version_control': '',
              'keepalived-mib': 'KEEPALIVED-MIB',
              'snmp_community': '',
              'snmp_host': '',
              'snmp_user': '',
              'snmp_password': ''            
              }
    shell = shell.VirtualPrompt(config)
    shell.settings['color'] = False
    maintenance_dir = path + '/maintenance'

    def test_status1(self):
        self.shell.settings['numeric'] = False
        output = StringIO.StringIO()
        sys.stdout = output
        expected_result = """
Layer 4 Load balancing
======================
TCP  dinsdale.python.org:http                 rr     
  -> slashdot.org:http                        Masq    1      0          0         

UDP  dinsdale.python.org:domain               rr     
  -> resolver1.opendns.com:domain             Masq    1      0          0         
  -> resolver2.opendns.com:domain             Masq    1      0          0         


Disabled real servers:
----------------------
lga15s34-in-f3.1e100.net:http\t\tReason: Disabled for testing"""
        self.shell.onecmd(' status')
        result = output.getvalue()
        self.assertEqual(result.rstrip(), expected_result.rstrip())

    def test_status2(self):
        # Veirfy error checking
        self.assertTrue(True)

    def test_showvirtualtcp1(self):
        self.shell.settings['numeric'] = False
        output = StringIO.StringIO()
        sys.stdout = output
        expected_result = """
Layer 4 Load balancing
======================
TCP  dinsdale.python.org:http                 rr     
  -> slashdot.org:http                        Masq    1      0          0         


IP Packet filter rules
======================
ACCEPT     tcp  --  anywhere             dinsdale.python.org tcp dpt:http"""
        self.shell.onecmd(' show tcp dinsdale.python.org http')
        result = output.getvalue()
        self.assertEqual(result.rstrip(), expected_result.rstrip())

    def test_showvirtualtcp2(self):
        # Verify error checking
        self.assertTrue(True)

    def test_showvirtualudp(self):
        self.shell.settings['numeric'] = False
        output = StringIO.StringIO()
        sys.stdout = output
        expected_result = """
Layer 4 Load balancing
======================
UDP  dinsdale.python.org:domain               rr     
  -> resolver1.opendns.com:domain             Masq    1      0          0         
  -> resolver2.opendns.com:domain             Masq    1      0          0"""
        self.shell.onecmd(' show udp dinsdale.python.org 53')
        result = output.getvalue()
        self.assertEqual(result.rstrip(), expected_result.rstrip())

#     def test_showrealactive(self):
#         self.shell.settings['numeric'] = False
#         output = StringIO.StringIO()
#         sys.stdout = output
#         expected_result = """
# Active servers:
# ---------------
# TCP dinsdale.python.org:http
#   -> slashdot.org:http"""
#         self.shell.onecmd(' show real slashdot.org 80')
#         result = output.getvalue()
#         self.assertEqual(result.rstrip(), expected_result.rstrip())

#     def test_showrealdisabled(self):
#         output = StringIO.StringIO()
#         sys.stdout = output
#         expected_result = """
# Disabled servers:
# -----------------
# lga15s34-in-f3.1e100.net:http\t\tReason: Disabled for testing"""
#         self.shell.onecmd(' show real 173.194.43.3 80')
#         result = output.getvalue()
#         self.assertEqual(result.rstrip(), expected_result.rstrip())

    # def test_disablereal(self):
    #     filepath = self.maintenance_dir + '/208.67.222.222'
    #     # this is the disabling message we'll store in the file
    #     sys.stdin = StringIO.StringIO('disabled by test case')
    #     self.shell.onecmd('disable 208.67.222.222')
    #     self.assertTrue(os.path.exists(filepath))
    #     # now clean up the file
    #     try:
    #         os.unlink(filepath)
    #     except OSError as e:
    #         pass

    # def test_enablereal(self):
    #     filepath = self.maintenance_dir + '/208.67.222.222:53'
    #     try:
    #         # create the file before we continue
    #         f = open(filepath, 'w')
    #         f.close()
    #         self.shell.onecmd('enable 208.67.222.222 domain')
    #         self.assertTrue(not os.path.exists(filepath))
    #     except IOError as e:
    #         pass

class Real(unittest.TestCase):
    config = {'ipvsadm': path + '/scripts/ipvsadm',
              'iptables': path + '/scripts/iptables',
              'pager': 'none',
              'cache_dir': path + '/cache',
              'director_config': path + '/etc/ldirectord.conf',
              'firewall_config': path + '/etc/iptables.rules',
              'director': 'ldirectord',
              'director_cmd': '',
              'director_bin': '',
              'firewall_cmd': '',
              'nodes':'',
              'version_control': '',
              'keepalived-mib': 'KEEPALIVED-MIB',
              'snmp_community': '',
              'snmp_host': '',
              'snmp_user': '',
              'snmp_password': ''            
              }
    shell = shell.RealPrompt(config)
    shell.settings['color'] = False
    maintenance_dir = path + '/maintenance'

    def test_showrealactive(self):
        # Test 'show real' without port
        self.shell.settings['numeric'] = True
        output = StringIO.StringIO()
        sys.stdout = output
        expected_result = """
Layer 4 Load balancing
======================

Active servers:
---------------
UDP  82.94.164.162:53                         rr     
  -> 208.67.222.222:53                        Masq    1      0          0
"""
        self.shell.onecmd(' show resolver1.opendns.com')
        result = output.getvalue()
        self.assertEqual(result.rstrip(), expected_result.rstrip())      

#     def test_showrealdisabled(self):
#         # Test 'show real' on a disabled host
#         self.shell.settings['numeric'] = True
#         output = StringIO.StringIO()
#         sys.stdout = output
#         expected_result = """
# Layer 4 Load balancing
# ======================

# Disabled servers:
# -----------------
# 173.194.43.3:80     Reason: Disabled for testing
# """
#         self.shell.onecmd(' show 173.194.43.3')
#         result = output.getvalue()
#         # self.assertEqual(result.rstrip(), expected_result.rstrip()) 
#         self.assertTrue(True)
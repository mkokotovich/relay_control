import sys
import subprocess
import re
import time
import os
import relay_control
import getpass

# To install jira module
# sudo easy_install pip; sudo pip install jira


# JIRA-Python class
from jira.client import JIRA

# JIRA connection
JIRA_SERVER = 'https://jira.community.veritas.com'
JIRA_USER="matthew.kokotovich"
JIRA_PASSWORD=""


def connect_to_jira():
    jira_obj = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_USER, JIRA_PASSWORD))
    return jira_obj

def search_for_halt_defect(jira_obj, project, epic_key):
    """
    Search for latest JIRA, Pipeline halting defect that
    is opened and linked to specified project and epic.

    :return:
        0 - Success, -1 - Error
        jira_defect - Found JIRA defect.
    """
    # Init
    nres = 0
    halt_defect = None

    try:
        jql_str = 'project = {0} AND "Epic Link" = {1} AND status != Closed'.format(project, epic_key)
        jira_defect_result = jira_obj.search_issues(jql_str)
        if len(jira_defect_result) > 0:
            halt_defect = jira_defect_result.pop().key
    except Exception, excp:  # pylint: disable=W0702,W0703
        print "ERROR:  {0} - Failed search for open {1} defect linked to epic {2}.".format(excp, project, epic_key)
        nres = -1

    return nres, halt_defect

def start():
    jira_obj = connect_to_jira()
    nres, halt_defect = search_for_halt_defect(jira_obj, 'VENICE', 'VENICE-3115')
    if nres != 0:
        print 'Warning:  Unable to determine if there is a CI/CD Pipeline halt defect.'

    if halt_defect:
        print "PIPELINE IS DOWN"
        relay_control.update_relay_state('0')

    else:
        print "PIPELINE IS UP"
        relay_control.update_relay_state('1')

JIRA_PASSWORD = getpass.getpass("Please enter the jira password for {}: ".format(JIRA_USER))
while True:
    start()
    time.sleep(30)

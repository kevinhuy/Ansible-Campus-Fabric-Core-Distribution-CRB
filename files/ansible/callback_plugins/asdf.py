# These imports are defined for every callback plugin I've seen so far.
# If you don't import `absolute_import` standard library modules may be
# overriden by Ansible python modules with the same name. For example: I use the
# standard library `json` module, but Ansible has a callback plugin with the
# same name. When I excluded `absolute_import` and imported `json` the json
# module I got was Ansible's json module and not the standard library one.
# I'm not sure why `division` and `print_function` need to be imported.
from __future__ import (absolute_import, division, print_function)
from ansible.plugins.callback import CallbackBase

__metaclass__ = type

import json
import urllib
import sys
import os

# Ansible documentation of the module. I'm also not sure why this is required,
# but other plugins add documentation so it seems to be a standard.
DOCUMENTATION = '''
    callback: slack
    options:
      slack_webhook_url:
        required: True
        env:
          - name: SLACK_WEBHOOK_URL
      slack_channel:
        required: False
        env:
          - name: SLACK_CHANNEL
'''

class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_NAME = 'slack'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()

    def set_options(self, task_keys=None, var_options=None, direct=None):
        super(CallbackModule, self).set_options(task_keys=task_keys, var_options=var_options, direct=direct)

        # Read and assign environment variables to memory so that we can use
        # them later.
        self.slack_webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
        self.slack_channel = os.environ.get('SLACK_CHANNEL')

        if self.slack_webhook_url is None:
            self._display.display('Error: The slack callback plugin requires `SLACK_WEBHOOK_URL` to be defined in the environment')
            sys.exit(1)

    def v2_runner_on_failed(self, taskResult, ignore_errors=False):
        notify(self.slack_webhook_url, taskResult, self.slack_channel)

    def v2_runner_on_unreachable(self, taskResult):
        notify(self.slack_webhook_url, taskResult, self.slack_channel)


def notify(slack_webhook_url, taskResult, slack_channel=None):
    # Format the Slack message. We'll use message attachments
    # https://api.slack.com/docs/message-attachments
    payload = {
        'username': 'Ansible',
        'attachments': [
            {
                'title': 'Ansible run has failed. HOST: {} {}'.format(taskResult._host, taskResult._task),
                'color': '#FF0000',
                'text': '```{}```'.format(json.dumps(taskResult._result, indent=2))
            }
        ]
    }

    # The webhook has a default url. If one is not configured, we'll use the
    # default
    if slack_channel:
        payload['channel'] = slack_channel

    req = urllib2.Request(slack_webhook_url)
    urllib2.urlopen(req, data=json.dumps(payload))
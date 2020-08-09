# Bonus playbooks

## Overview

### pb.awx.test.environmentals

Validate that the AWX environment has the correct enviornmentals set. Very helpful for debugging your environment.

### pb.configuration.backup

Logs into your devices and backs up their facts can configurations into local files.

### pb.configuration.bootstrap

Restores the device's configuration to essentially management only.

## pb.configuration.diff

Compares a device's running configuration with that of was just generated. More helpful in an Ansible Tower Workflow.

### pb.configuration.golden.diff

Compares a device's running configuration with that of the golden config. More helpful in an Ansible Tower Workflow.

#### pb.netbox.retrieve.info

Retrieve k/v pairs of devices from netbox.

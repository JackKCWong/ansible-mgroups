from ansible.plugins.inventory import BaseInventoryPlugin


DOCUMENTATION = '''
    name: mgroups
    plugin_type: inventory
    short_description: Reads a YAML file with that define groups as attribute of hosts
    description:
        - This plugin reads a YAML file where hosts have a list of groups
    options:
        plugin:
            description: Token that ensures this is a source file for the 'mgroups' plugin.
            required: True
            choices: ['mgroups']
        hosts:
            description: hosts with groups and vars
            required: true
'''

EXAMPLES = '''
# mgroups example
plugin: mgroups 
hosts: 
  host1:
    groups: group1 group2
    vars:
      var1: value1
      var2: value2
  host2:
    groups: group2 group3
    vars:
      var1: value3
      var2: value4
'''

class InventoryModule(BaseInventoryPlugin):
    NAME = 'myplugin'  # used internally by Ansible, it should match the file name but not required

    def __init__(self):
        super().__init__()

    def verify_file(self, path):
        """Verify that the source file can be processed correctly."""
        valid = False
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('.yaml', '.yml')):
                valid = True
        return valid

    def parse(self, inventory, loader, path, cache=True):
        """Parse the inventory file and create the inventory."""
        super(InventoryModule, self).parse(inventory, loader, path, cache)
        self._read_config_data(path)

        # Get the list of hosts and their labels from the YAML file
        hosts_data = self.get_option('hosts')

        for host, maps in hosts_data.items():
            # Add the host to the inventory
            self.inventory.add_host(host)

            # Add the host to the groups
            for group in maps.get('groups', []).split(" "):
                self.inventory.add_group(group)
                self.inventory.add_host(host, group=group)

            # Add the vars to the hosts
            vars = maps.get('vars', {})
            for var in vars.items():
                self.inventory.set_variable(host, var[0], var[1])

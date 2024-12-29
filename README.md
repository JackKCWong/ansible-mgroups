# ansible-mgroups

An inventory plugin to assign mutliple groups to a host on a single line, because I find it clumsy to use a hierarchy structure for my use case.

## usage examples

1. add the plugin in your `ansible.cfg` file:

```cfg
[inventory]
enable_plugins = mgroups, host_list, script, auto, yaml, ini, toml

[defaults]
inventory_plugins = ./inventory_plugins
```

2. create inventory file in yml / yaml format, using `groups` (a space separated list) to assign multiple groups to a host:

```yml
plugin: mgroups
hosts: 
  host1:
    groups: db east
    vars:
      var1: value1
      var2: value2
  host2:
    groups: db west
    vars:
      var1: value3
      var2: value4
```

3. You can define host vars with `vars` or the usual `group_vars` and `host_vars` folders.

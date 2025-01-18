# flaskapp

A role to deploy a Flask application.

## Requirements

- Ansible 2.9 or higher

## Role Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `variable_name` | Description of the variable | `default_value` |

## Dependencies

None.

## Example Playbook

```yaml
- hosts: all
  become: yes
  roles:
    - flaskapp

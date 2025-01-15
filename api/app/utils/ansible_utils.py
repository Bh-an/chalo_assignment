import os
import subprocess
from jinja2 import Environment, FileSystemLoader
from api.app.utils.config import Config
from api.app.utils.helpers import setup_logger

config = Config()
logger = setup_logger("ansible_utils", log_file='logs/ansible_utils.log')

def configure_ansible(terraform_outputs, config_data):
    """Configures Ansible files based on Terraform outputs and user input."""
    try:
      bastion_eip_address = terraform_outputs.get("bastion_eip_address", {}).get("value")
      primary_db_addr = terraform_outputs.get("primary_db_addr", {}).get("value")
      replica_db_addresses = terraform_outputs.get("replica_db_addresses", {}).get("value")
      
      bastion_key_path = config_data.get('bastion_key_path')
      db_key_path = config_data.get('db_key_path')

      if not all([bastion_eip_address, primary_db_addr, replica_db_addresses, bastion_key_path, db_key_path]):
          logger.error("Missing essential terraform outputs or user provided configuration.")
          return None, "Missing essential terraform outputs or user provided configuration."
      
      template_env = Environment(loader=FileSystemLoader(config.TEMPLATE_DIR))

      # Configure hosts.ini
      hosts_template = template_env.get_template('hosts.ini.j2')
      rendered_hosts = hosts_template.render(
            bastion_eip_address=bastion_eip_address,
            primary_db_addr=primary_db_addr,
            replica_db_addresses=replica_db_addresses,
            db_key_path=db_key_path,
            bastion_key_path=bastion_key_path
        )
      
      with open(config.ANSIBLE_INVENTORY_FILE, 'w') as f:
        f.write(rendered_hosts)
        
      # Configure ansible.cfg
      ansible_cfg_template = template_env.get_template('ansible.cfg.j2')
      rendered_ansible_cfg = ansible_cfg_template.render(bastion_key_path=bastion_key_path)
      with open(os.path.join(config.ANSIBLE_DIR, "ansible.cfg"), 'w') as f:
        f.write(rendered_ansible_cfg)

      # Configure postgresql settings
      postgress_settings_template = template_env.get_template('postgress_settings.yaml.j2')
      
      # Remove unwanted keys
      filtered_config_data = {k: v for k,v in config_data.items() if k not in ["bastion_key_path", "db_key_path"]}
      rendered_template = postgress_settings_template.render(config=filtered_config_data)
      
      with open(config.ANSIBLE_VARS_FILE, 'w') as f:
            f.write(rendered_template)

      return {"message": "Ansible configuration completed successfully"}, None
    except Exception as e:
         logger.error(f"Error configuring ansible {e}")
         return None, f"Error configuring ansible: {e}"

def run_ansible_playbook(show_output=False, postgresql_version=None):
    """Runs the Ansible playbook and returns the output or an error message."""
    try:
       vault_password = os.environ.get("ANSIBLE_VAULT_PASSWORD")
       if not vault_password:
            logger.error(f"The environment variable ANSIBLE_VAULT_PASSWORD is not set")
            return None, {"error": "The environment variable ANSIBLE_VAULT_PASSWORD is not set"}
       command = f"""
            ansible-playbook playbooks/main.yaml --vault-password-file <(echo "{vault_password}") -i inventory/hosts.ini
        """
       if postgresql_version:
           command = f"""
            ansible-playbook playbooks/main.yaml --vault-password-file <(echo "{vault_password}") -e "postgresql_version={postgresql_version}" -i inventory/hosts.ini
           """


       process = subprocess.Popen(
            command,
            cwd=config.ANSIBLE_DIR,
            shell=True,
            executable="/bin/bash",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
       stdout, stderr = process.communicate()

       if show_output:
           logger.debug(f"Ansible playbook output:\n{stdout}")

       if process.returncode == 0:
           return_value = {"message": "Ansible playbook executed successfully"}
           if show_output:
               return_value["output"] = stdout.strip()
           return return_value, None
       else:
           return None, {"error": "Ansible playbook execution failed", "details": stderr.strip()}

    except FileNotFoundError:
        logger.error(f"Ansible executable or inventory not found")
        return None, {"error": "Ansible executable or inventory not found"}
    except Exception as e:
         logger.error(f"Error while running ansible playbook {e}")
         return None, {"error": f"Error while running ansible playbook: {e}"}
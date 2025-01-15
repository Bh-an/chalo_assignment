import os
import subprocess
import json
from jinja2 import Environment, FileSystemLoader
from api.app.utils.config import Config
from api.app.utils.helpers import setup_logger

config = Config()
logger = setup_logger("terraform_utils", log_file='logs/terraform_utils.log')


# Hardcoded required variables
REQUIRED_VARIABLES = {
    "bastion_key_pair",
    "db_key_pair"
}

# Hardcoded optional variables with default values
OPTIONAL_VARIABLES = {
    "region": "ap-south-1",
    "environment": "dev",
    "vpc_cidr": "10.0.0.0/16",
    "public_subnet_block": "10.0.1.0/24",
    "private_subnets_block": ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"],
    "bastion_ami": "ami-023a307f3d27ea427",
    "bastion_instance_type": "t2.micro",
    "postgresql_ami": "ami-023a307f3d27ea427",
    "replica_count": "2",
    "db_instance_type": "t2.small"
}


def generate_tfvars(user_config):
    """Generates a terraform.tfvars file from a template and user input."""
    
    # Filter out any invalid variables
    valid_vars = set(OPTIONAL_VARIABLES.keys()).union(REQUIRED_VARIABLES)
    invalid_vars = set(user_config.keys()).difference(valid_vars)
    if invalid_vars:
        logger.error(f"Invalid vars provided: {invalid_vars}")
        return None, f"Invalid variables provided: {invalid_vars}"
    
    if not REQUIRED_VARIABLES.issubset(user_config.keys()):
      missing_vars = REQUIRED_VARIABLES.difference(user_config.keys())
      logger.error(f"Missing required vars: {missing_vars}")
      return None, f"Missing required variables: {missing_vars}"
    
    template_env = Environment(loader=FileSystemLoader(config.TEMPLATE_DIR))
    template = template_env.get_template('terraform.tfvars.j2') # Corrected line, changed template name

    # Merge default values with user input, user input taking precedence
    merged_config = {**OPTIONAL_VARIABLES, **user_config}

      # Filter the config to only include user provided values
    filtered_config = {key: value for key, value in merged_config.items() if key in user_config}
    try:
        rendered_template = template.render(config=filtered_config)

        with open(config.TERRAFORM_VARS_FILE, 'w') as tfvars_file:
            tfvars_file.write(rendered_template)

        return {
            "message": "terraform.tfvars file generated successfully",
             "used_variables": filtered_config,
            "default_variables": {key: value for key, value in merged_config.items() if key not in user_config}
        }, None
    except Exception as e:
        logger.error(f"Error while generating terraform file {e}")
        return None, f"Error while generating terraform file: {e}"

def run_terraform_command(command, show_output=False):
    """Runs a terraform command and returns the output or an error message."""
    try:
        process = subprocess.Popen(
            command,
            cwd=config.TERRAFORM_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate()
        
        if show_output:
            logger.debug(f"Terraform command '{command[1]}' output:\n{stdout}") # Log output
        
        if process.returncode == 0:
           return_value = {"message": f"Terraform command '{command[1]}' executed successfully"}
           if show_output:
               return_value["output"] = stdout.strip()
           return return_value, None
        else:
            return None, {"error": f"Terraform command '{command[1]}' failed", "details": stderr.strip()}

    except FileNotFoundError:
        logger.error(f"Terraform binary not found: {config.TERRAFORM_BINARY}")
        return None, {"error": f"Terraform binary not found"}
    except Exception as e:
        logger.error(f"Error while running terraform command {e}")
        return None, {"error": f"Error while running terraform command: {e}"}
    

def get_terraform_outputs():
    """Fetches and returns terraform outputs in a dictionary format."""
    try:
      command = [config.TERRAFORM_BINARY, 'output', '-json']
      process = subprocess.Popen(
          command,
          cwd=config.TERRAFORM_DIR,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          text=True,
      )
      stdout, stderr = process.communicate()
      if process.returncode == 0:
        try:
          outputs = json.loads(stdout)
          return outputs, None
        except json.JSONDecodeError:
          logger.error(f"Error decoding terraform outputs: {stdout}")
          return None, f"Error decoding terraform output: {stdout}"
      else:
          logger.error(f"Error getting terraform output {stderr}")
          return None, f"Error getting terraform output: {stderr}"
          
    except FileNotFoundError:
         logger.error(f"Terraform binary not found: {config.TERRAFORM_BINARY}")
         return None, f"Terraform binary not found"
    except Exception as e:
          logger.error(f"Error while getting terraform output {e}")
          return None, f"Error while getting terraform output: {e}"

def get_terraform_output(show_output=False):
    """Fetches and returns terraform output."""
    try:
      command = [config.TERRAFORM_BINARY, 'output']
      process = subprocess.Popen(
          command,
          cwd=config.TERRAFORM_DIR,
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE,
          text=True,
      )
      stdout, stderr = process.communicate()
      if process.returncode == 0:
          return_value = {"message": "Terraform output command executed successfully"}
          if show_output:
               return_value["output"] = stdout.strip()
          return return_value, None

      else:
          logger.error(f"Error getting terraform output: {stderr}")
          return None, {"error": f"Error getting terraform output: {stderr}"}
    except FileNotFoundError:
         logger.error(f"Terraform binary not found: {config.TERRAFORM_BINARY}")
         return None, f"Terraform binary not found"
    except Exception as e:
          logger.error(f"Error while getting terraform output {e}")
          return None, f"Error while getting terraform output: {e}"
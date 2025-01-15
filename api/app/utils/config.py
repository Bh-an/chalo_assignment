import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings for the API."""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    TERRAFORM_DIR = os.path.join(BASE_DIR, "terraform", "main")
    TEMPLATE_DIR = os.path.join(BASE_DIR, "api","templates")
    ANSIBLE_DIR = os.path.join(BASE_DIR, "ansible")

    # API Configuration
    DEBUG = os.environ.get("DEBUG", "False").lower() == "true"
    API_PORT = int(os.environ.get("API_PORT", 5000))
    HOST_ADDRESS = os.environ.get("HOST_ADDRESS", "0.0.0.0")
    ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

    # Terraform Configuration
    TERRAFORM_BINARY = os.environ.get("TERRAFORM_BINARY", "terraform")
    OUTPUT_FORMAT = os.environ.get("OUTPUT_FORMAT", "json")
    TERRAFORM_VARS_FILE = os.path.join(TERRAFORM_DIR, "terraform.tfvars")

    #Ansible Configuration
    ANSIBLE_INVENTORY_FILE = os.path.join(ANSIBLE_DIR,"inventory","hosts.ini")
    ANSIBLE_PLAYBOOK_FILE = os.path.join(ANSIBLE_DIR, "playbooks","main.yaml")
    ANSIBLE_VARS_FILE = os.path.join(ANSIBLE_DIR, "roles", "postgresql", "vars", "postgress_settings.yaml")
    ANSIBLE_VAULT_PASS_FILE = os.path.join(ANSIBLE_DIR, "vault_pass.sh")

    def __repr__(self):
        return str(self.__dict__)
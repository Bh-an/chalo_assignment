from flask import request, jsonify
from api.app.utils.terraform_utils import generate_tfvars, run_terraform_command, get_terraform_output
from api.app.utils.helpers import setup_logger
from api.app.utils.config import Config

config = Config()
logger = setup_logger("terraform_controller", log_file='logs/terraform_controller.log')

def generate_terraform_config():
    """Handles the generation of terraform.tfvars file."""
    try:
        user_config = request.get_json()
        if not user_config:
            logger.error("Request body is empty")
            return jsonify({"error": "Request body is empty"}), 400
        
        result, error = generate_tfvars(user_config)

        if error:
            return jsonify({"error": error}), 400
        
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

def terraform_init():
    """Handles terraform init command."""
    try:
        request_data = request.get_json()
        if not request_data:
            request_data = {}
        output = request_data.get('output', False)
        result, error = run_terraform_command([config.TERRAFORM_BINARY, "init"], output)
        if error:
            return jsonify(error), 400
        return jsonify(result), 200
    except Exception as e:
         logger.error(f"An unexpected error occurred: {e}")
         return jsonify({"error": "An unexpected error occurred"}), 500

def terraform_plan():
    """Handles terraform plan command."""
    try:
        request_data = request.get_json()
        if not request_data:
            request_data = {}
        output = request_data.get('output', False)
        result, error = run_terraform_command([config.TERRAFORM_BINARY, "plan"], output)
        if error:
            return jsonify(error), 400
        return jsonify(result), 200
    except Exception as e:
         logger.error(f"An unexpected error occurred: {e}")
         return jsonify({"error": "An unexpected error occurred"}), 500

def terraform_apply():
    """Handles terraform apply command."""
    try:
        request_data = request.get_json()
        if not request_data:
            request_data = {}
        output = request_data.get('output', False)
        result, error = run_terraform_command([config.TERRAFORM_BINARY, "apply", "-auto-approve"], output)
        if error:
             return jsonify(error), 400
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
def terraform_destroy():
    """Handles terraform destroy command."""
    try:
        request_data = request.get_json()
        if not request_data:
             request_data = {}
        output = request_data.get('output', False)
        result, error = run_terraform_command([config.TERRAFORM_BINARY, "destroy", "-auto-approve"], output)
        if error:
            return jsonify(error), 400
        return jsonify(result), 200
    except Exception as e:
         logger.error(f"An unexpected error occurred: {e}")
         return jsonify({"error": "An unexpected error occurred"}), 500
def terraform_output():
    """Handles terraform output command."""
    try:
      request_data = request.get_json()
      if not request_data:
           request_data = {}
      output = request_data.get('output', False)
      result, error = get_terraform_output(output)
      if error:
            return jsonify(error), 400
      return jsonify(result), 200
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
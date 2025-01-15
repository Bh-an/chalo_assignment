from flask import request, jsonify
from api.app.utils.terraform_utils import get_terraform_outputs
from api.app.utils.ansible_utils import configure_ansible, run_ansible_playbook
from api.app.utils.helpers import setup_logger

logger = setup_logger("ansible_controller", log_file='logs/ansible_controller.log')

def ansible_configure():
    """Handles the ansible configuration."""
    try:
        config_data = request.get_json()
        if not config_data:
          logger.error("Request body is empty")
          return jsonify({"error": "Request body is empty"}), 400

        terraform_outputs, error = get_terraform_outputs()
        if error:
            return jsonify({"error": f"Error getting terraform output {error}"}), 400

        result, error = configure_ansible(terraform_outputs, config_data)

        if error:
          return jsonify({"error": f"Error configuring ansible {error}"}), 400

        return jsonify(result), 200
    
    except Exception as e:
      logger.error(f"An unexpected error occurred: {e}")
      return jsonify({"error": "An unexpected error occurred"}), 500

def ansible_run():
    """Handles the ansible run command."""
    try:
        request_data = request.get_json()
        if not request_data:
             request_data = {}
        output = request_data.get('output', False)
        postgresql_version = request_data.get('postgresql_version')
        result, error = run_ansible_playbook(output, postgresql_version)
        if error:
            return jsonify(error), 400
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500
from api.app.controllers.terraform_controller import generate_terraform_config, terraform_init, terraform_plan, terraform_apply, terraform_destroy, terraform_output
from api.app.controllers.ansible_controller import ansible_configure, ansible_run

def register_routes(app):
    
    app.add_url_rule('/terraform/generate', methods=['POST'], view_func=generate_terraform_config)
    app.add_url_rule('/terraform/init', methods=['POST'], view_func=terraform_init)
    app.add_url_rule('/terraform/plan', methods=['POST'], view_func=terraform_plan)
    app.add_url_rule('/terraform/apply', methods=['POST'], view_func=terraform_apply)
    app.add_url_rule('/terraform/destroy', methods=['POST'], view_func=terraform_destroy)
    app.add_url_rule('/terraform/output', methods=['POST'], view_func=terraform_output)


    app.add_url_rule('/ansible/configure', methods=['POST'], view_func=ansible_configure)
    app.add_url_rule('/ansible/run', methods=['POST'], view_func=ansible_run)
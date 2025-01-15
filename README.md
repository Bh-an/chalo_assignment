# API platform for PostgreSQL setup

An API platform for provisioning and setting up a replicated PostgreSQL ckuster on AWS elastic compute resources along with underlying infrastructure.

---

### Pre-requisites

- A Linux based machine with a **Python 3.8+** environment to run the python app
- **Terraform** installed and available in your system's `PATH`. [installation](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli).
- **Ansible** installed and available in your system's `PATH`. [installation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-for-development)
- **AWS CLI** is required to be installed and configured for running terraform commands that use the aws provider. [instruction](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

### Setup

1.  **Clone the Repository:**
    ```bash
    git clone git@github.com:Bh-an/chalo_assignment.git
    cd chalo_assignment
    ```
2.  **Create a virtual environment and Install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```
3.  **Configuring the API server:**
    *   Create a `.env` file in the root directory, use the template in the repository.
    ```
    # .env file example
    DEBUG=True            # Enable debug mode (True or False)
    API_PORT=5000         # Port on which the API will run
    HOST_ADDRESS=0.0.0.0 # Host address to bind the server to (0.0.0.0 for all interfaces)
    ALLOWED_HOSTS=*      # Comma separated list of allowed hosts, use * to allow all
    TERRAFORM_BINARY=terraform    # Path to the terraform binary, it must exist in your PATH
    OUTPUT_FORMAT=json    # Format of terraform output (json)

    ```
    *   Set `DEBUG=True` to enable debug mode and logging.
    *   You can configure other settings like `API_PORT`, `HOST_ADDRESS`, etc.
  
4. **Creating and securing the Ansible Vault**
   > Note: It is important to configure the vault manually as it will contain our replication password
  
   * Remove any existing vault file and make a new one
   * ```bash
     rm -f ansible/vault/vault.yaml && touch rm -f ansible/vault/vault.yaml
     ```
    * Add replication password to the file
     ```bash
     echo "replication_password: '<your_replication_pass>'" > ansible/vault/vault.yaml
     ```
     * Encrypt the vault
     ```bash
     ansible-vault encrypt ansible/vault/vault.yaml
     ```
     set vault password when prompted
     * Pass password into the `ANSIBLE_VAULT_PASSWORD` env variable
    ```bash
     export ANSIBLE_VAULT_PASSWORD=<your_vault_password>
     ```

5. **Creating and storing private key files for ec2 key-pairs**
   Create two key pairs
     * For bastion host in public subnet
     * For DB servers in private subnets
     > Make sure you set proper file level permission for ssh usage
   
  
### Usage 

Start the API server
```bash
python run.py
```

#### API Endpoints
*   **`/terraform/generate` (POST):**
    *   **Description:** Generates the `terraform.tfvars` file from a Jinja2 template and user-provided variables.
    *   **Request Body:** JSON object containing variables for configuring variables for the provisioned infrastructure
    > Full list of variables are available in this [file](terraform/main/variables.tf); bastion_key_pair and db_key_pair are required, others will default to values in file
    *   **Response:**
        *   `200 OK`: On success, returns a success message, the list of used variables, and the list of default variables.
        *   `400 Bad Request`: On failure, returns an error message specifying any missing or invalid parameters.
        * `500 Internal Server Error`: Returns an error stating something unexpected happened.
    *   **Example:**
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{
            "bastion_key_pair": "path_to_your-bastion-key",
            "db_key_pair": "path_to_your-db-key",
            "environment": "staging",
            "replica_count": "2",
            "db_instance_type": "t2_medium"
            ""
        }' http://localhost:5000/terraform/generate
        ```
*   **`/terraform/init` (POST):**
    *   **Description:** Executes `terraform init` to initialize the terraform directory.
    *   **Request Body:** Optional JSON object that takes `output`, where if `true` then STDOUT is returned.
    *   **Response:**
        *  `200 OK`: On Success, returns a JSON object which contains a success message, if output=false only success/failure message is returned, if output = true, then the output is returned.
        *  `400 Bad Request`: On failure, returns an error message stating why the operation failed.
         * `500 Internal Server Error`: Returns an error stating something unexpected happened.
    *   **Example:**
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"output": true}' http://localhost:5000/terraform/init
        ```
*   **`/terraform/plan` (POST):**
    *   **Description:** Executes `terraform plan` to plan the changes.
    *   **Request Body:** Optional JSON object that takes `output`, where if `true` then STDOUT is returned.
    *   **Response:**
        *  `200 OK`: On Success, returns a JSON object which contains a success message, if output=false only success/failure message is returned, if output = true, then the output is returned.
         *  `400 Bad Request`: On failure, returns an error message stating why the operation failed.
          * `500 Internal Server Error`: Returns an error stating something unexpected happened.
    *   **Example:**
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"output": true}' http://localhost:5000/terraform/plan
        ```
*   **`/terraform/apply` (POST):**
    *   **Description:** Executes `terraform apply` to provision the resources.
    *   **Request Body:** Optional JSON object that takes `output`, where if `true` then STDOUT is returned.
    *   **Response:**
        *  `200 OK`: On Success, returns a JSON object which contains a success message, if output=false only success/failure message is returned, if output = true, then the output is returned.
        *  `400 Bad Request`: On failure, returns an error message stating why the operation failed.
         * `500 Internal Server Error`: Returns an error stating something unexpected happened.
    *   **Example:**
        ```bash
         curl -X POST -H "Content-Type: application/json" -d '{"output": true}' http://localhost:5000/terraform/apply
         ```
*   **`/terraform/destroy` (POST):**
    *   **Description:** Executes `terraform destroy` to remove the resources.
    *   **Request Body:** Optional JSON object that takes `output`, where if `true` then STDOUT is returned.
    *  **Response:**
        *  `200 OK`: On Success, returns a JSON object which contains a success message, if output=false only success/failure message is returned, if output = true, then the output is returned.
         *  `400 Bad Request`: On failure, returns an error message stating why the operation failed.
          * `500 Internal Server Error`: Returns an error stating something unexpected happened.
    *   **Example:**
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"output": true}' http://localhost:5000/terraform/destroy
        ```
*    **`/terraform/output` (POST):**
    *   **Description:** Executes `terraform output` to fetch terraform output values.
    *   **Request Body:** Optional JSON object that takes `output`, where if `true` then STDOUT is returned.
    *  **Response:**
        *  `200 OK`: On Success, returns a JSON object which contains a success message, if output=false only success/failure message is returned, if output = true, then the output is returned.
        *   `400 Bad Request`: On failure, returns an error message stating why the operation failed.
         * `500 Internal Server Error`: Returns an error stating something unexpected happened.
    *   **Example:**
       ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"output": true}' http://localhost:5000/terraform/output
       ```

*   **`/ansible/configure` (POST):**
    *   **Description:** Configures Ansible files (`hosts.ini`, `ansible.cfg`, `postgress_settings.yaml`).
    *   **Request Body:** JSON object with required keys `bastion_key_path` and `db_key_path` and optional key-value pairs for `postgress_settings.yaml`
    > The optional variables support almost variables included in the [postgresql.conf](https://github.com/postgres/postgres/blob/master/src/backend/utils/misc/postgresql.conf.sample) file. be aware of impact changing certain values may cause
    *   **Response:**
        *   `200 OK`: On success, returns a success message.
        *   `400 Bad Request`: On failure, returns an error message detailing any issues.
         * `500 Internal Server Error`: Returns an error stating something unexpected happened.
    *   **Example:**
        ```bash
          curl -X POST -H "Content-Type: application/json" -d '{
              "bastion_key_path": "<bastion_key_path>",
              "db_key_path": "<db_key_path>",
              "max_connections": "50",
              "max_wal_senders": "15"
            }' http://localhost:5000/ansible/configure
        ```
*   **`/ansible/run` (POST):**
    *   **Description:** Runs the Ansible playbook using the values in the inventory and the `postgress_settings.yaml` using process substitution to pass the vault password from an environment variable.
    *   **Request Body:** Optional JSON object that takes `output` and `postgresql_version`. If output is set to `true` then the output is returned.
    *   **Response:**
        *   `200 OK`: On success, returns a success message and output
        *   `400 Bad Request`: On failure, returns an error message stating why the operation failed.
         * `500 Internal Server Error`: Returns an error stating something unexpected happened.
    *   **Example:**
        ```bash
        curl -X POST -H "Content-Type: application/json" -d '{"output": true}' http://localhost:5000/ansible/run
        ```

### Logging

*   The application logs to both console and log files (located at `logs/app.log`, `logs/terraform_utils.log`, and `logs/ansible_utils.log`).
*   Logs include timestamps, log levels (DEBUG, INFO, ERROR, etc.), and messages.
*  When output is set to true on terraform and ansible endpoints the output is logged to the `debug` log level.

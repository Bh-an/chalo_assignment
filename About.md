# Overview

The core of the profect revolves around three development areas:

* **Infrastructure provisioning:** Bringing up the required cloud resources through use of IaC and a declarative tool like Terraform.

* **Configuration management:** Setting up the desired server environment and installing/configuring services that will run on them through Ansible.

* **Automation API:** Bringing together the workflow to provide a programatic and flexible way of applying required changes to the base configurations. 

The retrospective will be divided between these three areas of work

## Infrastructure provisioning

*  ### Approach
      The problem statement hiinted at progamatically generated templates for the required terraform files however it has some drawbacks like verbose code affecting manageability and extension,
   and seems almost counterintuitive to the declarative nature of a tool like terraform. A better approach would be to take advantage of terraform's inbuilt variable specific capabilities to fully
  detatch configurations into a single file which can be changed as needed. The output also provides the ip-addresses for the created instances.

* ### Methodology
    There is a main terraform HCL file that imports and runs the various modules while exchanging variables between them through terraform's robust outputs functionailty.
  This provides a very modular structure which makes it easier for madules to be added and removed with very little changes required. The modules are split into `networking`:
  which creates all the networking resources like the vpc, subnets, gateways etc; `instances`: which creates the servers (ec2-instances) for Postgreql to run on; `security_groups`: which contain the firewall rules
  for internal and external network communication. Variables are used where possible and their configuration is centrally controlled through a single .tfvars file. Primary DB and replicas are spread over multiple
  zones for reliability. 

* ### Improvements
  * Storage module to be added providing control over attached volumes used by the instances running postgress
  * Different default configurations based on variables like region, environment etc applied automatically.
  * A more robust output to enable querying of resources from state file
 
## Configuration management

*  ### Approach
      To set up a PostgreSQL primary-read-replica architecture, ansible had to connect to each instance to install and configure postgreSQL on it. For security, ansible will connect to a bastion host with a public
   ip-address and do a proxy jump to the DB instances in the private subnet. The terraform config allowed a variable number of replicas so ansible should also be able to hande a variable amount of replicas.
   
* ### Methodology
    The hosts are populated in an inventory file that also defines how ansible will connect to them. They are grouped so that tasks can be conditionally performed on primary and/or replica servers as needed.
   The tasks have been split into three files for easier maintenance and changes `install`: for adding repos and downloading/installing postgres and any dependencies.
  `configure`: this configures the primary server's by writing jinja templated postgreql.conf(configuration) file. `replicate`: which sets up replication by setting up a
  replication user, writing a jinja templated pg_hba.conf(auth) on the primary and setting the replicas into read-only hot standby mode.

* ### Improvements
  * Making it OS independent. Since the terraform config allows different amis to be used; playbooks can be added with OS appropriate tasks that run depending on host OS
  * Extending functionalaity by adding tasks allowing user creation, db creation and other such DB admin tasks that need to run initially
  
## Automation API

* ### Approach
  Python was the language of choice because time to build is the smallest with it. It has good libraries for building APIs and is much easier to set up. The structure follows a modular approach defining controllers,
  utilities, templates and configs seperately allowing it to be extensible. The endpoints were defined first followed by the development of it's functionality. Usage of subprocess was preffered since the different tools
  were developed independently so using the native CLI is better when compared to using SDK libraries since additions to functionality will be hard to refactor everywhere.

* ### Methodology
  Configuration changes were carried out using jinja templating; to both generate the .tfvars file, the hosts.ini file, the ansible config as well as the postgress_settings file. Commands for both terraform and ansible
  carried out with the use of subprocess. Terraform and Ansible have seperate controllers driven by seperate utils with a config to define all the constants, configurations and file paths. When `/terraform/generate` is called,
  the inputs are verified and used to generate a .tfvars file with jinja templates. Other terraform api call commands and return the STOUT along with appropriate messages. When `/ansible/configure` is the output variables from terraform
  are obtained using `terraform output` and used to populate the hosts.ini and ansible.cfg file with instance ip addresses. It also populates the postgress_settings var file.

* ### Improvements
  * Better input validation for .tfvars file by parsing the variables.tf to automatically recognise required, valid and optional variable names
  * Stream processing for the STOUT so human users can get a streamed output from subprocess commands
  * Tests for validating unit-level logic and presence of required binaries in the environment
  
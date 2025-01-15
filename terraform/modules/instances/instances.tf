resource "aws_instance" "bastion" {
  ami           = var.bastion_ami
  instance_type = var.bastion_instance_type
  subnet_id     = var.public_subnet_id
  key_name      = var.bastion_key_pair
  security_groups = [var.bastion_sg_id]

  # user_data = <<-EOF
  #   #!/bin/bash
  #   # Update the system
  #   apt-get update -y
  #   apt-get upgrade -y

  #   # Install Ansible dependencies
  #   apt-get install -y software-properties-common

  #   # Add the Ansible PPA (Personal Package Archive)
  #   add-apt-repository ppa:ansible/ansible -y

  #   # Update apt sources again after adding PPA
  #   apt-get update -y

  #   # Install Ansible
  #   apt-get install -y ansible

  #   # Verify Ansible installation
  #   ansible --version
  # EOF

  tags = {
    Name = "bastion-host"
  }
  
}

resource "aws_eip_association" "bastion_eip_assoc" {
  instance_id   = aws_instance.bastion.id
  allocation_id = var.bastion_eip_id
}

resource "aws_instance" "db_primary" {
  ami           = var.postgresql_ami
  instance_type = var.db_instance_type
  subnet_id     = var.private_subnet_ids[0]
  key_name      = var.db_key_pair
  security_groups = [var.db_sg_id]

  # user_data = <<-EOF
  #   #!/bin/bash
  #   # Update the system
  #   apt-get update -y
  #   apt-get upgrade -y

  #   # Install Ansible dependencies
  #   apt-get install -y software-properties-common

  #   # Add the Ansible PPA (Personal Package Archive)
  #   add-apt-repository ppa:ansible/ansible -y

  #   # Update apt sources again after adding PPA
  #   apt-get update -y

  #   # Install Ansible
  #   apt-get install -y ansible

  #   # Verify Ansible installation
  #   ansible --version
  # EOF

  tags = {
    Name = "db-primary"
  }
}

resource "aws_instance" "db_replica" {
  count         = var.replica_count
  ami           = var.postgresql_ami
  instance_type = var.db_instance_type
  subnet_id     = element(var.private_subnet_ids, count.index + 1)
  key_name      = var.db_key_pair
  security_groups = [var.db_sg_id]

  # user_data = <<-EOF
  #   #!/bin/bash
  #   # Update the system
  #   apt-get update -y
  #   apt-get upgrade -y

  #   # Install Ansible dependencies
  #   apt-get install -y software-properties-common

  #   # Add the Ansible PPA (Personal Package Archive)
  #   add-apt-repository ppa:ansible/ansible -y

  #   # Update apt sources again after adding PPA
  #   apt-get update -y

  #   # Install Ansible
  #   apt-get install -y ansible

  #   # Verify Ansible installation
  #   ansible --version
  # EOF

  tags = {
    Name = "db-replica-${count.index + 1}"
  }
}
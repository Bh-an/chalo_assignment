variable "bastion_ami" {
  description = "AMI for bastion instance creation"
  default = "ami-0f2e255ec956ade7f"
}

variable "public_subnet_id" {
  description = "subnet id for bastion instance"
}

variable "bastion_key_pair" {
  description = "key pair for bastion instance"
}

variable "bastion_sg_id" {
  description = "security group id for bastion host"
}

variable "bastion_instance_type" {
  description = "Instance type for bastion"
}

variable "bastion_eip_id" {
  description = "elastic ip id for bastion"
}

variable "postgresql_ami" {
  description = "AMI for postgresql instance creation"
  default = "ami-0f2e255ec956ade7f"
}


variable "replica_count" {
  description = "Number of required replica instances"
}

variable "db_instance_type" {
  description = "Instance type for DB"
}

variable "private_subnet_ids" {
  description = "subnet id for db instances"
}

variable "db_key_pair" {
  description = "key pair for bastion instances"
}

variable "db_sg_id" {
  description = "security group id for db instances"
}
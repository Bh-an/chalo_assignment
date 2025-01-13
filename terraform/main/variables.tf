variable "region" {

}

variable "environment" {

}

variable "vpc_cidr" {

}

variable "public_subnet_block" {

}

variable "private_subnets_block" {

}

variable "bastion_ami" {
  description = "AMI for bastion instance creation"
  default = "ami-0f2e255ec956ade7f"
}

variable "bastion_key_pair" {
  description = "key pair for bastion instance"
}


variable "bastion_instance_type" {
  description = "Instance type for bastion"
  default = "t2.micro"
}

variable "postgresql_ami" {
  description = "AMI for postgresql instance creation"
  default = "ami-0f2e255ec956ade7f"
}


variable "replica_count" {
  description = "Number of required replica instances"
  default = "2"
}

variable "db_instance_type" {
  description = "Instance type for DB"
  default = "t2.micro"
}

variable "db_key_pair" {
  description = "key pair for bastion instances"
}
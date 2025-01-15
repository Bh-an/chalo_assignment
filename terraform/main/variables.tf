variable "region" {
  description = "aws region"
  default = "ap-south-1"
}

variable "environment" {
  description = "deployment environment tag for provisioned resources"
  default = "dev"
}

variable "vpc_cidr" {
  description = "cidr block for vpc creation"
  default = "10.0.0.0/16"
}

variable "public_subnet_block" {
  description = "cidr block for public subnet which bastion lives in"
  default = "10.0.1.0/24"
}

variable "private_subnets_block" {
  description = "cidr blocks of private subnet for rds instances, should ideally match count"
  default = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

variable "bastion_ami" {
  description = "AMI for bastion instance creation"
  default = "ami-023a307f3d27ea427"
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
  default = "ami-023a307f3d27ea427"
}


variable "replica_count" {
  description = "Number of required replica instances"
  default = "2"
}

variable "db_instance_type" {
  description = "Instance type for DB"
  default = "t2.small"
}

variable "db_key_pair" {
  description = "key pair for bastion instances"
}
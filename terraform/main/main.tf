provider "aws" {
    region = var.region
}

locals {
  availaibility_zones = ["${var.region}a", "${var.region}b"]
}

module "networking" {
    source = "../modules/networking"
    region=var.region
    environment=var.environment
    vpc_cidr=var.vpc_cidr
    public_subnet_cidr=var.public_subnet_block
    private_subnets_cidr=var.private_subnets_block
    availability_zones=local.availaibility_zones

}

module "security_groups" {
     depends_on = [
        module.networking
    ]
    source = "../modules/security_groups"
    vpc_id = module.networking.vpc_id
}

module "instances" {
     depends_on = [
        module.security_groups,
        module.networking
    ]
    source = "../modules/instances"
    bastion_ami = var.bastion_ami
    public_subnet_id = module.networking.public_subnet_id
    bastion_key_pair = var.bastion_key_pair
    bastion_sg_id = module.security_groups.bastion_sg_id
    bastion_instance_type = var.bastion_instance_type
    bastion_eip_id = module.networking.bastion_eip_id
    postgresql_ami = var.postgresql_ami
    replica_count = var.replica_count
    db_instance_type = var.db_instance_type
    private_subnet_ids = module.networking.private_subnet_ids
    db_key_pair = var.db_key_pair
    db_sg_id = module.security_groups.db_sg_id

}


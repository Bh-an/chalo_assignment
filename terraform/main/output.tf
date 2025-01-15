output "bastion_eip_address" {
    value = module.networking.bastion_eip_address
}

output "primary_db_addr" {
    value = module.instances.primary_db_ip
}

output "replica_db_addresses" {
    value = module.instances.replica_db_ips
}
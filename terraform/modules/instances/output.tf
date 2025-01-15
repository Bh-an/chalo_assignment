output "primary_db_ip" {
  value = aws_instance.db_primary.private_ip
}

output "replica_db_ips" {
  value = aws_instance.db_replica[*].private_ip
}
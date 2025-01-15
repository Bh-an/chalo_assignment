# VPC
resource "aws_vpc" "vpc" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

# Public subnet(s)
resource "aws_subnet" "public_subnet" {
    depends_on = [aws_vpc.vpc]
    vpc_id                  = aws_vpc.vpc.id
    cidr_block              = var.public_subnet_cidr
    availability_zone       = element(var.availability_zones, 0)
    map_public_ip_on_launch = false
    tags = {
        Name        = "${var.environment}-${var.region}-public-subnet"
        Environment = "${var.environment}"
    }
}

# Private Subnet
resource "aws_subnet" "private_subnet" {
  depends_on = [aws_vpc.vpc]
  vpc_id                  = aws_vpc.vpc.id
  count                   = length(var.private_subnets_cidr)
  cidr_block              = element(var.private_subnets_cidr, count.index)
  availability_zone       = element(var.availability_zones, (count.index % length(var.availability_zones)))
  map_public_ip_on_launch = false

  tags = {
    Name        = "${var.environment}-${element(var.availability_zones, (count.index % length(var.availability_zones)))}-private-subnet"
    Environment = "${var.environment}"
  }
}


# Internet Gateway for Public Subnet
resource "aws_internet_gateway" "ig" {
  depends_on = [aws_subnet.public_subnet]
  vpc_id = aws_vpc.vpc.id
  tags = {
    Name        = "${var.environment}-igw"
    Environment = var.environment
  }
}

# Elastic-IP (eip) for NAT
resource "aws_eip" "nat_eip" {
  depends_on = [aws_internet_gateway.ig]
  tags = {
    Name        = "eip"
    Environment = "${var.environment}"
  }

}

# NAT for private subnet
resource "aws_nat_gateway" "nat" {
  depends_on = [aws_eip.nat_eip]
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = element(aws_subnet.public_subnet.*.id, 0)

  tags = {
    Name        = "nat"
    Environment = "${var.environment}"
  }
}


# Routing tables to route traffic for Private Subnet
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name        = "${var.environment}-private-route-table"
    Environment = "${var.environment}"
  }
}

# Routing tables to route traffic for Public Subnet
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name        = "${var.environment}-public-route-table"
    Environment = "${var.environment}"
  }
}

# Route for Internet Gateway
resource "aws_route" "public_internet_gateway" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.ig.id
}

# Route for NAT
resource "aws_route" "private_nat_gateway" {
  route_table_id         = aws_route_table.private.id
  destination_cidr_block = "0.0.0.0/0"
  nat_gateway_id         = aws_nat_gateway.nat.id
}

# Route table associations for both Public & Private Subnets
resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public_subnet.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = length(var.private_subnets_cidr)
  subnet_id      = element(aws_subnet.private_subnet.*.id, count.index)
  route_table_id = aws_route_table.private.id
}

# Elastic IP for bastion host
resource "aws_eip" "bastion_eip" {
  depends_on = [aws_internet_gateway.ig]
  domain = "vpc"
}


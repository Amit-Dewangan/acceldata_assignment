provider "aws" {
  region = var.region
}

data "aws_availability_zones" "available" {}


resource "aws_db_subnet_group" "test_psql" {
  name       = "test-psql"
  subnet_ids = ["subnet-03f0caabb603b8431","subnet-0c65adb2ca3db763b"]

  tags = {
    Name = "test-psql"
  }
}

resource "aws_security_group" "rds" {
  name   = "test_psql_rds"
  vpc_id = "vpc-047587b4d264163ef"

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  egress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "test_rds_psql"
  }
}

resource "aws_db_parameter_group" "test_psql" {
  name   = "test-psql"
  family = "postgres14"

  parameter {
    name  = "log_connections"
    value = "1"
  }
}

# provider "random" {}

# resource "random_pet" "random" {
#   length = 1
# }

resource "aws_db_instance" "test_psql" {
  identifier             = "test-psql"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "14.7"
  username               = "postgres"
  password               = "postgres"
  db_subnet_group_name   = aws_db_subnet_group.test_psql.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  parameter_group_name   = aws_db_parameter_group.test_psql.name
  publicly_accessible    = true
  skip_final_snapshot    = true
}
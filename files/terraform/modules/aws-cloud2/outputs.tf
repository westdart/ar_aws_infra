output "vpc" {
  value = aws_vpc.cloud
}

output "vpc-id" {
  value = aws_vpc.cloud.id
}

output "public_route_id" {
  value = aws_route_table.public_route.id
}
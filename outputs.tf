output "knowledge_bucket_name" {
  value = aws_s3_bucket.knowledge.bucket
}

output "api_endpoint" {
  value = aws_apigatewayv2_api.http_api.api_endpoint
}

output "chat_api_url" {
  value = "${aws_apigatewayv2_api.http_api.api_endpoint}/chat"
}

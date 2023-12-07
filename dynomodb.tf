
resource "aws_dynamodb_table" "bookmark-test1.0" {
  name           = "bookmark-test"
  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = "postid"
    type = "S"
  }
  attribute {
    name = "userid"
    type = "S"
  }

  hash_key = "postid"
  range_key = "userid"
}

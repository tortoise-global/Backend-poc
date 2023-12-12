
/*
resource "aws_dynamodb_table" "bookmarksample" {
  name           = "bookmarksample"
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



resource "aws_dynamodb_table" "lastbookmarksampletest" {
  name           = "lastbookmarksampletest"
  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = "postid"
    type = "S"
  }
  

  hash_key = "postid"

}
*/


resource "aws_dynamodb_table" "bookmark_example" {
  name           = "bookmark_example"
  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = "postid"
    type = "S"
  }
  

  hash_key = "postid"

}


resource "aws_dynamodb_table" "lastbookmark_example" {
  name           = "lastbookmark_example"
  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = "postid"
    type = "S"
  }
  

  hash_key = "postid"

}



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


resource "aws_dynamodb_table" "post" {
  name           = "post"
  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = "postid"
    type = "S"
  }
  

  hash_key = "postid"

}



/*
resource "aws_dynamodb_table" "testingrollback" {
  name           = "testingrollback"
  billing_mode   = "PAY_PER_REQUEST"

  attribute {
    name = "rollbackid"
    type = "S"
  }
  

  hash_key = "rollbackid"

}
*/



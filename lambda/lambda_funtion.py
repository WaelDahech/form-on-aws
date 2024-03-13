import json
import boto3

# Create the DynamoDB client
dynamodb = boto3.client('dynamodb')
# Set the name of the DynamoDB table
table_name = 'form'
s3_client = boto3.client('s3')
bucket_name = 'safahat-form-upload'
expiration = 3600  # URL expiration time in seconds


def lambda_handler(event, context):


   # Parse the JSON data passed to the Lambda function
   print(event)
   data = event
   # Extract the values from the data
   
   name = data['name']
   surname = data["surname"]
   age = data["age"]
   state=data["state"]
   city = data["city"]
   email = data['email']
   phone= data["phone"]
   filename = data["filename"]
   
   key_to_check = {'email': {'S': email}}

   try:
      response = dynamodb.get_item(
            TableName=table_name,
            Key=key_to_check,
            ConsistentRead=True  # Optional: Whether to use consistent read or not
        )
        
        # If the item is found, response will contain the item
      if 'Item' in response:
         return {
                 'statusCode': 200,
                    'url': 'already_exist'
                     }
   except Exception as e:
        return f"Error: {str(e)}"

   # Create an item to put in the DynamoDB table
   item = {
      'name': {'S': name},
      'surname': {'S': surname},
      'age': {'S': age},
      'email': {'S': email},
      'phone': {'S': phone},
      'state': {'S': state},
      'city': {'S': city},
      'filename': {'S': filename}


   }
   
   # response = table.put_item(
   #     Item={
   #          'name': name,
   #          'email': email
   #     }
   #  )
   # Put the item in the DynamoDB table
   response = dynamodb.put_item(
      TableName=table_name,
      Item=item
   )
   key = email + "/" + filename
   
   try:
      presigned_url = s3_client.generate_presigned_url(
           'put_object',
            Params={'Bucket': bucket_name, 'Key': key},
            ExpiresIn=expiration,
            HttpMethod='PUT'
        )
      return {
            'statusCode': 200,
            'url' : presigned_url
        }
   except Exception as e:
      return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
   
   

   
   
import boto3
s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('customer')
def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    csv_file_name = event['Records'][0]['s3']['object']['key']
    csv_object = s3_client.get_object(Bucket=bucket,Key=csv_file_name)
    file_reader = csv_object['Body'].read().decode("utf-8")
    print(file_reader)
    users = file_reader.split("\n")
    users = list(filter(None, users))
    for user in users:
        user_data = user.split(",")
        table.put_item(Item = {
            "CustomerID" : user_data[0],
            "CustomerName" : user_data[1],
            "CustomerType" : user_data[2],
            "MarketBase" : user_data[3],
            "Transaction" : user_data[4]
        })
    return 'success'

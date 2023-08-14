from app import lambda_handler

# Define a test event (You can modify this as needed to simulate different EventBridge payloads)
test_event = {}

# Define a test context (a mock, since it's only needed if you access context attributes in your function)
test_context = {}

# Invoke the lambda function handler
response = lambda_handler(test_event, test_context)

# Print the response
print(response)

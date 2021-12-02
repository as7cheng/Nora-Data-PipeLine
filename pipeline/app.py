"""
File to start the application
"""
import json
import deliver_data
import data_log


PROCESS_PROMPT = '========Data Piepline======'

def handler(event, lambda_context):
    """
    Function to handle lambda request
    """
    print(event)
    print(lambda_context)
    data_log.send_log(PROCESS_PROMPT)
    res = deliver_data.deliver()
    response = {
        'statusCode': 200,
        'body': json.dumps(res)
    }
    # print(response)
    return response

def lambda_handler():
    """
    Function to handle the request sent to lambda function
    """
    data_log.send_log(PROCESS_PROMPT)
    deliver_data.deliver()


import azure.functions as func
import logging
import json
import requests
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import base64
from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logging.info("step1 %s", req)  # Use %s as a placeholder for req
        req_body = req.get_json()
        
        # logging.info("step2 %s,%s", req_body["name"],req_body["email"])  # Use %s as a placeholder for req_body
        # Airtable API settings
        base_url = "https://api.airtable.com/v0/appI34Vn7ZF4w0qYK/tbl0a4R9VODJ08u3M"
        api_key = "pat3IE7xoc7es7kb8.1e70fbf139f3d5720a1911db4985452c2a91491dd761ef83b761498b427ba9a5"
        
        # Record Details to add
        PoleID = req_body["PoleID"]
        Community = req_body["Community"]
        ReportedBy = req_body["ReportedBy"]
        Issue = req_body["Issue"]
        IssueReportedOn = req_body["IssueReportedOn"]
        
        ScannedVal =  req_body["scanner"]
        lat =  req_body["lat"]
        long =  req_body["long"]
        Severity =  req_body["severity"]
        
        #Set Up Blob Service Client:
        connection_string = "DefaultEndpointsProtocol=https;AccountName=reportformb837;AccountKey=a4xNi9g6P2OofjEGXx3GXzhiiRE3v1tzalCDzssyaDmTMCVCTbq3v/lxyW07dRr/d9u7jtjdY5+E+AStqqzOiQ==;EndpointSuffix=core.windows.net"
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        #Upload Image to Blob Container:

        container_name = "testimages"
        blob_name = f'{random_with_N_digits(5)}' + ".png"  # Replace with your desired blob name
        #local_file_path = "/Users/apekshasaraf/Desktop/"  # Replace with your local image path
        base64_image_data = "iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAhGVYSWZNTQAqAAAACAAFARIAAwAAAAEAAQAAARoABQAAAAEAAABKARsABQAAAAEAAABSASgAAwAAAAEAAgAAh2kABAAAAAEAAABaAAAAAAAAAEgAAAABAAAASAAAAAEAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAQKADAAQAAAABAAAAQAAAAAC1ay+zAAAACXBIWXMAAAsTAAALEwEAmpwYAAACyGlUWHRYTUw6Y29tLmFkb2JlLnhtcAAAAAAAPHg6eG1wbWV0YSB4bWxuczp4PSJhZG9iZTpuczptZXRhLyIgeDp4bXB0az0iWE1QIENvcmUgNi4wLjAiPgogICA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogICAgICA8cmRmOkRlc2NyaXB0aW9uIHJkZjphYm91dD0iIgogICAgICAgICAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgICAgICAgICAgeG1sbnM6ZXhpZj0iaHR0cDovL25zLmFkb2JlLmNvbS9leGlmLzEuMC8iPgogICAgICAgICA8dGlmZjpZUmVzb2x1dGlvbj43MjwvdGlmZjpZUmVzb2x1dGlvbj4KICAgICAgICAgPHRpZmY6UmVzb2x1dGlvblVuaXQ+MjwvdGlmZjpSZXNvbHV0aW9uVW5pdD4KICAgICAgICAgPHRpZmY6WFJlc29sdXRpb24+NzI8L3RpZmY6WFJlc29sdXRpb24+CiAgICAgICAgIDx0aWZmOk9yaWVudGF0aW9uPjE8L3RpZmY6T3JpZW50YXRpb24+CiAgICAgICAgIDxleGlmOlBpeGVsWERpbWVuc2lvbj42NDwvZXhpZjpQaXhlbFhEaW1lbnNpb24+CiAgICAgICAgIDxleGlmOkNvbG9yU3BhY2U+MTwvZXhpZjpDb2xvclNwYWNlPgogICAgICAgICA8ZXhpZjpQaXhlbFlEaW1lbnNpb24+NjQ8L2V4aWY6UGl4ZWxZRGltZW5zaW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4Kiv76YwAAAI9JREFUeAHt1QENwCAQBEGoaPQgAn8lwcZOHXDZ6c+z9j/C3xd++3u6ARQQXwCBeABDAQqIL4BAPAA/QQQQiC+AQDwAVwABBOILIBAPwBVAAIH4AgjEA3AFEEAgvgAC8QBcAQQQiC+AQDwAVwABBOILIBAPwBVAAIH4AgjEA3AFEEAgvgAC8QBcAQQQiC9wAUZxA0mbqL7zAAAAAElFTkSuQmCC"

        container_client = blob_service_client.get_container_client(container_name)

        decoded_image_data = base64.b64decode(base64_image_data)


        with container_client.get_blob_client(blob_name) as blob_client:
            blob_client.upload_blob(decoded_image_data)
        
        # Setup complete url for blob image
        url = "https://reportformb837.blob.core.windows.net/testimages/" + blob_name
        
        payload = json.dumps({
        "records": [
            {
            "fields": {
                "PoleID": PoleID,
                "Community": Community,
                "ReportedBy": ReportedBy,
                "Issue": Issue,
                "IssueReportedOn": IssueReportedOn,
                "PoleImage": [
                {
                    "url": url
                }
                ],
                "ScannedVal": ScannedVal,
                "lat" : lat,
                "long": long,
                "Severity" : Severity
            }
            }
        ]
        })
        
        
        # Send the POST request to update the record
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", base_url, headers=headers, data=payload)
        logging.info(response.text)
        # Your processing logic here

        return func.HttpResponse("Request processed successfully.", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
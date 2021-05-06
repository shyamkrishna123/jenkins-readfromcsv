import pandas as pd
import datetime
import argparse
import requests
import json
from pandas.core.frame import DataFrame
class SendNotification:
    def __init__(self, input_file: str, build_url: str, build_status: str) -> None:
        self.input_file = input_file
        self.build_url = build_url
        self.build_status = build_status
        
    def read_response_from_csv(self) -> DataFrame:
        col_list = ["URL", "responseCode", "responseMessage", "success", "failureMessage"]
        data = pd.read_csv(self.input_file, usecols=col_list)
        return data
    
    def generate_payload(self):
        results = self.read_response_from_csv()
        table_content = ''
        for result in results.index:
            if results['responseCode'][result] != 200:
                table_content = table_content+"<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(results['URL'][result], results['responseCode'][result], results['responseMessage'][result], results['success'][result], results['failureMessage'][result])
        html_table = "<table bordercolor='black' border= '2'><thead><tr style = 'background-color : Teal; color: White'><th>URL</th><th>responseCode</th><th>responseMessage</th><th>success</th><th>failureMessage</th></tr></thead></thead><tbody>{}</tbody></table>".format(table_content)
        date = datetime.datetime.now()
        date = date.isoformat()
        payload = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": "Perfomance Result",
            "sections": [
                {
                    "activityTitle": "Perfomance Result",
                    "activitySubtitle": date,
                    "activityImage": "",
                    "facts": [
                        {
                        "name": "webapp",
                        "value": "Prod"
                        }
                    ],
                    "markdown": True
                },
                {
                    "startGroup": True,
                    "text": html_table}
            ],
            "potentialAction": [{
                "@type": "OpenUri",
                "name": "Build Url",
                "targets": [{
                    "os": "default",
                    "uri": self.build_url
                }]
            },  {
                "@type": "OpenUri",
                "name": self.build_status,
                "targets": [{
                    "os": "default",
                    "uri": self.build_url
                }]
            }]
        }
        return payload
        
    def send_reponse_to_team(self) -> None:
        payload = json.dumps(self.generate_payload())
        url = "https://merckgroup.webhook.office.com/webhookb2/2ab1469d-2271-4f35-9e65-f7f5971e8bd6@db76fb59-a377-4120-bc54-59dead7d39c9/IncomingWebhook/7a4be16453004c3e96ed43354cbfe074/82012211-8afb-4d42-b7fa-4421bfe4eac5"
        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache"
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return(response.text)
        
        
def get_argparser() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(description="Specify the file")
    arg_parser.add_argument("input_file", metavar="path", type=str, help="the path to file")
    arg_parser.add_argument("build_url", metavar="url", type=str, help="build url of the job")
    arg_parser.add_argument("build_status", metavar="status", type=str, help="build status of the job")
    
    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    arg_parser = get_argparser()
    send_notification = SendNotification(arg_parser.input_file, arg_parser.build_url, arg_parser.build_status )
    send_notification.send_reponse_to_team()

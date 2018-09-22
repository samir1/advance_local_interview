
import boto3
from chalice import Chalice, Response
import datetime
import random
import requests
import logging
import uuid

states_list = [

    'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
    'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
    'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
    'Maine' 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
    'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
    'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
    'North Carolina', 'North Dakota', 'Ohio',
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
    'South  Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
    'Vermont', 'Virginia', 'Washington', 'West Virginia',
    'Wisconsin', 'Wyoming'
]

app = Chalice(app_name='advancelocal')
s3 = boto3.client('s3')
kms_client = boto3.client('kms')
BUCKET = 'advancelocal-samir'
keys = dict()

key_lists = kms_client.list_resource_tags(
    KeyId='f6f4d761-dd36-4a27-a055-11f219883aa9')['Tags']
keys[key_lists[0]['TagKey']] = key_lists[0]['TagValue']


def get_five_articles_from_query(query):
    json_data = requests.get(
        "https://content.guardianapis.com/search?q=" +
        query + "&api-key=" + keys['guardian_api_key']).json()
    articles = {}
    for article in json_data['response']['results']:
        articles[article['webTitle']] = article['webUrl']

    return articles


@app.route('/status', methods=['GET'])
def status():
    return {'status': 'OK',
            'current-time': str(datetime.datetime.now())}


@app.route('/news_for_state', methods=['GET'])
def news_for_state():
    state = random.choice(states_list)
    return get_five_articles_from_query(state)


@app.route('/news_for_state/{state}', methods=['GET'])
def news_for_state(state):
    if state == 'random':
        state = random.choice(states_list)
    return get_five_articles_from_query(state)

# Upload file with:
# curl --header "Content-Type:image/png" --data-binary @file.png -X POST https://[rest_api_id].execute-api.us-east-1.amazonaws.com/api/upload_png
@app.route('/upload_png', methods=['POST'], content_types=['image/png'])
def upload_png():
    try:
        body = app.current_request.raw_body
        key = str(uuid.uuid4())
        img_filename = key + '.png'
        html_filename = key + '.html'
        s3.put_object(Body=body, Bucket=BUCKET,
                      Key=img_filename, ACL='public-read')
        html = open('template.html', 'r').read().replace('{key}', img_filename)
        s3.put_object(Body=html, Bucket=BUCKET,
                      Key=html_filename, ACL='public-read')
        return Response(body='https://s3.amazonaws.com/advancelocal-samir/'+html_filename,
                        status_code=200,
                        headers={'Content-Type': 'text/plain'})

    except Exception as e:
        logging.exception(e)
        app.log.error("error occurred during upload {e}".format(e))
        return Response(message={
            'status': 'ERROR',
            'reason': "{e}".format(e)},
            header={'Content-Type': 'application/json'},
            status_code=400)

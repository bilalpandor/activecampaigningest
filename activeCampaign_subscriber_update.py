import aws_glcUsers

all_users = aws_glcUsers.get_all_users()
allMarketing = aws_glcUsers.getMarketingList()


all_users_neat = []
uniqueUser = {}
for i in all_users:
    email = ''
    name = ''
    subscription_status = ''
    for j in i['Attributes']:
        if j['Name'] == 'email':
            email = j['Value']
        if j['Name'] == 'given_name':
            name = j['Value'].split(' ')[0]
        if j['Name'] == 'custom:subscription_status':
            subscription_status = j['Value']
    try:
        uniqueUser[email]
    except:
        all_users_neat.append({
            'email':email,
            'name':name,
            'source':"cognito_registered",
            'subscription_status':subscription_status,
            'createTime':i['UserCreateDate']
        })
        uniqueUser[email] = 1

import re

# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


# Define a function for
# for validating an Email
def check(email):
    # pass the regular expression
    # and the string into the fullmatch() method
    if (re.fullmatch(regex, email)):
        return True

    else:
        return False

for i in allMarketing:
    groups = ['e9Lp9B']
    try:
        uniqueUser[i['email']['S']]
    except:
        if check(i['email']['S']):
            all_users_neat.append({
                'email':i['email']['S'],
                'name':'there',
                'source':"dynamo_marketing",
                'subscription_status': "Only Email",
                'createTime':i['createTime']['N']
            })
            uniqueUser[i['email']['S']] = 1
        else:
            print(i['email']['S'])



####get sender

activeCampaign_token = "b5f6ff02cdf779fb58298cf00b2c0cb5dc2f76d747a3c4f6ba63a4b01dbc3fbe9a6ed648"
import requests
import json



thisStepStart = 0

while thisStepStart < len(all_users_neat):
    thisStepEned = thisStepStart+200
    url = "https://glcoverage52987.activehosted.com/api/3/import/bulk_import"
    payload = { }
    payload['contacts'] = []
    for thisUser in all_users_neat[thisStepStart:thisStepEned]:
        if thisUser['email'] != "" and thisUser['email'] != None:
            payload['contacts'].append({
                "email": thisUser['email'],
                "first_name": thisUser['name'],
                "tags": [thisUser['subscription_status']],
            })

    headers = {
        "Api-Token": activeCampaign_token,
        #"Content-Type": "application/json",
        "accept": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    thisStepStart += 200
    print(str(thisStepStart))
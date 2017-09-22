# -*- coding: utf-8 -*-

import json, requests, sys, getpass

def get_token():
    print "\nEnter User name"
    user_id = sys.stdin.readline()
    user_id = user_id.rstrip('\n')

    print '\nEnter Password'
    password = getpass.getpass()

    post_token_data = {'url_name': user_id, 'password': password}
    token_request = requests.post(url='https://qiita.com/api/v1/auth', data=post_token_data)

    if "token" in token_request.json:
        print "Verify"
        return token_request.json
    else:
        print "Wrong User id or Password"
        exit()

#--------------------------------------------
# Cheak my dailyreport
#--------------------------------------------
print "\nBrowse your post \n If you want to browse Qiita Team, Enter Team name, \n otherwise, press Enter"

team_id = sys.stdin.readline()
team_id = team_id.rstrip('\n')

token = get_token()

# Without Token ... display only PUBLISHED posts
#url = "https://qiita.com/api/v1/users/tksh_nkmr/items

# With Token
url = "https://qiita.com/api/v1/users/" + token['url_name']  + "/items?token=" + token['token']

# DO NOT Encode parameter
values ={'team_url_name': team_id}

if len(team_id) > 0:
    ret = requests.get(url=url, data = values)
else:
    ret = requests.get(url=url)

print ret.json


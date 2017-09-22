# -*- coding: utf-8 -*-
import os, os.path, re, sys, codecs, requests, json, getpass, time

#============================================
# Check the path
#============================================
# Set path
path = 'hogehoge/hoge/foo'

#-------------------------------------
# User authentication, obtain token
#-------------------------------------
def get_token():
    print "\nEnter the user name"
    user_id = sys.stdin.readline()
    user_id = user_id.rstrip('\n')

    print '\nEnter the pass work'
    password = getpass.getpass()

    post_token_data = {'url_name': user_id, 'password': password}
    token_request = requests.post(url='https://qiita.com/api/v1/auth', data=post_token_data)

    if "token" in token_request.json:
        print "Varify"
        return token_request.json
    else:
        print "Wround User id or Password"
        exit()
#-------------------------------------
# Change encoding to utf-8
#-------------------------------------
def guess_charset(data):
    f = lambda d, enc: d.decode(enc) and enc

    try: return f(data, 'utf-8')
    except: pass
    try: return f(data, 'shift-jis')
    except: pass
    try: return f(data, 'iso2022-jp')
    except: pass
    try: return f(data, 'cp932')
    except: pass
    return None

def conv(data):
    charset = guess_charset(data)
    u = data.decode(charset)
    return u.encode('utf-8')

#-------------------------------------
# Post
#-------------------------------------
print "\nEnter Qiita Team name"
team_id = sys.stdin.readline()
team_id = team_id.rstrip('\n')

token = get_token()

# The URL to post Qiita:team
post_url = 'https://qiita.com/api/v1/items?token=' + token['token']

# json type of data
headers = {'Content-type': 'application/json'}

objective_dirs =[]

# obtain dir path
for root, dirs, files in os.walk(path):
    for dir in dirs:
        objective_dirs.append(os.path.join(root, dir))       
#print objective_dirs

#-------------------------------------------------
# files: DIR name
# tag_list: Tag for files
#-------------------------------------------------
for files in objective_dirs:
    print files
    texts = os.listdir(files)
    for file in texts:
        file_name, ext = os.path.splitext(file)
        #check the extention
        if ext == '.txt' or ext == '.TXT':
            f = open(files + '/' + file)
            text_data = f.read()
            f.close
            
            # encoding 
            try:
                text_data = conv(text_data)
            except:
                continue

            print file_name

            # Tag to json
            tag_array = []
            tag_dict = {}
            tag_line = files[len(path)+1:]
            tag_list = tag_line.split('/')
            
            for i in tag_list:
                tag_dict = { "name" : i}
                tag_array.append(tag_dict)

            # restructure input data
            post_data ={
                "title": file_name,
                "body": text_data,
                "tags": tag_array
                }
            if len(team_id) > 0:
                post_data["team_url_name"] = team_id
            #else:
                #post_data["private"] = False

            # http post request 
            post_request = requests.post(url=post_url, data=json.dumps(post_data), headers=headers)
            print post_request

            time.sleep(24)
            

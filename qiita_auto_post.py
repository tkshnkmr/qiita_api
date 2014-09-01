# -*- coding: utf-8 -*-
import os, os.path, re, sys, codecs, requests, json, getpass, time

#============================================
# Path を確認すること
#============================================
# パスを設定
path = 'hogehoge/hoge/foo'

#-------------------------------------
# ユーザー認証，トークンの取得
#-------------------------------------
def get_token():
    print "\nユーザー名を入力して下さい"
    user_id = sys.stdin.readline()
    user_id = user_id.rstrip('\n')

    print '\nパスワードを入力して下さい'
    password = getpass.getpass()

    post_token_data = {'url_name': user_id, 'password': password}
    token_request = requests.post(url='https://qiita.com/api/v1/auth', data=post_token_data)

    if "token" in token_request.json:
        print "認証成功"
        return token_request.json
    else:
        print "User id, または Password が違います．"
        exit()
#-------------------------------------
# エンコーディングをutf-8にする
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
# 投稿する
#-------------------------------------
print "\nQiita Team名を入力して下さい"
team_id = sys.stdin.readline()
team_id = team_id.rstrip('\n')

token = get_token()

# Qiita:team にポストするURL
post_url = 'https://qiita.com/api/v1/items?token=' + token['token']

# post 用のヘッダーはjson
headers = {'Content-type': 'application/json'}

objective_dirs =[]

# path以下のディレクトリを取得
for root, dirs, files in os.walk(path):
    for dir in dirs:
        objective_dirs.append(os.path.join(root, dir))       
#print objective_dirs

#-------------------------------------------------
# files : ディレクトリ名
# tag_list : ファイルごとのタグ(path以降のディレクトリ名)
#-------------------------------------------------
for files in objective_dirs:
    print files
    texts = os.listdir(files)
    for file in texts:
        file_name, ext = os.path.splitext(file)
        #もし拡張子が.txtだったら
        if ext == '.txt' or ext == '.TXT':
            # ファイル読み込み
            f = open(files + '/' + file)
            text_data = f.read()
            f.close
            
            # encoding 
            try:
                text_data = conv(text_data)
            except:
                continue

            print file_name

            # Tagをjson形式に整える
            tag_array = []
            tag_dict = {}
            tag_line = files[len(path)+1:]
            tag_list = tag_line.split('/')
            
            for i in tag_list:
                tag_dict = { "name" : i}
                tag_array.append(tag_dict)

            # post の際の input data
            post_data ={
                "title": file_name,
                "body": text_data,
                "tags": tag_array
                }
            if len(team_id) > 0:
                post_data["team_url_name"] = team_id
            #else:
                #post_data["private"] = False

            # http postリクエスト
            post_request = requests.post(url=post_url, data=json.dumps(post_data), headers=headers)
            print post_request

            # 150ポスト/1時間なので，
            # 24秒/1ポスト とすると，24*150=3600秒=1時間
            time.sleep(24)
            

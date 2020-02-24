from selenium import webdriver
import shaonutil
import requests
import facebook

def get_user_id(access_token):
	API_URL = "https://graph.facebook.com/v3.0"
	PARAMS = {'access_token':access_token}
	r = requests.get(url = API_URL + '/me', params = PARAMS) 
	data = r.json()
	id_ = data['id']
	return id_

def debug_access_token(access_token):
	url = 'https://graph.facebook.com/v3.2/debug_token'
	PARAMS = {'input_token':access_token,'access_token':access_token}
	r = requests.get(url = url, params = PARAMS)
	data = r.json()
	return data

def getParams(url):
    dict_ = {}
    params = url.split("?")[1]
    params = params.split('&')
    for param in params:
    	key, val = param.split('=',1)
    	dict_[key] = val
    # {'access_token': 'EAADKbVke6LMBAPfT8ZACpnmrTzS8GZAuLff7epYnfq6AmEExsVwjXr1inXqeC9fL6vQVzlLbRPOxxJinzAhnPg9RLAOWQZA0Go9ti0DvZAmndp3lZBzjg17cQUsTHggfhn0UpBmm85DLnqH7FZC2iZBZCizJc2c3Qo6fi2FzL3mfZCywvHFLERoMWG1HtmoERFxtemqSZCIISGHwZDZD', 'data_access_expiration_time': '1590265814', 'expires_in': '5386'}
    return dict_

def get_app_access_token(fb_app_id, fb_app_secret):
    client = facebook.GraphAPI()
    return client.get_app_access_token( fb_app_id, fb_app_secret)

def get_access_token_via_dialogue(client_id,permissions):
	redirect_uri = 'https://m.facebook.com'
	driver = webdriver.Chrome('private/chromedriver.exe')
	driver.get('https://www.facebook.com/dialog/oauth?client_id='+client_id+'&display=popup&response_type=token&redirect_uri='+redirect_uri+'&scope='+permissions)
	while 'access_token' not in driver.current_url:
		pass
	
	return_url = driver.current_url
	return_url = return_url.replace('#','')
	dict_ = getParams(return_url)
	return dict_['access_token']



def get_permanant_access_token(client_id,client_secret,access_token):
	API_URL = "https://graph.facebook.com/v3.0"
	PARAMS = {
		'grant_type':'fb_exchange_token',
		'client_id':client_id,
		'client_secret':client_secret,
		'fb_exchange_token':access_token
	}

	r = requests.get(url = API_URL + '/oauth/access_token', params = PARAMS) 
	data = r.json()
	# {'error': {'message': 'Error validating access token: Session has expired on Sunday, 23-Feb-20 08:00:00 PST. The current time is Sunday, 23-Feb-20 08:37:46 PST.', 'type': 'OAuthException', 'code': 190, 'error_subcode': 463, 'fbtrace_id': 'AZzY-xbsxuhYlmMUECWzuHV'}}
	n_access_token = data['access_token']
  

	id_ = get_user_id(n_access_token)

	PARAMS = {'access_token':n_access_token}

	r = requests.get(url = API_URL + '/'+id_+'/accounts', params = PARAMS) 
	data = r.json()
	#print(data)
	access_token = data['data'][0]['access_token']

	debug_data = debug_access_token(access_token)
	# {'error': {'message': 'Error validating access token: The session was invalidated previously using an API call.', 'type': 'OAuthException', 'code': 190, 'error_subcode': 463, 'fbtrace_id': 'AJR-Mef9z_ajsFlIK9IhtVf'}}
	if debug_data['data']['expires_at'] == 0:
		return access_token	
	else:
		raise ValueError("Getting permanent_user_access_token failed !")

def routine_on_access_error_get_permanent_token(client_id,client_secret,permissions):
	config = shaonutil.file.read_configuration_ini('private/config.ini')
	

	access_token = get_access_token_via_dialogue(client_id,permissions)
	permanent_user_access_token = get_permanant_access_token(client_id,client_secret,access_token)

	debug_data = debug_access_token(permanent_user_access_token)

	runable = True
	for pname in permissions.split(','):
		if pname not in debug_data['data']['scopes']:
			runable = False
			raise ValueError("Getting all permissions failed")

	if(runable):
		config['fbaccess']['user_access_token'] = permanent_user_access_token
		shaonutil.file.write_configuration_ini(config, 'private/config.ini')
		print("permanent access_token achieved !")
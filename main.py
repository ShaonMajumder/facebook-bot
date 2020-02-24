#-*-coding:utf-8-*-
from fb_utility import *


def post(page_access_token,page_id):
	fb = facebook.GraphAPI(page_access_token)
	try:
		fb.put_object(page_id,'feed',message = message_s)
	except facebook.GraphAPIError:
		raise ValueError("Go to https://developers.facebook.com/tools/explorer/v2 to get access token")

def get_info(page_access_token,page_id,fields='id'):
	# fields = 'id,country_page_likes,likes,new_like_count,fan_count'
	fb = facebook.GraphAPI(page_access_token)
	default_info = fb.get_object(id=page_id,fields=fields)
	print(default_info)

def get_insights(page_access_token,page_id):
	fb = facebook.GraphAPI(page_access_token)
	#page_impressions = fb.get_connections(id=page_id,connection_name='insights',metric='page_impressions',date_preset='yesterday',period='lifetime',show_description_from_api_doc=True)
	#print(page_impressions)
	#posts_25 = fb.get_object(id=page_id, fields='posts.fields(type, name, created_time, object_id)')
	#print(posts_25)
	page_impressions = fb.get_connections(id=page_id,connection_name='insights',metric='page_impressions',date_preset='yesterday',period='lifetime',show_description_from_api_doc=True)
	print(page_impressions)

def get_post_reach(page_access_token,post_id):
	fb = facebook.GraphAPI(page_access_token)
	s_post = fb.get_object(id=post_id,fields='id,created_time,message,comments.summary(total_count),reactions.summary(total_count),shares')
	print(s_post)


config = shaonutil.file.read_configuration_ini('private/config.ini')

user_id = config['fbaccess']['user_id']
#get from app
client_id = config['fbaccess']['client_id']
client_secret = config['fbaccess']['client_secret']
page_access_token = config['fbaccess']['page_access_token']
user_access_token = config['fbaccess']['user_access_token']
page_id = config['fbaccess']['page_id']
message_s = 'posted by test app'


# get_access_token_via_dialogue(client_id,'pages_show_list,manage_pages,publish_pages')

try:
	get_post_reach(user_access_token,'105374151053772_108251464099374')
except Exception as e:
    s = str(e)
    print(s)
    if 'Error validating access token' in s:
    	routine_on_access_error_get_permanent_token(client_id,client_secret,'pages_show_list,manage_pages,publish_pages')

# {'error': {'message': 'Error validating access token: The session was invalidated previously using an API call.', 'type': 'OAuthException', 'code': 190, 'error_subcode': 463, 'fbtrace_id': 'ALveHTVATc4kDV-X7je8jpR'}}



"""
Output for analyzing
{
	'id': '105374151053772_108251464099374', 
	'created_time': '2020-02-20T06:05:28+0000', 
	'message': 'Second Test Post by app', 
	'comments': {'data': [], 'summary': {'total_count': 0}}, 
	'reactions': {
		'data': [
			{'id': '780552288661036', 'name': 'Robist', 'type': 'LIKE'},
 			{'id': '2511694345603044', 'name': 'Shaon Majumder', 'type': 'LIKE'}, 
 			{'id': '105374151053772', 'name': 'Business Test Page', 'type': 'LIKE'}
 		],
  		'paging': {'cursors': {'before': 'QVFIUnpuendLM2Q2STE2UEFJd3hFRVg3SXdUbGc5THZAqTEJ0dDZAQN3RBbE1ZAVUdHNi0wSm1IYW1sQ0k4Q1oySml0NXRYZAGJTZATA0b24wUjJBV1lmRldZAM0JR', 'after': 'QVFIUlpnVHF3X3NyaHZA4NzEwNHA2YWl3RjlFOVBsM1JWbGg5VDZAGVTFWOHk5ZADA5NUw4RTBJdTRZAX1dHNURLRFl5TEpEckpTNXl1bWx6a1cxVlVETlh5b1h3'}},
  		'summary': {'total_count': 3}
  	}
}
"""
import urllib.request,os

## Auth 
user = os.getenv('API_USER')
passd = os.environ.get('API_PASS')

password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
top_level_url = "https://api.justhumanz.me/"
password_mgr.add_password(None, top_level_url, user,passd)
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
opener = urllib.request.build_opener(handler)
opener.open("https://api.justhumanz.me/hanayori/")

urllib.request.install_opener(opener)



from qiniu import Auth

access_key = 'Ra2PcGh1GPQ3ofh173XtBb4I0A48VvjGbclH5Hzv'
secret_key = '_fBWVYqvKXAYmbpcnxhwOcvv1uwoiTPWiMZAMWXn'

q = Auth(access_key, secret_key)

bucket_domain = '7xpc8i.com1.z0.glb.clouddn.com' #可以在空间设置的域名设置中找到
key = 'shifu.mp4'
base_url = 'http://%s/%s' % (bucket_domain, key)
private_url = q.private_download_url(base_url, expires=3600)
print(private_url)

# browser = str('Android')
import os

browser = str('IOS')
apiTestingURL = str('http://127.0.0.1:8080/hello-world?name=Tony')
iosDeviceUDID = str('f14bcd4c08d3456b74a45107514217e6ba57c3da')
iosDeviceName = str('iPhone 6s Plus')
suite = str('smoke')

implicit_wait = int(30)

app_url = str('https://keep.google.com')
app_login = str('testmykeep')
app_password = str('testmykip')

PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)
ios_desired_caps = {'app': PATH('iosapp/CardDecks.app'),
                    'appName': 'CardDecks',
                    'deviceName': iosDeviceName,
                    'platformName': 'iOS',
                    'platformVersion': '9.3'}
#desired_caps['udid'] = properties.iosDeviceUDID

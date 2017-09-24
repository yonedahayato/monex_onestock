from datetime import date
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
import apiclient
import sys
import datetime

### 参考資料はこちら
# https://developers.google.com/google-apps/calendar/quickstart/python

def holiday_check(day_str=None):
    ### APIの認証を行う
    # API用の認証JSON
    json_file = 'gcp-4e840c069c31.json'
    # スコープ設定
    scopes = ['https://www.googleapis.com/auth/calendar.readonly']
    # 認証情報作成
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scopes=scopes)
    http_auth = credentials.authorize(Http())
    # API利用できる状態を作る
    service = apiclient.discovery.build("calendar", "v3", http=http_auth)


    ### 祝日を取得する
    # カレンダーIDには、日本の祝日カレンダーを指定
    calendar_id = "ja.japanese#holiday@group.v.calendar.google.com"

    if day_str == None:
        today = datetime.date.today()
        year = int(today.year)
        day_str = str(today)
    else:
        try:
            year = int(day_str[:4])
        except:
            raise Exception("day str is invalid")

    dtfrom = date(year=year, month=1, day=1).isoformat() + "T00:00:00.000000Z"
    dtto   = date(year=year, month=12, day=31).isoformat() + "T00:00:00.000000Z"
    # API実行
    events_results = service.events().list(
            calendarId = calendar_id,
            timeMin = dtfrom,
            timeMax = dtto,
            maxResults = 50,
            singleEvents = True,
            orderBy = "startTime"
        ).execute()
    # API結果から値を取り出す
    events = events_results.get('items', [])
    Hday_list = []
    for event in events:
        print("%s\t%s" % (event["start"]["date"], event["summary"]))
        Hday_list.append(str(event["start"]["date"]))

    print("\n"+"="*30)
    if day_str in Hday_list:
        print("{} is holiday".format(day_str))
        Hday_flag = True
    else:
        print("{} is not holiday".format(day_str))
        Hday_flag = False
    print("="*30)
    return Hday_flag

if __name__ == "__main__":
    day_str = "2017-01-03"
    holiday_check()

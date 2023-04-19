from utils.auth import access_token, refresh_token
from utils.extract import get_current_recently_played
from utils.validation import check_if_valid_data
from utils.load import load_to_sql
from utils.reporting import get_datas

if __name__ == '__main__':
    # request token
    # token = access_token()
    token = refresh_token()

    song_df = get_current_recently_played(token)
    print('extract process pass.......')

    if check_if_valid_data(song_df):
        print('data valid, continue process.....')

    load_to_sql(song_df)
    print('load to sql passed............')

    get_datas()
    print('passed the get datas.........')





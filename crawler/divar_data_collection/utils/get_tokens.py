import requests


def get_tokens(last_post_date, city_number, post_category='apartment-sell', n_pages=4):
    # example:
    #   url = 'https://api.divar.ir/v8/web-search/1/apartment-sell'
    #   last_post_date = 1650392836073764
    #   city_number = 1

    url = 'https://api.divar.ir/v8/web-search/{city_number}/{post_category}'.format(
        city_number=city_number,
        post_category=post_category
    )

    headers = {
        'Content-Type': 'application/json'
    }

    list_of_tokens = []
    for i in range(n_pages):
        json = {"json_schema": {"category": {"value": post_category}},
                "last-post-date": last_post_date}
        res = requests.post(url, json=json, headers=headers)
        data = res.json()
        last_post_date = data['last_post_date']

        for widget in data['web_widgets']['post_list']:
            token = widget['data']['token']
            list_of_tokens.append(token)

    return list_of_tokens
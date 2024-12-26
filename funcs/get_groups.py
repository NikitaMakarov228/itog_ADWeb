import vk_api
from funcs.global_t import ACCESS_TOKEN


def search_vk_groups(query, count=5) -> list:
    vk_session = vk_api.VkApi(token=ACCESS_TOKEN)
    vk = vk_session.get_api()

    try:
        groups = vk.groups.search(q=query, count=count, access_token=ACCESS_TOKEN)[
            "items"
        ]
        answer = [
            [group["name"], f'https://vk.com/public{group["id"]}'] for group in groups
        ]
        return answer
    except vk_api.exceptions.ApiError as e:
        print(f"Ошибка API: {e}")
        return

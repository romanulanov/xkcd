class VkApiError(Exception):
    pass

def handle_vk_error(response):
    response_unpacked = response.json()
    if 'error' in response.keys():
        output = {
            'code': response_unpacked['error']['error_code'],
            'message': response_unpacked['error']['error_msg'],
        }
        raise VkApiError(output)
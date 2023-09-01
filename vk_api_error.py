class VkApiError(Exception):
    pass

def handle_vk_error(response):
    if 'error' in response.keys():
        output = {
            'code': response.json()['error']['error_code'],
            'message': response.json()['error']['error_msg'],
        }
        raise VkApiError(output)
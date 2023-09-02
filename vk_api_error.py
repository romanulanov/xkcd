class VkApiError(Exception):
    pass

def handle_vk_error(response):
    unpacked_response = response.json()
    if 'error' in response.keys():
        output = {
            'code': unpacked_response['error']['error_code'],
            'message': unpacked_response['error']['error_msg'],
        }
        raise VkApiError(output)
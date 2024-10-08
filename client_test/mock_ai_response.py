from personalities.base_personality import handle_ai_response
# Mock example with proper structure for testing

mock_response = {
    'id': 'gen-1728322239-cWxBE7iqbF3CfJl5ILBG',
    'provider': 'Infermatic',
    'model': 'thedrummer/rocinante-12b',
    'object': 'chat.completion',
    'created': 1728322239,
    'choices': [
        {
            'logprobs': None,
            'finish_reason': 'stop',
            'index': 0,
            'message': {
                'role': 'assistant',
                'content': "Hello everyone, and welcome to the AI Radio Show! I'm humanGPT..."
            }
        }
    ],
    'usage': {
        'prompt_tokens': 49,
        'completion_tokens': 86,
        'total_tokens': 135
    }
}

#

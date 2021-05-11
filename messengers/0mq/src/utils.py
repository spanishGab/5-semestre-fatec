from constants import TEXT_MESAGE, MESSAGE_SPACE


def print_message(message: str, message_sender: str):
    print(MESSAGE_SPACE)
    print(TEXT_MESAGE.format(cli=message_sender,
                             msg=message))
    print(MESSAGE_SPACE)

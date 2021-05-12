from constants import TEXT_MESAGE, MESSAGE_SPACE


def print_message(message: str, message_sender: str):
    print(MESSAGE_SPACE, end='')
    print(TEXT_MESAGE.format(sender=message_sender,
                             msg=message), end='')
    print(MESSAGE_SPACE, end='')

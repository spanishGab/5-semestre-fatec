from constants import DEFAULT_HOST

from Controller import Controller

def controll_access():
    controller = Controller(semaphore=1)

    controller.add_connection('client_1', host=DEFAULT_HOST, port=5000)

    while True:
        controller.request_aquire('client_1')
        controller.request_release('client_1')

        # controller.request_aquire('client_2')
        # controller.request_release('client_2')



if __name__ == '__main__':
    controll_access()



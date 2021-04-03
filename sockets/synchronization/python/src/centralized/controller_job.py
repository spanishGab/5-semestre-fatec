from constants import DEFAULT_HOST

from Controller import Controller

from  concurrent.futures import ThreadPoolExecutor

FOO_CLIENT_PORT = 5000
BAR_CLIENT_PORT = 5001

controller_semaphore = 1


def controll_access(client: str, port: int):
    global controller_semaphore
    controller = Controller(controller_semaphore)

    try:
        controller.add_connection(connection_alias=client, host=DEFAULT_HOST, 
            port=port, listen=1)
        controller.connections[client].log_message("Connected to "+ client)

        while controller_semaphore == 0: continue

        controller.connections[client].log_message(client+" requesting acquire")
        controller_semaphore = controller.request_aquire(client, controller_semaphore)

        controller.connections[client].log_message(client+" requesting release")
        controller_semaphore = controller.request_release(client, controller_semaphore)
    except Exception as e:
            controller.connections[client].shutdown_connection()
            raise e
    finally:
        controller.connections[client].shutdown_connection()



if __name__ == '__main__':
    # controll_access('client_foo', FOO_CLIENT_PORT)
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(controll_access, 'client_foo', FOO_CLIENT_PORT)
        executor.submit(controll_access, 'client_bar', BAR_CLIENT_PORT)
        



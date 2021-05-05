import Pyro5.api

#! Teste com variável global
# result = None

@Pyro5.api.expose
class NumberSum:
    def sum_numbers(self, client, nbr1, nbr2):
        result = nbr1+nbr2

        print(f'{client}: {nbr1} + {nbr2} = {result}')
        return result

daemon = Pyro5.server.Daemon()
ns = Pyro5.api.locate_ns()
uri = daemon.register(NumberSum)
ns.register("number.sum", uri)

print("Server Ready.")
daemon.requestLoop()
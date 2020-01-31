import threading

class WittyThread():

    def __init__(self,name):
        self.name = name
        threading.Thread(name=self.name,target=run)

        def run():
            i = 0
            while i <= 10:
                i += 1
                print("{0} thread us running for {1} seconds".format(self.name, i))
            

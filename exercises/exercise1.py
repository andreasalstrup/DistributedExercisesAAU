import random

from emulators.Device import Device
from emulators.Medium import Medium
from emulators.MessageStub import MessageStub


class GossipMessage(MessageStub):

    def __init__(self, sender: int, destination: int, secrets):
        super().__init__(sender, destination)
        # we use a set to keep the "secrets" here
        self.secrets = secrets

    def __str__(self):
        return f'{self.source} -> {self.destination} : {self.secrets}'


class Gossip(Device):

    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        # for this exercise we use the index as the "secret", but it could have been a new routing-table (for instance)
        # or sharing of all the public keys in a cryptographic system
        self._secrets = set([index])

    def run(self):
        DEVICES = self.number_of_devices()
        SENDER_ID = self.index()
        DES_ID = random.randrange(0, DEVICES)
        SECRETS = self._secrets

        # Avoid talking to yourself
        while (SENDER_ID == DES_ID):
            DES_ID = random.randrange(0, DEVICES)
            continue
        
        # Send the message
        message = MessageStub(SENDER_ID, DES_ID)
        self.medium().send(message)

        # Wait for the message to be delivered
        while True:
            print(F"{GossipMessage(SENDER_ID, DES_ID, SECRETS).__str__()}")

            if len(SECRETS) == DEVICES:
                return
        
            ingoing = self.medium().receive()
            if ingoing is None:
                break
            
            self._secrets.add(ingoing.source)
        
        self.medium().wait_for_next_round()

    def print_result(self):
        print(f'\tDevice {self.index()} got secrets: {self._secrets}')

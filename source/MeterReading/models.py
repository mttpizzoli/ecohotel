from django.db import models
from django.utils import timezone
from web3 import Web3
import os


class MeterReading(models.Model):
    produced_energy_in_wh = models.FloatField()
    consumed_energy_in_wh = models.FloatField()
    timestamp = models.DateTimeField(blank=True, null=True)
    transaction_id = models.TextField(blank=True, null=True)

    def get_timestamp(self):
        self.timestamp = timezone.now()
        self.save()

    def send_transaction(self, message="None"):
        infura_key = os.environ.get("INFURA_KEY")
        w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/" + infura_key))
        address = os.environ.get("ADDRESS")
        private_key = os.environ.get("PRIVATE_KEY")
        nonce = w3.eth.getTransactionCount(address)
        gas_price = w3.eth.gasPrice
        value = w3.toWei(0, "ether")
        signed_transaction = w3.eth.account.signTransaction(dict(
            nonce=nonce,
            gasPrice=gas_price,
            gas=100000,
            to="0x0000000000000000000000000000000000000000",
            value=value,
            data=message.encode("utf-8")
        ), private_key)
        transaction = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
        self.transaction_id = w3.toHex(transaction)
        self.save()

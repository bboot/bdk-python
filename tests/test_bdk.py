import bdkpython as bdk
import unittest

db_config = bdk.DatabaseConfig.MEMORY()
blockchain_config = bdk.BlockchainConfig.ELECTRUM(
    bdk.ElectrumConfig(
        "ssl://electrum.blockstream.info:60002",
        None,
        5,
        None,
        100
    )
)
blockchain = bdk.Blockchain(blockchain_config)


class TestSimpleBip84Wallet(unittest.TestCase):
    descriptor = "wpkh([c258d2e4/84h/1h/0h]tpubDDYkZojQFQjht8Tm4jsS3iuEmKjTiEGjG6KnuFNKKJb5A6ZUCUZKdvLdSDWofKi4ToRCwb9poe1XdqfUnP4jaJjCB2Zwv11ZLgSbnZSNecE/0/*)"
    def test_address_bip84_testnet(self):
        wallet = bdk.Wallet(
            descriptor=self.descriptor,
            change_descriptor=None,
            network=bdk.Network.TESTNET,
            database_config=db_config
        )
        address = wallet.get_address(bdk.AddressIndex.NEW)
        self.assertEqual(address.address, "tb1qzg4mckdh50nwdm9hkzq06528rsu73hjxxzem3e")

    def test_wallet_balance(self):
        wallet = bdk.Wallet(
            descriptor=self.descriptor,
            change_descriptor=None,
            network=bdk.Network.TESTNET,
            database_config=db_config,
        )
        wallet.sync(blockchain, None)
        balance = wallet.get_balance()
        self.assertGreater(balance, 0,
            "Balance is 0, send testnet coins to tb1qzg4mckdh50nwdm9hkzq06528rsu73hjxxzem3e"
        )

    def test_get_transactions(self):
        wallet = bdk.Wallet(
            descriptor=self.descriptor,
            change_descriptor=None,
            network=bdk.Network.TESTNET,
            database_config=db_config,
        )
        wallet.sync(blockchain, None)
        transactions = wallet.get_transactions()
        self.assertGreaterEqual(len(transactions), 38)

    def test_invalid_network(self):
        with self.assertRaises(bdk.BdkError.Descriptor):
            wallet = bdk.Wallet(
                descriptor=self.descriptor,
                change_descriptor=None,
                network=bdk.Network.BITCOIN,
                database_config=db_config,
            )


class TestBip84FullWallet(unittest.TestCase):
    '''
    Created with https://iancoleman.io/bip39/
    '''
    mnemonic = "tuition bright run olympic table near trial century memory unit rifle express"
    password = "my-password"
    # BIP32 Root Key
    xprv = "tprv8ZgxMBicQKsPcwtRNFZPYqeQ8r9fhDYNjs2Psnj11EiGVGHsZectUh2VbEeaZapoWsz9KbD1ZgpXju8FhbvJ2F8Dd4JznEspegB2Bnu2Jvq"
    fingerprint = "ab5313e8"

    def test_restore_key(self):
        key_info = bdk.restore_extended_key(bdk.Network.TESTNET,
            self.mnemonic, self.password
        )
        self.assertEqual(key_info.xprv, self.xprv)
        self.assertEqual(key_info.fingerprint, self.fingerprint)


class TestBip84WatchWallet(unittest.TestCase):
    # HD wallet xpub at m/84'/0'/0'
    xpub = "tpubDDmEgrFuptCnGRkXZ2Pye4Wten31u6jWESxZnc8a3VGkUyJh7KLZun6Hfh8iUWp7cEFM63vCyxCedcNhWUhfmaMzpXnbHzmeNVFseB4Hgr7"
    descriptor = f'wpkh([{TestBip84FullWallet.fingerprint}/84h/0h/0h]{xpub}/0/*)'

    def test_get_last_unused_address(self):
        wallet = bdk.Wallet(
            descriptor=self.descriptor,
            change_descriptor=None,
            network=bdk.Network.TESTNET,
            database_config=db_config,
        )
        address = wallet.get_address(bdk.AddressIndex.LAST_UNUSED)
        self.assertEqual(address.address, "tb1qkuge0xj8lmhv9vh0rckdgctv6a5x7707d0z9ky")


if __name__ == '__main__':
    unittest.main()


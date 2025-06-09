import json
import os

from eth_typing import HexAddress
from staking_deposit.credentials import (
    CredentialList,
)
from staking_deposit.exceptions import ValidationError
from staking_deposit.settings import (
    get_chain_setting,
    get_devnet_chain_setting,
)
from staking_deposit.utils.ascii_art import RHINO_0
from staking_deposit.utils.constants import (
    MAX_DEPOSIT_AMOUNT,
    DEFAULT_VALIDATOR_KEYS_FOLDER_NAME,
)
from staking_deposit.utils.intl import (
    load_text,
)
from staking_deposit.utils.validation import (
    verify_deposit_data_json
)


def generate_keys(mnemonic: str, mnemonic_password: str, validator_start_index: int, num_validators: int, folder: str,
                  chain: str, keystore_password: str, execution_address: HexAddress, devnet_chain_setting_path: str = None) -> None:
    
    amounts = [MAX_DEPOSIT_AMOUNT] * num_validators
    folder = os.path.join(folder, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)

    chain_setting = get_chain_setting(chain)
    if devnet_chain_setting_path is not None:
        print('\n**[Warning] Using devnet chain setting to generate the signed keys.**\n')
        with open(devnet_chain_setting_path, 'r') as file_content:
            devnet_chain_setting_dict = json.load(file_content)
        chain_setting = get_devnet_chain_setting(
            network_name=devnet_chain_setting_dict['network_name'],
            genesis_fork_version=devnet_chain_setting_dict['genesis_fork_version'],
            genesis_validator_root=devnet_chain_setting_dict['genesis_validator_root'],
        )

    os.makedirs(folder, exist_ok=True)

    print(RHINO_0)
    # print(load_text(['msg_key_creation']))

    credentials = CredentialList.from_mnemonic(
        mnemonic=mnemonic,
        mnemonic_password=mnemonic_password,
        num_keys=num_validators,
        amounts=amounts,
        chain_setting=chain_setting,
        start_index=validator_start_index,
        hex_eth1_withdrawal_address=execution_address,
    )

    keystore_filefolders = credentials.export_keystores(password=keystore_password, folder=folder)
    deposits_file = credentials.export_deposit_data_json(folder=folder)

    if not credentials.verify_keystores(keystore_filefolders=keystore_filefolders, password=keystore_password):
        raise ValidationError(load_text(['err_verify_keystores']))

    if not verify_deposit_data_json(deposits_file, credentials.credentials):
        raise ValidationError(load_text(['err_verify_deposit']))

    # print(load_text(['msg_creation_success']) + folder)


if __name__ == '__main__':
    # check_python_version()
    # print('\n***Using the tool on an offline and secure device is highly recommended to keep your mnemonic safe.***\n')
    generate_keys(
        mnemonic="energy six vacuum wrestle supply breeze cannon wine baby raise chef second beef hat number spray edit attack arrest donkey mean auto utility try",
        mnemonic_password="",
        validator_start_index=0,
        num_validators=2,
        folder=".",
        chain="testnet",
        keystore_password="password.txt",
        execution_address=None,
        devnet_chain_setting_path="testnet.json"
    )

import os

from eth_typing import HexAddress
from lib.credentials import (
    CredentialList,
)
from lib.exceptions import ValidationError
from lib.settings import BaseChainSetting
from lib.utils.ascii_art import APPLICATION_NAME
from lib.utils.constants import (
    MAX_DEPOSIT_AMOUNT,
    DEFAULT_VALIDATOR_KEYS_FOLDER_NAME,
)
from lib.utils.intl import (
    load_text,
)
from lib.utils.validation import (
    verify_deposit_data_json
)


def generate_keys(mnemonic: str, validator_start_index: int, num_validators: int, folder: str,
                  chain_setting: BaseChainSetting, execution_address: HexAddress = None) -> None:
    
    amounts = [MAX_DEPOSIT_AMOUNT] * num_validators
    folder = os.path.join(folder, DEFAULT_VALIDATOR_KEYS_FOLDER_NAME)

    os.makedirs(folder, exist_ok=True)

    print(APPLICATION_NAME)
    print(load_text(['msg_key_creation']))

    credentials = CredentialList.from_mnemonic(
        mnemonic=mnemonic,
        mnemonic_password='',
        num_keys=num_validators,
        amounts=amounts,
        chain_setting=chain_setting,
        start_index=validator_start_index,
        hex_eth1_withdrawal_address=execution_address,
    )

    keystore_password = "password"

    keystore_filefolders = credentials.export_keystores(password=keystore_password, folder=folder)
    deposits_file = credentials.export_deposit_data_json(folder=folder)

    if not credentials.verify_keystores(keystore_filefolders=keystore_filefolders, password=keystore_password):
        raise ValidationError(load_text(['err_verify_keystores']))

    if not verify_deposit_data_json(deposits_file, credentials.credentials):
        raise ValidationError(load_text(['err_verify_deposit']))

    print(load_text(['msg_creation_success']) + folder)

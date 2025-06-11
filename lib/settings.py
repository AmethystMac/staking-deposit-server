from typing import NamedTuple
from eth_utils import decode_hex

DEPOSIT_CLI_VERSION = '2.8.0'


class BaseChainSetting(NamedTuple):
    NETWORK_NAME: str
    GENESIS_FORK_VERSION: bytes
    GENESIS_VALIDATORS_ROOT: bytes


def get_chain_setting(network_name: str,
                             genesis_fork_version: str,
                             genesis_validator_root: str) -> BaseChainSetting:
    return BaseChainSetting(
        NETWORK_NAME=network_name,
        GENESIS_FORK_VERSION=decode_hex(genesis_fork_version),
        GENESIS_VALIDATORS_ROOT=decode_hex(genesis_validator_root),
    )

def convert_chain_setting(chain_setting: any) -> BaseChainSetting:
    return get_chain_setting(
        network_name=chain_setting.NETWORK_NAME,
        genesis_fork_version=chain_setting.GENESIS_FORK_VERSION,
        genesis_validator_root=chain_setting.GENESIS_VALIDATORS_ROOT,
    )

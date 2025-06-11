from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import NamedTuple
from lib.deposit import generate_keys
from lib.settings import (
    convert_chain_setting
)
from lib.utils.constants import DEFAULT_VALIDATOR_KEYS_FOLDER_NAME


class BaseChainSetting(NamedTuple):
    NETWORK_NAME: str
    GENESIS_FORK_VERSION: str
    GENESIS_VALIDATORS_ROOT: str

class TestRequest(BaseModel):
    value: str

class KeyGenRequest(BaseModel):
    mnemonic: str
    validator_start_index: int
    num_validators: int
    folder: str
    chain_setting: BaseChainSetting
    # execution_address: str


app = FastAPI()

@app.post("/test")
def test_endpoint(req: TestRequest):
    return {"status": "success", "message": f"Value received from the API call is { req.value }"}


@app.post("/generate-keys")
def generate_keys_endpoint(req: KeyGenRequest):
    try:
        generate_keys(
            mnemonic=req.mnemonic,
            validator_start_index=req.validator_start_index,
            num_validators=req.num_validators,
            folder=req.folder,
            chain_setting=convert_chain_setting(req.chain_setting),
            # execution_address=req.execution_address,
        )
        return {"status": "success", "message": f"Keys generated in { DEFAULT_VALIDATOR_KEYS_FOLDER_NAME }"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

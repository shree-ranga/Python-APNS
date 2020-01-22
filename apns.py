import json
from hyper import HTTP20Connection
from hyper.tls import init_context

token = "device-hex-token"  # (no spaces)
payload = {"aps": {"alert": "Hello from Python!"}}
cert_file = "/path/to/cert.pem"
development_server = "api.sandbox.push.apple.com"
port = 2197
url = f"/3/device/{token}"
# data = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
apns_push_type = "alert"
apns_topic = "your-app-bundle-id"
apns_priority = "10"
headers = {}

# payload
json_payload = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode(
    "utf-8"
)

# configure headers
headers["apns-topic"] = apns_topic
headers["apns-push-type"] = apns_push_type
headers["apns-priority"] = apns_priority

# ssl context
ssl_context = init_context(cert=cert_file)

# connection
connection = HTTP20Connection(
    host=development_server,
    port=port,
    ssl_context=ssl_context,
    force_proto="h2",
    secure=True,
)
# connection.connect()

# stream
stread_id = connection.request("POST", url, json_payload, headers)

# result
with connection.get_response(stread_id) as response:
    if response.status == 200:
        print("success")
    else:
        raw_data = response.read().decode("utf-8")
        data = json.loads(raw_data)
        print(data["reason"], data["timestamp"])

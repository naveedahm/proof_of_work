# Simple example
from jsonrpctcp import connect

conn = connect('localhost', 8001)
# Optionally, you can add a third string parameter which is the
# encryption key used on the server.
conn = connect('localhost', 8001, '12345abcdef67890')
# Just use simple dot-syntax to call methods. Don't use a method
# that starts with an underscore -- those are automatically private.
result = conn.add(1, 2)
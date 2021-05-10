STX = b'\x02'
ACK = b'\x06'
EOT = b'\x04'
SOH = b'\x01'
NAK = b'\x15'
CAN = b'\x18'


TYPE_ERROR_MESAGE = ("The '{param}' param must be an instance of the {tp} class"+
                     ", got {inst}")

VALUE_ERROR_MESSAGE = "The '{param}' param must respect the restriction: {restr}"
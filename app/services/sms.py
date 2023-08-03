import logging
import sys
from type_def.configs import SMPP

import smpplib.gsm
import smpplib.client
import smpplib.consts

logging.basicConfig(level="DEBUG")


def send_sms(source_name: str, destination_addr: str, msg: str, smpp_config: SMPP):
    # if you want to know what's happening

    # Two parts, GSM default / UCS2, SMS with UDH
    parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(msg)

    client = smpplib.client.Client(smpp_config.host, smpp_config.password)

    # Print when obtain message_id
    client.set_message_sent_handler(
        lambda pdu: sys.stdout.write(
            "sent {} {}\n".format(pdu.sequence, pdu.message_id)
        )
    )

    # Handle delivery receipts (and any MO SMS)
    def handle_deliver_sm(pdu):
        sys.stdout.write("delivered {}\n".format(pdu.receipted_message_id))
        return 0  # cmd status for deliver_sm_resp

    client.set_message_received_handler(lambda pdu: handle_deliver_sm(pdu))

    client.connect()
    client.bind_transceiver(system_id=smpp_config.sys_id, password=smpp_config.password)

    for part in parts:
        pdu = client.send_message(
            source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
            source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
            # Make sure it is a byte string, not unicode:
            source_addr=source_name,
            dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
            dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
            # Make sure thease two params are byte strings, not unicode:
            # destination_addr='94715334864',
            destination_addr=destination_addr,
            short_message=part,
            data_coding=encoding_flag,
            esm_class=msg_type_flag,
            registered_delivery=True,
        )
        print(pdu.sequence)

    # Enters a loop, waiting for incoming PDUs
    client.listen()
    client.disconnect()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test packet mux and demux
# GNU Radio version: 3.10.9.2

from gnuradio import blocks
import pmt
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import pdu
import pmt, numpy as np




class test_packet_mux_and_demux(gr.top_block):

    def __init__(self, out='out.bin', packet_size=64):
        gr.top_block.__init__(self, "Test packet mux and demux", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.out = out
        self.packet_size = packet_size

        ##################################################
        # Variables
        ##################################################
        self.garbage_preamble_length_n_bytes = garbage_preamble_length_n_bytes = packet_size*10
        self.access_code = access_code = "11100001010110101110100010010011"
        self.samp_rate = samp_rate = 32000
        self.num_pream_packets = num_pream_packets = int(garbage_preamble_length_n_bytes/packet_size)
        self.format_used = format_used = digital.header_format_counter(access_code,0,8)
        self.format_default = format_default = digital.header_format_default(access_code,0)

        ##################################################
        # Blocks
        ##################################################

        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'frame_len')
        self.pdu_pdu_to_tagged_stream_0_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.pdu_pdu_lambda_1 = pdu.pdu_lambda(lambda x: pmt.cons(pmt.to_pmt({ 'select': True }) if pmt.to_long(pmt.dict_ref(pmt.car(x), pmt.string_to_symbol("counter"), pmt.from_long(0))) >= num_pream_packets else pmt.to_pmt({ 'select': False }), pmt.cdr(x)), "RAW", pmt.intern("key"))
        self.pdu_pdu_lambda_0 = pdu.pdu_lambda(lambda x: pmt.dict_add(x, pmt.string_to_symbol("frame_len"), pmt.from_long(8*pmt.to_long(pmt.dict_ref(x,pmt.string_to_symbol("payload symbols"),pmt.from_long(0))))), "RAW", pmt.intern("key"))
        self.pdu_pdu_filter_0 = pdu.pdu_filter(pmt.intern("select"), pmt.PMT_T, False)
        self.digital_protocol_parser_b_0 = digital.protocol_parser_b(format_used)
        self.digital_protocol_formatter_bb_1 = digital.protocol_formatter_bb(format_default, "packet_len")
        self.digital_protocol_formatter_async_0 = digital.protocol_formatter_async(format_used)
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
            96,
            1,
            0,
            "frame_len",
            "packet_len",
            False,
            gr.sizeof_char,
            "",
            samp_rate,
            (),
            0)
        self.digital_crc32_bb_2 = digital.crc32_bb(True, "packet_len", True)
        self.digital_crc32_bb_1 = digital.crc32_bb(False, "packet_len", True)
        self.digital_crc32_bb_0 = digital.crc32_bb(True, "frame_len", True)
        self.digital_crc32_async_bb_0 = digital.crc32_async_bb(False)
        self.digital_correlate_access_code_xx_ts_0 = digital.correlate_access_code_bb_ts(access_code,
          0, 'packet_len')
        self.blocks_tagged_stream_mux_2 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_char * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_repack_bits_bb_3 = blocks.repack_bits_bb(8, 1, "", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_2 = blocks.repack_bits_bb(1, 8, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_1 = blocks.repack_bits_bb(1, 8, "frame_len", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, 1, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(6,[0x01,0x02,0x03,0x04,0x00,0x00])), 1000)
        self.blocks_message_debug_2 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_message_debug_1 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_message_debug_0 = blocks.message_debug(False, gr.log_levels.debug)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, out, False)
        self.blocks_file_sink_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.digital_crc32_async_bb_0, 'in'))
        self.msg_connect((self.digital_crc32_async_bb_0, 'out'), (self.digital_protocol_formatter_async_0, 'in'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'header'), (self.blocks_message_debug_2, 'print'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'header'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'payload'), (self.pdu_pdu_to_tagged_stream_0_0, 'pdus'))
        self.msg_connect((self.digital_protocol_parser_b_0, 'info'), (self.pdu_pdu_lambda_0, 'pdu'))
        self.msg_connect((self.pdu_pdu_filter_0, 'pdus'), (self.blocks_message_debug_1, 'print'))
        self.msg_connect((self.pdu_pdu_lambda_0, 'pdu'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.pdu_pdu_lambda_0, 'pdu'), (self.digital_header_payload_demux_0, 'header_data'))
        self.msg_connect((self.pdu_pdu_lambda_1, 'pdu'), (self.pdu_pdu_filter_0, 'pdus'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.pdu_pdu_lambda_1, 'pdu'))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_repack_bits_bb_1, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_repack_bits_bb_2, 0), (self.digital_crc32_bb_2, 0))
        self.connect((self.blocks_repack_bits_bb_3, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.digital_correlate_access_code_xx_ts_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_crc32_bb_1, 0))
        self.connect((self.blocks_tagged_stream_mux_2, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_tagged_stream_mux_2, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0, 0), (self.blocks_repack_bits_bb_2, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.digital_crc32_bb_1, 0), (self.blocks_tagged_stream_mux_2, 1))
        self.connect((self.digital_crc32_bb_1, 0), (self.digital_protocol_formatter_bb_1, 0))
        self.connect((self.digital_crc32_bb_2, 0), (self.blocks_repack_bits_bb_3, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.blocks_repack_bits_bb_1, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.digital_protocol_parser_b_0, 0))
        self.connect((self.digital_protocol_formatter_bb_1, 0), (self.blocks_tagged_stream_mux_2, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))


    def get_out(self):
        return self.out

    def set_out(self, out):
        self.out = out
        self.blocks_file_sink_0.open(self.out)

    def get_packet_size(self):
        return self.packet_size

    def set_packet_size(self, packet_size):
        self.packet_size = packet_size
        self.set_garbage_preamble_length_n_bytes(self.packet_size*10)
        self.set_num_pream_packets(int(self.garbage_preamble_length_n_bytes/self.packet_size))

    def get_garbage_preamble_length_n_bytes(self):
        return self.garbage_preamble_length_n_bytes

    def set_garbage_preamble_length_n_bytes(self, garbage_preamble_length_n_bytes):
        self.garbage_preamble_length_n_bytes = garbage_preamble_length_n_bytes
        self.set_num_pream_packets(int(self.garbage_preamble_length_n_bytes/self.packet_size))

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code
        self.set_format_default(digital.header_format_default(self.access_code,0))
        self.set_format_used(digital.header_format_counter(self.access_code,0,8))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_num_pream_packets(self):
        return self.num_pream_packets

    def set_num_pream_packets(self, num_pream_packets):
        self.num_pream_packets = num_pream_packets
        self.pdu_pdu_lambda_1.set_fn(lambda x: pmt.cons(pmt.to_pmt({ 'select': True }) if pmt.to_long(pmt.dict_ref(pmt.car(x), pmt.string_to_symbol("counter"), pmt.from_long(0))) >= self.num_pream_packets else pmt.to_pmt({ 'select': False }), pmt.cdr(x)))

    def get_format_used(self):
        return self.format_used

    def set_format_used(self, format_used):
        self.format_used = format_used

    def get_format_default(self):
        return self.format_default

    def set_format_default(self, format_default):
        self.format_default = format_default



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--out", dest="out", type=str, default='out.bin',
        help="Set Output filename [default=%(default)r]")
    parser.add_argument(
        "--packet-size", dest="packet_size", type=intx, default=64,
        help="Set Packet Size [default=%(default)r]")
    return parser


def main(top_block_cls=test_packet_mux_and_demux, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(out=options.out, packet_size=options.packet_size)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test barker code
# Author: ubuntu
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
import pmt
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu



class test_barker_code_demo(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Test barker code", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Test barker code")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "test_barker_code_demo")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.access_code = access_code = "11100001010110101110100010010011"
        self.samp_rate = samp_rate = 32000
        self.format_used = format_used = digital.header_format_default(access_code,0)
        self.access_code_cplx = access_code_cplx = [(complex(x)-0.5)*2 for x in list(access_code)]

        ##################################################
        # Blocks
        ##################################################

        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'payload symbols')
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.digital_protocol_parser_b_0 = digital.protocol_parser_b(format_used)
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(format_used, "packet_len")
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
            (len(access_code)+(2*2*8)),
            1,
            0,
            "payload symbols",
            "time_est",
            False,
            gr.sizeof_gr_complex,
            "",
            samp_rate,
            (),
            0)
        self.digital_crc32_bb_1 = digital.crc32_bb(True, "payload symbols", True)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_corr_est_cc_0 = digital.corr_est_cc(access_code_cplx, 1, 1, 0.9, digital.THRESHOLD_ABSOLUTE)
        self.digital_binary_slicer_fb_1 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_vector_source_x_1 = blocks.vector_source_f([0,], True, 1, [])
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_char * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, 8, "payload symbols", False, gr.GR_MSB_FIRST)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(2)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(16, [0x48,0x65,0x6c,0x6c,0x6f,0x2c,0x20,0x57,0x6f,0x72,0x6c,0x64,0x21])), 1000)
        self.blocks_message_debug_1 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_float_1 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-0.5))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.digital_protocol_parser_b_0, 'info'), (self.digital_header_payload_demux_0, 'header_data'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.blocks_message_debug_1, 'print'))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_complex_to_float_1, 1), (self.blocks_null_sink_1, 0))
        self.connect((self.blocks_complex_to_float_1, 0), (self.digital_binary_slicer_fb_1, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.digital_corr_est_cc_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_crc32_bb_1, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_vector_source_x_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_protocol_parser_b_0, 0))
        self.connect((self.digital_binary_slicer_fb_1, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.digital_crc32_bb_1, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.blocks_complex_to_float_1, 0))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test_barker_code_demo")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code
        self.set_access_code_cplx([(complex(x)-0.5)*2 for x in list(self.access_code)])
        self.set_format_used(digital.header_format_default(self.access_code,0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_format_used(self):
        return self.format_used

    def set_format_used(self, format_used):
        self.format_used = format_used

    def get_access_code_cplx(self):
        return self.access_code_cplx

    def set_access_code_cplx(self, access_code_cplx):
        self.access_code_cplx = access_code_cplx




def main(top_block_cls=test_barker_code_demo, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()

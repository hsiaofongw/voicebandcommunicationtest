#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test packet mux and demux
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
from gnuradio import pdu
import pmt, numpy as np
import sip



class test_packet_mux_and_demux(gr.top_block, Qt.QWidget):

    def __init__(self, out='out.bin'):
        gr.top_block.__init__(self, "Test packet mux and demux", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Test packet mux and demux")
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

        self.settings = Qt.QSettings("GNU Radio", "test_packet_mux_and_demux")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Parameters
        ##################################################
        self.out = out

        ##################################################
        # Variables
        ##################################################
        self.access_code = access_code = "11100001010110101110100010010011"
        self.samp_rate = samp_rate = 32000
        self.format_used = format_used = digital.header_format_counter(access_code,0,8)

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            21, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.pdu_pdu_to_tagged_stream_0_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.pdu_pdu_lambda_0 = pdu.pdu_lambda(lambda x: pmt.dict_add(x, pmt.string_to_symbol("frame_len"), pmt.from_long(8*pmt.to_long(pmt.dict_ref(x,pmt.string_to_symbol("payload symbols"),pmt.from_long(0))))), "RAW", pmt.intern("key"))
        self.digital_protocol_parser_b_0 = digital.protocol_parser_b(format_used)
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
        self.digital_crc32_async_bb_0 = digital.crc32_async_bb(False)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_repack_bits_bb_1 = blocks.repack_bits_bb(1, 8, "frame_len", False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, 1, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(6,[0x01,0x02,0x03,0x04,0x00,0x00])), 1000)
        self.blocks_message_debug_0 = blocks.message_debug(True, gr.log_levels.debug)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, out, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.digital_crc32_async_bb_0, 'in'))
        self.msg_connect((self.digital_crc32_async_bb_0, 'out'), (self.digital_protocol_formatter_async_0, 'in'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'header'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.digital_protocol_formatter_async_0, 'payload'), (self.pdu_pdu_to_tagged_stream_0_0, 'pdus'))
        self.msg_connect((self.digital_protocol_parser_b_0, 'info'), (self.pdu_pdu_lambda_0, 'pdu'))
        self.msg_connect((self.pdu_pdu_lambda_0, 'pdu'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.pdu_pdu_lambda_0, 'pdu'), (self.digital_header_payload_demux_0, 'header_data'))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.blocks_repack_bits_bb_1, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.blocks_repack_bits_bb_1, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.digital_protocol_parser_b_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test_packet_mux_and_demux")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_out(self):
        return self.out

    def set_out(self, out):
        self.out = out
        self.blocks_file_sink_0.open(self.out)

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code
        self.set_format_used(digital.header_format_counter(self.access_code,0,8))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_format_used(self):
        return self.format_used

    def set_format_used(self, format_used):
        self.format_used = format_used



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--out", dest="out", type=str, default='out.bin',
        help="Set Output filename [default=%(default)r]")
    return parser


def main(top_block_cls=test_packet_mux_and_demux, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(out=options.out)

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

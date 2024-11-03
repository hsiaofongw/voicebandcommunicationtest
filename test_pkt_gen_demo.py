#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test Packet Generation demo
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
import pmt
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
import sip



class test_pkt_gen_demo(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Test Packet Generation demo", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Test Packet Generation demo")
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

        self.settings = Qt.QSettings("GNU Radio", "test_pkt_gen_demo")

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
        self.samp_rate = samp_rate = 48000
        self.pkt_len = pkt_len = 16
        self.format_used = format_used = digital.header_format_default(access_code, 0)

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1000, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 17)

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
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(format_used, "packet_len")
        self.digital_crc32_bb_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_corr_est_cc_0 = digital.corr_est_cc([complex(x) for x in list(access_code)], 1, 0, 0, digital.THRESHOLD_ABSOLUTE)
        self.blocks_vector_source_x_0 = blocks.vector_source_f((0,), True, 1, [])
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_gr_complex * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_tag_debug_0 = blocks.tag_debug(gr.sizeof_gr_complex*1, 'Phase Estimator', "phase_est")
        self.blocks_tag_debug_0.set_display(True)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, pkt_len, "packet_len")
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(16, [0x48,0x65,0x6c,0x6c,0x6f,0x2c,0x20,0x57,0x6f,0x72,0x6c,0x64,0x21])), 1000)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_null_sink_1, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.digital_corr_est_cc_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.digital_corr_est_cc_0, 0), (self.blocks_tag_debug_0, 0))
        self.connect((self.digital_corr_est_cc_0, 1), (self.blocks_tag_gate_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.blocks_throttle2_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test_pkt_gen_demo")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code
        self.set_format_used(digital.header_format_default(self.access_code, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_pkt_len(self):
        return self.pkt_len

    def set_pkt_len(self, pkt_len):
        self.pkt_len = pkt_len
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.pkt_len)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.pkt_len)

    def get_format_used(self):
        return self.format_used

    def set_format_used(self, format_used):
        self.format_used = format_used




def main(top_block_cls=test_pkt_gen_demo, options=None):

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

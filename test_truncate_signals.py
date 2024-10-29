#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test truncated signals
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation



class test_truncate_signals(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Test truncated signals", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Test truncated signals")
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

        self.settings = Qt.QSettings("GNU Radio", "test_truncate_signals")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.read_size = read_size = 256
        self.preamble_len = preamble_len = 32
        self.output_filename = output_filename = "test.bin"
        self.input_filename = input_filename = "threekingdoms.txt"

        ##################################################
        # Blocks
        ##################################################

        self.blocks_vector_source_x_0_0_0 = blocks.vector_source_f((1,2,3,4), True, 1, [])
        self.blocks_vector_source_x_0_0 = blocks.vector_source_f((1,), True, 1, [])
        self.blocks_vector_source_x_0 = blocks.vector_source_b((1,), True, 1, [])
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_head_0 = blocks.head(gr.sizeof_char*1, (preamble_len + read_size))
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, input_filename, False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, output_filename, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_char*1, preamble_len)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, preamble_len)
        self.blocks_char_to_float_1 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_xx_0 = blocks.add_vff(1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_float_to_char_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_char_to_float_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_delay_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_char_to_float_1, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.blocks_float_to_char_0, 0), (self.blocks_head_0, 0))
        self.connect((self.blocks_head_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_vector_source_x_0_0_0, 0), (self.blocks_multiply_xx_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test_truncate_signals")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_read_size(self):
        return self.read_size

    def set_read_size(self, read_size):
        self.read_size = read_size
        self.blocks_head_0.set_length((self.preamble_len + self.read_size))

    def get_preamble_len(self):
        return self.preamble_len

    def set_preamble_len(self, preamble_len):
        self.preamble_len = preamble_len
        self.blocks_delay_0.set_dly(int(self.preamble_len))
        self.blocks_head_0.set_length((self.preamble_len + self.read_size))
        self.blocks_delay_0_0.set_dly(int(self.preamble_len))

    def get_output_filename(self):
        return self.output_filename

    def set_output_filename(self, output_filename):
        self.output_filename = output_filename
        self.blocks_file_sink_0.open(self.output_filename)

    def get_input_filename(self):
        return self.input_filename

    def set_input_filename(self, input_filename):
        self.input_filename = input_filename
        self.blocks_file_source_0.open(self.input_filename, False)




def main(top_block_cls=test_truncate_signals, options=None):

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

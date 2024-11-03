#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test BFSK RX Demo
# Author: ubuntu
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import analog
import math
from gnuradio import audio
from gnuradio import blocks
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import network
import sip



class test_bfsk_rx_demo(gr.top_block, Qt.QWidget):

    def __init__(self, audio_in='plughw:0,0,0', deviation=800, fc=3000, pkt_size=16, sps=1500, udp_out_host='127.0.0.1', udp_out_port=47898):
        gr.top_block.__init__(self, "Test BFSK RX Demo", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Test BFSK RX Demo")
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

        self.settings = Qt.QSettings("GNU Radio", "test_bfsk_rx_demo")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Parameters
        ##################################################
        self.audio_in = audio_in
        self.deviation = deviation
        self.fc = fc
        self.pkt_size = pkt_size
        self.sps = sps
        self.udp_out_host = udp_out_host
        self.udp_out_port = udp_out_port

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.access_code = access_code = "11100001010110101110100010010011"
        self.sensitivity = sensitivity = 2*math.pi*deviation
        self.noise_voltage = noise_voltage = 0.002
        self.lowpassfiltertaps = lowpassfiltertaps = firdes.low_pass(1.0, samp_rate, fc,deviation*1.5, window.WIN_HAMMING, 6.76)
        self.format_used = format_used = digital.header_format_counter(access_code,0,1)
        self.access_code_cplx = access_code_cplx = [(complex(x)-0.5)*2 for x in list(access_code)]

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            (5*sps), #size
            samp_rate, #samp_rate
            "Rx symbols", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
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
        self.pdu_tagged_stream_to_pdu_0 = pdu.tagged_stream_to_pdu(gr.types.byte_t, 'payload symbols')
        self._noise_voltage_range = qtgui.Range(0, 0.5, 0.001, 0.002, 200)
        self._noise_voltage_win = qtgui.RangeWidget(self._noise_voltage_range, self.set_noise_voltage, "Noise Voltage", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_voltage_win)
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_char, 1, udp_out_host, udp_out_port, 0, pkt_size, False)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_fcc(1, lowpassfiltertaps, fc, samp_rate)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_ff(
            digital.TED_EARLY_LATE,
            sps,
            0.045,
            1.0,
            1.0,
            1.5,
            1,
            digital.constellation_bpsk().base(),
            digital.IR_MMSE_8TAP,
            128,
            [])
        self.digital_protocol_parser_b_0 = digital.protocol_parser_b(format_used)
        self.digital_header_payload_demux_0 = digital.header_payload_demux(
            (12*8),
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
        self.digital_corr_est_cc_0 = digital.corr_est_cc(access_code_cplx, 1, 1, 0.9, digital.THRESHOLD_ABSOLUTE)
        self.digital_binary_slicer_fb_2 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_1 = digital.binary_slicer_fb()
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_vector_source_x_1 = blocks.vector_source_f([0,], True, 1, [])
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, 8, "payload symbols", False, gr.GR_MSB_FIRST)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(2)
        self.blocks_message_debug_1 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_float_1 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff((-0.5))
        self.audio_source_0 = audio.source(samp_rate, '', True)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf((samp_rate/(2*math.pi*deviation)))
        self.analog_agc_xx_0 = analog.agc_ff((1e-4), 1.0, 1.0, 65536)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_protocol_parser_b_0, 'info'), (self.digital_header_payload_demux_0, 'header_data'))
        self.msg_connect((self.pdu_tagged_stream_to_pdu_0, 'pdus'), (self.blocks_message_debug_1, 'print'))
        self.connect((self.analog_agc_xx_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.audio_source_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.digital_binary_slicer_fb_0, 0))
        self.connect((self.blocks_complex_to_float_1, 1), (self.blocks_null_sink_1, 0))
        self.connect((self.blocks_complex_to_float_1, 0), (self.digital_binary_slicer_fb_1, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.digital_corr_est_cc_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_crc32_bb_1, 0))
        self.connect((self.blocks_vector_source_x_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.digital_protocol_parser_b_0, 0))
        self.connect((self.digital_binary_slicer_fb_1, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_binary_slicer_fb_2, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_corr_est_cc_0, 0), (self.digital_header_payload_demux_0, 0))
        self.connect((self.digital_crc32_bb_1, 0), (self.network_udp_sink_0, 0))
        self.connect((self.digital_crc32_bb_1, 0), (self.pdu_tagged_stream_to_pdu_0, 0))
        self.connect((self.digital_header_payload_demux_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.digital_header_payload_demux_0, 1), (self.blocks_complex_to_float_1, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_binary_slicer_fb_2, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.analog_quadrature_demod_cf_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test_bfsk_rx_demo")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_audio_in(self):
        return self.audio_in

    def set_audio_in(self, audio_in):
        self.audio_in = audio_in

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation
        self.set_lowpassfiltertaps(firdes.low_pass(1.0, self.samp_rate, self.fc, self.deviation*1.5, window.WIN_HAMMING, 6.76))
        self.set_sensitivity(2*math.pi*self.deviation)
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/(2*math.pi*self.deviation)))

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.set_lowpassfiltertaps(firdes.low_pass(1.0, self.samp_rate, self.fc, self.deviation*1.5, window.WIN_HAMMING, 6.76))
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.fc)

    def get_pkt_size(self):
        return self.pkt_size

    def set_pkt_size(self, pkt_size):
        self.pkt_size = pkt_size

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.digital_symbol_sync_xx_0.set_sps(self.sps)

    def get_udp_out_host(self):
        return self.udp_out_host

    def set_udp_out_host(self, udp_out_host):
        self.udp_out_host = udp_out_host

    def get_udp_out_port(self):
        return self.udp_out_port

    def set_udp_out_port(self, udp_out_port):
        self.udp_out_port = udp_out_port

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_lowpassfiltertaps(firdes.low_pass(1.0, self.samp_rate, self.fc, self.deviation*1.5, window.WIN_HAMMING, 6.76))
        self.analog_quadrature_demod_cf_0.set_gain((self.samp_rate/(2*math.pi*self.deviation)))
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code
        self.set_access_code_cplx([(complex(x)-0.5)*2 for x in list(self.access_code)])
        self.set_format_used(digital.header_format_counter(self.access_code,0,1))

    def get_sensitivity(self):
        return self.sensitivity

    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity

    def get_noise_voltage(self):
        return self.noise_voltage

    def set_noise_voltage(self, noise_voltage):
        self.noise_voltage = noise_voltage

    def get_lowpassfiltertaps(self):
        return self.lowpassfiltertaps

    def set_lowpassfiltertaps(self, lowpassfiltertaps):
        self.lowpassfiltertaps = lowpassfiltertaps
        self.freq_xlating_fir_filter_xxx_0.set_taps(self.lowpassfiltertaps)

    def get_format_used(self):
        return self.format_used

    def set_format_used(self, format_used):
        self.format_used = format_used

    def get_access_code_cplx(self):
        return self.access_code_cplx

    def set_access_code_cplx(self, access_code_cplx):
        self.access_code_cplx = access_code_cplx



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--audio-in", dest="audio_in", type=str, default='plughw:0,0,0',
        help="Set Audio Input [default=%(default)r]")
    parser.add_argument(
        "--deviation", dest="deviation", type=eng_float, default=eng_notation.num_to_str(float(800)),
        help="Set BFSK Deviation [default=%(default)r]")
    parser.add_argument(
        "--fc", dest="fc", type=eng_float, default=eng_notation.num_to_str(float(3000)),
        help="Set Center frequency [default=%(default)r]")
    parser.add_argument(
        "--pkt-size", dest="pkt_size", type=intx, default=16,
        help="Set Packet size [default=%(default)r]")
    parser.add_argument(
        "--sps", dest="sps", type=intx, default=1500,
        help="Set Samples per symbol [default=%(default)r]")
    parser.add_argument(
        "--udp-out-host", dest="udp_out_host", type=str, default='127.0.0.1',
        help="Set UDP Output Host [default=%(default)r]")
    parser.add_argument(
        "--udp-out-port", dest="udp_out_port", type=intx, default=47898,
        help="Set UDP Output Port [default=%(default)r]")
    return parser


def main(top_block_cls=test_bfsk_rx_demo, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(audio_in=options.audio_in, deviation=options.deviation, fc=options.fc, pkt_size=options.pkt_size, sps=options.sps, udp_out_host=options.udp_out_host, udp_out_port=options.udp_out_port)

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
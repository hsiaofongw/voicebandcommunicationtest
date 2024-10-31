#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: BFSK Receive
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from custom_bfsk_demod import custom_bfsk_demod  # grc-generated hier_block
from custom_packet_parser import custom_packet_parser  # grc-generated hier_block
from custom_remove_preamble import custom_remove_preamble  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import blocks, gr
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import network
import sip



class bfsk_receive(gr.top_block, Qt.QWidget):

    def __init__(self, dest_host='127.0.0.1', dest_port='42028', deviation=600, num_pream_packets=2, packet_size=4, passband_fc=2800, samp_rate=48000, sps=5400, wav_in='record.wav', zmq_source='tcp://10.0.4.105:14748'):
        gr.top_block.__init__(self, "BFSK Receive", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("BFSK Receive")
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

        self.settings = Qt.QSettings("GNU Radio", "bfsk_receive")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Parameters
        ##################################################
        self.dest_host = dest_host
        self.dest_port = dest_port
        self.deviation = deviation
        self.num_pream_packets = num_pream_packets
        self.packet_size = packet_size
        self.passband_fc = passband_fc
        self.samp_rate = samp_rate
        self.sps = sps
        self.wav_in = wav_in
        self.zmq_source = zmq_source

        ##################################################
        # Variables
        ##################################################
        self.access_code = access_code = "11100001010110101110100010010011"
        self.garbage_preamble_length_n_bytes = garbage_preamble_length_n_bytes = packet_size*num_pream_packets
        self.format_used = format_used = digital.header_format_counter(access_code,0,8)
        self.constellation_bpsk = constellation_bpsk = digital.constellation_bpsk().base()
        self.constellation_bpsk.set_npwr(0)

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Rx", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)


        self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.network_tcp_sink_0 = network.tcp_sink(gr.sizeof_char, 1, dest_host, int(dest_port),1)
        self.custom_remove_preamble_0 = custom_remove_preamble(
            num_pream_packets=num_pream_packets,
        )
        self.custom_packet_parser_0 = custom_packet_parser(
            samp_rate=48000,
        )
        self.custom_bfsk_demod_0 = custom_bfsk_demod(
            deviation=deviation,
            fc=passband_fc,
            sps=sps,
        )
        self.blocks_wavfile_source_0 = blocks.wavfile_source(wav_in, True)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_message_debug_1_0 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_message_debug_1 = blocks.message_debug(True, gr.log_levels.info)
        self.band_pass_filter_0 = filter.interp_fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                samp_rate,
                (passband_fc-deviation),
                (passband_fc+deviation),
                200,
                window.WIN_HAMMING,
                6.76))


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.custom_packet_parser_0, 'header_data'), (self.blocks_message_debug_1_0, 'print'))
        self.msg_connect((self.custom_remove_preamble_0, 'out'), (self.blocks_message_debug_1, 'print'))
        self.msg_connect((self.custom_remove_preamble_0, 'out'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.band_pass_filter_0, 0), (self.custom_bfsk_demod_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.custom_bfsk_demod_0, 0), (self.custom_packet_parser_0, 0))
        self.connect((self.custom_packet_parser_0, 0), (self.custom_remove_preamble_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.network_tcp_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "bfsk_receive")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_dest_host(self):
        return self.dest_host

    def set_dest_host(self, dest_host):
        self.dest_host = dest_host

    def get_dest_port(self):
        return self.dest_port

    def set_dest_port(self, dest_port):
        self.dest_port = dest_port

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, (self.passband_fc-self.deviation), (self.passband_fc+self.deviation), 200, window.WIN_HAMMING, 6.76))
        self.custom_bfsk_demod_0.set_deviation(self.deviation)

    def get_num_pream_packets(self):
        return self.num_pream_packets

    def set_num_pream_packets(self, num_pream_packets):
        self.num_pream_packets = num_pream_packets
        self.set_garbage_preamble_length_n_bytes(self.packet_size*self.num_pream_packets)
        self.custom_remove_preamble_0.set_num_pream_packets(self.num_pream_packets)

    def get_packet_size(self):
        return self.packet_size

    def set_packet_size(self, packet_size):
        self.packet_size = packet_size
        self.set_garbage_preamble_length_n_bytes(self.packet_size*self.num_pream_packets)

    def get_passband_fc(self):
        return self.passband_fc

    def set_passband_fc(self, passband_fc):
        self.passband_fc = passband_fc
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, (self.passband_fc-self.deviation), (self.passband_fc+self.deviation), 200, window.WIN_HAMMING, 6.76))
        self.custom_bfsk_demod_0.set_fc(self.passband_fc)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.samp_rate, (self.passband_fc-self.deviation), (self.passband_fc+self.deviation), 200, window.WIN_HAMMING, 6.76))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.custom_bfsk_demod_0.set_sps(self.sps)

    def get_wav_in(self):
        return self.wav_in

    def set_wav_in(self, wav_in):
        self.wav_in = wav_in

    def get_zmq_source(self):
        return self.zmq_source

    def set_zmq_source(self, zmq_source):
        self.zmq_source = zmq_source

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code
        self.set_format_used(digital.header_format_counter(self.access_code,0,8))

    def get_garbage_preamble_length_n_bytes(self):
        return self.garbage_preamble_length_n_bytes

    def set_garbage_preamble_length_n_bytes(self, garbage_preamble_length_n_bytes):
        self.garbage_preamble_length_n_bytes = garbage_preamble_length_n_bytes

    def get_format_used(self):
        return self.format_used

    def set_format_used(self, format_used):
        self.format_used = format_used

    def get_constellation_bpsk(self):
        return self.constellation_bpsk

    def set_constellation_bpsk(self, constellation_bpsk):
        self.constellation_bpsk = constellation_bpsk



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--dest-host", dest="dest_host", type=str, default='127.0.0.1',
        help="Set Destination Host [default=%(default)r]")
    parser.add_argument(
        "--dest-port", dest="dest_port", type=str, default='42028',
        help="Set Destination Port [default=%(default)r]")
    parser.add_argument(
        "--deviation", dest="deviation", type=eng_float, default=eng_notation.num_to_str(float(600)),
        help="Set Deviation bandwidth for 2-FSK modulation [default=%(default)r]")
    parser.add_argument(
        "--num-pream-packets", dest="num_pream_packets", type=intx, default=2,
        help="Set Number of preamble garbage packets [default=%(default)r]")
    parser.add_argument(
        "--packet-size", dest="packet_size", type=intx, default=4,
        help="Set Packet Size [default=%(default)r]")
    parser.add_argument(
        "--passband-fc", dest="passband_fc", type=eng_float, default=eng_notation.num_to_str(float(2800)),
        help="Set Passband Center Frequency [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(48000)),
        help="Set Sampe Rate [default=%(default)r]")
    parser.add_argument(
        "--sps", dest="sps", type=intx, default=5400,
        help="Set Samples per Symbol [default=%(default)r]")
    parser.add_argument(
        "--wav-in", dest="wav_in", type=str, default='record.wav',
        help="Set Waveform file input [default=%(default)r]")
    parser.add_argument(
        "--zmq-source", dest="zmq_source", type=str, default='tcp://10.0.4.105:14748',
        help="Set ZMQ Source [default=%(default)r]")
    return parser


def main(top_block_cls=bfsk_receive, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(dest_host=options.dest_host, dest_port=options.dest_port, deviation=options.deviation, num_pream_packets=options.num_pream_packets, packet_size=options.packet_size, passband_fc=options.passband_fc, samp_rate=options.samp_rate, sps=options.sps, wav_in=options.wav_in, zmq_source=options.zmq_source)

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

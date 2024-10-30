#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Test transceiving
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from custom_iq_complex_to_passband_real import custom_iq_complex_to_passband_real  # grc-generated hier_block
from custom_packet_formatter import custom_packet_formatter  # grc-generated hier_block
from custom_packet_parser import custom_packet_parser  # grc-generated hier_block
from custom_passband_real_to_iq_complex import custom_passband_real_to_iq_complex  # grc-generated hier_block
from custom_remove_preamble import custom_remove_preamble  # grc-generated hier_block
from custom_stream_prepend import custom_stream_prepend  # grc-generated hier_block
from gnuradio import blocks
import numpy
import pmt
from gnuradio import blocks, gr
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
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



class test_transceive(gr.top_block, Qt.QWidget):

    def __init__(self, dest_host='127.0.0.1', dest_port='42028', filtersize=84, in_file='in.bin', noisevoltage=0.1, num_pream_packets=20, out='out.bin', packet_size=16, passband_fc=3600, samp_rate=48000, sps=72, txgain=2, wav_out='out.wav'):
        gr.top_block.__init__(self, "Test transceiving", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Test transceiving")
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

        self.settings = Qt.QSettings("GNU Radio", "test_transceive")

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
        self.filtersize = filtersize
        self.in_file = in_file
        self.noisevoltage = noisevoltage
        self.num_pream_packets = num_pream_packets
        self.out = out
        self.packet_size = packet_size
        self.passband_fc = passband_fc
        self.samp_rate = samp_rate
        self.sps = sps
        self.txgain = txgain
        self.wav_out = wav_out

        ##################################################
        # Variables
        ##################################################
        self.constellation_bpsk = constellation_bpsk = digital.constellation_bpsk().base()
        self.constellation_bpsk.set_npwr(0)
        self.access_code = access_code = "11100001010110101110100010010011"
        self.variable_rrc_filter_taps_0 = variable_rrc_filter_taps_0 = firdes.root_raised_cosine(sps+1, samp_rate,samp_rate/sps, 0.35, (11*sps))
        self.garbage_preamble_length_n_bytes = garbage_preamble_length_n_bytes = packet_size*num_pream_packets
        self.format_used = format_used = digital.header_format_counter(access_code,0,8)
        self.adaptive_algorithm_bpsk = adaptive_algorithm_bpsk = digital.adaptive_algorithm_cma( constellation_bpsk, .0001, 2).base()

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Rx signal", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "Rx symbols", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.network_tcp_sink_0 = network.tcp_sink(gr.sizeof_char, 1, dest_host, int(dest_port),1)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, (2*3.14/100), variable_rrc_filter_taps_0, filtersize, 0, 1.5, 2)
        self.digital_linear_equalizer_0 = digital.linear_equalizer(15, 2, adaptive_algorithm_bpsk, True, [ ], 'corr_est')
        self.digital_diff_decoder_bb_0_0 = digital.diff_decoder_bb(2, digital.DIFF_DIFFERENTIAL)
        self.digital_costas_loop_cc_0_0 = digital.costas_loop_cc((2*3.14/100), 2, False)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=constellation_bpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(constellation_bpsk)
        self.custom_stream_prepend_0 = custom_stream_prepend(
            garbage_preamble_length_n_bytes=garbage_preamble_length_n_bytes,
        )
        self.custom_remove_preamble_0 = custom_remove_preamble(
            num_pream_packets=num_pream_packets,
        )
        self.custom_passband_real_to_iq_complex_0 = custom_passband_real_to_iq_complex(
            passband_fc=passband_fc,
            samp_rate=samp_rate,
        )
        self.custom_packet_parser_0 = custom_packet_parser(
            samp_rate=48000,
        )
        self.custom_packet_formatter_0 = custom_packet_formatter(
            access_code=access_code,
            packet_size=packet_size,
        )
        self.custom_iq_complex_to_passband_real_0 = custom_iq_complex_to_passband_real(
            passband_fc=passband_fc,
            samp_rate=samp_rate,
            txgain=txgain,
        )
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noisevoltage,
            frequency_offset=0.0,
            epsilon=1.0,
            taps=[1.0],
            noise_seed=0,
            block_tags=False)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(
            wav_out,
            1,
            int(samp_rate),
            blocks.FORMAT_WAV,
            blocks.FORMAT_FLOAT,
            False
            )
        self.blocks_throttle2_1 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_tag_gate_1 = blocks.tag_gate(gr.sizeof_float * 1, False)
        self.blocks_tag_gate_1.set_single_key("")
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_char * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_message_debug_1_0 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_message_debug_1 = blocks.message_debug(True, gr.log_levels.info)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, in_file, False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 1000))), True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.custom_packet_parser_0, 'header_data'), (self.blocks_message_debug_1_0, 'print'))
        self.msg_connect((self.custom_remove_preamble_0, 'out'), (self.blocks_message_debug_1, 'print'))
        self.msg_connect((self.custom_remove_preamble_0, 'out'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.connect((self.analog_random_source_x_0, 0), (self.custom_stream_prepend_0, 1))
        self.connect((self.blocks_file_source_0, 0), (self.custom_stream_prepend_0, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_tag_gate_1, 0), (self.custom_passband_real_to_iq_complex_0, 0))
        self.connect((self.blocks_throttle2_1, 0), (self.blocks_tag_gate_1, 0))
        self.connect((self.blocks_throttle2_1, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.custom_iq_complex_to_passband_real_0, 0), (self.blocks_throttle2_1, 0))
        self.connect((self.custom_packet_formatter_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.custom_packet_parser_0, 0), (self.custom_remove_preamble_0, 0))
        self.connect((self.custom_passband_real_to_iq_complex_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.custom_stream_prepend_0, 0), (self.custom_packet_formatter_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.custom_iq_complex_to_passband_real_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_costas_loop_cc_0_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_diff_decoder_bb_0_0, 0), (self.custom_packet_parser_0, 0))
        self.connect((self.digital_linear_equalizer_0, 0), (self.digital_costas_loop_cc_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_linear_equalizer_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.network_tcp_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "test_transceive")
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

    def get_filtersize(self):
        return self.filtersize

    def set_filtersize(self, filtersize):
        self.filtersize = filtersize

    def get_in_file(self):
        return self.in_file

    def set_in_file(self, in_file):
        self.in_file = in_file
        self.blocks_file_source_0.open(self.in_file, False)

    def get_noisevoltage(self):
        return self.noisevoltage

    def set_noisevoltage(self, noisevoltage):
        self.noisevoltage = noisevoltage
        self.channels_channel_model_0.set_noise_voltage(self.noisevoltage)

    def get_num_pream_packets(self):
        return self.num_pream_packets

    def set_num_pream_packets(self, num_pream_packets):
        self.num_pream_packets = num_pream_packets
        self.set_garbage_preamble_length_n_bytes(self.packet_size*self.num_pream_packets)
        self.custom_remove_preamble_0.set_num_pream_packets(self.num_pream_packets)

    def get_out(self):
        return self.out

    def set_out(self, out):
        self.out = out

    def get_packet_size(self):
        return self.packet_size

    def set_packet_size(self, packet_size):
        self.packet_size = packet_size
        self.set_garbage_preamble_length_n_bytes(self.packet_size*self.num_pream_packets)
        self.custom_packet_formatter_0.set_packet_size(self.packet_size)

    def get_passband_fc(self):
        return self.passband_fc

    def set_passband_fc(self, passband_fc):
        self.passband_fc = passband_fc
        self.custom_iq_complex_to_passband_real_0.set_passband_fc(self.passband_fc)
        self.custom_passband_real_to_iq_complex_0.set_passband_fc(self.passband_fc)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_variable_rrc_filter_taps_0(firdes.root_raised_cosine(self.sps+1, self.samp_rate, self.samp_rate/self.sps, 0.35, (11*self.sps)))
        self.blocks_throttle2_1.set_sample_rate(self.samp_rate)
        self.custom_iq_complex_to_passband_real_0.set_samp_rate(self.samp_rate)
        self.custom_passband_real_to_iq_complex_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_variable_rrc_filter_taps_0(firdes.root_raised_cosine(self.sps+1, self.samp_rate, self.samp_rate/self.sps, 0.35, (11*self.sps)))

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain
        self.custom_iq_complex_to_passband_real_0.set_txgain(self.txgain)

    def get_wav_out(self):
        return self.wav_out

    def set_wav_out(self, wav_out):
        self.wav_out = wav_out
        self.blocks_wavfile_sink_0.open(self.wav_out)

    def get_constellation_bpsk(self):
        return self.constellation_bpsk

    def set_constellation_bpsk(self, constellation_bpsk):
        self.constellation_bpsk = constellation_bpsk
        self.digital_constellation_decoder_cb_0.set_constellation(self.constellation_bpsk)

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code
        self.set_format_used(digital.header_format_counter(self.access_code,0,8))
        self.custom_packet_formatter_0.set_access_code(self.access_code)

    def get_variable_rrc_filter_taps_0(self):
        return self.variable_rrc_filter_taps_0

    def set_variable_rrc_filter_taps_0(self, variable_rrc_filter_taps_0):
        self.variable_rrc_filter_taps_0 = variable_rrc_filter_taps_0
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.variable_rrc_filter_taps_0)

    def get_garbage_preamble_length_n_bytes(self):
        return self.garbage_preamble_length_n_bytes

    def set_garbage_preamble_length_n_bytes(self, garbage_preamble_length_n_bytes):
        self.garbage_preamble_length_n_bytes = garbage_preamble_length_n_bytes
        self.custom_stream_prepend_0.set_garbage_preamble_length_n_bytes(self.garbage_preamble_length_n_bytes)

    def get_format_used(self):
        return self.format_used

    def set_format_used(self, format_used):
        self.format_used = format_used

    def get_adaptive_algorithm_bpsk(self):
        return self.adaptive_algorithm_bpsk

    def set_adaptive_algorithm_bpsk(self, adaptive_algorithm_bpsk):
        self.adaptive_algorithm_bpsk = adaptive_algorithm_bpsk



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--dest-host", dest="dest_host", type=str, default='127.0.0.1',
        help="Set Destination Host [default=%(default)r]")
    parser.add_argument(
        "--dest-port", dest="dest_port", type=str, default='42028',
        help="Set Destination Port [default=%(default)r]")
    parser.add_argument(
        "--filtersize", dest="filtersize", type=intx, default=84,
        help="Set Polyphase Clock Sync Filter size [default=%(default)r]")
    parser.add_argument(
        "--in-file", dest="in_file", type=str, default='in.bin',
        help="Set Input filename [default=%(default)r]")
    parser.add_argument(
        "--noisevoltage", dest="noisevoltage", type=eng_float, default=eng_notation.num_to_str(float(0.1)),
        help="Set Noise Voltage [default=%(default)r]")
    parser.add_argument(
        "--num-pream-packets", dest="num_pream_packets", type=intx, default=20,
        help="Set Number of preamble garbage packets [default=%(default)r]")
    parser.add_argument(
        "--out", dest="out", type=str, default='out.bin',
        help="Set Output filename [default=%(default)r]")
    parser.add_argument(
        "--packet-size", dest="packet_size", type=intx, default=16,
        help="Set Packet Size [default=%(default)r]")
    parser.add_argument(
        "--passband-fc", dest="passband_fc", type=eng_float, default=eng_notation.num_to_str(float(3600)),
        help="Set Passband Center Frequency [default=%(default)r]")
    parser.add_argument(
        "--samp-rate", dest="samp_rate", type=eng_float, default=eng_notation.num_to_str(float(48000)),
        help="Set Sampe Rate [default=%(default)r]")
    parser.add_argument(
        "--sps", dest="sps", type=intx, default=72,
        help="Set Samples per Symbol [default=%(default)r]")
    parser.add_argument(
        "--txgain", dest="txgain", type=eng_float, default=eng_notation.num_to_str(float(2)),
        help="Set Tx Gain [default=%(default)r]")
    parser.add_argument(
        "--wav-out", dest="wav_out", type=str, default='out.wav',
        help="Set Waveform output [default=%(default)r]")
    return parser


def main(top_block_cls=test_transceive, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(dest_host=options.dest_host, dest_port=options.dest_port, filtersize=options.filtersize, in_file=options.in_file, noisevoltage=options.noisevoltage, num_pream_packets=options.num_pream_packets, out=options.out, packet_size=options.packet_size, passband_fc=options.passband_fc, samp_rate=options.samp_rate, sps=options.sps, txgain=options.txgain, wav_out=options.wav_out)

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

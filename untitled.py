#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
import pmt
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
from gnuradio import network
import sip



class untitled(gr.top_block, Qt.QWidget):

    def __init__(self, dest_host='127.0.0.1', dest_port='42028', in_file="in.bin", out_file="out.bin", sps=48, wav_out='out.wav'):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("GNU Radio", "untitled")

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
        self.in_file = in_file
        self.out_file = out_file
        self.sps = sps
        self.wav_out = wav_out

        ##################################################
        # Variables
        ##################################################
        self.variable_constellation_0 = variable_constellation_0 = digital.constellation_calcdist([-1-1j, -1+1j, 1+1j, 1-1j], [0, 1, 3, 2],
        4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.variable_constellation_0.set_npwr(1.0)
        self.samp_rate = samp_rate = 48000
        self.access_code = access_code = "11100001010110101110100010010011"
        self.variable_rrc_filter_taps_0 = variable_rrc_filter_taps_0 = firdes.root_raised_cosine(sps+1, samp_rate,samp_rate/sps, 0.35, (11*sps))
        self.variable_low_pass_filter_taps_0 = variable_low_pass_filter_taps_0 = firdes.low_pass(1.0, samp_rate, 10e3,1e3, window.WIN_HAMMING, 6.76)
        self.variable_adaptive_algorithm_0 = variable_adaptive_algorithm_0 = digital.adaptive_algorithm_cma( variable_constellation_0, .0001, 4).base()
        self.passband_fc = passband_fc = 1700
        self.format_obj = format_obj = digital.header_format_default(access_code, 0)

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            150, #size
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
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Tx", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_1.set_plot_pos_half(not True)

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
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
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
        self.network_tcp_sink_0 = network.tcp_sink(gr.sizeof_char, 1, dest_host, int(dest_port),1)
        self.low_pass_filter_0_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                passband_fc,
                1e3,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                passband_fc,
                1e3,
                window.WIN_HAMMING,
                6.76))
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(format_obj, "packet_len")
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, (2*3.14/100), variable_rrc_filter_taps_0, 8, 0, 1.5, 2)
        self.digital_map_bb_0 = digital.map_bb([0,1,3,2])
        self.digital_linear_equalizer_0 = digital.linear_equalizer(15, 2, variable_adaptive_algorithm_0, True, [ ], 'corr_est')
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(4, digital.DIFF_DIFFERENTIAL)
        self.digital_crc32_bb_1 = digital.crc32_bb(True, "packet_len", True)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc((2*3.14/100), 4, False)
        self.digital_correlate_access_code_xx_ts_0 = digital.correlate_access_code_bb_ts(access_code,
          0, 'packet_len')
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=variable_constellation_0,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(variable_constellation_0)
        self.blocks_wavfile_sink_0 = blocks.wavfile_sink(
            wav_out,
            1,
            samp_rate,
            blocks.FORMAT_WAV,
            blocks.FORMAT_PCM_16,
            False
            )
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(2)
        self.blocks_throttle2_1 = blocks.throttle( gr.sizeof_float*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, "packet_len", 0)
        self.blocks_tag_gate_0 = blocks.tag_gate(gr.sizeof_char * 1, False)
        self.blocks_tag_gate_0.set_single_key("")
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 128, "packet_len")
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, 8, "packet_len", False, gr.GR_MSB_FIRST)
        self.blocks_multiply_xx_0_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff((-2))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(2)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, in_file, False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_complex_to_float_1 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, passband_fc, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, passband_fc, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_complex_to_float_0_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_complex_to_float_0_0, 1), (self.blocks_multiply_xx_0_0_0, 0))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.blocks_multiply_xx_0_1, 0))
        self.connect((self.blocks_complex_to_float_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_float_1, 1), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_crc32_bb_1, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_multiply_xx_0_0_0, 1))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_multiply_xx_0_1, 1))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_throttle2_1, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.blocks_tag_gate_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_tag_gate_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_throttle2_1, 0), (self.blocks_wavfile_sink_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.digital_correlate_access_code_xx_ts_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_complex_to_float_1, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.digital_crc32_bb_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_crc32_bb_0, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.digital_crc32_bb_1, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_crc32_bb_1, 0), (self.network_tcp_sink_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_linear_equalizer_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_linear_equalizer_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_float_to_complex_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "untitled")
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

    def get_in_file(self):
        return self.in_file

    def set_in_file(self, in_file):
        self.in_file = in_file
        self.blocks_file_source_0.open(self.in_file, False)

    def get_out_file(self):
        return self.out_file

    def set_out_file(self, out_file):
        self.out_file = out_file

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_variable_rrc_filter_taps_0(firdes.root_raised_cosine(self.sps+1, self.samp_rate, self.samp_rate/self.sps, 0.35, (11*self.sps)))

    def get_wav_out(self):
        return self.wav_out

    def set_wav_out(self, wav_out):
        self.wav_out = wav_out
        self.blocks_wavfile_sink_0.open(self.wav_out)

    def get_variable_constellation_0(self):
        return self.variable_constellation_0

    def set_variable_constellation_0(self, variable_constellation_0):
        self.variable_constellation_0 = variable_constellation_0
        self.digital_constellation_decoder_cb_0.set_constellation(self.variable_constellation_0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_variable_low_pass_filter_taps_0(firdes.low_pass(1.0, self.samp_rate, 10e3, 1e3, window.WIN_HAMMING, 6.76))
        self.set_variable_rrc_filter_taps_0(firdes.root_raised_cosine(self.sps+1, self.samp_rate, self.samp_rate/self.sps, 0.35, (11*self.sps)))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle2_1.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.passband_fc, 1e3, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.passband_fc, 1e3, window.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)

    def get_access_code(self):
        return self.access_code

    def set_access_code(self, access_code):
        self.access_code = access_code
        self.set_format_obj(digital.header_format_default(self.access_code, 0))

    def get_variable_rrc_filter_taps_0(self):
        return self.variable_rrc_filter_taps_0

    def set_variable_rrc_filter_taps_0(self, variable_rrc_filter_taps_0):
        self.variable_rrc_filter_taps_0 = variable_rrc_filter_taps_0
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.variable_rrc_filter_taps_0)

    def get_variable_low_pass_filter_taps_0(self):
        return self.variable_low_pass_filter_taps_0

    def set_variable_low_pass_filter_taps_0(self, variable_low_pass_filter_taps_0):
        self.variable_low_pass_filter_taps_0 = variable_low_pass_filter_taps_0

    def get_variable_adaptive_algorithm_0(self):
        return self.variable_adaptive_algorithm_0

    def set_variable_adaptive_algorithm_0(self, variable_adaptive_algorithm_0):
        self.variable_adaptive_algorithm_0 = variable_adaptive_algorithm_0

    def get_passband_fc(self):
        return self.passband_fc

    def set_passband_fc(self, passband_fc):
        self.passband_fc = passband_fc
        self.analog_sig_source_x_0.set_frequency(self.passband_fc)
        self.analog_sig_source_x_0_0.set_frequency(self.passband_fc)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.passband_fc, 1e3, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.passband_fc, 1e3, window.WIN_HAMMING, 6.76))

    def get_format_obj(self):
        return self.format_obj

    def set_format_obj(self, format_obj):
        self.format_obj = format_obj



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--dest-host", dest="dest_host", type=str, default='127.0.0.1',
        help="Set Destination Host [default=%(default)r]")
    parser.add_argument(
        "--dest-port", dest="dest_port", type=str, default='42028',
        help="Set Destination Port [default=%(default)r]")
    parser.add_argument(
        "--in-file", dest="in_file", type=str, default="in.bin",
        help="Set Input filename [default=%(default)r]")
    parser.add_argument(
        "--out-file", dest="out_file", type=str, default="out.bin",
        help="Set Output filename [default=%(default)r]")
    parser.add_argument(
        "--sps", dest="sps", type=intx, default=48,
        help="Set Samples per Symbol [default=%(default)r]")
    parser.add_argument(
        "--wav-out", dest="wav_out", type=str, default='out.wav',
        help="Set Wave file output filename [default=%(default)r]")
    return parser


def main(top_block_cls=untitled, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(dest_host=options.dest_host, dest_port=options.dest_port, in_file=options.in_file, out_file=options.out_file, sps=options.sps, wav_out=options.wav_out)

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

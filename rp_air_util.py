#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

from rp_utils import get_http_body, rp_print_escape, rp_print, html_regex

AIR_FORECAST_URL = "http://air.incheon.go.kr/airinch/dust.html"
AIR_CAI_URL = "http://air.incheon.go.kr/airinch/cai.html"
AIR_STAT = {"1": "좋음", "2": "보통", "3": "나쁨", "4": "매우나쁨"}
AIR_STAT_COLOR = {"좋음": "#00BFFF", "보통": "#32CD32", "나쁨": "#DAA520", "매우나쁨": "#FF4500", "-": "#646464"}
AIR_DATA_MIN_MAX_SIZE = [(2, 4), (9, 17), (11, 11)]
# AIR_DUST_COLUMN = {0:"미세먼지(PM-10)", 1:"미세먼지(PM-2.5)"}
# AIR_DUST_HEADER = {0:"인천", 1:"서울", 2:"경기북부", 3:"경기남부"}
# AIR_CAI_HEADER = {0:"측정소", 1:"SO2", 2:"NO2", 3:"O3", 4:"CO", 5:"PM-10", 6:"PM-2.5", 7:"CAI 지수", 8:"구분", 9:"대표오염물질"}


class AirDustUtil():
    def __init__(self):
        pass

    _debug_mode = False

    @staticmethod
    def get_air_forecast_url():
        return AIR_FORECAST_URL

    @staticmethod
    def get_air_cai_url():
        return AIR_CAI_URL

    @staticmethod
    def get_air_data_min_max_size():
        return AIR_DATA_MIN_MAX_SIZE

    @staticmethod
    def get_air_stat_color(status="-"):
        """
        상태에 따른 색상 값을 가져온다.

        :param status: 색상을 가져올 문구
        :return: 색상 코드
        """
        if AIR_STAT_COLOR.get(status) is None:
            return AIR_STAT_COLOR.get("-")

        return AIR_STAT_COLOR.get(status)

    def set_debug_mode(self, debug_mode):
        self._debug_mode = debug_mode

    def get_debug_mode(self):
        return self._debug_mode

    def get_air_dust_data(self):
        """
        미세먼지 데이터를 가져온다.

        :return: 미세먼지 데이터
        :rtype : [list or bool, list or bool, ...]
        """

        html_body = get_http_body(AIR_FORECAST_URL)
        html_body_cai = get_http_body(AIR_CAI_URL)

        return_data = []

        if html_body is False:
            return_data.append(False)
            return_data.append(False)
        else:
            try:
                html_body_encode = re.sub("<!--(.*?)-->", "", html_body)
                html_body_encode = unicode(html_body_encode, "euc-kr").encode("utf-8")

                air_forecast = self.get_air_dust_forecast(html_body_encode)
                return_data.append(air_forecast)
                rp_print_escape(air_forecast, self._debug_mode)

                air_analysis = self.get_air_dust_analysis(html_body_encode)
                return_data.append(air_analysis)
                rp_print_escape(air_analysis, self._debug_mode)

            except Exception, e:
                rp_print("[ERROR] get_air_dust_data [html_body] -> %s" % e, self._debug_mode)
                return_data.append(False)
                return_data.append(False)

        if html_body_cai is False:
            return_data.append(False)
        else:
            try:
                html_body_encode = re.sub("<!--(.*?)-->", "", html_body_cai)
                html_body_encode = unicode(html_body_encode, "euc-kr").encode("utf-8")
                air_cai = self.get_air_cai(html_body_encode)

                rp_print_escape(air_cai, self._debug_mode)
                return_data.append(air_cai)

            except Exception, e:
                rp_print("[ERROR] get_air_dust_data [html_body_cai] -> %s" % e, self._debug_mode)
                return_data.append(False)

        return return_data

    def get_air_dust_forecast(self, html_body):
        """
        미세먼지 예보현황(오늘, 내일)

        :param html_body: 원본 웹 페이지 데이터
        :return: 미세먼지 데이터
        :rtype : list or bool
        """
        forecast_data = []

        try:
            forecast_header_today = html_regex(html_body, "font-weight:bold['\"]>", "<br")
            forecast_header_tomorrow = html_regex(html_body, "", "<br />\[내일예보\]")
            forecast_icon = html_regex(html_body, "<img src=['']images/Harange/level_", "['.]png")

            if len(forecast_header_today) == 0:
                forecast_header_today.append("")

            if len(forecast_header_tomorrow) == 0:
                forecast_header_tomorrow.append("")

            if len(forecast_icon) >= 1:
                forecast_data.append(forecast_header_today[0])
                forecast_data.append(AIR_STAT[forecast_icon[0]])

            if len(forecast_icon) >= 2:
                forecast_data.append(forecast_header_tomorrow[0])
                forecast_data.append(AIR_STAT[forecast_icon[1]])

        except Exception, e:
            rp_print("[ERROR] getAirDustForecast -> %s" % e, self._debug_mode)
            return False

        return forecast_data

    def get_air_dust_analysis(self, html_body):
        """
        미세먼지 예보분석(오늘, 내일)

        :param html_body: 원본 웹 페이지 데이터
        :return: 미세먼지 데이터
        :rtype : list or bool
        """
        analysis_data = []

        try:
            analysis_header_time = html_regex(html_body, "<span tabindex=['']0['']>", "</span>")
            analysis_status = html_regex(html_body, "<span sytyle=\"text-align:center\">", "</span>")

            if len(analysis_header_time) < 3:
                analysis_header_time.append("")
                analysis_header_time.append("")
                analysis_header_time.append("")

            analysis_header = html_regex(analysis_header_time[2], "['(]", "[')]")
            analysis_data.append(analysis_header[0])

            for status in analysis_status:
                analysis_data.append(status)

        except Exception, e:
            rp_print("[ERROR] getAirDustAnalysis -> %s" % e, self._debug_mode)
            return False

        return analysis_data

    def get_air_cai(self, html_body):
        """
        CAI 지수

        :param html_body: 원본 웹 페이지 데이터
        :return: CAI 지수 데이터
        :rtype : list or bool
        """
        cai_data = []

        try:
            cai_header = html_regex(html_body, ">\[", "\]</a>")
            cai_status = html_regex(html_body, "<tr", "</tr>")

            cai_status_regex = []
            for i, value in enumerate(cai_status):
                checker = html_regex(value, "<span tabindex=[']0[']>", "</span>")

                if checker[0] == "부평":
                    checker_join = "\t".join(checker)
                    checker_join = re.sub("['<](.*?)['>]", "", checker_join)
                    cai_status_regex = str(checker_join).split("\t")
                    break
                else:
                    continue

            if len(cai_status_regex) > 0:
                cai_data = [cai_header[0]] + cai_status_regex

        except Exception, e:
            rp_print("[ERROR] getAirCAI -> %s" % e, self._debug_mode)
            return False

        return cai_data

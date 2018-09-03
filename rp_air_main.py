#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import uic

import rp_settings
from rp_air_main_ui import Ui_MainWindow
from rp_air_util import AirDustUtil
from rp_utils import resource_path, resize_list, ui_text, rp_len, run_cmd, os_info, WEB_COMMAND

# PySide
# from PySide import QtCore
# from PySide import QtGui
# from PySide import QtUiTools


# PATH_MAIN_UI = "ui/rp_air_main_ui.ui"
PATH_WIN_ICON = "ui/icon/icon_512.png"

# 프로젝트 기본 환경 설정
Setting = rp_settings.Init()
Setting.set_debug_mode(False)

# 미세먼지 데이터 클래스
AirDustUtil = AirDustUtil()
AirDustUtil.set_debug_mode(False)
AIR_DUST_MIN_MAX_SIZE = AirDustUtil.get_air_data_min_max_size()

# PyQt4 uic
# uic_form_class = uic.loadUiType(PATH_MAIN_UI)[0]  # todo PySide 변환 함수
# uic_form_class = Ui_MainWindow


class AirDustMainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """
    메인 클래스 : PyQt4
    """

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(resource_path(PATH_WIN_ICON)))

        self.pushButton_refresh_data.clicked.connect(self.ui_all_data)
        self.pushButton_forecast.clicked.connect(lambda: self.run_browser(AirDustUtil.get_air_forecast_url()))
        self.pushButton_cai.clicked.connect(lambda: self.run_browser(AirDustUtil.get_air_cai_url()))

        # self.QGroupBox.setStyleSheet("border-style: solid;border-width: 1px;border-color:black;")
        # self.groupBox_forecast.setStyleSheet("border-style: solid;border-width: 1px;border-color:black;")
        # self.groupBox_forecast.setPalette()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.timer_timeout)
        self.timer.start(1000 * 60 * 5)

        self.init_timer = QtCore.QTimer(self)
        self.init_timer.timeout.connect(self.init_timer_timeout)
        self.init_timer.start(1000 * 1)

        # self.timer.timeout.emit()
        # self.ui_all_data()

        # self.timerEvent(self.slot_timer_timeout)
        # self.startTimer()
        # self.pButton01.clicked.connect(self.pButton01_clicked) # Example
        # self.connect(self.pButton01_clicked, SIGNAL("clicked()"), self.pButton01_clicked) # Example
        # self.set_all_data()

    # def pButton01_clicked(self):
    #     self.label01.setText(Rutil.KOR("천재"))

    def ui_status_bar(self, msg, timeout=3):
        """
        StatusBar 문구를 설정한다.

        :param msg: 보여줄 메시지
        :param timeout: 보여줄 시간
        """

        self.statusbar.showMessage(ui_text(msg), timeout * 1000)

    def ui_clear_all(self):
        """
        모든 UI 내용을 초기화 한다.
        """

        self.ui_air_dust_forecast([])
        self.ui_air_dust_analysis([])
        self.ui_air_dust_cai([])

    def ui_all_data(self):
        """
        미세먼지 데이터 가져오기
        """

        self.ui_status_bar("초기화중...")
        self.pushButton_refresh_data.setEnabled(False)
        self.ui_clear_all()

        self.ui_status_bar("데이터 요청중...", 60)
        air_dust_data = AirDustUtil.get_air_dust_data()
        self.ui_status_bar("데이터 분석중...")
        air_dust_data = resize_list(air_dust_data, rp_len(AIR_DUST_MIN_MAX_SIZE), rp_len(AIR_DUST_MIN_MAX_SIZE), [])

        self.ui_air_dust_forecast(air_dust_data[0])
        self.ui_air_dust_analysis(air_dust_data[1])
        self.ui_air_dust_cai(air_dust_data[2])
        self.ui_status_bar("완료")
        self.pushButton_refresh_data.setEnabled(True)

    def ui_air_dust_forecast(self, param_data):
        """
        미세먼지 예보현황 UI 적용

        :param param_data: 입력할 데이터
        """

        forecast_data = resize_list(param_data, AIR_DUST_MIN_MAX_SIZE[0][1], AIR_DUST_MIN_MAX_SIZE[0][1], "-")
        self.label_forecast_today_time.setText(ui_text(forecast_data[0]))
        self.label_forecast_today_status.setText(ui_text(forecast_data[1]))
        self.label_forecast_tomorrow_time.setText(ui_text(forecast_data[2]))
        self.label_forecast_tomorrow_status.setText(ui_text(forecast_data[3]))

        self.label_forecast_today_status.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(forecast_data[1]))
        self.label_forecast_tomorrow_status.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(forecast_data[3]))

    def ui_air_dust_analysis(self, param_data):
        """
        미세먼지 예보분석 UI 적용

        :param param_data: 입력할 데이터
        """

        if rp_len(param_data) < AIR_DUST_MIN_MAX_SIZE[1][1]:
            is_tomorrow = False
        else:
            is_tomorrow = True

        analysis_data = resize_list(param_data, AIR_DUST_MIN_MAX_SIZE[1][1], AIR_DUST_MIN_MAX_SIZE[1][1], "-")

        self.label_analysis_time.setText(ui_text(analysis_data[0]))

        self.label_analysis_pm10_today_01.setText(ui_text(analysis_data[1]))
        self.label_analysis_pm10_today_02.setText(ui_text(analysis_data[2]))
        self.label_analysis_pm10_today_03.setText(ui_text(analysis_data[3]))
        self.label_analysis_pm10_today_04.setText(ui_text(analysis_data[4]))

        self.label_analysis_pm25_today_01.setText(ui_text(analysis_data[5]))
        self.label_analysis_pm25_today_02.setText(ui_text(analysis_data[6]))
        self.label_analysis_pm25_today_03.setText(ui_text(analysis_data[7]))
        self.label_analysis_pm25_today_04.setText(ui_text(analysis_data[8]))

        self.label_analysis_pm10_today_01.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[1]))
        self.label_analysis_pm10_today_02.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[2]))
        self.label_analysis_pm10_today_03.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[3]))
        self.label_analysis_pm10_today_04.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[4]))

        self.label_analysis_pm25_today_01.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[5]))
        self.label_analysis_pm25_today_02.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[6]))
        self.label_analysis_pm25_today_03.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[7]))
        self.label_analysis_pm25_today_04.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[8]))

        if is_tomorrow:
            self.label_analysis_tomorrow_title.setText(ui_text(analysis_data[0]))
        else:
            self.label_analysis_tomorrow_title.setText(ui_text("-"))

        self.label_analysis_pm10_tomorrow_01.setText(ui_text(analysis_data[9]))
        self.label_analysis_pm10_tomorrow_02.setText(ui_text(analysis_data[10]))
        self.label_analysis_pm10_tomorrow_03.setText(ui_text(analysis_data[11]))
        self.label_analysis_pm10_tomorrow_04.setText(ui_text(analysis_data[12]))

        self.label_analysis_pm25_tomorrow_01.setText(ui_text(analysis_data[13]))
        self.label_analysis_pm25_tomorrow_02.setText(ui_text(analysis_data[14]))
        self.label_analysis_pm25_tomorrow_03.setText(ui_text(analysis_data[15]))
        self.label_analysis_pm25_tomorrow_04.setText(ui_text(analysis_data[16]))

        self.label_analysis_pm10_tomorrow_01.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[9]))
        self.label_analysis_pm10_tomorrow_02.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[10]))
        self.label_analysis_pm10_tomorrow_03.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[11]))
        self.label_analysis_pm10_tomorrow_04.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[12]))

        self.label_analysis_pm25_tomorrow_01.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[13]))
        self.label_analysis_pm25_tomorrow_02.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[14]))
        self.label_analysis_pm25_tomorrow_03.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[15]))
        self.label_analysis_pm25_tomorrow_04.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(analysis_data[16]))

    def ui_air_dust_cai(self, param_data):
        """
        CAI UI 적용

        :param param_data: 입력할 데이터
        """

        cai_data = resize_list(param_data, AIR_DUST_MIN_MAX_SIZE[2][1], AIR_DUST_MIN_MAX_SIZE[2][1], "-")

        self.label_cai_time.setText(ui_text(cai_data[0]))

        self.label_cai_city_01.setText(ui_text(cai_data[1]))
        self.label_cai_so2_01.setText(ui_text(cai_data[2]))
        self.label_cai_no2_01.setText(ui_text(cai_data[3]))
        self.label_cai_o3_01.setText(ui_text(cai_data[4]))
        self.label_cai_co_01.setText(ui_text(cai_data[5]))
        self.label_cai_pm10_01.setText(ui_text(cai_data[6]))
        self.label_cai_pm25_01.setText(ui_text(cai_data[7]))
        self.label_cai_cai_01.setText(ui_text(cai_data[8]))
        self.label_cai_status_01.setText(ui_text(cai_data[9]))
        self.label_cai_maxstatus_01.setText(ui_text(cai_data[10]))

        self.label_cai_status_01.setStyleSheet("background-color: " + AirDustUtil.get_air_stat_color(cai_data[9]))

    def timer_timeout(self):
        """
        일정 주기마다 동작
        """

        self.ui_all_data()

    def init_timer_timeout(self):  # todo Thread로 대체
        """
        초기화면 설정 후 단 한번 실행하기 위한 동작 모음
        """

        self.init_timer.stop()

        self.timer_timeout()

    def run_browser(self, url):
        """
        특정 URL을 보여주는 웹 브라우저를 실행한다.
        """

        command = WEB_COMMAND.get("WIN")
        os_name = os_info()

        if os_name.find("window") > 0 or os_name.find("win32"):
            command = WEB_COMMAND.get("WIN")
        elif os_name.find("linux") > 0:
            command = WEB_COMMAND.get("LINUX")
        elif os_name.find("darwin") > 0:
            command = WEB_COMMAND.get("MAC")
        else:
            return False

        run_cmd(command + url)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MainClass = AirDustMainWindow(None)
    MainClass.show()
    sys.exit(app.exec_())

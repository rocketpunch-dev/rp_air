#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from tendo import singleton

from rp_utils import rp_print

me = singleton.SingleInstance()  # 1개만 실행 가능
DISPLAY_MODE = dict(CONSOLE=0, GUI=1, ALL=2)


class Init:  # todo 로그 기능, 다국어 기능
    """
    Init Class
    시스템에서 기본적으로 설정해야 하는 기능을 처리한다.
    """

    _debug_mode = False
    _display_mode = DISPLAY_MODE["CONSOLE"]

    def __init__(self):
        self.set_default_charset()

    def set_default_charset(self, charset="utf-8"):  # Bad Code
        """
        unicode 변환시 기본 인코딩 명시적 설정을 한다.

        :param charset: 캐릭터셋
        """
        reload(sys)
        rp_print("Get Default Encoding [%s]" % sys.getdefaultencoding(), self._debug_mode)
        sys.setdefaultencoding(charset)
        rp_print("Set Default Encoding [%s]" % sys.getdefaultencoding(), self._debug_mode)

    def set_debug_mode(self, debug_mode):
        self._debug_mode = debug_mode

    def get_debug_mode(self):
        return self._debug_mode

    def set_display_mode(self, display_mode):
        self._display_mode = display_mode

    def get_display_mode(self):
        return self._display_mode

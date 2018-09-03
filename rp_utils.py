#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import platform
import re
import sys
import urllib

WEB_COMMAND = dict(WIN="rundll32 url.dll,FileProtocolHandler ", MAC="", LINUX="", WIN2="start ")  # todo mac, windows version


def ui_text(text_str):  # todo 다국어 고려
    """
    한글 표출용 Define 함수
    QT UI 에서 한글이 깨지는 현상처리

    :param text_str: 변환시킬 텍스트

    :return: unicode 변환 텍스트
    :rtype : str
    """

    try:
        unicode_str = unicode(text_str)

    except Exception, e:
        rp_print("[ERROR] ui_text -> %s" % e)
        return text_str

    return unicode_str


def rp_print(param, debug=False):  # todo log 연동, console / gui 구분 출력
    """
    통합 print

    :param param: print 할 내용
    :param debug: DEBUG 모드 flag 변수

    :return: 원본 param
    :rtype : object
    """

    if debug:
        print param

    return param


def rp_print_escape(param, debug=False):
    """
    escape 출력기능

    :param param: 출력할 object(list)
    :param debug:

    :return: 원본 param
    :rtype : object
    """

    if debug:
        rp_print(repr(param).decode('string-escape'), debug)

    return param


def get_http_body(dns):  # todo POST 방식 고려 / 파라미터 추가
    """
    HTTP 요청에 따른 body 값을 가져온다.

    :param dns: 요청할 도메인명

    :return: 요청하여 받은 body 내용 / 실패시 False
    :rtype : str or bool
    """

    rp_print("[GET] [HTTP] [%s]" % dns)

    try:
        return_value = urllib.urlopen(dns).read()

    except Exception, e:
        rp_print("[ERROR] get_http_body -> %s" % e)
        return_value = False

    return return_value


def html_regex(source, start_pattern, end_pattern):  # todo 정규식 모듈 추가(sub, match, search...)
    """
    정규식 : 원본 str 내 정규식 조건에 맞는 값을 찾는다.

    :param source: 원본 str
    :param start_pattern: 시작 패턴
    :param end_pattern: 끝 패턴

    :return: 정규식 조건에 부합하는 값 list
    """

    pattern = "%s(.*?)%s" % (start_pattern, end_pattern)

    return re.findall(pattern, source)


def resize_list(source, min_size, max_size, append_data=""):
    """
    list 의 사이즈를 확인하여 사이즈가 작을 경우 데이터를 추가시킨다.
    min_size 보다 작을 경우 min_size 만큼 추가
    min_size 보다 크고 max_size 보다 작을 경우 max_size 만큼 추가

    :param source: 원본 list
    :param min_size: 최소 크기
    :param max_size: 최대 크기
    :param append_data: 추가시킬 값

    :return: 사이즈 적용된 리스트
    :rtype : list
    """

    if isinstance(source, list):
        list_source = source
        len_source = len(source)
    else:
        list_source = []
        len_source = 0

    if len_source < min_size:
        for i in range(len_source, min_size):
            list_source.append(append_data)
    elif len_source < max_size:
        for i in range(len_source, max_size):
            list_source.append(append_data)

    return list_source


def os_info():
    """
    OS 이름을 알려준다.

    :return: OS 이름(lower case)
    :rtype : str
    """

    return platform.system().lower()


def run_cmd(command):
    """
    시스템 명령어 실행 함수

    :param command:
    """
    os.system(rp_print(command))


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS

    except:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def rp_len(param):
    """
    변수의 길이를 리턴한다.
    변수의 길이를 확인 할 수 없는 타입 인 경우 -1을 리턴한다.

    :param param: len 확인 변수
    :return : len(변수) or -1
    """

    try:
        len_param = len(param)
    except:
        len_param = -1

    return len_param

# -*- coding: utf-8 -*-

from app.constants import Code


def record_success(in_type, result):
    success, match = Code.FAIL_PECORED, Code.FAIL_PECORED

    if in_type in ["xiaoshi_idcard"]:
        code = int(result.get("RESULT"))
        if code in [1, 2, 3]:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["tianxing_idcard"]:
        code = int(result.get("result"))
        if code == 1 or code == -1 or code == 3:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["ccx_idcard"]:
        code = result.get("resCode", "") or ""
        if code == "2011" or code == "2010":
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["yunbei_address"]:
        code = int(result.get("code"))
        if code == 1:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        elif code == -1 or code == -2:
            pass
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["youla_address"]:
        code = str(result.get("code"))
        if code == "0000":
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        elif code == "0002":
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["screen_telecomtime", "screen_cmcctime",
                   "screen_unicomtime"]:
        code = int(result.get("RESULT"))
        if code in [1, 2, 3, 4, 5, 6]:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        elif code == -1:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["tianxing_cmcctime"]:
        code = result.get("result")
        if code == "-1" or isinstance(code, dict):
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["datatang_telecomtime"]:
        code = result.get("resCode") or result.get("status")
        if code == "0000":
            res = result.get("data").get("result").get("netLength")
            if res in ["A", "B", "C", "D", "E", "F"]:
                success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
            else:
                success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["datatang_unicomtime"]:
        code = result.get("resCode") or result.get("status")
        if code == "0000":
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["datatang_cmcctime"]:
        code = result.get("resCode") or result.get("status")
        if code == "0000":
            res = result.get("data").get("result").get("netLength")
            if res == "0":
                success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
            else:
                success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["screen_cmccby3ele", "screen_bankcardby3ele",
                   "screen_bankcardby4ele"]:
        code = int(result.get("RESULT"))
        if code in [1, 2]:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["screen_unicomby3ele", "screen_telecomby3ele"]:
        code = int(result.get("RESULT"))
        if code in [1, 2, 3]:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["screen_idnamefacecheck"]:
        code = int(result.get("RESULT"))
        if code in [1, 2, 3, 4]:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["datatang_bankcardby3ele", "datatang_bankcardby4ele"]:
        code = result.get("resCode") or result.get("status")
        if code == "0000":
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["datatang_operatorby3ele"]:
        code = result.get("resCode") or result.get("status")
        if code == "0000":
            res = result.get("data").get("result")
            if res in ["1", "-1"]:
                success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
            else:
                success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["ccx_bankcardby3ele", "ccx_bankcardby4ele"]:
        code = result.get("resCode")
        if code in ["2030", "2031"]:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["wescore_netloanblacklist"]:
        code = result.get("CODE")
        if code == "0":
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["wescore_riskinfocheck"]:
        code = result.get("CODE")
        if code in ["201", "0"]:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["ccx_operatorby3ele"]:
        code = result.get("resCode")
        if code in ["2060", "2061"]:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["ccx_phonetime"]:
        code = result.get("resCode")
        if code in ["0000"]:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["zm_fraudscore", "zm_verifyfraudmsg", "zm_fraudrisklist"]:
        if result.get("success"):
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["zmop_score", "zmop_watchlist"]:
        status = result.get("success")
        if status:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["moxie_funddetail", "moxie_securitydetail", "moxie_fundreport", "moxie_securityreport"]:
        if result:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["wescore_education"]:
        code = result.get("CODE")
        if code in ["0", "200", "201"]:
            success, match = Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            success, match = Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["junyu_idcardOCR", "junyu_bankcardOCR", "junyu_drivinglicenseOCR", "junyu_vehiclelicenseOCR"]:
        if result.get("code") == 0:
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED
    if in_type == "junyu_piccompare":
        code = result.get("code")
        if code in [0, 1, 2, -1200, -1201, -1202, -1203, -1204, -1205, -1205,
                    -1206, -1208, -1209, -1210, -1211]:
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type == "shengdun_loanintegration":
        code = result.get("CODE")
        if code == "200":
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type == "shengdun_loanriskinquiry":
        code = result.get("code")
        if code == "0000":
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type == "moxie_peoplebankreport":
        if result:
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type == "kaola_loandebtdetail":
        if result.get("result") == "1":
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["shengdun_accountverify"]:
        if result.get("resp_body", {}).get("msg", {}).get("queryStatus") == 1:
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED
    if in_type in ["shengdun_drivinglicensestatus", "shengdun_licenseidcheck", "shengdun_firsthavelicense",
                   "shengdun_candrivecar", "shengdun_drivinglicenseauth"]:
        if result.get("status") == "1":
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED
    if in_type in ["shengdun_vehiclebreakrule", "shengdun_housevalue"]:
        if result.get("code") in ["0000", 200]:
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["kaola_cmccby3ele", "kaola_unicomby3ele", "kaola_telecomby3ele"]:
        if result.get("result") in ["T", "F", "0", "1"]:
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["kaola_cmcctime", "kaola_unicomtime", "kaola_telecomtime"]:
        # 考拉在网时长返回Z代表查询无记录，不计费
        if result.get("result") == "Z":
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED
        else:
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED

    if in_type in ["kaola_cmccstatus", "kaola_unicomstatus", "kaola_telecomstatus"]:
        # 考拉在网状态返回9代表查询无记录，不计费
        if result.get("result") == "9":
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED
        else:
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED

    if in_type == "kaola_idcardpic":
        if result.get("result") in ["00", "01"]:
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type == "kaola_dishonesty":
        if result.get("result") == "01":
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type in ["kaola_banktrans", "kaola_personaleducation"]:
        if result.get("result") == "0":
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED

    if in_type == "kaola_airpassengerinfo":
        if result.get("result") == "200":
            return Code.SUCCESS_RECORED, Code.SUCCESS_RECORED
        else:
            return Code.SUCCESS_RECORED, Code.FAIL_PECORED

    return success, match

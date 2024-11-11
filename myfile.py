import time, os, math, pyautogui as ui, pyperclip
from datetime import datetime, timedelta
import win32gui, requests, json, win32con, random, paramiko
from ftplib import FTP
import threading, io, logging, traceback, sqlite3, socket, webview, ctypes, keyboard, hashlib, subprocess, sys, psutil, win32process, winreg
ui.FAILSAFE = False
robotIsOffline = False
clearMotoTime = ""
showZJLHD = True
currentVer = "1.0"
bjxHost = "111"
bjxFtpport = "222"
bjxUser = "333"
bjxPwd = "444"
bjxFtpType = "555"
lastLogsName = {
  'chat': "",
  'gameplay': "",
  'kill': "",
  'login': ""}
sys.stdout = io.TextIOWrapper((sys.stdout.buffer), encoding="utf-8")
datatableConnect2 = sqlite3.connect("beijixiong.db")
datatableConnect = sqlite3.connect("beijixiong.db")
logging.basicConfig(filename="error.log", level=(logging.ERROR))
serverRoot = "https://scum.52ai.org/public/index.php/index/index/"
loginFtpIsPending = False
killFtpIsPending = False
longhudouObj = {'isOpen':"0", 
 'currentTotoalAmount':"0"}
zjLonghdObj = {
  'uperSteamid': "",
  'uperName': "系统",
  'uperTimes': "0",
  'todayAmount': "0",
  'totalAmount': "0",
  'lastDate': ""}
fakeNameNeedFresh = True
checkServerIsRight = False
goodsKeys = []
qaKeys = []
qaObjs = []
transKeys = []
giftsKeys = []
zjLonghdKeys = []
timeAnnKyes = []
timeAnnObjs = {}
goodsObjs = {}
transObjs = {}
giftsObjs = {}
vipGiftsObjs = {}
vipGiftsKeys = []
choujiangKeys = []
lotteryObjs = {}
robotOptions = {}
totalRobotOptions = {}
lastVIPGiftChatArr = []
needSendLoginLogArr = []
needSendKillLogArr = []
godModePlayerLoginByDroneArr = []
monitPlayerLoginByDroneSended = []
lastLoginLogArr = []
lastKillLogArr = []
sendedGiftDataObj = {}
ftp = None
sftp = None
t = None
adminKyes = ["@取消装备卡","@授予装备卡","@更新联办","@清理垃圾","@重置红包","@重置记录","@修改称号等级","@取消自定义称号","@设置自定义称号","@修改vip等级","@修改vip到期时间","@充值熊币","@扣除熊币","@初始化称号","@权限监控","@取消监控","@授予权限","@取消权限","@查询所有权限","@查询指定权限","@重启机器人","@重置称号","@重置所有人称号","@重置VIP","@重置所有人VIP"]
isOnlyGift = False
directory = ""
initChoujiangKey = "@抽奖"
userZJLhdWinRatio = 0.5
systemZJLhdWinRatio = 0.5
needTransNewPlayer = []
threadPool = []
stop_event = threading.Event()
window = None
robotIsRunning = False
robotRunLogs = []
robotIsSlow = 0
ftpHasPlugin = False

def printToLog(val):
    global robotRunLogs
    if len(robotRunLogs) > 15:
        robotRunLogs.pop(0)
    robotRunLogs.append(str(val))


def checkDatabase():
    global datatableConnect
    global ftpHasPlugin
    global systemZJLhdWinRatio
    global userZJLhdWinRatio
    directory = os.getcwd()
    folder_path = directory + "/Plugin"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    folder_path = directory + "/Logs"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    WinSCPName = directory + "/Plugin/WinSCP.com"
    if os.path.exists(WinSCPName):
        ftpHasPlugin = True
    contJson = {'userZJLhdWinRatio':"0.5", 
     'systemZJLhdWinRatio':"0.5"}
    with open((directory + "/LHDRatio.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/LHDRatio.txt"), "r", encoding="utf-8") as file:
        try:
            contJson = json.load(file)
        except Exception as e:
            try:
                with open((directory + "/LHDRatio.txt"), "w", encoding="UTF-8") as f:
                    f.write(json.dumps(contJson, ensure_ascii=False))
            finally:
                e = None
                del e

    if "userZJLhdWinRatio" in contJson:
        userZJLhdWinRatio = float(contJson["userZJLhdWinRatio"])
        systemZJLhdWinRatio = float(contJson["systemZJLhdWinRatio"])
    userCursor = datatableConnect.cursor()
    userCursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sign_log'")
    table_exists = userCursor.fetchone() is not None
    if not table_exists:
        userCursor.execute("\n            CREATE TABLE sign_log (\n                sign_id INTEGER PRIMARY KEY AUTOINCREMENT,\n                player_name VARCHAR(255),\n                player_steamid VARCHAR(255),\n                sign_date VARCHAR(60),\n                sign_time VARCHAR(60)\n            )\n        ")
        printToLog("车险保单表创建成功.")
    userCursor = datatableConnect.cursor()
    userCursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='car_insur'")
    table_exists = userCursor.fetchone() is not None
    if not table_exists:
        userCursor.execute("\n            CREATE TABLE car_insur (\n                insur_id INTEGER PRIMARY KEY AUTOINCREMENT,\n                player_name VARCHAR(255),\n                player_steamid VARCHAR(255),\n                insurd_time VARCHAR(60),\n                end_insur_time VARCHAR(60),\n                last_car_id VARCHAR(60),\n                car_type VARCHAR(60),\n                get_time_space VARCHAR(60),\n                total_max VARCHAR(60),\n                day_max VARCHAR(60),\n                is_destory VARCHAR(60)\n            )\n        ")
        printToLog("车险保单表创建成功.")
    userCursor = datatableConnect.cursor()
    userCursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='car_insur_get_list'")
    table_exists = userCursor.fetchone() is not None
    if not table_exists:
        userCursor.execute("\n            CREATE TABLE car_insur_get_list (\n                get_id INTEGER PRIMARY KEY AUTOINCREMENT,\n                player_name VARCHAR(255),\n                player_steamid VARCHAR(255),\n                insur_id VARCHAR(255),\n                get_time VARCHAR(60),\n                car_type VARCHAR(60),\n                get_location VARCHAR(255),\n                pre_car_id VARCHAR(60),\n                pre_car_owner VARCHAR(60),\n                cur_car_id VARCHAR(60),\n                is_destoryed VARCHAR(10)\n                           \n            )\n        ")
        printToLog("车险领取记录表创建成功.")
    userCursor = datatableConnect.cursor()
    userCursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='lhd_log'")
    table_exists = userCursor.fetchone() is not None
    if not table_exists:
        userCursor.execute("\n            CREATE TABLE lhd_log (\n                lhd_id INTEGER PRIMARY KEY AUTOINCREMENT,\n                player_name VARCHAR(255),\n                player_steamid VARCHAR(255),\n                play_amount VARCHAR(255),\n                win_amount VARCHAR(255),\n                result VARCHAR(40),\n                uper_name VARCHAR(255),\n                uper_steamid VARCHAR(255),\n                date VARCHAR(40),\n                time VARCHAR(40)\n            )\n        ")
        printToLog("用户表创建成功.")
    userCursor = datatableConnect.cursor()
    userCursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='card_list'")
    table_exists = userCursor.fetchone() is not None
    if not table_exists:
        userCursor.execute("\n            CREATE TABLE card_list (\n                card_id INTEGER PRIMARY KEY AUTOINCREMENT,\n                card_value VARCHAR(255),\n                card_name VARCHAR(255),\n                card_code TEXT(9999999),\n                gold_num VARCHAR(40),\n                amount_num VARCHAR(40),\n                fame_num VARCHAR(40),\n                xiong_num VARCHAR(40),         \n                card_state VARCHAR(40),\n                create_time VARCHAR(255),\n                send_time VARCHAR(255),\n                player_steamid VARCHAR(255),\n                player_name VARCHAR(255)\n            )\n        ")
        printToLog("礼品卡表创建成功.")
    userCursor.execute("PRAGMA table_info(card_list);")
    table_info = userCursor.fetchall()
    column_names = [col[1] for col in table_info]
    print(column_names)
    if "admin_time" not in column_names:
        userCursor.execute("ALTER TABLE card_list ADD COLUMN admin_time VARCHAR(40) DEFAULT '0'")
    datatableConnect.commit()
    userCursor = datatableConnect.cursor()
    userCursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user_list'")
    table_exists = userCursor.fetchone() is not None
    if not table_exists:
        userCursor.execute("\n            CREATE TABLE user_list (\n                user_id INTEGER PRIMARY KEY AUTOINCREMENT,\n                user_name VARCHAR(255),\n                nick_name VARCHAR(255),\n                amount VARCHAR(40),\n                reg_time VARCHAR(40),\n                total_time VARCHAR(40),\n                last_log_time VARCHAR(40),\n                vip_level VARCHAR(40),\n                vip_end_time VARCHAR(40),\n                integral VARCHAR(40),\n                steam_id VARCHAR(40),\n                normal_integral VARCHAR(40),\n                normal_vip_level VARCHAR(40)\n            )\n        ")
        printToLog("龙虎斗记录表创建成功.")
    userCursor.execute("PRAGMA table_info(user_list);")
    table_info = userCursor.fetchall()
    column_names = [col[1] for col in table_info]
    print(column_names)
    if "normal_integral" not in column_names:
        userCursor.execute("ALTER TABLE user_list ADD COLUMN normal_integral VARCHAR(40) DEFAULT '0'")
    if "normal_vip_level" not in column_names:
        userCursor.execute("ALTER TABLE user_list ADD COLUMN normal_vip_level VARCHAR(40) DEFAULT '0'")
    if "custom_title" not in column_names:
        userCursor.execute("ALTER TABLE user_list ADD COLUMN custom_title VARCHAR(200) DEFAULT ''")
    if "gift_cards" not in column_names:
        userCursor.execute("ALTER TABLE user_list ADD COLUMN gift_cards TEXT DEFAULT ''")
    if "skill_data" not in column_names:
        userCursor.execute("ALTER TABLE user_list ADD COLUMN skill_data TEXT DEFAULT ''")
    datatableConnect.commit()
    sendGiftCursor = datatableConnect.cursor()
    sendGiftCursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sended_gift'")
    table_exists = sendGiftCursor.fetchone() is not None
    if table_exists:
        sendGiftCursor.execute("PRAGMA table_info(sended_gift);")
        table_info = sendGiftCursor.fetchall()
        has_primary_key = False
        for row in table_info:
            if row[5] == 1:
                has_primary_key = True
                break

        if not has_primary_key:
            printToLog("领取记录表没有主键，创建新领取记录表")
            sendGiftCursorNew = datatableConnect.cursor()
            sendGiftCursorNew.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sended_gift_new'")
            table_exists = sendGiftCursorNew.fetchone() is not None
            if not table_exists:
                sendGiftCursorNew.execute("\n                    CREATE TABLE sended_gift_new (\n                        id INTEGER PRIMARY KEY AUTOINCREMENT,\n                        server_time VARCHAR(50),\n                        local_time VARCHAR(50),\n                        keyword VARCHAR(100),\n                        username VARCHAR(200),\n                        usercode VARCHAR(50),\n                        steamid VARCHAR(50)\n                    )\n                ")
                printToLog("领取记录表创建成功.")
            sendGiftCursor.execute("INSERT INTO sended_gift_new (server_time, local_time, keyword, username, usercode, steamid) SELECT server_time, local_time, keyword, username, usercode, steamid FROM sended_gift")
            sendGiftCursor.execute("DROP TABLE IF EXISTS sended_gift")
            sendGiftCursor.execute("ALTER TABLE sended_gift_new RENAME TO sended_gift")
            datatableConnect.commit()
    else:
        printToLog("领取记录表不存在，创建领取记录表")
        sendGiftCursorNew = datatableConnect.cursor()
        sendGiftCursorNew.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sended_gift'")
        table_exists = sendGiftCursorNew.fetchone() is not None
        if not table_exists:
            sendGiftCursorNew.execute("\n                CREATE TABLE sended_gift (\n                    id INTEGER PRIMARY KEY AUTOINCREMENT,\n                    server_time VARCHAR(50),\n                    local_time VARCHAR(50),\n                    keyword VARCHAR(100),\n                    username VARCHAR(200),\n                    usercode VARCHAR(50),\n                    steamid VARCHAR(50)\n                )\n            ")
        printToLog("导入新表成功")


checkDatabase()

def createSigninLog(obj):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("INSERT INTO sign_log (player_name, player_steamid, sign_date, sign_time) VALUES (?, ?, ?, ?)", (obj[0], obj[1], obj[2], obj[3]))
    datatableConnectLocal.commit()
    cursor.close()
    datatableConnectLocal.close()


def getTotalSigninLogList():
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("SELECT * FROM sign_log")
    results = cursor.fetchall()
    cursor.close()
    datatableConnectLocal.close()
    return results


def getSigninLogBySteamid(id):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("SELECT * FROM sign_log WHERE player_steamid = ?", (id,))
    results = cursor.fetchall()
    cursor.close()
    datatableConnectLocal.close()
    return results


def getSigninLogBySteamidAndDate(id, date):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("SELECT * FROM sign_log WHERE player_steamid = ? AND sign_date = ? ", (id, date))
    results = cursor.fetchall()
    cursor.close()
    datatableConnectLocal.close()
    return results


def deleteSigninLogById(id):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("DELETE FROM sign_log WHERE sign_id = ?", (id,))
    datatableConnectLocal.commit()
    cursor.close()
    datatableConnectLocal.close()


def createCarInsurPolicy(obj):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("INSERT INTO car_insur (player_name, player_steamid, insurd_time, end_insur_time, last_car_id, car_type, get_time_space, total_max, day_max, is_destory) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7], obj[8], obj[9]))
    datatableConnectLocal.commit()
    cursor.close()
    datatableConnectLocal.close()


def updateCarInsurPolicy(data):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    for i in data:
        cursor.execute("UPDATE car_insur SET " + i + " = ? WHERE insur_id = ?", (data[i], data["insur_id"]))

    datatableConnectLocal.commit()
    cursor.close()
    datatableConnectLocal.close()


def getCarInsurPolicyTotalList():
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("SELECT * FROM car_insur")
    results = cursor.fetchall()
    cursor.close()
    datatableConnectLocal.close()
    return results


def getCarInsurPolicyBySteamid(id):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("SELECT * FROM car_insur WHERE player_steamid = ?", (id,))
    results = cursor.fetchall()
    cursor.close()
    datatableConnectLocal.close()
    return results


def getCarInsurPolicyBuyCarid(id):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("SELECT * FROM car_insur WHERE last_car_id = ?", (id,))
    results = cursor.fetchall()
    cursor.close()
    datatableConnectLocal.close()
    return results


def deleteCarInsurPolicyById(id):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("DELETE FROM car_insur WHERE insur_id = ?", (id,))
    datatableConnectLocal.commit()
    cursor.close()
    datatableConnectLocal.close()


def createCarInsurGetLog(obj):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("INSERT INTO car_insur_get_list (player_name, player_steamid, insur_id, get_time, car_type, get_location, pre_car_id, pre_car_owner, cur_car_id, is_destoryed) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (obj[0], obj[1], obj[2], obj[3], obj[4], obj[5], obj[6], obj[7], obj[8], obj[9]))
    datatableConnectLocal.commit()
    cursor.close()
    datatableConnectLocal.close()


def getCarInsurTotalGetList():
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("SELECT * FROM car_insur_get_list")
    results = cursor.fetchall()
    cursor.close()
    datatableConnectLocal.close()
    return results


def getCarInsurUserGetListByInsurId(id):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("SELECT * FROM car_insur_get_list WHERE insur_id = ?", (id,))
    results = cursor.fetchall()
    cursor.close()
    datatableConnectLocal.close()
    return results


def getCarInsurUserGetListBySteamId(id):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("SELECT * FROM car_insur_get_list WHERE player_steamid = ?", (id,))
    results = cursor.fetchall()
    cursor.close()
    datatableConnectLocal.close()
    return results


def deleteCarInsurGetList(id):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("DELETE FROM car_insur WHERE get_id = ?", (id,))
    datatableConnectLocal.commit()
    cursor.close()
    datatableConnectLocal.close()


def carInsurPlayerWordAct(val, inserStr):
    global robotOptions
    userInfo = getUserInfo(inserStr.split("&&&&&")[3], inserStr.split("&&&&&")[2])
    userKeyword = val.split("LogSCUM: Message: ")[1].split(": ")[1]
    if userInfo == False or len(userInfo) == 0:
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    regUser(inserStr.split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    orderUserName = inserStr.split("&&&&&")[3]
    if len(userDataInfo) == 1:
        if robotOptions["carInsurPlayerKeyword"] in userKeyword:
            userByCarInsur(userKeyword, orderUserName, userSteamId, userInfo, userDataInfo)
        elif robotOptions["carInsurGetPlayerKeyword"] in userKeyword:
            userGetCarInsur(userKeyword, orderUserName, userSteamId)
        elif robotOptions["checkCarInsurPlayerKeyword"] in userKeyword:
            userCheckCarInsur(userSteamId, orderUserName)
        elif robotOptions["carInsurGetHideTimeKeyword"] in userKeyword:
            userHideCarInsur(userKeyword, orderUserName, userSteamId)


def userCheckCarInsur(steamid, playerName):
    insurList = getCarInsurPolicyBySteamid(steamid)
    nowTimeStr = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime("%Y-%m-%d %H:%M:%S")
    dateStr = nowTimeStr.split(" ")[0]
    if insurList and len(insurList) > 0:
        for item in insurList:
            totalConunt = 0
            dayCount = 0
            insurLogsList = getCarInsurUserGetListByInsurId(item[0])
            if insurLogsList:
                if len(insurLogsList) > 0:
                    totalConunt = len(insurLogsList)
                    for ditem in insurLogsList:
                        if dateStr in ditem[4]:
                            dayCount = dayCount + 1

                carName = item[6]
                if item[6] == "BPC_WolfsWagen":
                    carName = "大众"
                elif item[6] == "BPC_WolfsWagen_FULL":
                    carName = "装甲大众"
                elif item[6] == "BPC_Laika":
                    carName = "莱卡"
                elif item[6] == "BPC_Laika_FULL":
                    carName = "装甲莱卡"
                elif item[6] == "BPC_Rager":
                    carName = "拉格"
                elif item[6] == "BPC_Rager_FULL":
                    carName = "装甲拉格"
                elif item[6] == "BPC_Dirtbike":
                    carName = "摩托"
                elif item[6] == "BPC_Kinglet_Duster":
                    carName = "飞机"
                inputSimpleText("玩家：【" + playerName + "】，保单号：【" + str(item[0]) + "】，被保车ID：【" + item[5] + "】，被保车类型：【" + carName + "】，保单开始时间：【" + item[3] + "】，保单结束时间：【" + item[4] + "】，总最大可兑换次数：【" + item[8] + "】，已兑换总次数：【" + str(totalConunt) + "】，每日最大可兑换次数：【" + item[9] + "】，今日已兑换次数：【" + str(dayCount) + "】")

    else:
        inputSimpleText("车险服务提示：未查询到玩家【" + playerName + "】存在正在生效的保单")


def userHideCarInsur(word, orderUserName, userSteamId):
    wordsArr = word.split(" ")
    insurId = wordsArr[1]
    try:
        if len(wordsArr) == 2:
            insurList = getPlayerCarInsurList(userSteamId)
            if len(insurList) == 0:
                inputSimpleText("车险服务提示：未查询到玩家【" + orderUserName + "】存在正在生效的保单")
            else:
                haveId = False
                insurItem = []
                for item in insurList:
                    if str(item[0]) == insurId:
                        haveId = True
                        insurItem = item

                if haveId == False:
                    inputSimpleText("车险服务提示：未查询到玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单，请确认保单号")
                else:
                    endInsurTime = int(datetime.strptime(str(insurItem[4]), "%Y-%m-%d %H:%M:%S").timestamp())
                    nowTime = datetime.timestamp(datetime.now())
                    getedList = getCarInsurUserGetListByInsurId(insurId)
                    getedTimes = 0
                    dayGetedTime = 0
                    lastGetTime = 0
                    nowTimeStr = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime("%Y-%m-%d %H:%M:%S")
                    dateStr = nowTimeStr.split(" ")[0]
                    if getedList:
                        if len(getedList) > 0:
                            getedTimes = len(getedList)
                            for gtdItem in getedList:
                                lastGetTime = int(datetime.strptime(str(gtdItem[4]), "%Y-%m-%d %H:%M:%S").timestamp())
                                if dateStr in gtdItem[4]:
                                    dayGetedTime = dayGetedTime + 1

                    if nowTime > endInsurTime:
                        inputSimpleText("车险服务提示：玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单已过期，无法执行此指令")
                    elif insurItem[8] != "-1" and getedTimes >= int(insurItem[8]):
                        inputSimpleText("车险服务提示：玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单兑换次数已超出最大可兑换次数，无法执行此指令")
                    elif insurItem[9] != "-1" and dayGetedTime >= int(insurItem[9]):
                        inputSimpleText("车险服务提示：玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单今日兑换次数已超出今日最大可兑换次数，今日无法执行此指令")
                    elif insurItem[7] != "-1" and nowTime - lastGetTime < float(insurItem[7]) * 60:
                        inputSimpleText("车险服务提示：玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单距离上次兑换车险时间小于最低兑换时间间隔【" + insurItem[7] + "】分钟，暂时无法执行此指令")
                    else:
                        inputSimpleText("#DestroyVehicle " + insurItem[5])
                        inputSimpleText("车险服务提示：玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单所属载具暂时删除，如果需要领取，请发送保单领取指令~")
        else:
            inputSimpleText("车险服务提示：您的指令格式有误")
    except Exception as e:
        try:
            inputSimpleText("车险查询错误，请联系管理员")
        finally:
            e = None
            del e


def userGetCarInsur(word, orderUserName, userSteamId):
    wordsArr = word.split(" ")
    insurId = wordsArr[1]
    try:
        if len(wordsArr) == 2:
            insurList = getPlayerCarInsurList(userSteamId)
            if len(insurList) == 0:
                inputSimpleText("车险服务提示：未查询到玩家【" + orderUserName + "】存在正在生效的保单")
            else:
                haveId = False
                insurItem = []
                for item in insurList:
                    if str(item[0]) == insurId:
                        haveId = True
                        insurItem = item

                if haveId == False:
                    inputSimpleText("车险服务提示：未查询到玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单，请确认保单号")
                else:
                    endInsurTime = int(datetime.strptime(str(insurItem[4]), "%Y-%m-%d %H:%M:%S").timestamp())
                    nowTime = datetime.timestamp(datetime.now())
                    getedList = getCarInsurUserGetListByInsurId(insurId)
                    getedTimes = 0
                    dayGetedTime = 0
                    lastGetTime = 0
                    nowTimeStr = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime("%Y-%m-%d %H:%M:%S")
                    dateStr = nowTimeStr.split(" ")[0]
                    if getedList:
                        if len(getedList) > 0:
                            getedTimes = len(getedList)
                            for gtdItem in getedList:
                                lastGetTime = int(datetime.strptime(str(gtdItem[4]), "%Y-%m-%d %H:%M:%S").timestamp())
                                if dateStr in gtdItem[4]:
                                    dayGetedTime = dayGetedTime + 1

                    if nowTime > endInsurTime:
                        inputSimpleText("车险服务提示：玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单已过期，无法兑换车险")
                    elif insurItem[8] != "-1" and getedTimes >= int(insurItem[8]):
                        inputSimpleText("车险服务提示：玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单兑换次数已超出最大可兑换次数，无法兑换车险")
                    elif insurItem[9] != "-1" and dayGetedTime >= int(insurItem[9]):
                        inputSimpleText("车险服务提示：玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单今日兑换次数已超出今日最大可兑换次数，今日无法兑换车险")
                    elif insurItem[7] != "-1" and nowTime - lastGetTime < float(insurItem[7]) * 60:
                        inputSimpleText("车险服务提示：玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单距离上次兑换车险时间小于最低兑换时间间隔【" + insurItem[7] + "】分钟，暂时无法兑换车险")
                    else:
                        preCarList = getAllCarsList()
                        inputSimpleText("车险服务提示：玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单兑即将发货，请在原地等待~")
                        if insurItem[10] == "1":
                            inputSimpleText("#DestroyVehicle " + insurItem[5])
                        insurCarType = insurItem[6]
                        if "_FULL" in insurCarType:
                            inputSimpleText("#SpawnVehicle " + insurCarType.split("_FULL")[0] + " 1 Modifier full Location " + userSteamId)
                        else:
                            inputSimpleText("#SpawnVehicle " + insurCarType + " 1 Location " + userSteamId)
                        if "goodsWithCarInsur" in robotOptions:
                            if robotOptions["goodsWithCarInsur"] != "":
                                goodsArr = robotOptions["goodsWithCarInsur"].split(",")
                                for gitem in goodsArr:
                                    inputSimpleText(gitem + " Location " + userSteamId)

                            time.sleep(3)
                            curCarList = getAllCarsList()
                            if preCarList[-1] == curCarList[-1]:
                                time.sleep(3)
                                curCarList = getAllCarsList()
                        if preCarList[-1] != curCarList[-1]:
                            curCarItem = curCarList[-1]
                            curCarId = curCarItem.split(":")[0].split("#")[1]
                            insurObj = {'insur_id':insurItem[0], 
                             'last_car_id':curCarId}
                            getLogObj = [
                             orderUserName, userSteamId, insurItem[0], nowTimeStr, insurCarType, "-", insurItem[5], "-", curCarId, insurItem[10]]
                            updateCarInsurPolicy(insurObj)
                            createCarInsurGetLog(getLogObj)
                            inputSimpleText("车险服务提示：玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单兑换成功，请注意查收~")
                        else:
                            inputSimpleText("车险服务提示：玩家【" + orderUserName + "】的保单号为【" + insurId + "】的保单兑换失败，请前往室外开阔平坦的位置重试~")
        else:
            inputSimpleText("车险服务提示：您的指令格式有误")
    except Exception as e:
        try:
            inputSimpleText("车险查询错误，请联系管理员")
        finally:
            e = None
            del e


def getPlayerCarInsurList(steamid):
    insurList = getCarInsurPolicyBySteamid(steamid)
    if insurList:
        if len(insurList) > 0:
            return insurList
        return []


def userByCarInsur(word, orderUserName, userSteamId, userInfo, userDataInfo):
    wordsArr = word.split(" ")
    try:
        if len(wordsArr) == 2:
            carIsInsured = False
            carInsuredList = getCarInsurPolicyBuyCarid(wordsArr[1])
            if carInsuredList:
                if len(carInsuredList) > 0:
                    nowTime = datetime.timestamp(datetime.now())
                    for citem in carInsuredList:
                        endInsurTime = int(datetime.strptime(str(citem[4]), "%Y-%m-%d %H:%M:%S").timestamp())
                        if nowTime < endInsurTime:
                            carIsInsured = True

            if carIsInsured == True:
                inputSimpleText("车险服务提示：车牌号为【" + wordsArr[1] + "】的车辆已有一个生效中的保单")
            else:
                checkCar = getPlayerOwnerCarWithId(wordsArr[1], userSteamId, orderUserName)
                if checkCar != False:
                    if robotOptions["carInsurMoneyType"] == "0":
                        userBalance = userInfo[3].split("Account balance: ")[1]
                        if int(userBalance) < int(robotOptions["carInsurPlayerBuyAmount"]):
                            inputSimpleText("车险服务提示：您的余额不足，无法购买车险")
                        elif robotOptions["carInsurAllowMuti"] == "0" and len(getPlayerIsOpeningCarInsurList(userSteamId)) > 0:
                            inputSimpleText("玩家【" + orderUserName + "】已存在一个生效中的保单~")
                        else:
                            inputSimpleText("#ChangeCurrencyBalance Normal -" + str(robotOptions["carInsurPlayerBuyAmount"]) + " " + userSteamId)
                            setCarInsurPolicy(userSteamId, wordsArr[1], checkCar)
                    elif robotOptions["carInsurMoneyType"] == "1":
                        userBalance = userDataInfo[0][3]
                        if int(userBalance) < int(robotOptions["carInsurPlayerBuyAmount"]):
                            inputSimpleText("车险服务提示：您的余额不足，无法购买车险")
                        elif robotOptions["carInsurAllowMuti"] == "0" and len(getPlayerIsOpeningCarInsurList(userSteamId)) > 0:
                            inputSimpleText("玩家【" + orderUserName + "】已存在一个生效中的保单~")
                        else:
                            reduceUserAmount(str(robotOptions["carInsurPlayerBuyAmount"]), userSteamId, 0)
                            setCarInsurPolicy(userSteamId, wordsArr[1], checkCar)
        else:
            inputSimpleText("车险服务提示：您的指令格式有误")
    except Exception as e:
        try:
            printToLog(e)
            logging.error(str(datetime.now()))
            logging.error(traceback.format_exc())
            inputSimpleText("车险查询错误，请联系管理员")
        finally:
            e = None
            del e


def getPlayerOwnerCarWithId(userCarId, userUserId, orderUserName):
    carList = getAllCarsList()
    hasCar = False
    carIsUser = False
    carItem = ""
    for item in carList:
        carId = item.split("   ")[0].split(":")[0].split("#")[1]
        userId = item.split("   ")[-1]
        if carId == userCarId:
            hasCar = True
            if userId == userUserId:
                carIsUser = True
                carItem = item

    if hasCar == False:
        inputSimpleText("车险服务提示：未找到指定车牌的车辆")
        return False
    if carIsUser == False:
        inputSimpleText("车险服务提示：玩家【" + orderUserName + "】不是指定车牌的车辆的车主，无法为此车辆购买车险~")
        return False
    if carIsUser == True:
        return carItem


def getAllCarsList():
    totalUserList = []
    inputSimpleText("#ListSpawnedVehicles true")
    if "slowGetCarsWaitTime" in robotOptions:
        if robotOptions["slowGetCarsWaitTime"] != "0":
            time.sleep(float(robotOptions["slowGetCarsWaitTime"]))
    try:
        havData = False
        userListSp = []
        havNum = 0
        while havData == False:
            userData = pyperclip.paste()
            userListSp = userData.split("\n")
            if len(userListSp) > 0:
                havData = True
            havNum = havNum + 1
            if havNum > 30:
                havData = True
                printToLog("未获取到载具列表，请调整获取载具列表延时")
            if "slowGetCarsWaitTime" in robotOptions:
                if robotOptions["slowGetCarsWaitTime"] != "0":
                    time.sleep(float(robotOptions["slowGetCarsWaitTime"]))

        return userListSp
    except Exception as e:
        try:
            printToLog(e)
            logging.error(str(datetime.now()))
            logging.error(traceback.format_exc())
            inputSimpleText("南极熊机器人提示：未正常获取到载具列表，请管理员适当调整【基本设置】中【获取载具列表延时】，原因：【电脑卡了】")
            return False
        finally:
            e = None
            del e


def adminGiveCarInsurToPlayer(cmdArr):
    checkResult = False
    if not len(cmdArr) == 4 or cmdArr[3] == "0" or cmdArr[3] == "1":
        checkResult = True
    elif len(cmdArr) == 3:
        checkResult = True
    if checkResult == False:
        inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
    else:
        userUserId = cmdArr[1]
        userCarId = cmdArr[2]
        fullType = "0"
        if len(cmdArr) == 4:
            fullType = cmdArr[3]
        carList = getAllCarsList()
        hasCar = False
        carIsUser = False
        insurCarItem = ""
        for item in carList:
            carId = item.split("   ")[0].split(":")[0].split("#")[1]
            userId = item.split("   ")[-1]
            if carId == userCarId:
                hasCar = True
                if userId == userUserId:
                    carIsUser = True
                    insurCarItem = item

        carIsInsured = False
        carInsuredList = getCarInsurPolicyBuyCarid(userCarId)
        if carInsuredList:
            if len(carInsuredList) > 0:
                nowTime = datetime.timestamp(datetime.now())
                for citem in carInsuredList:
                    endInsurTime = int(datetime.strptime(str(citem[4]), "%Y-%m-%d %H:%M:%S").timestamp())
                    if nowTime < endInsurTime:
                        carIsInsured = True

            haveOpenListLen = 0
            haveOpenList = getPlayerIsOpeningCarInsurList(userUserId)
            if haveOpenList:
                for item in haveOpenList:
                    haveOpenListLen = haveOpenListLen + 1

        if carIsInsured == True:
            inputSimpleText("车险服务提示：车牌号为【" + userCarId + "】的车辆已有一个生效中的保单")
        elif hasCar == False:
            inputSimpleText("未找到车牌号为：【" + userCarId + "】的车辆")
        elif carIsUser == False:
            inputSimpleText("车险服务提示：玩家【" + userUserId + "】不是车牌为【" + userCarId + "】的车辆的车主，无法为此车辆购买车险~")
        elif len(getCarInsurPolicyBuyCarid(userCarId)) > 0:
            inputSimpleText("车牌号为【" + userCarId + "】的车辆已存在车险保单")
        elif robotOptions["carInsurAllowMuti"] == "0" and haveOpenListLen > 0:
            inputSimpleText("玩家【" + userUserId + "】已存在一个生效中的保单~")
        else:
            setCarInsurPolicy(userUserId, userCarId, insurCarItem, fullType)


def getPlayerIsOpeningCarInsurList(steamid):
    insurList = getCarInsurPolicyBySteamid(steamid)
    openArr = []
    if insurList:
        if len(insurList) > 0:
            nowTime = datetime.timestamp(datetime.now())
            for item in insurList:
                endInsurTime = int(datetime.strptime(str(item[4]), "%Y-%m-%d %H:%M:%S").timestamp())
                if nowTime < endInsurTime:
                    openArr.append(item)

        return openArr


def setCarInsurPolicy(steamid, carid, insurIdCar, fullType='0'):
    uperInfo = getUserInfoBySteamidFromTotal(steamid)
    uperName = ""
    if uperInfo and len(uperInfo) > 0:
        uperNameArr = uperInfo[0].split(". ")
        uperNameArr.pop(0)
        uperName = ". ".join(uperNameArr)
        insurdTime = str(datetime.now()).split(".")[0]
        initDays = 30
        getTimeSpace = "30"
        totalMax = "-1"
        dayMax = "1"
        isDestory = "1"
        if "carInsurInitTime" in robotOptions:
            try:
                initDays = int(robotOptions["carInsurInitTime"])
            except Exception:
                initDays = 30

            if "carInsurGetTimeSpace" in robotOptions:
                try:
                    getTimeSpace = str(int(robotOptions["carInsurGetTimeSpace"]))
                except Exception:
                    getTimeSpace = 30

    if "carInsurGetMaxTimes" in robotOptions:
        try:
            totalMax = str(int(robotOptions["carInsurGetMaxTimes"]))
        except Exception:
            totalMax = "-1"

        if "carInsurGetDayMaxTimes" in robotOptions:
            try:
                dayMax = str(int(robotOptions["carInsurGetDayMaxTimes"]))
            except Exception:
                dayMax = "1"

            if "carInsurIsDestoryPreCar" in robotOptions:
                try:
                    isDestory = str(int(robotOptions["carInsurIsDestoryPreCar"]))
                except Exception:
                    isDestory = "1"

                endInsuredTime = datetime.fromtimestamp(datetime.timestamp(datetime.now()) + 86400 * initDays).strftime("%Y-%m-%d %H:%M:%S")
                carType = insurIdCar.split(": ")[1].split(" ")[0]
                if "carInsurAllowAirplan" in robotOptions and robotOptions["carInsurAllowAirplan"] == "0" and carType == "BPC_Kinglet_Duster":
                    inputSimpleText("车险服务提示：不允许为类型为【飞机】的载具投保车险")
                elif "carInsurAllowAirplan" not in robotOptions and carType == "BPC_Kinglet_Duster":
                    inputSimpleText("车险服务提示：不允许为类型为【飞机】的载具投保车险")
                else:
                    if fullType == "1":
                        carType = carType + "_FULL"
                    insurData = [
                     uperName,steamid,insurdTime,endInsuredTime,carid,carType,getTimeSpace,totalMax,dayMax,isDestory]
                    createCarInsurPolicy(insurData)
                    inputSimpleText("创建车险保单成功，投保玩家：【" + uperName + "】，投保车ID：【" + carid + "】，投保截止日期：【" + endInsuredTime + "】，投保时长：【" + str(initDays) + "天】")
        inputSimpleText("未找到玩家【" + steamid + "】的信息，玩家可能不在线，跳过本次任务")


def insertDataIntoLHDLog(strval):
    strarr = strval.split("&&&&&")
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("INSERT INTO lhd_log (player_name, player_steamid, play_amount, win_amount, result, uper_name, uper_steamid, date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (strarr[0], strarr[1], strarr[2], strarr[3], strarr[4], strarr[5], strarr[6], strarr[7], strarr[8]))
    datatableConnectLocal.commit()
    cursor.close()
    datatableConnectLocal.close()


def insertDataIntoSendedGiftByOldData(strval):
    strarr = strval.split("&&&&&")
    cursor = datatableConnect.cursor()
    cursor.execute("INSERT INTO sended_gift (server_time, local_time, keyword, username, usercode, steamid) VALUES (?, ?, ?, ?, ?, ?)", (strarr[0], strarr[1], strarr[2], strarr[3], strarr[4], strarr[5]))


def insertDataIntoSendedGift(strval):
    strarr = strval.split("&&&&&")
    steamid = strarr[5]
    if len(strarr) == 7:
        steamid = strarr[6]
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("INSERT INTO sended_gift (server_time, local_time, keyword, username, usercode, steamid) VALUES (?, ?, ?, ?, ?, ?)", (strarr[0], strarr[1], strarr[2], strarr[3], strarr[4], steamid))
    datatableConnectLocal.commit()
    cursor.close()
    datatableConnectLocal.close()
    time.sleep(1)


def getUserGiftLogsByKey(keyword, steamid, date):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("SELECT * FROM sended_gift WHERE keyword = ? AND steamid = ? AND local_time = ?", (keyword, steamid, date))
    results = cursor.fetchall()
    cursor.close()
    datatableConnectLocal.close()
    return results


def deleteAllGiftLogByName(name):
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("SELECT * FROM sended_gift")
    rows = cursor.fetchall()
    print(len(rows))
    datatableConnectLocal.commit()
    cursor.close()
    datatableConnectLocal.close()
    time.sleep(1)


def insertDataIntoUser(data):
    fatchObj = fatchUser(data["steam_id"])
    if len(fatchObj) == 0:
        cursor = datatableConnect.cursor()
        cursor.execute("INSERT INTO user_list (user_name, nick_name, amount, reg_time, total_time, last_log_time, vip_level, vip_end_time, integral, steam_id, normal_integral, normal_vip_level) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data["user_name"], data["nick_name"], data["amount"], data["reg_time"], data["total_time"], data["last_log_time"], data["vip_level"], data["vip_end_time"], data["integral"], data["steam_id"], data["normal_integral"], data["normal_vip_level"]))
        datatableConnect.commit()
        printToLog("插入玩家数据成功")
    elif len(fatchObj) == 1:
        printToLog("玩家已存在")
    elif len(fatchObj) > 1:
        printToLog("有多个重复玩家")


initUserData = {
  'user_name': "",
  'nick_name': "",
  'amount': "0",
  'reg_time': "",
  'total_time': "0",
  'last_log_time': "",
  'vip_level': "0",
  'vip_end_time': "0",
  'integral': "0",
  'steam_id': ""}

def updateDataToUser(data):
    userInfoList = fatchUser(data["steam_id"])
    if len(userInfoList) == 0:
        printToLog("未找到玩家")
    elif len(userInfoList) == 1:
        cursor = datatableConnect.cursor()
        for i in data:
            cursor.execute("UPDATE user_list SET " + i + " = ? WHERE steam_id = ?", (data[i], data["steam_id"]))

        datatableConnect.commit()
        printToLog("更新成功")
    else:
        printToLog("发现重复数据")


def fatchSendedDataByUserByDay(localtime, keyword, usercode):
    localtime = localtime
    keyword = keyword
    usercode = usercode
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    cursor.execute("SELECT * FROM sended_gift WHERE local_time = ? AND keyword = ? AND usercode = ?", (localtime, keyword, usercode))
    results = cursor.fetchall()
    cursor.close()
    datatableConnectLocal.close()
    return results


def fatchSendedDataByUserByTotal(keyword, usercode):
    keyword = keyword
    usercode = usercode
    cursor = datatableConnect.cursor()
    cursor.execute("SELECT * FROM sended_gift WHERE keyword = ? AND usercode = ?", (keyword, usercode))
    results = cursor.fetchall()
    return results


def fatchUser(steamid):
    cursor = datatableConnect.cursor()
    cursor.execute("SELECT * FROM user_list WHERE steam_id = ?", (steamid,))
    results = cursor.fetchall()
    if len(results) == 0:
        printToLog("未查询到玩家数据")
    elif len(results) == 1:
        pass
    else:
        printToLog("查询到多条同steamid玩家数据，请处理")
    return results


def addUser():
    userData = {
      'user_name': "老狼2",
      'nick_name': "【老板】",
      'amount': "0",
      'reg_time': "2023-12-20 21:19:05",
      'total_time': "0",
      'last_log_time': "2023-12-20 21:19:05",
      'vip_level': "0",
      'vip_end_time': "2023-12-22",
      'integral': "0",
      'steam_id': "9877565656561"}
    insertDataIntoUser(userData)


def getUserAmount(steamid):
    results = fatchUser(steamid)
    amount = 0
    if len(results) == 1:
        amount = results[0][3]
    return amount


def getUserJifen(steamid):
    results = fatchUser(steamid)
    amount = 0
    if len(results) == 1:
        amount = results[0][9]
    return str(int(float(amount)))


def getUserNormalJifen(steamid):
    results = fatchUser(steamid)
    amount = 0
    if len(results) == 1:
        amount = results[0][11] or "0"
    return str(int(float(amount)))


def getUserCustomTitle(steamid):
    results = fatchUser(steamid)
    amount = 0
    if len(results) == 1:
        amount = results[0][13]
    return amount


def getUserVipLevel(steamid):
    results = fatchUser(steamid)
    amount = 0
    if len(results) == 1:
        amount = results[0][7]
    return amount


def getUserNormalVipLevel(steamid):
    results = fatchUser(steamid)
    amount = 0
    if len(results) == 1:
        amount = results[0][12] or "0"
    return amount


def getUserPersonGiftCard(steamid):
    results = fatchUser(steamid)
    amount = {}
    if len(results) == 1:
        cardInfoStr = results[0][14]
        if cardInfoStr == "":
            cardInfoStr = "{}"
        cardInfoObj = json.loads(cardInfoStr)
        amount = cardInfoObj
    return amount


def getUserPersonSkillData(steamid):
    results = fatchUser(steamid)
    amount = {}
    if len(results) == 1:
        cardInfoStr = results[0][15]
        if cardInfoStr == "":
            cardInfoStr = "{}"
        cardInfoObj = json.loads(cardInfoStr)
        amount = cardInfoObj
    return amount


def updateUserPersonGiftCard(steamid, cardinfo):
    info = {'steam_id':steamid, 
     'gift_cards':(json.dumps)(cardinfo)}
    updateDataToUser(info)


def updateUserPersonSkillData(steamid, cardinfo):
    info = {'steam_id':steamid, 
     'skill_data':(json.dumps)(cardinfo)}
    updateDataToUser(info)
    updateUserSkillName(steamid)


def addUserAmount(steamid, amount):
    currentAmount = int(getUserAmount(steamid))
    currentAmount = currentAmount + int(amount)
    updateUserData = {'steam_id':steamid, 
     'amount':currentAmount}
    updateDataToUser(updateUserData)


def justUpNormalLevelFun(val):
    global totalRobotOptions
    userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
    userOutName = val["inserStr"].split("&&&&&")[3]
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    userBalance = userInfo[3].split("Account balance: ")[1]
    currentInt = int(getUserNormalJifen(userSteamId) or 0)
    currentLevel = int(getUserNormalVipLevel(userSteamId) or 0)
    vipLevelDicts = totalRobotOptions["normalVipLevel"].keys()
    vipLevelKeys = []
    nextLevel = "0"
    nextInt = "0"
    for i in vipLevelDicts:
        vipLevelKeys.append(i)

    forIndex = 0
    for i in vipLevelKeys:
        if currentLevel == 0:
            nextLevel = totalRobotOptions["normalVipLevel"][vipLevelKeys[0]]["keyword"]
            nextInt = totalRobotOptions["normalVipLevel"][vipLevelKeys[0]]["upAmount"]
        if int(totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex]]["keyword"]) == currentLevel:
            if forIndex < len(vipLevelKeys) - 1:
                nextLevel = totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex + 1]]["keyword"]
                nextInt = totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex + 1]]["upAmount"]
            else:
                nextLevel = "-1"
                nextInt = "-1"
        forIndex = forIndex + 1

    if nextLevel == "-1" and nextInt == "-1":
        if "language" in robotOptions and robotOptions["language"] == 1:
            inputSimpleText("player【" + userOutName + "】Currently at the highest level, unable to continue upgrading~")
        else:
            inputSimpleText("玩家【" + userOutName + "】当前是最高等级，无法继续升级~")
    else:
        intRadio = 1
        try:
            if "inteJustUpNormalLevel" in totalRobotOptions["options"]:
                intRadio = float(totalRobotOptions["options"]["inteJustUpNormalLevel"])
        except Exception:
            intRadio = 1

        diffInt = int((int(nextInt) - int(currentInt) + 1) / intRadio)
        if int(userBalance) < diffInt:
            if "language" in robotOptions and robotOptions["language"] == 1:
                inputSimpleText("player【" + userOutName + "】Insufficient balance required for upgrade~")
            else:
                inputSimpleText("玩家【" + userOutName + "】升级所需余额不足")
        else:
            try:
                inputSimpleText("#ChangeCurrencyBalance Normal -" + str(diffInt) + " " + userSteamId)
                updata = {'steam_id':userSteamId, 
                 'normal_vip_level':nextLevel, 
                 'normal_integral':str(int(nextInt) + 1), 
                 'vip_level':getUserVipLevel(userSteamId), 
                 'custom_title':getUserCustomTitle(userSteamId)}
                updatePlayerName(updata, "normal")
                updateDataToUser(updata)
            except Exception as e:
                try:
                    printToLog("错误发生行号：" + traceback.format_exc())
                    printToLog("获取数据出错，机器人重启中，如长时间未能恢复，请联系管理员协助解决")
                    logging.error(str(datetime.now()))
                    logging.error(traceback.format_exc())
                finally:
                    e = None
                    del e


def updateUserNormalInt(amount, steamid, integ):
    currentInt = int(getUserNormalJifen(steamid) or 0)
    currentLevel = int(getUserNormalVipLevel(steamid) or 0)
    updateUserData = {'steam_id':steamid, 
     'normal_integral':currentInt, 
     'normal_vip_level':currentLevel}
    if "isAllowNormalVipAutoUp" in totalRobotOptions["options"] and totalRobotOptions["options"]["isAllowNormalVipAutoUp"] == 1:
        vipMaxLevel = "0"
        nextInt = currentInt + int(integ)
        updateUserData["normal_integral"] = str(nextInt)
        preListInt = ""
        currentListInt = ""
        if "normalVipLevel" in totalRobotOptions:
            vipLevelDicts = totalRobotOptions["normalVipLevel"].keys()
            vipLevelKeys = []
            for i in vipLevelDicts:
                vipLevelKeys.append(i)

            forIndex = 0
            for i in vipLevelKeys:
                vipMaxLevel = totalRobotOptions["normalVipLevel"][i]["keyword"]
                if forIndex == 0:
                    preListInt = int(totalRobotOptions["normalVipLevel"][i]["upAmount"])
                    nextListInt = int(totalRobotOptions["normalVipLevel"][i]["upAmount"])
                else:
                    preListInt = int(totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex - 1]]["upAmount"])
                    if forIndex == len(vipLevelKeys) - 1:
                        nextListInt = int(totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex]]["upAmount"])
                    else:
                        nextListInt = int(totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex + 1]]["upAmount"])
                currentListInt = int(totalRobotOptions["normalVipLevel"][i]["upAmount"])
                if forIndex == 0:
                    if nextInt >= preListInt:
                        updateUserData["normal_vip_level"] = totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex]]["keyword"]
                    if nextInt >= currentListInt:
                        if nextInt < nextListInt:
                            updateUserData["normal_vip_level"] = totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex]]["keyword"]
                        if forIndex == len(vipLevelKeys) - 1:
                            if nextInt >= currentListInt:
                                updateUserData["normal_vip_level"] = totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex]]["keyword"]
                            forIndex = forIndex + 1

            if "isAllowNormalVipAutoUp" in totalRobotOptions["options"]:
                if totalRobotOptions["options"]["isAllowNormalVipAutoUp"] == 1:
                    if str(currentLevel) != str(updateUserData["normal_vip_level"]):
                        updata = {'steam_id':steamid, 
                         'normal_vip_level':updateUserData["normal_vip_level"] or "0", 
                         'vip_level':getUserVipLevel(steamid), 
                         'custom_title':getUserCustomTitle(steamid)}
                        updatePlayerName(updata, "normal")
        updateDataToUser(updateUserData)


def updatePlayerName(data, type):
    allPlayer = getAllPlayerList()
    playerName = ""
    for item in allPlayer:
        if item["steamid"] == data["steam_id"]:
            playerName = item["userName"]

    if playerName:
        resetPlayerName(playerName, data, type)
        updateUserData = {'steam_id':data["steam_id"], 
         'user_name':playerName}
        updateDataToUser(updateUserData)


def updateAllPlayerName():
    allPlayer = getAllPlayerList()
    playerName = ""
    for item in allPlayer:
        playerName = item["userName"]
        normalVipLevel = getUserNormalVipLevel(item["steamid"]) or "0"
        vipLevel = getUserVipLevel(item["steamid"]) or "0"
        customTitle = getUserCustomTitle(item["steamid"]) or ""
        normalJifen = getUserNormalJifen(item["steamid"]) or "0"
        vipJifen = getUserJifen(item["steamid"]) or "0"
        if "normalVipLevel" in totalRobotOptions:
            normalList = []
            for i in totalRobotOptions["normalVipLevel"]:
                normalList.append(totalRobotOptions["normalVipLevel"][i])

            forIndex = 0
            for i in normalList:
                if forIndex == len(normalList) - 1:
                    if int(normalJifen) >= int(normalList[forIndex]["upAmount"]):
                        normalVipLevel = normalList[forIndex]["keyword"]
                elif int(normalJifen) >= int(normalList[forIndex]["upAmount"]):
                    if int(normalJifen) < int(normalList[forIndex + 1]["upAmount"]):
                        normalVipLevel = normalList[forIndex]["keyword"]
                forIndex = forIndex + 1

        updata = {'steam_id':item["steamid"], 
         'normal_vip_level':normalVipLevel, 
         'vip_level':vipLevel, 
         'custom_title':customTitle}
        if playerName:
            updateDataToUser(updata)
            resetPlayerName(playerName, updata, "init")


def updateUserSkillName(steamid):
    if "skillOptions" in robotOptions:
        if "showSKillName" in robotOptions["skillOptions"]:
            if robotOptions["skillOptions"]["showSKillName"] == "1":
                normalVipLevel = getUserNormalVipLevel(steamid) or "0"
                vipLevel = getUserVipLevel(steamid) or "0"
                customTitle = getUserCustomTitle(steamid) or ""
                updata = {
                  'steam_id': steamid,
                  'normal_vip_level': normalVipLevel,
                  'vip_level': vipLevel,
                  'custom_title': customTitle}
                allPlayer = getAllPlayerList()
                playerName = ""
                for item in allPlayer:
                    if item["steamid"] == steamid:
                        playerName = item["userName"]
                        resetPlayerName(playerName, updata, "init")


def resetPlayerName(name, data, type):
    normalTitle = ""
    vipTitle = ""
    fakename = ""
    nameIndexArr = [
     "1","2","3","4","5"]
    if "nameTitleIndex" in robotOptions and robotOptions["nameTitleIndex"] != "":
        if "" not in robotOptions["nameTitleIndex"]:
            nameIndexArr = robotOptions["nameTitleIndex"]
        for item in nameIndexArr:
            if item == "1":
                if "custom_title" in data:
                    if data["custom_title"] != "":
                        if data["custom_title"] != None:
                            fakename = fakename + "" + data["custom_title"] + ""
                        if item == "2":
                            if "skillOptions" in robotOptions:
                                if "showSKillName" in robotOptions["skillOptions"]:
                                    if robotOptions["skillOptions"]["showSKillName"] == "1":
                                        skillData = getUserPersonSkillData(data["steam_id"])
                                        preTag = "【"
                                        nextTag = "】"
                                        if "namePreTag" in robotOptions["skillOptions"]:
                                            if robotOptions["skillOptions"]["namePreTag"] != "":
                                                preTag = robotOptions["skillOptions"]["namePreTag"]
                                            if "nameNextTag" in robotOptions["skillOptions"]:
                                                if robotOptions["skillOptions"]["nameNextTag"] != "":
                                                    nextTag = robotOptions["skillOptions"]["nameNextTag"]
                                                for item in skillData:
                                                    fakename = fakename + preTag + item + nextTag

                                            if item == "3":
                                                if "isShowNormalVipName" in totalRobotOptions["options"]:
                                                    if totalRobotOptions["options"]["isShowNormalVipName"] == 1:
                                                        if "normalVipLevel" in totalRobotOptions:
                                                            for i in totalRobotOptions["normalVipLevel"]:
                                                                item = totalRobotOptions["normalVipLevel"][i]
                                                                if str(item["keyword"]) == str(data["normal_vip_level"]):
                                                                    normalTitle = item["name"]
                                                                    fakename = fakename + "" + normalTitle + ""

                                                        if item == "4":
                                                            if "isShowVipName" in totalRobotOptions["options"]:
                                                                if totalRobotOptions["options"]["isShowVipName"] == 1:
                                                                    if "vipLevel" in totalRobotOptions:
                                                                        for i in totalRobotOptions["vipLevel"]:
                                                                            item = totalRobotOptions["vipLevel"][i]
                                                                            if str(item["keyword"]) == str(data["vip_level"]):
                                                                                vipTitle = item["name"]
                                                                                fakename = fakename + "" + vipTitle + ""

                                                                    if item == "5":
                                                                        fakename = fakename + name

    if fakename != "" and fakename != name:
        inputSimpleText("#setfakename " + data["steam_id"] + ' "' + fakename + '"')
        if type == "normal":
            if "language" in robotOptions and robotOptions["language"] == 1:
                inputSimpleText("#Announce congratulations player【" + name + "】Upgrade to" + normalTitle + "!!!!!")
            else:
                inputSimpleText("#Announce 恭喜玩家【" + name + "】 荣升 " + normalTitle + "!!!!!")
        if type == "vip":
            if "language" in robotOptions and robotOptions["language"] == 1:
                inputSimpleText("#Announce congratulations player【" + name + "】Upgrade to" + vipTitle + "!!!!!")
            else:
                inputSimpleText("#Announce 恭喜玩家【" + name + "】 荣升 " + vipTitle + "!!!!!")
        if type == "custom" and data["custom_title"] != "":
            inputSimpleText("#Announce 恭喜玩家【" + name + "】 荣获 " + data["custom_title"] + "称号!!!!!")
    else:
        inputSimpleText("#ClearFakeName " + data["steam_id"])


def getAllPlayerList():
    totalUserList = []
    inputSimpleText("#ListPlayers true")
    time.sleep(0.1)
    try:
        havData = False
        havNum = 0
        userListSp = []
        while havData == False:
            userData = pyperclip.paste()
            userListSp = userData.split("\n")
            if len(userListSp) > 0:
                havData = True
            havNum = havNum + 1
            if havNum > 30:
                havData = True
                printToLog("未找到发言玩家，跳过本轮")
            if "slowGetPlayerWaitTime" in robotOptions:
                if robotOptions["slowGetPlayerWaitTime"] != "0":
                    time.sleep(float(robotOptions["slowGetPlayerWaitTime"]))

        userListSp.pop(0)
        userList = []
        chUs = []
        index = 0
        for item in userListSp:
            if index % 6 == 0:
                if index == 0:
                    chUs.append(item)
                else:
                    chUs.append(item)
                    userList.append(chUs)
                    chUs = []
                    index = -1
            else:
                chUs.append(item)
            index = index + 1

        for u in userList:
            name1 = u[0].split(". ")[1]
            userSteamId = u[1].split("(")[-1].split(")")[0]
            obj = {'steamid':userSteamId, 
             'userName':name1, 
             'location':u[5].split("Location: ")[1], 
             'fakename':""}
            if "/" in u[6]:
                obj["fakename"] = u[6].split("/")[1]
            totalUserList.append(obj)

        return totalUserList
    except Exception as e:
        try:
            inputSimpleText("南极熊机器人提示：未正常获取到在线列表，请管理员适当调整【基本设置】中【获取在线列表延时】，原因：【电脑卡了】")
            return False
        finally:
            e = None
            del e


def reduceUserAmount(amount, steamid, integ):
    currentAmount = int(getUserAmount(steamid))
    currentInt = int(getUserJifen(steamid))
    currentLevel = int(getUserVipLevel(steamid))
    currentAmount = currentAmount - int(amount)
    updateUserData = {
      'steam_id': steamid,
      'amount': currentAmount,
      'integral': currentInt,
      'vip_level': currentLevel}
    if "isAllowVipAutoUp" in robotOptions and robotOptions["isAllowVipAutoUp"] == 1:
        vipMaxLevel = "0"
        nextInt = currentInt + int(integ)
        updateUserData["integral"] = str(nextInt)
        preListInt = ""
        currentListInt = ""
        if "vipLevel" in totalRobotOptions:
            vipLevelDicts = totalRobotOptions["vipLevel"].keys()
            vipLevelKeys = []
            for i in vipLevelDicts:
                vipLevelKeys.append(i)

            forIndex = 0
            for i in vipLevelKeys:
                vipMaxLevel = totalRobotOptions["vipLevel"][i]["keyword"]
                if forIndex == 0:
                    preListInt = int(totalRobotOptions["vipLevel"][i]["upAmount"])
                else:
                    preListInt = int(totalRobotOptions["vipLevel"][vipLevelKeys[forIndex - 1]]["upAmount"])
                currentListInt = int(totalRobotOptions["vipLevel"][i]["upAmount"])
                if forIndex == 0:
                    if nextInt >= preListInt:
                        updateUserData["vip_level"] = totalRobotOptions["vipLevel"][vipLevelKeys[forIndex]]["keyword"]
                    if nextInt <= currentListInt:
                        if nextInt > preListInt:
                            updateUserData["vip_level"] = totalRobotOptions["vipLevel"][vipLevelKeys[forIndex - 1]]["keyword"]
                        if forIndex == len(vipLevelKeys) - 1:
                            if nextInt >= currentListInt:
                                updateUserData["vip_level"] = totalRobotOptions["vipLevel"][vipLevelKeys[-1]]["keyword"]
                            forIndex = forIndex + 1

            if "isAllowVipAutoUp" in totalRobotOptions["options"]:
                if totalRobotOptions["options"]["isAllowVipAutoUp"] == 1:
                    if str(currentLevel) != str(updateUserData["vip_level"]):
                        updata = {'steam_id':steamid, 
                         'normal_vip_level':getUserNormalVipLevel(steamid) or "0", 
                         'vip_level':updateUserData["vip_level"], 
                         'custom_title':getUserCustomTitle(steamid)}
                        updatePlayerName(updata, "vip")
        updateDataToUser(updateUserData)


def checkDayReduceInt():
    printToLog("开始检查每日扣减积分")
    directory = os.getcwd()
    curDayStr = str(datetime.now()).split(" ")[0]
    preDayReDay = ""
    with open((directory + "/DayReduceInt.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/DayReduceInt.txt"), "r", encoding="UTF-8") as file:
        preDayReDay = file.read()
    if preDayReDay == "":
        dayReduceAllInt()
        with open((directory + "/DayReduceInt.txt"), "w", encoding="UTF-8") as f:
            f.write(curDayStr)
    elif preDayReDay != curDayStr:
        dayReduceAllInt()
        with open((directory + "/DayReduceInt.txt"), "w", encoding="UTF-8") as f:
            f.write(curDayStr)


def dayReduceAllInt():
    printToLog("每日扣减所有玩家积分中...")
    dayRedVipInt = 0
    dayRedNormalVipInt = 0
    try:
        if "dayReduceVipInt" in robotOptions:
            if robotOptions["dayReduceVipInt"] != "":
                dayRedVipInt = float(robotOptions["dayReduceVipInt"])
            if "dayReduceNormalInt" in robotOptions:
                if robotOptions["dayReduceNormalInt"] != "":
                    dayRedNormalVipInt = float(robotOptions["dayReduceNormalInt"])
    except Exception as e:
        try:
            inputSimpleText("每日扣减积分数值错误，请检查")
        finally:
            e = None
            del e

    if dayRedVipInt > 0 or dayRedNormalVipInt > 0:
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        cursor.execute("SELECT * FROM user_list")
        results = cursor.fetchall()
        cursor.close()
        datatableConnectLocal.close()
        for item in results:
            if len(item) > 10:
                obj = {"steam_id": (item[10])}
                vipInt = int(float(item[9]))
                vipLevel = item[7]
                normalInt = int(float(item[11]))
                normalVipLevel = item[12]
            if dayRedVipInt > 0:
                if dayRedVipInt < 1:
                    vipInt = vipInt - vipInt * dayRedVipInt
                    if vipInt < 0:
                        vipInt = 0
                    if vipInt > dayRedVipInt:
                        vipInt = vipInt - dayRedVipInt
                    else:
                        vipInt = 0
                    obj["integral"] = int(vipInt)
                    obj["vip_level"] = int(vipLevel)
                if dayRedNormalVipInt > 0:
                    if dayRedNormalVipInt < 1:
                        normalInt = normalInt - normalInt * dayRedNormalVipInt
                        if normalInt < 0:
                            normalInt = 0
                    elif normalInt > dayRedNormalVipInt:
                        normalInt = normalInt - dayRedNormalVipInt
                    else:
                        normalInt = 0
                    obj["normal_integral"] = int(normalInt)
                    obj["normal_vip_level"] = int(normalVipLevel)
                dayRedDoVipLevel(obj)

        updateAllPlayerName()
    printToLog("每日扣减所有玩家积分完成！！")


def dayRedDoVipLevel(updateUserData):
    if "vipLevel" in totalRobotOptions:
        if "integral" in updateUserData:
            nextInt = updateUserData["integral"]
            vipLevelDicts = totalRobotOptions["vipLevel"].keys()
            vipLevelKeys = []
            for i in vipLevelDicts:
                vipLevelKeys.append(i)

            forIndex = 0
            for i in vipLevelKeys:
                vipMaxLevel = totalRobotOptions["vipLevel"][i]["keyword"]
                if forIndex == 0:
                    preListInt = int(totalRobotOptions["vipLevel"][i]["upAmount"])
                else:
                    preListInt = int(totalRobotOptions["vipLevel"][vipLevelKeys[forIndex - 1]]["upAmount"])
                currentListInt = int(totalRobotOptions["vipLevel"][i]["upAmount"])
                if forIndex == 0:
                    if nextInt >= preListInt:
                        updateUserData["vip_level"] = totalRobotOptions["vipLevel"][vipLevelKeys[forIndex]]["keyword"]
                    if nextInt <= currentListInt:
                        if nextInt > preListInt:
                            updateUserData["vip_level"] = totalRobotOptions["vipLevel"][vipLevelKeys[forIndex - 1]]["keyword"]
                        if forIndex == len(vipLevelKeys) - 1:
                            if nextInt >= currentListInt:
                                updateUserData["vip_level"] = totalRobotOptions["vipLevel"][vipLevelKeys[-1]]["keyword"]
                            forIndex = forIndex + 1

        if "normalVipLevel" in totalRobotOptions:
            if "normal_integral" in updateUserData:
                nextNormalInt = updateUserData["normal_integral"]
                vipLevelDicts = totalRobotOptions["normalVipLevel"].keys()
                vipLevelKeys = []
                for i in vipLevelDicts:
                    vipLevelKeys.append(i)

                forIndex = 0
                for i in vipLevelKeys:
                    vipMaxLevel = totalRobotOptions["normalVipLevel"][i]["keyword"]
                    if forIndex == 0:
                        preListInt = int(totalRobotOptions["normalVipLevel"][i]["upAmount"])
                        nextListInt = int(totalRobotOptions["normalVipLevel"][i]["upAmount"])
                    else:
                        preListInt = int(totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex - 1]]["upAmount"])
                        if forIndex == len(vipLevelKeys) - 1:
                            nextListInt = int(totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex]]["upAmount"])
                        else:
                            nextListInt = int(totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex + 1]]["upAmount"])
                    currentListInt = int(totalRobotOptions["normalVipLevel"][i]["upAmount"])
                    if forIndex == 0:
                        if nextNormalInt >= preListInt:
                            updateUserData["normal_vip_level"] = totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex]]["keyword"]
                        if nextNormalInt >= currentListInt:
                            if nextNormalInt < nextListInt:
                                updateUserData["normal_vip_level"] = totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex]]["keyword"]
                            if forIndex == len(vipLevelKeys) - 1:
                                if nextNormalInt >= currentListInt:
                                    updateUserData["normal_vip_level"] = totalRobotOptions["normalVipLevel"][vipLevelKeys[forIndex]]["keyword"]
                                forIndex = forIndex + 1

    updateDataToUser(updateUserData)


def get_machine_guid():
    key = "SOFTWARE\\Microsoft\\Cryptography"
    registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key)
    (value, regtype) = winreg.QueryValueEx(registry_key, "MachineGuid")
    winreg.CloseKey(registry_key)
    return value


print(get_machine_guid())

def checkPeroid(str):
    global isOnlyGift
    if "123456" in str:
        endRobotRun()
    printToLog("检查卡密中.....")
    data = {"cardSecret": ""}
    checkUrl = ""
    if isOnlyGift == False:
        checkUrl = "checkPeroid"
    else:
        checkUrl = "checkPeroidGift"
    checkStatus = False
    checkMessage = ""
    interfaces = get_machine_guid()
    response = requests.get(url=(serverRoot + "checkPeroid" + "?cardSecret=" + str + "&meCode=" + interfaces), data=data)
    result = json.loads(response.text)
    response2 = requests.get(url=(serverRoot + "checkPeroidGift" + "?cardSecret=" + str + "&meCode=" + interfaces), data=data)
    result2 = json.loads(response2.text)
    if result["code"] == 0:
        checkStatus = True
        isOnlyGift = False
        checkMessage = result["message"] + "，机器人版本为：商城版"
    elif result2["code"] == 0:
        checkStatus = True
        isOnlyGift = True
        checkMessage = result2["message"] + "，机器人版本为：礼包版"
    else:
        checkStatus = False
        checkMessage = result["message"]
    if checkStatus == True:
        printToLog(checkMessage)
    else:
        printToLog(checkMessage)
        time.sleep(30)
        checkPeroid(str)
    timeCheckServerIsRight()


newRobotaOptionsData = {}

def readOptions():
    global choujiangKeys
    global clearMotoTime
    global giftsKeys
    global giftsObjs
    global goodsKeys
    global goodsObjs
    global lotteryObjs
    global newRobotaOptionsData
    global qaKeys
    global qaObjs
    global robotOptions
    global timeAnnKyes
    global timeAnnObjs
    global totalRobotOptions
    global transKeys
    global transObjs
    global vipGiftsKeys
    global vipGiftsObjs
    global zjLonghdKeys
    printToLog("感谢使用南极熊SCUM内置机器人  ^_^")
    printToLog("读取配置文件中....")
    time.sleep(1)
    choujiangKeys = []
    filepath = os.path.abspath(__file__)
    directory = os.getcwd()
    contJson = newRobotaOptionsData
    goodsObjs = contJson["goods"]
    transObjs = contJson["trans"]
    if "vipgifts" in contJson:
        vipGiftsObjs = contJson["vipgifts"]
        vipGiftsKeys = vipGiftsObjs.keys()
    if "choujiang" in contJson:
        if "singleKey" in contJson["choujiang"]:
            choujiangKeys.append(contJson["choujiang"]["singleKey"])
        if "mutiKey" in contJson["choujiang"]:
            choujiangKeys.append(contJson["choujiang"]["mutiKey"])
        if "timeAnnou" in contJson:
            timeAnnObjs = contJson["timeAnnou"]
            timeAnnKyes = timeAnnObjs.keys()
        if "wenda" in contJson:
            qaObjs = contJson["wenda"]
            qaKeys = qaObjs.keys()
        zjLonghdKeys = []
        if "zjLonghd" in contJson:
            zjLonghdKeys.append(contJson["zjLonghd"]["adminDownKeyword"])
            zjLonghdKeys.append(contJson["zjLonghd"]["userUpKeyword"])
            zjLonghdKeys.append(contJson["zjLonghd"]["userDownKeyword"])
            zjLonghdKeys.append(contJson["zjLonghd"]["userPlayKeyword"] + "/")
    goodsKeys = goodsObjs.keys()
    transKeys = transObjs.keys()
    robotOptions = contJson["options"]
    totalRobotOptions = contJson
    giftsObjs = contJson["gifts"]
    lotteryObjs = contJson["choujiang"]
    giftsKeys = giftsObjs.keys()
    clearMotoTime = robotOptions["clearTime"]
    checkPeroid(robotOptions["secertKey"])


def openGanme():
    subprocess.run("start steam://rungameid/513710", shell=True)


def md5_encrypt(input_string):
    hash_object = hashlib.md5()
    hash_object.update(input_string.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig


notAllowGetGiftIds = []

def runRobot():
    global bjxFtpType
    global bjxFtpport
    global bjxHost
    global bjxPwd
    global bjxUser
    global directory
    global hwnd
    global lastKillLogArr
    global lastLoginLogArr
    global lastVIPGiftChatArr
    global longhudouObj
    global notAllowGetGiftIds
    global zjLonghdObj
    readOptions()
    initAllFreeGiftLogs()
    hwnd = 0
    filepath = os.path.abspath(__file__)
    directory = os.getcwd()
    notAllowGetGiftIds = []
    sendedGiftDataPath = directory + "/sendedGiftData.txt"
    if os.path.exists(sendedGiftDataPath):
        printToLog("存在旧版领取记录文件，正在导入至数据库")
        with open((directory + "/sendedGiftData.txt"), "r", encoding="UTF-8") as file:
            oldData = file.read()
        oldArr = oldData.split("\n")
        for i in oldArr:
            if len(i) > 10:
                if "]LogSCUM: Message: " not in i:
                    insertDataIntoSendedGiftByOldData(i + "&&&&&00000")
                    datatableConnect.commit()

        printToLog("导入数据库成功，正在删除旧文件")
        os.remove(sendedGiftDataPath)
        printToLog("旧文件删除成功")
    with open((directory + "/nowAllowGetIds.txt"), "a", encoding="UTF-8") as file:
        printToLog("读取文件中")
    with open((directory + "/lastChatData.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/lastLoginLogData.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/LHDData.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/ZJLHDData.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/RedHBData.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/DayReduceInt.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/monitorAdmin.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/adminUserList.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/fubenData.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/forbiddenPlayers.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/banData.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/waitTrans.txt"), "a", encoding="UTF-8") as file:
        pass
    defaultLHDDate = ""
    with open((directory + "/LHDData.txt"), "r", encoding="UTF-8") as file:
        defaultLHDDate = file.read()
    defaultZjLHDDate = ""
    with open((directory + "/ZJLHDData.txt"), "r", encoding="UTF-8") as file:
        defaultZjLHDDate = file.read()
    defaultHBDate = ""
    with open((directory + "/RedHBData.txt"), "r", encoding="UTF-8") as file:
        defaultHBDate = file.read()
    if defaultZjLHDDate == "":
        with open((directory + "/ZJLHDData.txt"), "w", encoding="UTF-8") as f:
            f.write(json.dumps(zjLonghdObj, ensure_ascii=False))
    if defaultLHDDate == "":
        with open((directory + "/LHDData.txt"), "w", encoding="UTF-8") as f:
            f.write(json.dumps(longhudouObj, ensure_ascii=False))
    if defaultHBDate == "":
        resetHBData()
    with open((directory + "/lastKillLogData.txt"), "a", encoding="UTF-8") as file:
        pass
    with open((directory + "/nowAllowGetIds.txt"), "r", encoding="UTF-8") as file:
        printToLog("读取文件中")
        oldData = file.read()
        if oldData:
            oldArr = oldData.split("\n")
            notAllowGetGiftIds = oldArr
    with open((directory + "/lastChatData.txt"), "r", encoding="UTF-8") as file:
        printToLog("读取文件中")
        oldData = file.read()
        if oldData:
            oldArr = oldData.split("\n")
            lastVIPGiftChatArr = oldArr
    with open((directory + "/lastLoginLogData.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
        if oldData:
            oldArr = oldData.split("\n")
            lastLoginLogArr = oldArr
    with open((directory + "/lastKillLogData.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
        if oldData:
            oldArr = oldData.split("\n")
            lastKillLogArr = oldArr
    # respon3e3 = requests.get(url=(serverRoot + "getBjxFtpAc" + "?secert=" + robotOptions["secertKey"]))
    # result3 = json.loads(respon3e3.text)
    # if result3["code"] == 0:
    #     bjxData = result3["data"]
    #     bjxHost = bjxData["bjxHost"]
    #     bjxFtpport = bjxData["bjxFtpport"]
    #     bjxUser = bjxData["bjxUser"]
    #     bjxPwd = bjxData["bjxPwd"]
    #     bjxFtpType = bjxData["bjxFtpType"]
    reopenGameWindow()


def reopenGameWindow():
    win32gui.EnumWindows(callback, None)
    if hwnd == 0:
        printToLog("未检测到游戏窗口，正在启动游戏2...")
        openGanme()
        time.sleep(20)
        ui.press("enter")
        time.sleep(60)
        reopenGameWindow()
    else:
        win32gui.ShowWindow(hwnd, 1)
        win32gui.SetForegroundWindow(hwnd)
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        width = rect[2] - x
        height = rect[3] - y
        printToLog("当前游戏窗口分辨率为：" + str(width) + "x" + str(height))
        if width != 1280 or height != 720:
            printToLog("已修改游戏窗口分辨率为1280x720")
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 1280, 720, win32con.SWP_NOMOVE | win32con.SWP_NOZORDER)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 1280, 720, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        time.sleep(1)


def callback(wd, extra):
    global hwnd
    wintext = win32gui.GetWindowText(wd)
    if len(wintext.split(" ")) > 1:
        if wintext.split(" ")[0] == "SCUM":
            hwnd = wd
        if wintext == "SCUM":
            hwnd = wd
        return True


def doInputAndEnter(str):
    global robotIsSlow
    pyperclip.copy(str)
    if robotIsSlow == 1:
        pyperclip.copy(str)
        time.sleep(1)
    userData = pyperclip.paste()
    if "]LogSCUM: " in userData:
        time.sleep(0.05)
        doInputAndEnter(str)
    else:
        ui.press("t")
        time.sleep(0.05)
        ui.press("backspace")
        time.sleep(0.05)
        ui.hotkey("ctrl", "a")
        time.sleep(0.05)
        pyperclip.copy(str)
        time.sleep(0.05)
        ui.hotkey("ctrl", "v")
        time.sleep(0.05)
        pyperclip.copy("")
        time.sleep(0.05)
        ui.press("enter")
        time.sleep(0.05)
        ui.press("enter")


def doTimeAnnou(str):
    arr = str.split(",")
    for i in arr:
        inputSimpleText(i)


def regUser(username, steamid):
    userArr = fatchUser(steamid)
    if len(userArr) == 0:
        userData = {'user_name':username,  'nick_name':"", 
         'amount':"0", 
         'reg_time':str(datetime.now()).split(".")[0], 
         'total_time':"0", 
         'last_log_time':"", 
         'vip_level':"0", 
         'vip_end_time':"", 
         'integral':"0", 
         'steam_id':str(steamid), 
         'normal_integral':"0", 
         'normal_vip_level':"0"}
        insertDataIntoUser(userData)


def doSendFreeGift(val):
    userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
    userOutName = "【" + val["inserStr"].split("&&&&&")[3] + "】"
    if userInfo == False or len(userInfo) == 0:
        inputSimpleText("未找到玩家【" + userOutName + "】的信息，请尝试重新发送指令~")
        return False
    userSteamId = val["inserStr"].split("&&&&&")[4]
    codeList = val["data"]["code"].split(",")
    codeAmount = ""
    regUser(val["inserStr"].split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    vipIsOnline = checkUserVipIsOnline(userSteamId)
    if userDataInfo[0][7] != "0":
        if vipIsOnline == True:
            vipLevelArr = totalRobotOptions["vipLevel"]
            if "language" in robotOptions and robotOptions["language"] == 1:
                userOutName = "Noble【" + val["inserStr"].split("&&&&&")[3] + "】"
            else:
                userOutName = "尊贵的【" + val["inserStr"].split("&&&&&")[3] + "】"
    printToLog("收到" + val["data"]["showName"] + "配货请求")
    if "language" in robotOptions and robotOptions["language"] == 1:
        inputSimpleText(userOutName + " Your " + val["data"]["showName"] + " is about to be shipped, please wait in place~")
    else:
        inputSimpleText(userOutName + "的" + val["data"]["showName"] + "开始发货，请打开TAB收货~")
    if "isTransRobot" in robotOptions and robotOptions["isTransRobot"] == 0:
        if "codeAmount" in val["data"]:
            codeAmount = val["data"]["codeAmount"]
        if codeAmount != "":
            if codeAmount != 0:
                if codeAmount != "0":
                    inputSimpleText("#ChangeCurrencyBalance Normal " + str(codeAmount) + " " + userSteamId)
                if "codeGoldAmount" in val["data"]:
                    try:
                        goldAmount = int(val["data"]["codeGoldAmount"])
                        if goldAmount > 0:
                            inputSimpleText("#ChangeCurrencyBalance gold " + str(goldAmount) + " " + userSteamId)
                    except Exception:
                        pass

                    for i in codeList:
                        if "isPersonTrans" in val["data"] and val["data"]["isPersonTrans"] == 1:
                            inputSimpleText(i + " " + userSteamId)
                        else:
                            if "goodType" in val["data"]:
                                if val["data"]["goodType"] == 2:
                                    oldFame = int(userInfo[2].replace(" ", "", 50).split(":")[1])
                                    goodFame = int(i)
                                    newFame = str(oldFame + goodFame)
                                    inputSimpleText("#SetFamePoints " + newFame + " " + userSteamId)
                                inputSimpleText(i + " Location " + userSteamId)

                    if "language" in robotOptions and robotOptions["language"] == 1:
                        inputSimpleText(userOutName + " Your " + val["data"]["showName"] + " have been successfully shipped. Please check your receipt carefully~")
                    else:
                        inputSimpleText(userOutName + "的" + val["data"]["showName"] + "发货成功，请注意查收")
            inputSimpleText("#teleportTo " + userSteamId)
            time.sleep(robotOptions["sendSleepTime"])
            codeList = val["data"]["code"].split(",")
            for i in codeList:
                inputSimpleText(i)

            if "language" in robotOptions and robotOptions["language"] == 1:
                inputSimpleText(userOutName + " Your " + val["data"]["showName"] + " have been successfully shipped. Please check your receipt carefully")
            else:
                inputSimpleText(userOutName + "的" + val["data"]["showName"] + "发货成功，请注意查收")
            time.sleep(3)
            inputSimpleText("#teleport  X=-912058.688 Y=612209.313 Z=63116.238")
        insertDataIntoSendedGift(val["inserStr"] + "&&&&&" + userSteamId)
        insertToSendedGiftData(val["inserStr"])
        time.sleep(0.8)


def insertToSendedGiftData(inserStr):
    global sendedGiftDataObj
    arr = inserStr.split("&&&&&")
    localTime = arr[1]
    keyword = arr[2]
    usercode = arr[4]
    if keyword in sendedGiftDataObj:
        sendedGiftDataObj[keyword].append(localTime + "&&&&&" + usercode)


def doSendGift(val, goodNum=None):
    userOutName = "【" + val["inserStr"].split("&&&&&")[3] + "】"
    userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
    if userInfo == False or len(userInfo) == 0:
        inputSimpleText("未找到玩家【" + userOutName + "】的信息，请尝试重新发送指令~")
        return False
    userSteamId = val["inserStr"].split("&&&&&")[4]
    codeList = val["data"]["code"].split(",")
    codeAmount = ""
    regUser(val["inserStr"].split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    vipIsOnline = checkUserVipIsOnline(userSteamId)
    if userDataInfo[0][7] != "0":
        if vipIsOnline == True:
            if "language" in robotOptions and robotOptions["language"] == 1:
                userOutName = "Noble 【" + val["inserStr"].split("&&&&&")[3] + "】"
            else:
                userOutName = "尊贵的【" + val["inserStr"].split("&&&&&")[3] + "】"
        openUseXiong = False
        if "isOpenXiongAmount" in robotOptions:
            if robotOptions["isOpenXiongAmount"] == 1:
                openUseXiong = True
            goodUseXiong = False
            if "useXiong" in val["data"]:
                if val["data"]["useXiong"] == 1:
                    goodUseXiong = True
                vipLevelIsUnable = False
                if "onlyVipLevel" in val["data"]:
                    if int(val["data"]["onlyVipLevel"]) > int(userDataInfo[0][7]):
                        vipLevelIsUnable = True
                        if "language" in robotOptions and robotOptions["language"] == 1:
                            inputSimpleText(userOutName + "，Your VIP level is insufficient to purchase this product")
                        else:
                            inputSimpleText(userOutName + "，您的VIP等级不足，无法购买该商品")
                        return False
            vipIsOutTime = False
            if "onlyVipLevel" in val["data"] and val["data"]["onlyVipLevel"] != "0":
                try:
                    current = int(datetime.strptime(str(datetime.now()).split(" ")[0], "%Y-%m-%d").timestamp())
                    vipenddate = userDataInfo[0][8]
                    if vipenddate == None or len(vipenddate) < 2:
                        vipIsOutTime = True
                    else:
                        vipend = int(datetime.strptime(str(vipenddate), "%Y-%m-%d").timestamp())
                        if current > vipend:
                            vipIsOutTime = True
                except Exception as e:
                    try:
                        vipIsOutTime = False
                    finally:
                        e = None
                        del e

                if vipIsOutTime == True:
                    if "language" in robotOptions and robotOptions["language"] == 1:
                        inputSimpleText(userOutName + "，Your VIP has expired and you are unable to purchase this product~")
                    else:
                        inputSimpleText(userOutName + "，您的VIP已过期，无法购买该商品")
                    return False
                goodNeedTrans = False
                if "isTrans" in val["data"]:
                    if val["data"]["isTrans"] == 1:
                        goodNeedTrans = True
        if "isPersonTrans" in val["data"] and val["data"]["isPersonTrans"] == 1:
            isInWaitTime = False
            try:
                if "transWaitTime" in val["data"]:
                    if float(val["data"]["transWaitTime"]) > 0:
                        keyword = val["inserStr"].split("&&&&&")[2]
                        serverTime = val["inserStr"].split("&&&&&")[5]
                        localTime = val["inserStr"].split("&&&&&")[1]
                        giftList = getUserGiftLogsByKey(keyword, userSteamId, localTime)
                        orderUserName = "【" + val["inserStr"].split("&&&&&")[3] + "】"
                        if giftList != None:
                            if len(giftList) > 0:
                                preServerTime = formatServerTimeToStemp(giftList[-1][1])
                                currentTime = formatServerTimeToStemp(serverTime)
                                diffTime = currentTime - preServerTime
                                waitTime = float(val["data"]["transWaitTime"]) * 60
                                if diffTime < waitTime:
                                    if "language" in robotOptions and robotOptions["language"] == 1:
                                        inputSimpleText(userOutName + "，Your teleportation is cooling down...The cooling time is 【" + str(val["data"]["transWaitTime"]) + "】minutes~")
                                    else:
                                        inputSimpleText(orderUserName + "的传送正在冷却中...冷却时间为【" + str(val["data"]["transWaitTime"]) + "】分钟")
                                    isInWaitTime = True
            except Exception as e:
                try:
                    print(e)
                    isInWaitTime = False
                    logging.error(str(datetime.now()))
                    logging.error(traceback.format_exc())
                finally:
                    e = None
                    del e

            if isInWaitTime == True:
                return False
            printToLog("收到" + val["data"]["showName"] + "配货请求")
            if "language" in robotOptions and robotOptions["language"] == 1:
                inputSimpleText(userOutName + ", your " + val["data"]["showName"] + " is about to be shipped, please stand still and wait~")
            else:
                inputSimpleText(userOutName + "的" + val["data"]["showName"] + "开始发货，请打开TAB收货~")
            if "codeAmount" in val["data"]:
                codeAmount = val["data"]["codeAmount"]
            if codeAmount != "" and codeAmount != 0:
                if codeAmount != "0":
                    inputSimpleText("#ChangeCurrencyBalance Normal " + str(codeAmount) + " " + userSteamId)
                codeGold = ""
                if "codeGold" in val["data"]:
                    codeGold = val["data"]["codeGold"]
    if codeGold != "" and codeGold != 0:
        if codeGold != "0":
            inputSimpleText("#ChangeCurrencyBalance gold " + str(codeGold) + " " + userSteamId)
        if goodNeedTrans == False and "isTransRobot" in robotOptions and robotOptions["isTransRobot"] == 0:
            for i in codeList:
                if "isPersonTrans" in val["data"] and val["data"]["isPersonTrans"] == 1:
                    inputSimpleText(i + " " + userSteamId)
                else:
                    if "goodType" in val["data"] and val["data"]["goodType"] == 2:
                        oldFame = int(userInfo[2].replace(" ", "", 50).split(":")[1])
                        goodFame = int(i)
                        if goodNum != None:
                            newFame = str(oldFame + int(goodNum))
                        else:
                            newFame = str(oldFame + goodFame)
                        inputSimpleText("#SetFamePoints " + newFame + " " + userSteamId)
                    else:
                        if "goodType" in val["data"] and val["data"]["goodType"] == 3:
                            goldNum = int(i)
                            if goodNum != None:
                                goldNum = int(goodNum)
                            inputSimpleText("#ChangeCurrencyBalance Gold " + str(goldNum) + " " + userSteamId)
                        else:
                            if "goodType" in val["data"]:
                                if val["data"]["goodType"] == 4:
                                    goldNum = int(i)
                                    if goodNum != None:
                                        goldNum = int(goodNum)
                                    inputSimpleText("#ChangeCurrencyBalance Normal " + str(goldNum) + " " + userSteamId)
                                if "goodType" in val["data"] and val["data"]["goodType"] == 5:
                                    xiongBNum = int(i)
                                    if goodNum != None:
                                        xiongBNum = int(goodNum)
                                    preAmount = userDataInfo[0][3]
                                    newAmount = int(preAmount) + int(xiongBNum)
                                    updateUserData = {'steam_id':userSteamId, 
                                     'amount':newAmount}
                                    updateDataToUser(updateUserData)
                                else:
                                    if goodNum != None:
                                        tenNum = int(int(goodNum) / 10)
                                        oneNum = int(int(goodNum) % 10)
                                        codeArr = i.strip(" ").split(" ")
                                        codeStr = codeArr[0] + " " + codeArr[1] + " "
                                        if tenNum > 0:
                                            for ni in range(tenNum):
                                                inputSimpleText(codeStr + "10 Location " + userSteamId)

                                        if oneNum > 0:
                                            inputSimpleText(codeStr + str(oneNum) + " Location " + userSteamId)
                                    else:
                                        inputSimpleText(i + " Location " + userSteamId)

            if "language" in robotOptions and robotOptions["language"] == 1:
                inputSimpleText(userOutName + ", Your " + val["data"]["showName"] + "have been successfully shipped. Please check your receipt carefully~")
            else:
                inputSimpleText(userOutName + "的" + val["data"]["showName"] + "发货成功，请注意查收")
        else:
            inputSimpleText("#teleportTo " + userSteamId)
            time.sleep(robotOptions["sendSleepTime"])
            codeList = val["data"]["code"].split(",")
            for i in codeList:
                inputSimpleText(i)

            if "language" in robotOptions and robotOptions["language"] == 1:
                inputSimpleText(userOutName + ", Your " + val["data"]["showName"] + "have been successfully shipped. Please check your receipt carefully~")
            else:
                inputSimpleText(userOutName + "的" + val["data"]["showName"] + "发货成功，请注意查收")
            inputSimpleText("#teleport  X=-912058.688 Y=612209.313 Z=63116.238")
        insertDataIntoSendedGift(val["inserStr"] + "&&&&&" + userSteamId)
        insertToSendedGiftData(val["inserStr"])
        time.sleep(0.8)


def doLHDAdmin(val):
    userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
    message = val["inserStr"].split("&&&&&")[2]
    if userInfo == False or len(userInfo) == 0:
        inputSimpleText("未找到玩家【" + val["inserStr"].split("&&&&&")[3] + "】的信息，请尝试重新发送指令~")
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    isAdmin = False
    if userSteamId in totalRobotOptions["longhudou"]["admin"]:
        isAdmin = True
    if isAdmin == False:
        return False
    with open((directory + "/LHDData.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    stream = io.StringIO(oldData)
    oldObj = json.load(stream)
    printToLog("收到龙虎斗管理请求")
    openKey = totalRobotOptions["longhudou"]["adminKeyword"]
    closeKey = ""
    if "closeAdminKeyword" in totalRobotOptions["longhudou"]:
        closeKey = totalRobotOptions["longhudou"]["closeAdminKeyword"]
    if message == openKey:
        if oldObj["isOpen"] == "0":
            oldObj["isOpen"] = "1"
            inputSimpleText(totalRobotOptions["longhudou"]["openTip"])
            with open((directory + "/LHDData.txt"), "w", encoding="UTF-8") as f:
                f.write(json.dumps(oldObj, ensure_ascii=False))
        elif "language" in robotOptions and robotOptions["language"] == 1:
            inputSimpleText("The current activity is in progress and does not need to be restarted~")
        else:
            inputSimpleText("当前活动正在进行中，无需再次开启")
    if message == closeKey:
        if oldObj["isOpen"] == "1":
            oldObj["isOpen"] = "0"
            inputSimpleText(totalRobotOptions["longhudou"]["endTip"])
            with open((directory + "/LHDData.txt"), "w", encoding="UTF-8") as f:
                f.write(json.dumps(oldObj, ensure_ascii=False))
        else:
            inputSimpleText(totalRobotOptions["longhudou"]["endTip"])


def adminDownZjLhd(val):
    oldData = readZjLhdData()
    if oldData["uperSteamid"] == "":
        if "language" in robotOptions and robotOptions["language"] == 1:
            inputSimpleText("The current banker is 【system】, there is no need to lower the banker~")
        else:
            inputSimpleText("当前庄家为【系统】，无需下庄哦~")
    else:
        if "language" in robotOptions and robotOptions["language"] == 1:
            inputSimpleText("The current banker is 【system】, there is no need to lower the banker~")
        else:
            inputSimpleText("The current banker is 【" + oldData["uperName"] + "】，He was taken down from the bankers position by the administrator~")
        oldData["uperSteamid"] = ""
        oldData["uperName"] = "系统"
        oldData["uperTimes"] = "0"
        with open((directory + "/ZJLHDData.txt"), "w", encoding="UTF-8") as f:
            f.write(json.dumps(oldData, ensure_ascii=False))


def userUpZjLhd(val):
    userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
    userOutName = val["inserStr"].split("&&&&&")[3]
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    oldData = readZjLhdData()
    if oldData["uperSteamid"] == "":
        userBalance = userInfo[3].split("Account balance: ")[1]
        if int(userBalance) < float(totalRobotOptions["zjLonghd"]["upMinAmount"]):
            inputSimpleText("玩家【" + userOutName + "】无法成为庄家~庄家需最少需要【" + totalRobotOptions["zjLonghd"]["upMinAmount"] + "】美金哦~")
        else:
            oldData["uperSteamid"] = userSteamId
            oldData["uperName"] = userOutName
            oldData["uperTimes"] = "0"
            with open((directory + "/ZJLHDData.txt"), "w", encoding="UTF-8") as f:
                f.write(json.dumps(oldData, ensure_ascii=False))
            inputSimpleText("恭喜玩家【" + userOutName + "】成为当前庄家~庄家需最少坐庄【" + totalRobotOptions["zjLonghd"]["upMinTimes"] + "】次哦~")
    else:
        inputSimpleText("当前庄家为玩家【" + oldData["uperName"] + "】，庄家只能有一个哦~")
    ui.press("enter")


def userDownZjLhd(val):
    userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
    userOutName = val["inserStr"].split("&&&&&")[3]
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    oldData = readZjLhdData()
    if oldData["uperSteamid"] == userSteamId:
        if int(oldData["uperTimes"]) < int(totalRobotOptions["zjLonghd"]["upMinTimes"]):
            inputSimpleText("玩家【" + userOutName + "】坐庄次数未达到【" + totalRobotOptions["zjLonghd"]["upMinTimes"] + "】次，不可以跑路哦~")
        else:
            oldData["uperSteamid"] = ""
            oldData["uperName"] = ""
            oldData["uperTimes"] = "0"
            with open((directory + "/ZJLHDData.txt"), "w", encoding="UTF-8") as f:
                f.write(json.dumps(oldData, ensure_ascii=False))
            inputSimpleText("玩家【" + userOutName + "】离开了庄家位置~")
    ui.press("enter")


def playZjLhd(val):
    userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
    userOutName = val["inserStr"].split("&&&&&")[3]
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    userBalance = userInfo[3].split("Account balance: ")[1]
    oldData = readZjLhdData()
    typeModel = 0
    if "typeModel" in totalRobotOptions["zjLonghd"]:
        if totalRobotOptions["zjLonghd"]["typeModel"] == 1:
            typeModel = 1
        if oldData["uperSteamid"] != "":
            uperInfo = getUserInfoBySteamidFromTotal(oldData["uperSteamid"])
            if uperInfo == None or len(uperInfo) == 0:
                if typeModel == 1:
                    inputSimpleText("当前森林之王【" + oldData["uperName"] + "】不在线，森林之王自动变更为系统~")
                else:
                    inputSimpleText("当前庄家【" + oldData["uperName"] + "】不在线，庄家自动变更为系统~")
                oldData["uperName"] = "系统"
                oldData["uperSteamid"] = ""
                oldData["uperTimes"] = "0"
                with open((directory + "/ZJLHDData.txt"), "w", encoding="UTF-8") as f:
                    f.write(json.dumps(oldData, ensure_ascii=False))
    userWord = val["inserStr"].split("&&&&&")[2].split("/")[1]
    userLhdAmount = 0
    userKeyWord = ""
    try:
        if "isOnlyPlayer" in totalRobotOptions["zjLonghd"] and totalRobotOptions["zjLonghd"]["isOnlyPlayer"] == 1 and oldData["uperSteamid"] == "":
            if typeModel == 1:
                inputSimpleText("当前森林之王家里没人，无法开启挑战哦，请先发送 " + totalRobotOptions["zjLonghd"]["userUpKeyword"] + " 成为伟大的森立之王~")
            else:
                inputSimpleText("当前没有玩家坐庄，无法开启娱乐哦，请先发送 " + totalRobotOptions["zjLonghd"]["userUpKeyword"] + " 成为伟大的庄家~")
        else:
            if "龙" in userWord:
                userLhdAmount = float(userWord.split("龙")[1])
                userKeyWord = "龙"
            if "虎" in userWord:
                userLhdAmount = float(userWord.split("虎")[1])
                userKeyWord = "虎"
            if "和" in userWord:
                userLhdAmount = float(userWord.split("和")[1])
                userKeyWord = "和"
            if float(userBalance) < userLhdAmount:
                if typeModel == 1:
                    inputSimpleText("国王【" + userOutName + "】派出的战力少于自己城堡的驻兵哦，请先招募战士参战~")
                else:
                    inputSimpleText("玩家【" + userOutName + "】的押注数额超出了您自己的钱包余额哦~")
            elif userLhdAmount < float(totalRobotOptions["zjLonghd"]["oneMinAmount"]):
                if typeModel == 1:
                    inputSimpleText("国王【" + userOutName + "】派出的战士少于单场战役需要派出战士最小数量哦~单次战役战士最少为【" + totalRobotOptions["zjLonghd"]["oneMinAmount"] + "】~")
                else:
                    inputSimpleText("玩家【" + userOutName + "】的押注数额不足单次押注最小限额哦~单次最小限额为【" + totalRobotOptions["zjLonghd"]["oneMinAmount"] + "】~")
            elif float(userBalance) < float(totalRobotOptions["zjLonghd"]["userPlayMinAmount"]):
                if typeModel == 1:
                    inputSimpleText("国王【" + userOutName + "】的城堡驻兵不足以派出进行一次挑战哦~城堡驻兵最小限额为【" + totalRobotOptions["zjLonghd"]["userPlayMinAmount"] + "】~")
                else:
                    inputSimpleText("玩家【" + userOutName + "】的钱包余额不足参与押注的最小余额限制哦~玩家余额最小限额为【" + totalRobotOptions["zjLonghd"]["userPlayMinAmount"] + "】~")
            elif userLhdAmount > float(totalRobotOptions["zjLonghd"]["oneMaxAmount"]):
                if typeModel == 1:
                    inputSimpleText("国王【" + userOutName + "】派出的战士超出了单次战役最大战士数量哦~单次战役战士最大限额为【" + totalRobotOptions["zjLonghd"]["oneMaxAmount"] + "】~")
                else:
                    inputSimpleText("玩家【" + userOutName + "】的押注数额超出了单次押注最大限额哦~单次最大限额为【" + totalRobotOptions["zjLonghd"]["oneMaxAmount"] + "】~")
            elif userSteamId == oldData["uperSteamid"]:
                if typeModel == 1:
                    inputSimpleText("国王【" + userOutName + "】为当前的森林之子，不能自己挑战自己哦~")
                else:
                    inputSimpleText("玩家【" + userOutName + "】为当前庄家，庄家不可与自己对赌哦~")
            else:
                resultKeys = []
                resultTimes = int(totalRobotOptions["zjLonghd"]["keywordNum"])
                rewardKeys = ["龙", "虎", "和"]
                rewardVals = []
                winKey = ""
                heRatio = float(totalRobotOptions["zjLonghd"]["userHeWinRatio"])
                uperWinRatio = float(userZJLhdWinRatio)
                if oldData["uperSteamid"] != "":
                    uperWinRatio = float(userZJLhdWinRatio)
                else:
                    uperWinRatio = float(systemZJLhdWinRatio)
                rewardVals = [
                 1 - uperWinRatio, uperWinRatio, heRatio]
                if userKeyWord == "龙":
                    rewardKeys = [
                     "龙", "虎", "和"]
                elif userKeyWord == "虎":
                    rewardKeys = [
                     "虎", "龙", "和"]
                resultKeys = random.choices(rewardKeys, weights=rewardVals, k=(int(totalRobotOptions["zjLonghd"]["keywordNum"])))
                key1Num = 0
                key2Num = 0
                key3Num = 0
                for i in resultKeys:
                    if i == rewardKeys[0]:
                        key1Num = key1Num + 1
                    if i == rewardKeys[1]:
                        key2Num = key2Num + 1
                    if i == rewardKeys[2]:
                        key3Num = key3Num + 1

                numsArr = [
                 key1Num, key2Num, key3Num]
                max_index = max((enumerate(numsArr)), key=(lambda item: item[1]))[0]
                winKey = rewardKeys[max_index]
                keysResultStr = "、".join(resultKeys)
                userGetAmount = 0
                upUerName = oldData["uperName"]
                if oldData["uperName"] == "":
                    oldData["uperName"] = "系统"
                nowDate = str(datetime.now()).split(" ")[0]
                if oldData["lastDate"] != nowDate:
                    oldData["lastDate"] = nowDate
                    oldData["todayAmount"] = "0"
                userPlayAmount = userLhdAmount
                nowDateObj = str(datetime.now()).split(".")[0].split(" ")
                nowDateStr = nowDateObj[0]
                nowTimeStr = nowDateObj[1]
                insertStr = ""
                uperSteamid = oldData["uperSteamid"]
                if uperSteamid == "":
                    uperSteamid = "0"
                if userKeyWord == winKey:
                    userLhdAmountAdd = str(userLhdAmount - userLhdAmount * float(totalRobotOptions["zjLonghd"]["robotGetAmount"]))
                    if winKey == "和":
                        userLhdAmountAdd = str(float(userLhdAmount - userLhdAmount * float(totalRobotOptions["zjLonghd"]["robotGetAmount"])) * float(totalRobotOptions["zjLonghd"]["userHeWinMutip"]))
                        userLhdAmount = userLhdAmount * float(totalRobotOptions["zjLonghd"]["userHeWinMutip"])
                    uperIsOutAmount = False
                    if oldData["uperSteamid"] != "":
                        uperInfo = getUserInfoBySteamidFromTotal(oldData["uperSteamid"])
                        uperBalance = int(float(uperInfo[3].split("Account balance: ")[1]))
                        if userLhdAmount > uperBalance:
                            userLhdAmount = uperBalance
                            userLhdAmountAdd = str(uperBalance - uperBalance * float(totalRobotOptions["zjLonghd"]["robotGetAmount"]))
                            uperIsOutAmount = True
                        insertStr = userOutName + "&&&&&" + userSteamId + "&&&&&" + str(userLhdAmount) + "&&&&&" + userLhdAmountAdd + "&&&&&1&&&&&" + upUerName + "&&&&&" + uperSteamid + "&&&&&" + nowDateStr + "&&&&&" + nowTimeStr
                        insertDataIntoLHDLog(insertStr)
                        if oldData["uperSteamid"] != "":
                            inputSimpleText("#ChangeCurrencyBalance Normal -" + str(userLhdAmount) + " " + oldData["uperSteamid"])
                            insertStr = upUerName + "&&&&&" + oldData["uperSteamid"] + "&&&&&0&&&&&-" + str(userLhdAmount) + "&&&&&8&&&&&" + upUerName + "&&&&&" + uperSteamid + "&&&&&" + nowDateStr + "&&&&&" + nowTimeStr
                            insertDataIntoLHDLog(insertStr)
                    if typeModel == 1:
                        inputSimpleText("国王【" + userOutName + "】本次挑战战胜了森林之子【" + upUerName + "】，俘获了对方【" + userLhdAmountAdd + "】名战士，恭喜恭喜！")
                    else:
                        inputSimpleText("【" + userOutName + "】本期【" + winKey + "】胜，您赢得了【" + userLhdAmountAdd + "】美金，本期庄家【" + upUerName + "】，路单：" + keysResultStr)
                    inputSimpleText("#ChangeCurrencyBalance Normal " + userLhdAmountAdd + " " + userSteamId)
                    oldData["todayAmount"] = str(float(oldData["todayAmount"]) + userLhdAmount)
                    oldData["totalAmount"] = str(float(oldData["totalAmount"]) + userLhdAmount)
                    if uperIsOutAmount:
                        inputSimpleText("庄家【" + upUerName + "】已破产，【" + userOutName + "】赢得了庄家所有的资产~")
                else:
                    userLhdAmountAdd = str(userLhdAmount - userLhdAmount * float(totalRobotOptions["zjLonghd"]["robotGetAmount"]))
                    inputSimpleText("#ChangeCurrencyBalance Normal -" + str(userLhdAmount) + " " + userSteamId)
                    insertStr = userOutName + "&&&&&" + userSteamId + "&&&&&" + str(userLhdAmount) + "&&&&&-" + str(userLhdAmount) + "&&&&&0&&&&&" + upUerName + "&&&&&" + uperSteamid + "&&&&&" + nowDateStr + "&&&&&" + nowTimeStr
                    insertDataIntoLHDLog(insertStr)
                    if oldData["uperSteamid"] != "":
                        inputSimpleText("#ChangeCurrencyBalance Normal " + userLhdAmountAdd + " " + oldData["uperSteamid"])
                        insertStr = upUerName + "&&&&&" + oldData["uperSteamid"] + "&&&&&0&&&&&" + userLhdAmountAdd + "&&&&&9&&&&&" + upUerName + "&&&&&" + uperSteamid + "&&&&&" + nowDateStr + "&&&&&" + nowTimeStr
                        insertDataIntoLHDLog(insertStr)
                    if typeModel == 1:
                        inputSimpleText("国王【" + userOutName + "】本次挑战输给了森林之子【" + upUerName + "】，丢失了【" + str(userLhdAmount) + "】名城堡驻兵，不要灰心，屡败屡战！！！")
                    else:
                        inputSimpleText("【" + userOutName + "】本期【" + winKey + "】胜，您输掉了【" + str(userLhdAmount) + "】美金，本期庄家【" + upUerName + "】，路单：" + keysResultStr)
                    oldData["todayAmount"] = str(float(oldData["todayAmount"]) + userLhdAmount)
                    oldData["totalAmount"] = str(float(oldData["totalAmount"]) + userLhdAmount)
                    goodIntRatio = 1
                    try:
                        if "inteZJLhdNormal" in totalRobotOptions["options"]:
                            goodIntRatio = float(totalRobotOptions["options"]["inteZJLhdNormal"])
                    except Exception:
                        goodIntRatio = 1

                    updateUserNormalInt(str(int(userLhdAmount)), userSteamId, str(int(float(userLhdAmount) * goodIntRatio)))
                with open((directory + "/ZJLHDData.txt"), "w", encoding="UTF-8") as f:
                    f.write(json.dumps(oldData, ensure_ascii=False))
                if oldData["uperSteamid"] != "":
                    nowUperTimes = int(oldData["uperTimes"]) + 1
                    uperInfo = getUserInfoBySteamidFromTotal(oldData["uperSteamid"])
                    uperBalance = float(uperInfo[3].split("Account balance: ")[1])
                    if nowUperTimes > int(totalRobotOptions["zjLonghd"]["upMaxTimes"]):
                        zjLonghdObj = {'uperSteamid':"",  'uperName':"系统", 
                         'uperTimes':"0", 
                         'todayAmount':oldData["todayAmount"], 
                         'totalAmount':oldData["totalAmount"], 
                         'lastDate':oldData["lastDate"]}
                        with open((directory + "/ZJLHDData.txt"), "w", encoding="UTF-8") as f:
                            f.write(json.dumps(zjLonghdObj, ensure_ascii=False))
                        if typeModel == 1:
                            inputSimpleText("森林之子【" + oldData["uperName"] + "】离开了恶魔城堡，因为他被天使Lucy拯救了~")
                        else:
                            inputSimpleText("玩家【" + oldData["uperName"] + "】离开了庄家位置~因为到了最大坐庄局数啦~")
                    elif uperBalance < float(totalRobotOptions["zjLonghd"]["upMinAmount"]):
                        if typeModel == 1:
                            inputSimpleText("森林之子【" + oldData["uperName"] + "】离开了恶魔城堡~因为没有驻兵可以防守啦~")
                        else:
                            inputSimpleText("玩家【" + oldData["uperName"] + "】离开了庄家位置~因为庄家没钱啦~")
                        oldData["uperSteamid"] = ""
                        oldData["uperName"] = "系统"
                        oldData["uperTimes"] = "0"
                        with open((directory + "/ZJLHDData.txt"), "w", encoding="UTF-8") as f:
                            f.write(json.dumps(oldData, ensure_ascii=False))
                    else:
                        oldData["uperTimes"] = str(nowUperTimes)
                        with open((directory + "/ZJLHDData.txt"), "w", encoding="UTF-8") as f:
                            f.write(json.dumps(oldData, ensure_ascii=False))
        ui.press("enter")
    except Exception as e:
        try:
            logging.error(str(datetime.now()))
            logging.error(traceback.format_exc())
            inputSimpleText("玩家【" + userOutName + "】您的指令输入格式不对哦~")
            ui.press("enter")
        finally:
            e = None
            del e


def readZjLhdData():
    directory = os.getcwd()
    try:
        with open((directory + "/ZJLHDData.txt"), "r", encoding="UTF-8") as file:
            oldData = file.read()
        stream = io.StringIO(oldData)
        oldObj = json.load(stream)
    except Exception as e:
        try:
            oldObj = {
              'uperSteamid': "", 'uperName': "系统", 'uperTimes': "0", 'todayAmount': "0", 'totalAmount': "0", 'lastDate': ""}
        finally:
            e = None
            del e

    return oldObj


def readHBData():
    directory = os.getcwd()
    with open((directory + "/RedHBData.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    stream = io.StringIO(oldData)
    oldObj = json.load(stream)
    return oldObj


def getGiftCardDataByCardValue(val):
    cursor = datatableConnect.cursor()
    cursor.execute("SELECT * FROM card_list WHERE card_value = ?", (val,))
    results = cursor.fetchall()
    if len(results) == 0:
        printToLog("未查询到礼品卡")
    elif len(results) == 1:
        pass
    else:
        printToLog("查询到多条个礼品卡")
    return results


def getRecoveItem(name):
    coveItem = {}
    havCove = False
    if "recoveItemsList" in robotOptions:
        if len(robotOptions["recoveItemsList"]) > 0:
            for item in robotOptions["recoveItemsList"]:
                if item["name"] == name:
                    coveItem = item
                    havCove = True

        return {'havCove':havCove, 
         'coveItem':coveItem}


def getUserLocation(steamid):
    currentUser = getUserInfoBySteamidFromTotal(steamid)
    if currentUser == None or len(currentUser) == 0:
        return "no find player"
    inputSimpleText("#Location " + str(steamid) + " true")
    time.sleep(1)
    userData = pyperclip.paste()
    userLoc = userData.split(" ")[-3:]
    userLoc = " ".join(userLoc)
    return userLoc


def getLastDestoryItemNum():
    time.sleep(2)
    localappdata = os.getenv("LOCALAPPDATA")
    f = open((localappdata + "/SCUM/Saved/Logs/SCUM.log"), encoding="utf-8")
    cont = f.read()
    f.close()
    contList = cont.split("\n")
    desItemArr = []
    for i in contList:
        if i.find("LogSCUM: Sender player state null for message ") != -1:
            if i.find("items destroyed!!") != -1:
                desItemArr.append(i)

    lastItem = desItemArr[-1]
    lastTime = lastItem.split("]")[0].split("[")[1].split(":")[0]
    lastDesedNum = lastItem.split(" items destroyed!!")[0].split(" ")[-1]
    return lastDesedNum


def doCallDrop(val):
    printToLog("收到玩家召唤空投请求")
    userName = val["inserStr"].split("&&&&&")[3]
    desedNum = getLastDestoryItemNum()
    userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    playerLoc = getUserLocation(userSteamId)
    if "callDropItemCode" in robotOptions:
        if robotOptions["callDropItemCode"] != "" and "callDropItemNum" in robotOptions and robotOptions["callDropItemNum"] != "0":
            userName = val["inserStr"].split("&&&&&")[3]
            userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
            if userInfo == False or len(userInfo) == 0:
                inputSimpleText("未找到玩家【" + userName + "】的信息，请尝试重新发送指令~")
                return False
            userSteamId = userInfo[1].split("(")[-1].split(")")[0]
            regUser(val["inserStr"].split("&&&&&")[3], userSteamId)
            userDataInfo = fatchUser(userSteamId)
            playerLoc = getUserLocation(userSteamId)
            callItemCode = robotOptions["callDropItemCode"]
            callItemNum = robotOptions["callDropItemNum"]
            inputSimpleText("#DestroyAllItemsWithinRadius " + callItemCode + ' 2 "' + playerLoc + '"')
            desedNum = getLastDestoryItemNum()
            if int(desedNum) < int(callItemNum):
                inputSimpleText("【" + userName + "】发起的空投召唤失败，召唤空投需要指定物品数量为【" + str(callItemNum) + "】，您提供的指定物品数量为【" + str(desedNum) + "】~")
        else:
            inputSimpleText("【" + userName + "】成功发起空投召唤，您的空投即将送达，请在原地等待！！！您提供的指定物品数量为【" + str(desedNum) + "】~")
            inputSimpleText("#ScheduleWorldEvent BP_CargoDropEvent " + playerLoc)
            if "callDropRedInfo" in robotOptions and robotOptions["callDropRedInfo"] == "1":
                inputSimpleText("#Announce 【" + userName + "】成功发起空投召唤，您的空投即将送达，请在原地等待！！！")
    else:
        inputSimpleText("召唤空投参数配置不足，请联系管理员检查~")


def getPlayerDictKTDist(curPlayerLoc, centerLoc):
    if curPlayerLoc == "no find player":
        return curPlayerLoc
    curObj = curPlayerLoc.split(" ")
    cenObj = centerLoc.split(" ")
    curX = curObj[0]
    if "=" in curX:
        curX = curX.split("=")[1]
    curY = curObj[1]
    if "=" in curY:
        curY = curY.split("=")[1]
    cenX = cenObj[0]
    if "=" in cenX:
        cenX = cenX.split("=")[1]
    cenY = cenObj[1]
    if "=" in cenY:
        cenY = cenY.split("=")[1]
    return calculate_distance(curX, curY, cenX, cenY)


def doRecove(val):
    printToLog("收到玩家回收请求")
    cardVal = val["inserStr"].split("&&&&&")[2].split(robotOptions["recoveKeyword"] + "/")[1]
    userName = val["inserStr"].split("&&&&&")[3]
    cardInfo = getRecoveItem(cardVal)
    if cardInfo["havCove"] == False:
        inputSimpleText("暂不支持【" + userName + "】发起的【" + cardVal + "】物品回收哦~请联系管理员添加可回收物品~")
    else:
        cardData = None
        cardId = 0
        userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
        if userInfo == False or len(userInfo) == 0:
            inputSimpleText("未找到玩家【" + userName + "】的信息，请尝试重新发送指令~")
            return False
        userSteamId = userInfo[1].split("(")[-1].split(")")[0]
        regUser(val["inserStr"].split("&&&&&")[3], userSteamId)
        userDataInfo = fatchUser(userSteamId)
        playerLoc = getUserLocation(userSteamId)
        recoItem = cardInfo["coveItem"]
        codeArr = recoItem["code"].split(",")
        desedNum = 0
        for i in codeArr:
            inputSimpleText("#DestroyAllItemsWithinRadius " + i + ' 2 "' + playerLoc + '"')
            desedNumSp = getLastDestoryItemNum()
            desedNum = desedNum + int(desedNumSp)

        if desedNum == 0:
            inputSimpleText("玩家【" + userName + "】发起的【" + cardVal + "】成功回收数量为【0】，回收失败~请保证需回收物品在您脚下1米范围内~")
        elif int(desedNum) < int(recoItem["minNum"]):
            inputSimpleText("玩家【" + userName + "】发起的【" + cardVal + "】成功回收数量为【" + str(desedNum) + "】，最低要求回收数量为【" + str(recoItem["minNum"]) + "】，回收失败~请保证需回收物品在您脚下1米范围内~")
        else:
            inputSimpleText("玩家【" + userName + "】发起的【" + cardVal + "】成功回收数量为【" + str(desedNum) + "】，正在发放回收奖励~")
            signGiftObj = recoItem
            rewardNameStr = ""
            desedNumMuti = 1
            if "minNum" in recoItem and recoItem["minNum"] != "":
                desedNumMuti = int(int(desedNum) / int(recoItem["minNum"]))
            else:
                desedNumMuti = desedNum
            if "amount" in signGiftObj:
                if signGiftObj["amount"] != "":
                    amountVal = str(int(signGiftObj["amount"]) * int(desedNumMuti))
                    inputSimpleText("#ChangeCurrencyBalance Normal " + amountVal + " " + userSteamId)
                    rewardNameStr = rewardNameStr + amountVal + "美金，"
                if "gold" in signGiftObj:
                    if signGiftObj["gold"] != "":
                        goldVal = str(int(signGiftObj["gold"]) * int(desedNumMuti))
                        inputSimpleText("#ChangeCurrencyBalance gold " + goldVal + " " + userSteamId)
                        rewardNameStr = rewardNameStr + goldVal + "金条，"
                    if "xiongb" in signGiftObj and signGiftObj["xiongb"] != "":
                        try:
                            if signGiftObj["xiongb"] != "0":
                                xibAmount = int(int(float(signGiftObj["xiongb"])) * int(desedNumMuti))
                                preAmount = userDataInfo[0][3]
                                newAmount = int(preAmount) + xibAmount
                                updateUserData = {'steam_id':userSteamId, 
                                 'amount':newAmount}
                                updateDataToUser(updateUserData)
                                rewardNameStr = rewardNameStr + str(int(float(xibAmount))) + "熊币，"
                        except Exception:
                            pass

                    if "fame" in signGiftObj and signGiftObj["fame"] != "":
                        try:
                            if signGiftObj["fame"] != "0":
                                fameVal = int(int(float(signGiftObj["fame"])) * int(desedNumMuti))
                                oldFame = int(userInfo[2].replace(" ", "", 50).split(":")[1])
                                goodFame = fameVal
                                newFame = str(oldFame + goodFame)
                                inputSimpleText("#SetFamePoints " + newFame + " " + userSteamId)
                                rewardNameStr = rewardNameStr + str(fameVal) + "声望，"
                        except Exception:
                            pass

                        if "item" in signGiftObj:
                            if signGiftObj["item"] != "":
                                try:
                                    if signGiftObj["item"] != "":
                                        rewardCodes = signGiftObj["item"].split(",")
                                        for i in rewardCodes:
                                            for item in range(int(desedNumMuti)):
                                                inputSimpleText(i + " Location " + userSteamId)

                                        rewardNameStr = rewardNameStr + "许多物品装备，"
                                except Exception:
                                    pass

            if "customTitle" in signGiftObj and signGiftObj["customTitle"] != "":
                try:
                    if signGiftObj["customTitle"] != "":
                        cusTitle = signGiftObj["customTitle"]
                        currentNormalVipLevel = str(getUserNormalVipLevel(userSteamId))
                        currentVipLevel = str(getUserVipLevel(userSteamId))
                        updateUserData = {
                          'steam_id': userSteamId,
                          'vip_level': currentVipLevel,
                          'normal_vip_level': currentNormalVipLevel,
                          'custom_title': cusTitle}
                        updateDataToUser(updateUserData)
                        uperInfo = getUserInfoBySteamidFromTotal(userSteamId)
                        if uperInfo and len(uperInfo) > 0:
                            uperNameArr = uperInfo[0].split(". ")
                            uperNameArr.pop(0)
                            uperName = ". ".join(uperNameArr)
                            resetPlayerName(uperName, updateUserData, "custom")
                        else:
                            inputSimpleText("未找到玩家【" + userSteamId + "】的信息，玩家可能不在线，跳过本次任务")
                        rewardNameStr = rewardNameStr + "称号" + cusTitle + "，"
                except Exception:
                    pass

                inputSimpleText("玩家【" + userName + "】发起的【" + cardVal + "】成功回收数量为【" + str(desedNum) + "】，获得奖励【" + rewardNameStr + "】发放成功~~~")


def doFuben(val):
    printToLog("收到玩家副本请求")
    cardVal = val["inserStr"].split("&&&&&")[2].split(robotOptions["fubenMainKeyword"] + "/")[1]
    userName = val["inserStr"].split("&&&&&")[3]
    cardInfo = getFubenItem(cardVal)
    if cardInfo["havCove"] == False:
        inputSimpleText("未找到【" + userName + "】发起的【" + cardVal + "】副本挑战哦~请联系管理员添加副本~")
    else:
        cardInfo = cardInfo["coveItem"]
        userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
        if userInfo == False or len(userInfo) == 0:
            inputSimpleText("未找到玩家【" + userName + "】的信息，请尝试重新发送指令~")
            return False
        userSteamId = userInfo[1].split("(")[-1].split(")")[0]
        regUser(val["inserStr"].split("&&&&&")[3], userSteamId)
        userDataInfo = fatchUser(userSteamId)
        userBalance = 0
        ubType = "美金"
        if cardInfo["fbAmountType"] == "1":
            userBalance = userInfo[3].split("Account balance: ")[1]
        else:
            ubType = "熊币"
            userBalance = userDataInfo[0][3]
        oldData = ""
        with open((directory + "/fubenData.txt"), "r", encoding="UTF-8") as file:
            oldData = file.read()
        if oldData == "" or oldData == None:
            oldObj = {}
        else:
            stream = io.StringIO(oldData)
            oldObj = json.load(stream)
        if cardVal in oldObj:
            if oldObj[cardVal]["isDoing"] == 1:
                inputSimpleText("【" + userName + "】发起的【" + cardVal + "】副本挑战正在进行中哦~请等待上一名玩家结束挑战后再发起挑战~")
                return False
            if int(userBalance) < int(cardInfo["fbAmount"]):
                inputSimpleText("【" + userName + "】发起的【" + cardVal + "】副本挑战余额不足，该副本挑战价格为【" + cardInfo["fbAmount"] + "】" + ubType + "~")
                return False
        nowTimeStamp = int(datetime.timestamp(datetime.now()))
        if cardVal not in oldObj:
            isDoing = "0"
            fbTypeName = "多人本"
            if cardInfo["allowMutiPerson"] == "0":
                fbTypeName = "单人本"
                inputSimpleText("【" + userName + "】发起的【" + cardVal + "】副本挑战为【" + fbTypeName + "】，即将开始传送至活动区域，请做好准备，传送完成后一分钟开始发放副本装备，中途离开活动区域，将被判定为挑战失败~")
            else:
                inputSimpleText("【" + userName + "】发起的【" + cardVal + "】副本挑战为【" + fbTypeName + "】，即将开始传送至活动区域，其余参与副本台挑战的玩家请在一分钟内发出挑战指令参与副本挑战，第一名玩家传送完成后一分钟开始发放副本装备，并停止其他玩家参加挑战，中途离开活动区域，将被判定为挑战失败~")
            playerLoc = getUserLocation(userSteamId)
            if cardInfo["fbAmountType"] == "1":
                inputSimpleText("#ChangeCurrencyBalance Normal -" + str(cardInfo["fbAmount"]) + " " + userSteamId)
            else:
                reduceUserAmount(str(cardInfo["fbAmount"]), userSteamId, "0")
            playerLocItem = {'steamid':userSteamId, 
             'initLoc':playerLoc}
            fbItemObj = {'isDoing':isDoing, 
             'isMuti':cardInfo["allowMutiPerson"], 
             'players':[
              playerLocItem], 
             'location':cardInfo["location"], 
             'currentTime':nowTimeStamp, 
             'startTime':nowTimeStamp + 60, 
             'currentLevel':0, 
             'nextCheckTimeStr':(datetime.fromtimestamp(nowTimeStamp + 120).strftime)("%Y-%m-%d %H:%M:%S"), 
             'nextCheckTimestamp':nowTimeStamp + 120}
            oldObj[cardVal] = fbItemObj
            checkLeftZombiesNum(cardInfo["location"], cardInfo["radius"])
            if "beforeCode" in cardInfo:
                if cardInfo["beforeCode"] != "":
                    befCode = cardInfo["beforeCode"].split(",")
                    for item in befCode:
                        if "脸上" in item:
                            inputSimpleText(item.split("脸上")[0] + " " + userSteamId)
                        elif "传送 " in item:
                            inputSimpleText("#teleport " + item.split("传送 ")[1] + " " + userSteamId)
                        else:
                            inputSimpleText(item)

            if "beforeTime" in cardInfo and cardInfo["beforeTime"] != "":
                try:
                    slpTime = int(float(cardInfo["beforeTime"]))
                    time.sleep(slpTime)
                except Exception as e:
                    try:
                        pass
                    finally:
                        e = None
                        del e

                inputSimpleText("#teleport " + cardInfo["location"] + " " + userSteamId)
                with open((directory + "/fubenData.txt"), "w", encoding="UTF-8") as file:
                    file.write(json.dumps(oldObj, ensure_ascii=False))
        else:
            itemObj = oldObj[cardVal]
            if itemObj["isMuti"] == "0" and len(itemObj["players"]) > 0:
                inputSimpleText("【" + userName + "】发起的【" + cardVal + "】副本挑战为【单人本】，并且已有其他玩家在挑战中，请等待其他玩家完成挑战后再次发起台挑战~")
            elif itemObj["isMuti"] == "1" and nowTimeStamp < itemObj["startTime"]:
                playerLoc = getUserLocation(userSteamId)
                if cardInfo["fbAmountType"] == "1":
                    inputSimpleText("#ChangeCurrencyBalance Normal -" + str(cardInfo["fbAmount"]) + " " + userSteamId)
                else:
                    reduceUserAmount(str(cardInfo["fbAmount"]), userSteamId, "0")
                playerLocItem = {'steamid':userSteamId, 
                 'initLoc':playerLoc}
                oldObj[cardVal]["players"].append(playerLocItem)
                inputSimpleText("【" + userName + "】发起的【" + cardVal + "】副本挑战为【多人本】，即将开始传送至活动区域，其余参与副本台挑战的玩家请在一分钟内发出挑战指令参与副本挑战，第一名玩家传送完成后一分钟开始发放副本装备，并停止其他玩家参加挑战，中途离开活动区域，将被判定为挑战失败~")
                inputSimpleText("#teleport " + itemObj["location"] + " " + userSteamId)
                with open((directory + "/fubenData.txt"), "w", encoding="UTF-8") as file:
                    file.write(json.dumps(oldObj, ensure_ascii=False))
            elif itemObj["isMuti"] == "1":
                if nowTimeStamp >= itemObj["startTime"]:
                    inputSimpleText("【" + userName + "】发起的【" + cardVal + "】副本挑战为【多人本】，并且已有其他玩家在挑战中，请等待其他玩家完成挑战后再次发起台挑战~")


def calculate_distance(x1, y1, x2, y2):
    return int(math.sqrt((int(float(x2)) - int(float(x1))) ** 2 + (int(float(y2)) - int(float(y1))) ** 2) / 100)


def calPlayerToPlayerDist(playerLoc, centerLoc):
    curPlayerLoc = playerLoc
    curObj = curPlayerLoc.split(" ")
    cenObj = centerLoc.split(" ")
    curX = curObj[0]
    if "=" in curX:
        curX = curX.split("=")[1]
    curY = curObj[1]
    if "=" in curY:
        curY = curY.split("=")[1]
    cenX = cenObj[0]
    if "=" in cenX:
        cenX = cenX.split("=")[1]
    cenY = cenObj[1]
    if "=" in cenY:
        cenY = cenY.split("=")[1]
    return calculate_distance(curX, curY, cenX, cenY)


def getPlayerDisFubenDist(steamid, centerLoc):
    curPlayerLoc = getUserLocation(steamid)
    if curPlayerLoc == "no find player":
        return curPlayerLoc
    curObj = curPlayerLoc.split(" ")
    cenObj = centerLoc.split(" ")
    curX = curObj[0]
    if "=" in curX:
        curX = curX.split("=")[1]
    curY = curObj[1]
    if "=" in curY:
        curY = curY.split("=")[1]
    cenX = cenObj[0]
    if "=" in cenX:
        cenX = cenX.split("=")[1]
    cenY = cenObj[1]
    if "=" in cenY:
        cenY = cenY.split("=")[1]
    return calculate_distance(curX, curY, cenX, cenY)


def doCheckAllFuben():
    oldData = ""
    forOldObj = {}
    with open((directory + "/fubenData.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    if oldData == "" or oldData == None:
        oldObj = {}
    else:
        stream = io.StringIO(oldData)
        streamFor = io.StringIO(oldData)
        oldObj = json.load(stream)
        forOldObj = json.load(streamFor)
    nowTimeStamp = int(datetime.timestamp(datetime.now()))
    for item in forOldObj:
        fbItem = oldObj[item]
        cardInfoObj = getFubenItem(item)
        cardInfo = cardInfoObj["coveItem"]
        plIndex = 0
        plDelIndex = []
        for plItem in fbItem["players"]:
            curPDist = getPlayerDisFubenDist(plItem["steamid"], cardInfo["location"])
            printToLog(curPDist)
            if curPDist == "no find player":
                uperInfo = getUserInfoBySteamidFromTotal(plItem["steamid"])
                uperName = plItem["steamid"]
                if uperInfo:
                    if len(uperInfo) > 0:
                        uperNameArr = uperInfo[0].split(". ")
                        uperNameArr.pop(0)
                        uperName = ". ".join(uperNameArr)
                    inputSimpleText("玩家【" + uperName + "】已经离开了副本挑战区域，判定为挑战失败~")
                    plDelIndex.append(plIndex)
            if curPDist > int(cardInfo["radius"]):
                uperInfo = getUserInfoBySteamidFromTotal(plItem["steamid"])
                uperName = plItem["steamid"]
                if uperInfo:
                    if len(uperInfo) > 0:
                        uperNameArr = uperInfo[0].split(". ")
                        uperNameArr.pop(0)
                        uperName = ". ".join(uperNameArr)
                    inputSimpleText("玩家【" + uperName + "】已经离开了副本挑战区域，判定为挑战失败~")
                    plDelIndex.append(plIndex)
                plIndex = plIndex + 1

        for delItem in plDelIndex:
            del oldObj[item]["players"][delItem]

        if len(oldObj[item]["players"]) == 0:
            del oldObj[item]
            inputSimpleText("#Announce 【" + cardInfo["keyword"] + "】副本挑战失败，无人存活，副本已重置~")
        elif fbItem["isDoing"] == "0":
            if nowTimeStamp > fbItem["startTime"]:
                oldObj[item]["isDoing"] = "1"
                checkLeftZombiesNum(cardInfo["location"], cardInfo["radius"])
                inputSimpleText("【" + cardInfo["keyword"] + "】副本第1关即将开始~")
                doSendFBLevelRewards(oldObj[item], item)
        else:
            if fbItem["isDoing"] == "1":
                if nowTimeStamp > fbItem["nextCheckTimestamp"]:
                    leftZomNum = int(checkLeftZombiesNum(cardInfo["location"], cardInfo["radius"]))
                    if leftZomNum == 0:
                        if fbItem["currentLevel"] < len(cardInfo["levels"]) - 1:
                            oldObj[item]["currentLevel"] = oldObj[item]["currentLevel"] + 1
                            inputSimpleText("【" + cardInfo["keyword"] + "】副本第" + str(int(fbItem["currentLevel"]) + 1) + "关即将开始~")
                            doSendFBLevelRewards(oldObj[item], item)
                        else:
                            inputSimpleText("#Announce 【" + cardInfo["keyword"] + "】副本挑战成功！！即将传送玩家至参加挑战前的位置~")
                            for pitem in fbItem["players"]:
                                inputSimpleText("#teleport " + pitem["initLoc"] + " " + pitem["steamid"])

                            del oldObj[item]
                    elif leftZomNum > 10:
                        tenNum = int(int(leftZomNum) / 10)
                        oneNum = int(int(leftZomNum) % 10)
                        if tenNum > 0:
                            for ni in range(tenNum):
                                inputSimpleText('#spawnzombie BP_Zombie_Military_Armored 10 Location "' + cardInfo["location"] + '"')

                        if oneNum > 0:
                            inputSimpleText("#spawnzombie BP_Zombie_Military_Armored " + str(oneNum) + ' Location "' + cardInfo["location"] + '"')
                    else:
                        inputSimpleText("#spawnzombie BP_Zombie_Military_Armored " + str(leftZomNum) + ' Location "' + cardInfo["location"] + '"')

    with open((directory + "/fubenData.txt"), "w", encoding="UTF-8") as file:
        file.write(json.dumps(oldObj, ensure_ascii=False))


def checkLeftZombiesNum(loc, dist):
    inputSimpleText("#DestroyCorpsesWithinRadius " + dist + ' false "' + loc + '"')
    time.sleep(2)
    inputSimpleText("#DestroyZombiesWithinRadius " + dist + ' "' + loc + '"')
    desedNum = getLastDestoryZombieNum()
    return desedNum


def getLastDestoryZombieNum():
    time.sleep(2)
    localappdata = os.getenv("LOCALAPPDATA")
    f = open((localappdata + "/SCUM/Saved/Logs/SCUM.log"), encoding="utf-8")
    cont = f.read()
    f.close()
    contList = cont.split("\n")
    desItemArr = []
    for i in contList:
        if i.find("LogSCUM: Sender player state null for message ") != -1:
            if i.find("zombies destroyed!") != -1:
                desItemArr.append(i)

    lastItem = desItemArr[-1]
    lastTime = lastItem.split("]")[0].split("[")[1].split(":")[0]
    lastDesedNum = lastItem.split(" zombies destroyed!")[0].split(" ")[-1]
    return lastDesedNum


def doSendFBLevelRewards(fbItem, name):
    try:
        cardInfoObj = getFubenItem(name)
        cardInfo = cardInfoObj["coveItem"]
        levelItem = cardInfo["levels"][fbItem["currentLevel"]]
        if "userGoods" in levelItem:
            if levelItem["userGoods"] != "":
                goods = levelItem["userGoods"].split(",")
                inputSimpleText("【" + name + "】副本第" + str(int(fbItem["currentLevel"]) + 1) + "关玩家装备开始发放~")
                for item in fbItem["players"]:
                    for gitem in goods:
                        if gitem[0] == "#":
                            inputSimpleText(gitem + " Location " + item["steamid"])
                        else:
                            inputSimpleText(gitem)

            if "userAmount" in levelItem and levelItem["userAmount"] != "":
                if levelItem["userAmount"] != "0":
                    inputSimpleText("【" + name + "】副本第" + str(int(fbItem["currentLevel"]) + 1) + "关玩家美金奖励" + levelItem["userAmount"] + "开始发放~")
                    for item in fbItem["players"]:
                        inputSimpleText("#ChangeCurrencyBalance Normal " + levelItem["userAmount"] + " " + item["steamid"])

                if "userGold" in levelItem and levelItem["userGold"] != "":
                    if levelItem["userGold"] != "0":
                        inputSimpleText("【" + name + "】副本第" + str(int(fbItem["currentLevel"]) + 1) + "关玩家金条奖励" + levelItem["userGold"] + "开始发放~")
                        for item in fbItem["players"]:
                            inputSimpleText("#ChangeCurrencyBalance Gold " + levelItem["userGold"] + " " + item["steamid"])

                    if "userFame" in levelItem and levelItem["userFame"] != "":
                        if levelItem["userFame"] != "0":
                            inputSimpleText("【" + name + "】副本第" + str(int(fbItem["currentLevel"]) + 1) + "关玩家声望奖励" + levelItem["userFame"] + "开始发放~")
                            for item in fbItem["players"]:
                                uperInfo = getUserInfoBySteamidFromTotal(item["steamid"])
                                uperName = ""
                                if uperInfo:
                                    if len(uperInfo) > 0:
                                        oldFame = int(uperInfo[2].replace(" ", "", 50).split(":")[1])
                                        goodFame = int(levelItem["userFame"])
                                        newFame = str(oldFame + goodFame)
                                        inputSimpleText("#SetFamePoints " + newFame + " " + item["steamid"])

                        if "userXiongB" in levelItem and levelItem["userXiongB"] != "":
                            if levelItem["userXiongB"] != "0":
                                inputSimpleText("【" + name + "】副本第" + str(int(fbItem["currentLevel"]) + 1) + "关玩家熊币奖励" + levelItem["userXiongB"] + "开始发放~")
                                for item in fbItem["players"]:
                                    userDataInfo = fatchUser(item["steamid"])
                                    preAmount = userDataInfo[0][3]
                                    newAmount = int(preAmount) + int(levelItem["userXiongB"])
                                    updateUserData = {'steam_id':item["steamid"], 
                                     'amount':newAmount}
                                    updateDataToUser(updateUserData)

                            if "userNormalInt" in levelItem and levelItem["userNormalInt"] != "":
                                if levelItem["userNormalInt"] != "0":
                                    inputSimpleText("【" + name + "】副本第" + str(int(fbItem["currentLevel"]) + 1) + "关玩家称号积分奖励" + levelItem["userNormalInt"] + "开始发放~")
                                    for item in fbItem["players"]:
                                        updateUserNormalInt(0, item["steamid"], levelItem["userNormalInt"])

                                if "userVipInt" in levelItem and levelItem["userVipInt"] != "":
                                    if levelItem["userVipInt"] != "0":
                                        inputSimpleText("【" + name + "】副本第" + str(int(fbItem["currentLevel"]) + 1) + "关玩家VIP积分奖励" + levelItem["userVipInt"] + "开始发放~")
                                        for item in fbItem["players"]:
                                            upData = {'steam_id':item["steamid"],  'integral':getUserJifen(item["steamid"])}
                                            upData["integral"] = str(int(upData["integral"]) + int(levelItem["userVipInt"]))
                                            updateDataToUser(upData)

                                    if "levelCode" in levelItem:
                                        if levelItem["levelCode"] != "":
                                            inputSimpleText("【" + name + "】副本第" + str(int(fbItem["currentLevel"]) + 1) + "关守关者们开始出场~~")
                                            goods = levelItem["levelCode"].split(",")
                                            for item in fbItem["players"]:
                                                for gitem in goods:
                                                    if "脸上" in gitem:
                                                        inputSimpleText(gitem.split("脸上")[0] + " " + item["steamid"])
                                                    else:
                                                        inputSimpleText(gitem)

    except Exception as e:
        try:
            printToLog("副本数据读取错误，请检查")
            inputSimpleText("副本数据读取错误，请联系管理员检查")
            printToLog(e)
        finally:
            e = None
            del e


def getFubenItem(name):
    coveItem = {}
    havCove = False
    if "fubenObjs" in robotOptions:
        if len(robotOptions["fubenObjs"]) > 0:
            for item in robotOptions["fubenObjs"]:
                if item["keyword"] == name:
                    coveItem = item
                    havCove = True

        return {'havCove':havCove, 
         'coveItem':coveItem}


def doTiKa(val):
    printToLog("收到玩家提卡请求")
    cardVal = val["inserStr"].split("&&&&&")[2].split("@提卡/")[1]
    cardInfo = getGiftCardDataByCardValue(cardVal)
    cardData = None
    userName = val["inserStr"].split("&&&&&")[3]
    cardId = 0
    try:
        if cardInfo != None:
            if len(cardInfo) == 1:
                if cardInfo[0][8] != "0":
                    if "language" in robotOptions and robotOptions["language"] == 1:
                        inputSimpleText("【" + userName + "】input card password has expired")
                    else:
                        inputSimpleText("【" + userName + "】输入的卡密已失效")
                    return False
                cardData = cardInfo[0]
                cardId = cardInfo[0][0]
        if cardData != None:
            userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
            if userInfo == False or len(userInfo) == 0:
                inputSimpleText("未找到玩家【" + userName + "】的信息，请尝试重新发送指令~")
                return False
            userSteamId = userInfo[1].split("(")[-1].split(")")[0]
            regUser(val["inserStr"].split("&&&&&")[3], userSteamId)
            userDataInfo = fatchUser(userSteamId)
            if "language" in robotOptions and robotOptions["language"] == 1:
                inputSimpleText("【" + userName + "】, Your gift is about to start shipping~")
            else:
                inputSimpleText("【" + userName + "】的礼品即将开始发货~")
            try:
                if cardData[4] != "0":
                    goldVal = str(int(float(cardData[4])))
                    inputSimpleText("#ChangeCurrencyBalance gold " + goldVal + " " + userSteamId)
            except Exception:
                pass

            try:
                if cardData[5] != "0":
                    normalVal = str(int(float(cardData[5])))
                    inputSimpleText("#ChangeCurrencyBalance Normal " + normalVal + " " + userSteamId)
            except Exception:
                pass

            try:
                if cardData[6] != "0":
                    oldFame = int(userInfo[2].replace(" ", "", 50).split(":")[1])
                    goodFame = int(int(float(cardData[6])))
                    newFame = str(oldFame + goodFame)
                    inputSimpleText("#SetFamePoints " + newFame + " " + userSteamId)
            except Exception:
                pass

            try:
                if cardData[7] != "0":
                    preAmount = userDataInfo[0][3]
                    newAmount = int(preAmount) + int(int(float(cardData[7])))
                    updateUserData = {'steam_id':userSteamId, 
                     'amount':newAmount}
                    updateDataToUser(updateUserData)
            except Exception:
                pass

            try:
                if cardData[3] != "":
                    rewardCodes = cardData[3].split(",")
                    for i in rewardCodes:
                        inputSimpleText(i + " Location " + userSteamId)

            except Exception:
                pass

            try:
                if cardData[13] != "":
                    if cardData[13] != "0":
                        cmdArr = [
                         "", userSteamId, cardData[13]]
                        givePlayerAdmin(cmdArr)
            except Exception:
                pass

            datatableConnectLocal = sqlite3.connect("beijixiong.db")
            cursor = datatableConnectLocal.cursor()
            currentTime = str(datetime.now()).split(".")[0]
            cursor.execute("UPDATE card_list SET card_state = ?, send_time = ?, player_steamid = ?, player_name = ? WHERE card_id = ?", ("1", currentTime, userSteamId, userName, cardId))
            datatableConnectLocal.commit()
            cursor.close()
            datatableConnectLocal.close()
            if "language" in robotOptions and robotOptions["language"] == 1:
                inputSimpleText("【" + userName + "】, Your gift has been shipped and completed~")
            else:
                inputSimpleText("【" + userName + "】的礼品已完成发货~")
        else:
            inputSimpleText("【" + userName + "】输入的卡密有误")
    except Exception:
        inputSimpleText("【" + userName + "】输入的卡密有误")


def doMainPlayerSendHb(val):
    printToLog("收到玩家发红包请求")
    with open((directory + "/RedHBData.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    stream = io.StringIO(oldData)
    oldObj = json.load(stream)
    try:
        if oldObj["isOpen"] == "1":
            inputSimpleText("南极熊红包服务提示：当前还有未抢完的红包，请抢完之后再发哦~")
        else:
            cmdArrs = val.split("&&&&&")[2].split("/")
            if len(cmdArrs) != 3:
                inputSimpleText("南极熊红包服务提示：您的命令格式有误，请检查后重试~")
            else:
                userInfo = getUserInfoByNameFromTotal(val.split("&&&&&")[3], val.split("&&&&&")[2])
                userName = val.split("&&&&&")[3]
                userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                userBalance = userInfo[3].split("Account balance: ")[1]
                userOutName = "【" + val.split("&&&&&")[3] + "】"
                if userInfo == False or len(userInfo) == 0:
                    inputSimpleText("未找到玩家【" + userName + "】的信息，请尝试重新发送指令~")
                    return False
                regUser(val.split("&&&&&")[3], userSteamId)
                userDataInfo = fatchUser(userSteamId)
                amount = int(cmdArrs[1])
                hbNum = int(cmdArrs[2])
                qhbMinAmount = "0"
                if "qhbMinAmount" in robotOptions:
                    if robotOptions["qhbMinAmount"] != "":
                        qhbMinAmount = robotOptions["qhbMinAmount"]
                    qhbMaxNumber = "20"
                    if "qhbMaxNumber" in robotOptions:
                        if robotOptions["qhbMaxNumber"] != "":
                            qhbMaxNumber = robotOptions["qhbMaxNumber"]
                if int(userBalance) < amount:
                    inputSimpleText("南极熊红包服务提示：玩家" + userOutName + "发红包的金额大于自己钱包余额，无法发出红包哦~")
                elif amount < int(qhbMinAmount):
                    inputSimpleText("南极熊红包服务提示：玩家" + userOutName + "发红包的金额小于最低限额，无法发出红包哦~")
                elif hbNum > int(qhbMaxNumber):
                    inputSimpleText("南极熊红包服务提示：玩家" + userOutName + "发红包的数量大于最大限额，无法发出红包哦~")
                else:
                    maxAmount = int(random.uniform(1, amount / 2))
                    minAmount = 1
                    hbArrVals = [maxAmount]
                    leftAmount = amount - maxAmount
                    while len(hbArrVals) < hbNum:
                        curAmount = int(random.uniform(minAmount, leftAmount / 2))
                        leftAmount = leftAmount - curAmount
                        hbArrVals.append(curAmount)

                    if leftAmount > 0:
                        hbArrVals[-1] = hbArrVals[-1] + leftAmount
                    random.shuffle(hbArrVals)
                    maxTime = "30"
                    if "qhbMaxTime" in robotOptions:
                        if robotOptions["qhbMaxTime"] != "":
                            maxTime = robotOptions["qhbMaxTime"]
                        endTimeVal = datetime.fromtimestamp(datetime.timestamp(datetime.now()) + int(maxTime) * 60).strftime("%Y-%m-%d %H:%M:%S")
                        newObj = {'totalAmount':str(amount), 
                         'leftAmount':str(amount), 
                         'sendUser':userSteamId, 
                         'sendUserName':userName, 
                         'hbNum':str(hbNum), 
                         'isOpen':"1", 
                         'geted':[],  'getedIds':[],  'redHbAms':hbArrVals, 
                         'endTime':endTimeVal}
                        inputSimpleText("#ChangeCurrencyBalance Normal -" + str(amount) + " " + userSteamId)
                        with open((directory + "/RedHBData.txt"), "w", encoding="UTF-8") as f:
                            f.write(json.dumps(newObj, ensure_ascii=False))
                        inputSimpleText("感谢玩家" + userOutName + "发出的【" + str(hbNum) + "】个大红包，总金额为【" + str(amount) + "】美金！！！快发送【" + robotOptions["qhbJoinPlayerKeyword"] + "】指令开始抢红包吧~")
                        inputSimpleText("#Announce 感谢玩家" + userOutName + "发出的【" + str(hbNum) + "】个大红包，总金额为【" + str(amount) + "】美金！！！快发送【" + robotOptions["qhbJoinPlayerKeyword"] + "】指令开始抢红包吧~")
    except Exception as e:
        try:
            printToLog("错误发生行号：" + traceback.format_exc())
            printToLog("获取数据出错，机器人重启中，如长时间未能恢复，请联系管理员协助解决")
            logging.error(str(datetime.now()))
            logging.error(traceback.format_exc())
            inputSimpleText("南极熊红包服务提示：您的命令格式有误，请检查后重试~")
        finally:
            e = None
            del e


def resetHBData():
    hbObj = {'totalAmount':"0", 
     'leftAmount':"0", 
     'sendUser':"", 
     'sendUserName':"", 
     'hbNum':"0", 
     'isOpen':"0", 
     'geted':[],  'getedIds':[],  'redHbAms':[],  'endTime':""}
    with open((directory + "/RedHBData.txt"), "w", encoding="UTF-8") as f:
        f.write(json.dumps(hbObj, ensure_ascii=False))


def doCleanLaJi():
    if "cleanLaJiCode" in robotOptions:
        if robotOptions["cleanLaJiCode"] != "":
            inputSimpleText("正在清理垃圾中....")
            codeArr = robotOptions["cleanLaJiCode"].split(",")
            for i in codeArr:
                inputSimpleText(i)

            inputSimpleText("清理垃圾完成....")


def checkHBIsNeedReset():
    with open((directory + "/RedHBData.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    stream = io.StringIO(oldData)
    oldObj = json.load(stream)
    if "endTime" in oldObj:
        if oldObj["endTime"] != "":
            currentTimeStamp = datetime.timestamp(datetime.now())
            itemEndtamp = datetime.timestamp(datetime.strptime(oldObj["endTime"], "%Y-%m-%d %H:%M:%S"))
            if currentTimeStamp > itemEndtamp:
                inputSimpleText("#ChangeCurrencyBalance Normal " + str(oldObj["leftAmount"]) + " " + oldObj["sendUser"])
                inputSimpleText("玩家" + oldObj["sendUserName"] + "发出的红包超出最大时间，已退还至发红包人账户，红包金额剩余【" + str(oldObj["leftAmount"]) + "】~~")
                resetHBData()


def doJoinPlayerGetHB(val):
    printToLog("收到玩家抢红包请求")
    with open((directory + "/RedHBData.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    stream = io.StringIO(oldData)
    oldObj = json.load(stream)
    try:
        if oldObj["isOpen"] == "0":
            inputSimpleText("南极熊红包服务提示：当前没有玩家发出的红包可以抢哦~")
        else:
            userInfo = getUserInfoByNameFromTotal(val.split("&&&&&")[3], val.split("&&&&&")[2])
            userName = val.split("&&&&&")[3]
            userSteamId = userInfo[1].split("(")[-1].split(")")[0]
            userOutName = "【" + val.split("&&&&&")[3] + "】"
            if userInfo == False or len(userInfo) == 0:
                inputSimpleText("未找到玩家【" + userName + "】的信息，请尝试重新发送指令~")
                return False
            regUser(val.split("&&&&&")[3], userSteamId)
            userDataInfo = fatchUser(userSteamId)
            if userSteamId in oldObj["getedIds"]:
                inputSimpleText("玩家" + userOutName + "已抢过此红包，不能重复抢哦~~")
            else:
                curGetIndex = len(oldObj["geted"])
                curGetVal = oldObj["redHbAms"][curGetIndex]
                oldObj["geted"].append(userName)
                oldObj["getedIds"].append(userSteamId)
                inputSimpleText("#ChangeCurrencyBalance Normal " + str(curGetVal) + " " + userSteamId)
                inputSimpleText("恭喜玩家" + userOutName + "成功抢到红包，红包金额【" + str(curGetVal) + "】！！！")
                if len(oldObj["geted"]) == int(oldObj["hbNum"]):
                    oldObj["isOpen"] = "0"
                    oldObj["leftAmount"] = "0"
                    maxIndex = oldObj["redHbAms"].index(max(oldObj["redHbAms"]))
                    inputSimpleText("玩家" + oldObj["sendUserName"] + "发出的总金额为【" + str(oldObj["totalAmount"]) + "】美金的【" + str(oldObj["hbNum"]) + "】个大红包已被抢完，玩家【" + oldObj["geted"][maxIndex] + "】手气最佳，获得最大金额【" + str(oldObj["redHbAms"][maxIndex]) + "】~~")
                    resetHBData()
                else:
                    oldObj["leftAmount"] = str(int(oldObj["leftAmount"]) - curGetVal)
                    inputSimpleText("玩家" + oldObj["sendUserName"] + "发出的红包剩余【" + str(int(oldObj["hbNum"]) - len(oldObj["geted"])) + "】个，红包金额剩余【" + str(oldObj["leftAmount"]) + "】~~")
                    with open((directory + "/RedHBData.txt"), "w", encoding="UTF-8") as f:
                        f.write(json.dumps(oldObj, ensure_ascii=False))
    except Exception as e:
        try:
            printToLog("错误发生行号：" + traceback.format_exc())
            printToLog("获取数据出错，机器人重启中，如长时间未能恢复，请联系管理员协助解决")
            logging.error(str(datetime.now()))
            logging.error(traceback.format_exc())
            inputSimpleText("南极熊红包服务提示：红包数据有误，请联系管理员检查后重试~")
        finally:
            e = None
            del e


def doLHDUser(val, mutiType=0):
    printToLog("收到龙虎斗玩家请求")
    isOnlyAdmin = 0
    if "isOnlyAdmin" in totalRobotOptions["longhudou"]:
        isOnlyAdmin = totalRobotOptions["longhudou"]["isOnlyAdmin"]
    with open((directory + "/LHDData.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    stream = io.StringIO(oldData)
    oldObj = json.load(stream)
    initAmount = "0"
    initAmountVal = "0"
    if isOnlyAdmin == 1:
        if oldObj["isOpen"] == "0":
            inputSimpleText("当前活动仅可由管理员开启，请联系管理员开启活动")
            ui.press("enter")
            return False
        try:
            if "initAmount" in totalRobotOptions["longhudou"]:
                initAmountVal = int(totalRobotOptions["longhudou"]["initAmount"])
                initAmountVal = initAmountVal
                initAmount = totalRobotOptions["longhudou"]["initAmount"]
        except:
            initAmount = "0"

        if oldObj["isOpen"] == "0":
            oldObj["isOpen"] = "1"
            oldObj["currentTotoalAmount"] = initAmount
            with open((directory + "/LHDData.txt"), "w", encoding="UTF-8") as f:
                f.write(json.dumps(oldObj, ensure_ascii=False))
        userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
        userName = val["inserStr"].split("&&&&&")[3]
        if userInfo == False or len(userInfo) == 0:
            inputSimpleText("未找到玩家【" + userName + "】的信息，请尝试重新发送指令~")
            return False
        userSteamId = userInfo[1].split("(")[-1].split(")")[0]
        userBalance = userInfo[3].split("Account balance: ")[1]
        userOutName = "【" + val["inserStr"].split("&&&&&")[3] + "】"
        regUser(val["inserStr"].split("&&&&&")[3], userSteamId)
        userDataInfo = fatchUser(userSteamId)
        useXiongb = False
        if "longhudou" in totalRobotOptions and "amountType" in totalRobotOptions["longhudou"]:
            if totalRobotOptions["longhudou"]["amountType"] == 1:
                userBalance = userDataInfo[0][3]
                useXiongb = True
            vipIsOnline = checkUserVipIsOnline(userSteamId)
            if userDataInfo[0][7] != "0":
                if vipIsOnline == True:
                    userOutName = "尊贵的【" + val["inserStr"].split("&&&&&")[3] + "】"
            lhdReduceAmount = totalRobotOptions["longhudou"]["amount"]
            mutiTime = 1
            if mutiType == 1:
                if "JCLHDMutiTime" in robotOptions:
                    if robotOptions["JCLHDMutiTime"] != "":
                        mutiTime = int(robotOptions["JCLHDMutiTime"])
                lhdReduceAmount = int(lhdReduceAmount) * mutiTime
    if int(userBalance) < int(lhdReduceAmount):
        if useXiongb == True:
            inputSimpleText(userOutName + totalRobotOptions["longhudou"]["activeName"] + "南极熊币余额不足")
        else:
            inputSimpleText(userOutName + totalRobotOptions["longhudou"]["activeName"] + "余额不足")
    else:
        goodIntRatio = 1
        if useXiongb == True:
            try:
                if "inteJCLhdVip" in totalRobotOptions["options"]:
                    goodIntRatio = float(totalRobotOptions["options"]["inteJCLhdVip"])
            except Exception:
                goodIntRatio = 1

            reduceUserAmount(str(lhdReduceAmount), userSteamId, str(int(float(lhdReduceAmount) * goodIntRatio)))
        else:
            try:
                if "inteJCLhdNormal" in totalRobotOptions["options"]:
                    goodIntRatio = float(totalRobotOptions["options"]["inteJCLhdNormal"])
            except Exception:
                goodIntRatio = 1

            inputSimpleText("#ChangeCurrencyBalance Normal -" + str(lhdReduceAmount) + " " + userSteamId)
            updateUserNormalInt(str(lhdReduceAmount), userSteamId, str(int(float(lhdReduceAmount) * goodIntRatio)))
        lhdResult = []
        for i in range(int(totalRobotOptions["longhudou"]["resultLen"])):
            lhdResult.append("")

        wordArr = [
         totalRobotOptions["longhudou"]["word1"], totalRobotOptions["longhudou"]["word2"]]
        if mutiType == 1:
            mutiResult = []
            for k in range(mutiTime):
                lhdResult = []
                diff = False
                for m in range(int(totalRobotOptions["longhudou"]["resultLen"])):
                    lhdResult.append("")

                for i in range(len(lhdResult)):
                    rd = random.randint(0, 1)
                    lhdResult[int(i)] = wordArr[rd]
                    if int(i) > 0:
                        if lhdResult[int(i)] != lhdResult[int(i) - 1]:
                            diff = True

                mutiResult.append(diff)

            rewardNames = []
            totalWinResult = False
            for mu in mutiResult:
                if mu == True:
                    if totalRobotOptions["longhudou"]["isOpenMin"] == "1":
                        rewardKeys = []
                        rewardVals = []
                        rewardList = lotteryObjs["jiangpin"]
                        for i in rewardList:
                            rewardKeys.append(rewardList[i]["name"])
                            rewardVals.append(rewardList[i]["gailv"])

                        result = random.choices(rewardKeys, rewardVals)[0]
                        resultObj = rewardList[result]
                        rewardCodes = resultObj["code"].split(",")
                        for i in rewardCodes:
                            inputSimpleText(i + " Location " + userSteamId)

                        rewardNames.append(result)
                else:
                    totalWinResult = True

            oldObj["currentTotoalAmount"] = str(int(oldObj["currentTotoalAmount"]) + int(totalRobotOptions["longhudou"]["amountStep"]) * int(mutiTime))
            if totalWinResult == True:
                if totalRobotOptions["longhudou"]["isOpenMin"] == "1":
                    inputSimpleText(userOutName + "获得奖品【" + "、".join(rewardNames) + "】，并获得奖池内【" + oldObj["currentTotoalAmount"] + "】全部奖励，清空奖池，奖励已发放至您的账户余额内！！！")
                    if "isOpenRedInfo" in totalRobotOptions["longhudou"] and totalRobotOptions["longhudou"]["isOpenRedInfo"] == 1:
                        inputSimpleText("#Announce 恭喜玩家【" + userOutName + "获得奖品【" + "、".join(rewardNames) + "】，并获得奖池内【" + oldObj["currentTotoalAmount"] + "】全部奖励，清空奖池，奖励已发放至您的账户余额内！！！")
                else:
                    inputSimpleText(userOutName + "获得奖池内【" + oldObj["currentTotoalAmount"] + "】全部奖励，清空奖池，奖励已发放至您的账户余额内！！！")
                    if "isOpenRedInfo" in totalRobotOptions["longhudou"]:
                        if totalRobotOptions["longhudou"]["isOpenRedInfo"] == 1:
                            inputSimpleText("#Announce 恭喜玩家" + userOutName + "获得奖池内【" + oldObj["currentTotoalAmount"] + "】全部奖励，清空奖池，奖励已发放至您的账户余额内！！！")
                inputSimpleText("#ChangeCurrencyBalance Normal " + str(oldObj["currentTotoalAmount"]) + " " + userSteamId)
                oldObj["isOpen"] = "0"
                oldObj["currentTotoalAmount"] = initAmount
                with open((directory + "/LHDData.txt"), "w", encoding="UTF-8") as f:
                    f.write(json.dumps(oldObj, ensure_ascii=False))
            else:
                if totalRobotOptions["longhudou"]["isOpenMin"] == "1":
                    inputSimpleText(userOutName + "获得奖品【" + "、".join(rewardNames) + "】，未获得奖池内奖金，当前奖池内累计【" + oldObj["currentTotoalAmount"] + "】，下次继续努力~~")
                else:
                    inputSimpleText(userOutName + "未获得奖池内奖金，当前奖池内累计【" + oldObj["currentTotoalAmount"] + "】，下次继续努力~~")
                with open((directory + "/LHDData.txt"), "w", encoding="UTF-8") as f:
                    f.write(json.dumps(oldObj, ensure_ascii=False))
        else:
            diff = False
            for i in range(len(lhdResult)):
                rd = random.randint(0, 1)
                lhdResult[int(i)] = wordArr[rd]
                if int(i) > 0:
                    if lhdResult[int(i)] != lhdResult[int(i) - 1]:
                        diff = True

            oldObj["currentTotoalAmount"] = str(int(oldObj["currentTotoalAmount"]) + int(totalRobotOptions["longhudou"]["amountStep"]))
            if diff == True:
                if totalRobotOptions["longhudou"]["isOpenMin"] == "1":
                    rewardKeys = []
                    rewardVals = []
                    rewardList = lotteryObjs["jiangpin"]
                    for i in rewardList:
                        rewardKeys.append(rewardList[i]["name"])
                        rewardVals.append(rewardList[i]["gailv"])

                    result = random.choices(rewardKeys, rewardVals)[0]
                    resultObj = rewardList[result]
                    rewardCodes = resultObj["code"].split(",")
                    for i in rewardCodes:
                        inputSimpleText(i + " Location " + userSteamId)

                    if "JCLHDShowFlag" in robotOptions and robotOptions["JCLHDShowFlag"] == "0":
                        inputSimpleText(userOutName + "获得奖品【" + result + "】，未获得奖池内奖金，当前奖池内累计【" + oldObj["currentTotoalAmount"] + "】，下次继续努力~~")
                    else:
                        strOut = userOutName + "的【"
                        strOut = strOut + totalRobotOptions["longhudou"]["activeName"] + "】结果为：【 " + "，".join(lhdResult) + "】"
                        strOut = strOut + "，未赢得胜利，本次保底奖励为【" + result + "】，当前奖池累计【" + oldObj["currentTotoalAmount"] + "】"
                        inputSimpleText(strOut)
                        inputSimpleText(userOutName + "的保底奖励发货成功，请注意查收")
                elif "JCLHDShowFlag" in robotOptions and robotOptions["JCLHDShowFlag"] == "0":
                    inputSimpleText(userOutName + "未获得奖池内奖金，当前奖池内累计【" + oldObj["currentTotoalAmount"] + "】，下次继续努力~~")
                else:
                    strOut = userOutName + "的【"
                    strOut = strOut + totalRobotOptions["longhudou"]["activeName"] + "】结果为：【 " + "，".join(lhdResult) + "】"
                    strOut = strOut + "，未赢得胜利，当前奖池累计【" + oldObj["currentTotoalAmount"] + "】"
                    inputSimpleText(strOut)
            elif "JCLHDShowFlag" in robotOptions and robotOptions["JCLHDShowFlag"] == "0":
                inputSimpleText("恭喜玩家" + userOutName + "获得奖池内【" + oldObj["currentTotoalAmount"] + "】全部奖励，清空奖池，奖励已发放至您的账户余额内！！！")
                if "isOpenRedInfo" in totalRobotOptions["longhudou"]:
                    if totalRobotOptions["longhudou"]["isOpenRedInfo"] == 1:
                        inputSimpleText("#Announce 恭喜玩家" + userOutName + "获得奖池内【" + oldObj["currentTotoalAmount"] + "】全部奖励，清空奖池，奖励已发放至您的账户余额内！！！")
                inputSimpleText("#ChangeCurrencyBalance Normal " + str(oldObj["currentTotoalAmount"]) + " " + userSteamId)
                oldObj["isOpen"] = "0"
                oldObj["currentTotoalAmount"] = initAmount
            else:
                strOut = userOutName + "的【"
                strOut = strOut + totalRobotOptions["longhudou"]["activeName"] + "】结果为：【 " + "，".join(lhdResult) + "】"
                strOut = strOut + "，获得本次胜利，获得奖池【" + oldObj["currentTotoalAmount"] + "】全部奖励"
                inputSimpleText(strOut)
                if "isOpenRedInfo" in totalRobotOptions["longhudou"]:
                    if totalRobotOptions["longhudou"]["isOpenRedInfo"] == 1:
                        inputSimpleText("#Announce 恭喜玩家【" + userOutName + "】获得本次【" + totalRobotOptions["longhudou"]["activeName"] + "】胜利，获得奖池内【" + oldObj["currentTotoalAmount"] + "】全部奖励")
                    inputSimpleText("#ChangeCurrencyBalance Normal " + str(oldObj["currentTotoalAmount"]) + " " + userSteamId)
                    inputSimpleText(userOutName + "的奖励发货成功，请注意查收")
                    endInfo = "本次【" + totalRobotOptions["longhudou"]["activeName"] + "】活动已结束"
                    if "endTip" in totalRobotOptions["longhudou"]:
                        if totalRobotOptions["longhudou"]["endTip"] != "":
                            endInfo = endInfo + "，" + totalRobotOptions["longhudou"]["endTip"]
                    inputSimpleText(endInfo)
                    oldObj["isOpen"] = "0"
                    oldObj["currentTotoalAmount"] = initAmount
            with open((directory + "/LHDData.txt"), "w", encoding="UTF-8") as f:
                f.write(json.dumps(oldObj, ensure_ascii=False))


def adminResetUserKeyword(obj):
    playerSteamid = obj["steamid"]
    keyword = obj["keyword"]
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    data = {'code':0, 
     'message':""}
    try:
        cursor.execute("DELETE FROM sended_gift WHERE steamid = ? AND keyword = ?", (playerSteamid, keyword))
        datatableConnectLocal.commit()
        data["code"] = 0
        data["message"] = "删除成功"
        cursor.close()
        datatableConnectLocal.close()
        return data
    except Exception as e:
        try:
            data["code"] = 1000
            data["message"] = "删除失败"
            cursor.close()
            datatableConnectLocal.close()
            return data
        finally:
            e = None
            del e


def timeCheckWaitTransData():
    try:
        oldData = ""
        oldObj = []
        with open((directory + "/waitTrans.txt"), "r", encoding="UTF-8") as file:
            oldData = file.read()
        if oldData == "" or oldData == None:
            oldObj = []
        else:
            stream = io.StringIO(oldData)
            oldObj = json.load(stream)
        newList = []
        for item in oldObj:
            endInsurTime = int(datetime.strptime(str(item["endTime"]), "%Y-%m-%d %H:%M:%S").timestamp())
            nowTime = datetime.timestamp(datetime.now())
            if nowTime < endInsurTime:
                newList.append(item)
            with open((directory + "/waitTrans.txt"), "w", encoding="UTF-8") as f:
                f.write(json.dumps(newList, ensure_ascii=False))

    except Exception as e:
        try:
            with open((directory + "/waitTrans.txt"), "w", encoding="UTF-8") as f:
                f.write(json.dumps([], ensure_ascii=False))
            inputSimpleText("南极熊机器人提示：待传送人员名单格式错误，已全部重置，请重新发起传送！")
        finally:
            e = None
            del e


def agreeNotSquadPlayerTrans(val):
    userName = val["inserStr"].split("&&&&&")[3]
    userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
    if userInfo == False or len(userInfo) == 0:
        inputSimpleText("未找到玩家【" + userName + "】的信息，请尝试重新发送指令~")
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    oldData = ""
    with open((directory + "/waitTrans.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    if oldData == "" or oldData == None:
        oldObj = []
    else:
        stream = io.StringIO(oldData)
        oldObj = json.load(stream)
    newList = []
    for item in oldObj:
        if item["toId"] == userSteamId:
            diffAmount = 0
            useXiongb = False
            if "squardTransAmountType" in robotOptions:
                if robotOptions["squardTransAmountType"] == "1":
                    useXiongb = True
                if useXiongb == True:
                    reduceUserAmount(str(diffAmount), item["requestId"], str(0))
                else:
                    inputSimpleText("#ChangeCurrencyBalance Normal -" + str(diffAmount) + " " + item["requestId"])
                inputSimpleText("#TeleportTo " + item["toId"] + " " + item["requestId"])
                inputSimpleText("【" + userName + "】的非队友传送请求已执行~")
            newList.append(item)

    with open((directory + "/waitTrans.txt"), "w", encoding="UTF-8") as f:
        f.write(json.dumps(newList, ensure_ascii=False))


def requestSquardPlayerTrans(val):
    printToLog("收到玩家队友传送请求")
    targetPlayerSteamid = val["inserStr"].split("&&&&&")[2].split(robotOptions["requestSquardTransKeyword"] + "/")[1]
    if targetPlayerSteamid != "":
        diffAmount = 0
        useXiongb = False
        if "squardTransAmountType" in robotOptions:
            if robotOptions["squardTransAmountType"] == "1":
                useXiongb = True
            try:
                if "squardTransAmount" in robotOptions:
                    if robotOptions["squardTransAmount"] != "":
                        diffAmount = int(robotOptions["squardTransAmount"])
            except Exception as e:
                try:
                    diffAmount = 0
                finally:
                    e = None
                    del e

            userName = val["inserStr"].split("&&&&&")[3]
            userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
            if userInfo == False or len(userInfo) == 0:
                inputSimpleText("未找到玩家【" + userName + "】的信息，请尝试重新发送指令~")
                return False
            userSteamId = userInfo[1].split("(")[-1].split(")")[0]
            userBalance = userInfo[3].split("Account balance: ")[1]
            userOutName = "【" + val["inserStr"].split("&&&&&")[3] + "】"
            regUser(val["inserStr"].split("&&&&&")[3], userSteamId)
            userDataInfo = fatchUser(userSteamId)
            if useXiongb == True:
                userBalance = userDataInfo[0][3]
        if int(userBalance) < diffAmount:
            inputSimpleText(userOutName + "传送余额不足~")
        else:
            sqId = findSquadMemberNo(userSteamId)
            isSameSquad = False
            if sqId != "":
                sqList = findSquadMemberList(sqId)
                isSameSquad = False
                if len(sqList) > 0:
                    for item in sqList:
                        itemData = item.split(" ")
                        if targetPlayerSteamid in itemData:
                            isSameSquad = True

            if isSameSquad == True:
                if useXiongb == True:
                    reduceUserAmount(str(diffAmount), userSteamId, str(0))
                else:
                    inputSimpleText("#ChangeCurrencyBalance Normal -" + str(diffAmount) + " " + userSteamId)
                inputSimpleText("#TeleportTo " + targetPlayerSteamid + " " + userSteamId)
                inputSimpleText(userOutName + "的队友传送请求已执行~")
            else:
                oldData = ""
                with open((directory + "/waitTrans.txt"), "r", encoding="UTF-8") as file:
                    oldData = file.read()
                if oldData == "" or oldData == None:
                    oldObj = []
                else:
                    stream = io.StringIO(oldData)
                    oldObj = json.load(stream)
                waitSec = 0
                try:
                    if "notSquardTransWaitTime" in robotOptions:
                        if robotOptions["notSquardTransWaitTime"] != "":
                            waitSec = int(robotOptions["notSquardTransWaitTime"])
                except Exception as e:
                    try:
                        waitSec = 0
                    finally:
                        e = None
                        del e

                if waitSec > 0:
                    endTimeStr = datetime.fromtimestamp(datetime.timestamp(datetime.now()) + int(waitSec)).strftime("%Y-%m-%d %H:%M:%S")
                    newObj = {'requestId':userSteamId, 
                     'toId':targetPlayerSteamid, 
                     'endTime':endTimeStr}
                    oldObj.append(newObj)
                    with open((directory + "/waitTrans.txt"), "w", encoding="UTF-8") as f:
                        f.write(json.dumps(oldObj, ensure_ascii=False))
                    time.sleep(0.3)
                    inputSimpleText(userOutName + "的非队友传送已进入等待时间，请目标玩家在【" + str(waitSec) + "】秒内发送【" + robotOptions["agreeSquardTransKeyword"] + "】指令，同意此次传送，超过此时间此次传送将失效")


def findSquadMemberList(sqId):
    sqList = []
    inputSimpleText("#ListSquadMembers " + sqId + " true")
    time.sleep(0.1)
    havNum = 0
    havData = False
    userListSp = []
    while havData == False:
        userData = pyperclip.paste()
        if "\n" in userData:
            userListSp = userData.split("\n")
            if len(userListSp) > 0:
                havData = True
            havNum = havNum + 1
            if havNum > 30:
                havData = True
                printToLog("未找所属小队")
        if "slowGetPlayerWaitTime" in robotOptions:
            if robotOptions["slowGetPlayerWaitTime"] != "0":
                time.sleep(float(robotOptions["slowGetPlayerWaitTime"]))

    if len(userListSp) > 1:
        if len(userListSp[1]) > 0:
            userListSp.pop(0)
            sqList = userListSp
        return sqList


def findSquadMemberNo(steamid):
    squadId = ""
    inputSimpleText("#FindSquadMember " + steamid + " true")
    time.sleep(0.1)
    havNum = 0
    havData = False
    userListSp = []
    while havData == False:
        userData = pyperclip.paste()
        if "\n" in userData:
            userListSp = userData.split("\n")
            if len(userListSp) > 0:
                havData = True
            havNum = havNum + 1
            if havNum > 30:
                havData = True
                printToLog("未找所属小队")
        if "slowGetPlayerWaitTime" in robotOptions:
            if robotOptions["slowGetPlayerWaitTime"] != "0":
                time.sleep(float(robotOptions["slowGetPlayerWaitTime"]))

    if len(userListSp) > 1:
        squadId = userListSp[1].split(" ")[0]
    return squadId


def playerBuyAdmin(val):
    printToLog("收到玩家购买权限请求")
    diffAmount = 0
    useXiongb = False
    adminTime = 0
    if "playerBuyAdminAmountType" in robotOptions:
        if robotOptions["playerBuyAdminAmountType"] == "2":
            useXiongb = True
        try:
            if "playerBuyAdminAmount" in robotOptions:
                if robotOptions["playerBuyAdminAmount"] != "":
                    diffAmount = int(robotOptions["playerBuyAdminAmount"])
        except Exception as e:
            try:
                diffAmount = 0
            finally:
                e = None
                del e

        try:
            if "playerBuyAdminTime" in robotOptions:
                if robotOptions["playerBuyAdminTime"] != "":
                    adminTime = int(robotOptions["playerBuyAdminTime"])
        except Exception as e:
            try:
                adminTime = 0
            finally:
                e = None
                del e

        userName = val["inserStr"].split("&&&&&")[3]
        userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
        if userInfo == False or len(userInfo) == 0:
            inputSimpleText("未找到玩家【" + userName + "】的信息，请尝试重新发送指令~")
            return False
        userSteamId = userInfo[1].split("(")[-1].split(")")[0]
        userBalance = userInfo[3].split("Account balance: ")[1]
        userOutName = "【" + val["inserStr"].split("&&&&&")[3] + "】"
        regUser(val["inserStr"].split("&&&&&")[3], userSteamId)
        userDataInfo = fatchUser(userSteamId)
        if useXiongb == True:
            userBalance = userDataInfo[0][3]
    if int(userBalance) < diffAmount:
        inputSimpleText(userOutName + "购买建家权限余额不足")
    else:
        cmdArr = [
         "", userSteamId, str(adminTime)]
        if useXiongb == True:
            reduceUserAmount(str(diffAmount), userSteamId, str(0))
        else:
            inputSimpleText("#ChangeCurrencyBalance Normal -" + str(diffAmount) + " " + userSteamId)
            ui.press("enter")
            ui.press("enter")
        givePlayerAdmin(cmdArr)


def doLottery(val, type):
    printToLog("收到抽奖请求")
    userName = val["inserStr"].split("&&&&&")[3]
    userInfo = getUserInfoByNameFromTotal(val["inserStr"].split("&&&&&")[3], val["inserStr"].split("&&&&&")[2])
    if userInfo == False or len(userInfo) == 0:
        inputSimpleText("未找到玩家【" + userName + "】的信息，请尝试重新发送指令~")
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    userBalance = userInfo[3].split("Account balance: ")[1]
    userOutName = "【" + val["inserStr"].split("&&&&&")[3] + "】"
    regUser(val["inserStr"].split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    useXiongb = False
    diffAmount = lotteryObjs["amount"]
    mutiTime = 1
    if "mutiTime" in totalRobotOptions["choujiang"] and totalRobotOptions["choujiang"]["mutiTime"] != "":
        try:
            if type == 1:
                mutiTime = int(totalRobotOptions["choujiang"]["mutiTime"])
        except:
            mutiTime = 1

        if "amountType" in totalRobotOptions["choujiang"]:
            if totalRobotOptions["choujiang"]["amountType"] == 1:
                useXiongb = True
                userBalance = userDataInfo[0][3]
            vipIsOnline = checkUserVipIsOnline(userSteamId)
            if userDataInfo[0][7] != "0":
                if vipIsOnline == True:
                    userOutName = "尊贵的【" + val["inserStr"].split("&&&&&")[3] + "】"
            if type == 1:
                diffAmount = diffAmount * mutiTime
    if int(userBalance) < diffAmount:
        if useXiongb == True:
            inputSimpleText(userOutName + "抽奖南极熊币余额不足")
        else:
            inputSimpleText(userOutName + "抽奖余额不足")
    else:
        rewardKeys = []
        rewardVals = []
        rewardList = lotteryObjs["jiangpin"]
        for i in rewardList:
            rewardKeys.append(rewardList[i]["name"])
            rewardVals.append(rewardList[i]["gailv"])

        result = random.choices(rewardKeys, weights=rewardVals, k=mutiTime)
        resultObj = []
        for i in range(mutiTime):
            resultObj.append(rewardList[result[i]])

        goodIntRatio = 1
        if useXiongb == True:
            try:
                if "inteLottoryVip" in totalRobotOptions["options"]:
                    goodIntRatio = float(totalRobotOptions["options"]["inteLottoryVip"])
            except Exception:
                goodIntRatio = 1

            reduceUserAmount(str(diffAmount), userSteamId, str(int(float(diffAmount) * goodIntRatio)))
        else:
            try:
                if "inteLottoryNormal" in totalRobotOptions["options"]:
                    goodIntRatio = float(totalRobotOptions["options"]["inteLottoryNormal"])
            except Exception:
                goodIntRatio = 1

            inputSimpleText("#ChangeCurrencyBalance Normal -" + str(diffAmount) + " " + userSteamId)
            updateUserNormalInt(str(diffAmount), userSteamId, str(int(float(diffAmount) * goodIntRatio)))
        text = "、".join(result)
        inputSimpleText(userOutName + "的中奖结果为：【" + text + "】，本次抽奖扣款【" + str(diffAmount) + "】，您的奖品即将发货，请注意查收")
        for j in range(len(resultObj)):
            rewardCodes = resultObj[j]["code"].split(",")
            for i in rewardCodes:
                inputSimpleText(i + " Location " + userSteamId)

        inputSimpleText(userOutName + "的奖品发货成功，请注意查收")
        ui.press("enter")
        ui.press("enter")


def doSendTrans(val, userSteamId):
    userOutName = "【" + val["inserStr"].split("&&&&&")[3] + "】"
    regUser(val["inserStr"].split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    vipIsOnline = checkUserVipIsOnline(userSteamId)
    if userDataInfo[0][7] != "0":
        if vipIsOnline == True:
            userOutName = "尊贵的【" + val["inserStr"].split("&&&&&")[3] + "】"
    printToLog("收到" + val["data"]["showName"] + "传送请求")
    transCodeStr = val["data"]["code"]
    try:
        if int(val["data"]["mohuMaxRadius"]) != 0:
            resultTransCodeArr = []
            minRadius = 0
            maxRadius = 0
            try:
                minRadius = int(val["data"]["mohuRadius"])
            except Exception:
                minRadius = 0

            try:
                maxRadius = int(val["data"]["mohuMaxRadius"])
            except Exception:
                maxRadius = 0

            transCodeArr = transCodeStr.split("#teleport ")[1].split(" ")
            for item in transCodeArr:
                if item != "":
                    if "=" in item:
                        resultTransCodeArr.append(item.split("=")[1])
                    else:
                        resultTransCodeArr.append(item)

            loX = int(float(resultTransCodeArr[0]))
            loY = int(float(resultTransCodeArr[1]))
            loZ = resultTransCodeArr[2]
            random_number = random.randint(minRadius, maxRadius) * 100
            loTypeArr = random.choices([1, 2], weights=[1, 1], k=2)
            if loTypeArr[0] == 1:
                loX = loX + random_number
            if loTypeArr[0] == 2:
                loX = loX - random_number
            if loTypeArr[1] == 1:
                loY = loY + random_number
            if loTypeArr[1] == 2:
                loY = loY - random_number
            transCodeStr = "#teleport " + str(loX) + " " + str(loY) + " " + loZ
    except Exception as e:
        try:
            transCodeStr = val["data"]["code"]
        finally:
            e = None
            del e

    inputSimpleText(transCodeStr + " " + userSteamId)
    inputSimpleText(userOutName + "的" + val["data"]["showName"] + "传送发货成功，请注意查收")
    insertDataIntoSendedGift(val["inserStr"] + "&&&&&" + userSteamId)
    insertToSendedGiftData(val["inserStr"])
    time.sleep(0.8)


def doSendOnlineNum():
    printToLog("收到在线人数请求")
    response = requests.get(url=("https://api.battlemetrics.com/servers/" + robotOptions["serverName"]))
    result = json.loads(response.text)
    strPlay = "0"
    rank = "0"
    nowTime = ""
    try:
        if "data" in result:
            if "attributes" in result["data"]:
                cu = result["data"]["attributes"]["players"]
                max = result["data"]["attributes"]["maxPlayers"]
                rk = result["data"]["attributes"]["rank"]
                mt = result["data"]["attributes"]["details"]["time"]
                strPlay = str(cu) + "/" + str(max)
                rank = str(rk)
                nowTime = str(mt)
        inputSimpleText("当前在线人数：" + strPlay + "， 服务器排名：" + rank + "，当前时间：" + nowTime)
    except ZeroDivisionError:
        inputSimpleText("在线人数查询出错，请稍后重试")


def addNewPlayerTrans(id):
    global needTransNewPlayer
    time.sleep(60)
    needTransNewPlayer.append(id)


def sendNewPlayerTrans():
    for item in needTransNewPlayer:
        printToLog("收到新玩家传送请求")
        inputSimpleText(robotOptions["newUserAutoCode"] + " " + item)
        ui.press("enter")


def doSendLoginLog(arr):
    printToLog("收到上下线播报请求")
    for i in arr:
        data = i
        userName = data.split(" ")[2].split(":")[1].split("(")[0]
        userSteamId = data.split(" ")[2].split(":")[0]
        userLen = fatchUser(userSteamId)
        state = "上线"
        strInfo = ""
        if "logged out" in data:
            state = "下线"
            if "language" in robotOptions and robotOptions["language"] == 1:
                state = "logged out"
        else:
            state = "上线"
            if "language" in robotOptions:
                if robotOptions["language"] == 1:
                    state = "logged in"
        strInfo = "【" + userName + "】" + state + "啦"
        if "language" in robotOptions:
            if robotOptions["language"] == 1:
                strInfo = "【" + userName + "】 was " + state + "~"
        bossArrs = []
        if "bossLog" in robotOptions and len(robotOptions["bossLog"]) > 0:
            if robotOptions["bossLog"][0]["steamid"] != "":
                bossArrs = robotOptions["bossLog"]
            isBoss = False
            isNewPlayer = False
            for item in bossArrs:
                if userSteamId in item["steamid"]:
                    if "logged in" in data:
                        isBoss = True
                        if "language" in robotOptions and robotOptions["language"] == 1:
                            inputSimpleText("#Announce Welcome esteemed players【" + userName + "】 logged in~~" + item["redInfo"])
                        else:
                            inputSimpleText("#Announce 欢迎尊贵的玩家【" + userName + "】上线~~" + item["redInfo"])
                        ui.press("enter")

            if userLen == None or len(userLen) == 0:
                isNewPlayer = True
                regUser(userName, userSteamId)
                if "newPlayerEnterInitNormaInt" in robotOptions and robotOptions["newPlayerEnterInitNormaInt"] != "":
                    try:
                        intNormalInt = int(robotOptions["newPlayerEnterInitNormaInt"])
                        updata = {'steam_id':userSteamId, 
                         'normal_integral':intNormalInt}
                        if userSteamId:
                            updateDataToUser(updata)
                    except Exception as e:
                        try:
                            logging.error(str(datetime.now()))
                            logging.error(traceback.format_exc())
                        finally:
                            e = None
                            del e

            if "newPlayerEnterInitXB" in robotOptions and robotOptions["newPlayerEnterInitXB"] != "":
                try:
                    intXB = int(robotOptions["newPlayerEnterInitXB"])
                    updata = {'steam_id':userSteamId, 
                     'amount':intXB}
                    if userSteamId:
                        updateDataToUser(updata)
                except Exception as e:
                    try:
                        logging.error(str(datetime.now()))
                        logging.error(traceback.format_exc())
                    finally:
                        e = None
                        del e

        if "newPlayerEnterInitNormaLevel" in robotOptions and robotOptions["newPlayerEnterInitNormaLevel"] != "":
            try:
                intNormalLevel = int(robotOptions["newPlayerEnterInitNormaLevel"])
                updata = {
                  'steam_id': userSteamId,
                  'normal_vip_level': intNormalLevel,
                  'vip_level': "0",
                  'custom_title': ""}
                if userSteamId:
                    updateDataToUser(updata)
                    resetPlayerName(userName, updata, "init")
            except Exception as e:
                try:
                    logging.error(str(datetime.now()))
                    logging.error(traceback.format_exc())
                finally:
                    e = None
                    del e

            if "newUserAutoCode" in robotOptions:
                if robotOptions["newUserAutoCode"] != "":
                    threading.Thread(target=addNewPlayerTrans, args=(userSteamId,), daemon=True).start()
            if isBoss == False:
                if "logged in" in data and robotOptions["isOpenLoginLog"] == 1:
                    if "loginLastStr" in robotOptions:
                        if robotOptions["loginLastStr"] != "":
                            strInfo = strInfo + "，" + robotOptions["loginLastStr"]
                    if "redInfoOpen" in robotOptions and robotOptions["redInfoOpen"] == "1":
                        if "redInfoType" in robotOptions:
                            if robotOptions["redInfoType"] == "1":
                                inputSimpleText("#Announce 【" + userName + "】" + robotOptions["redInfoCont"])
                        if "redInfoType" in robotOptions and robotOptions["redInfoType"] == "2":
                            if isNewPlayer == True:
                                inputSimpleText("#Announce 【" + userName + "】" + robotOptions["redInfoCont"])
                            if "normalInfoOpen" in robotOptions:
                                if robotOptions["normalInfoOpen"] == 1:
                                    inputSimpleText(strInfo)
                            ui.press("enter")
        else:
            if "logged out" in data:
                if "isOpenLogoutLog" in robotOptions:
                    if robotOptions["isOpenLogoutLog"] == 1:
                        strInfo = strInfo + "，本次在线：" + data.split("-----")[1] + "分钟"
                        if "language" in robotOptions:
                            if robotOptions["language"] == 1:
                                strInfo = strInfo + "，Online for ：" + data.split("-----")[1] + " minutes this time~"
                            inputSimpleText(strInfo)
                            ui.press("enter")


def doSendKillLog(arr):
    printToLog("收到击杀播报请求")
    for i in arr:
        data = i
        infoArr = data.split(" ")
        if len(infoArr) > 5:
            diedName = infoArr[2]
            killerName = infoArr[5]
            weapon = infoArr[8]
            inst = data.split("Distance: ")[1].split(" m]")[0]
            strInfo = "【" + killerName + "】使用【" + weapon + "】击杀了【" + diedName + "】，距离【" + inst + "】米"
            if "language" in robotOptions:
                if robotOptions["language"] == 1:
                    strInfo = "【" + killerName + "】 used 【" + weapon + "】 killed 【" + diedName + "】，distance【" + inst + "】m"
                inputSimpleText(strInfo)


def sendFreeNewGift(giftArr):
    for i in giftArr:
        doSendFreeGift(i)
        time.sleep(1)


def sendNewGift(giftArr):
    for i in giftArr:
        doSendGift(i)
        time.sleep(1)


def sendGood(giftArr):
    for i in giftArr:
        orderUserName = i["inserStr"].split("&&&&&")[3]
        userInfo = getUserInfoByNameFromTotal(i["inserStr"].split("&&&&&")[3], i["inserStr"].split("&&&&&")[2])
        if userInfo == False or len(userInfo) == 0:
            inputSimpleText("未找到玩家【" + orderUserName + "】的信息，请尝试重新发送指令~")
            return False
        userSteamId = userInfo[1].split("(")[-1].split(")")[0]
        balance = userInfo[3].split("Account balance: ")[1]
        regUser(i["inserStr"].split("&&&&&")[3], userSteamId)
        userDataInfo = fatchUser(userSteamId)
        goodUseXiong = False
        openUseXiong = False
        goodUseAmount = i["data"]["amount"]
        userGoodNum = None
        if "customNum" in i["data"] and i["data"]["customNum"] == 1:
            try:
                userGoodNum = int(i["inserStr"].split("&&&&&")[5].split("*")[1])
                goodUseAmount = int(float(i["data"]["amount"]) * userGoodNum)
            except Exception:
                userGoodNum = None

            if "useXiong" in i["data"]:
                if i["data"]["useXiong"] == 1:
                    goodUseXiong = True
                if "isOpenXiongAmount" in robotOptions:
                    if robotOptions["isOpenXiongAmount"] == 1:
                        openUseXiong = True
        if openUseXiong == True:
            if goodUseXiong == True:
                balance = userDataInfo[0][3]
            if i["data"]["isCheckBalance"] == 0:
                doSendGift(i)
            elif int(balance) < goodUseAmount:
                if openUseXiong == True and goodUseXiong == True:
                    inputSimpleText("【" + orderUserName + "】购买" + i["data"]["showName"] + "南极熊币余额不足")
                else:
                    inputSimpleText("【" + orderUserName + "】购买" + i["data"]["showName"] + "余额不足")
            else:
                goodIntRatio = 1
                if openUseXiong == True and goodUseXiong == True:
                    try:
                        if "inteGoodVip" in totalRobotOptions["options"]:
                            goodIntRatio = float(totalRobotOptions["options"]["inteGoodVip"])
                    except Exception:
                        goodIntRatio = 1

                    reduceUserAmount(str(goodUseAmount), userSteamId, str(int(float(goodUseAmount) * goodIntRatio)))
                else:
                    try:
                        if "inteGoodNormal" in totalRobotOptions["options"]:
                            goodIntRatio = float(totalRobotOptions["options"]["inteGoodNormal"])
                    except Exception:
                        goodIntRatio = 1

                    inputSimpleText("#ChangeCurrencyBalance Normal -" + str(goodUseAmount) + " " + userSteamId)
                    updateUserNormalInt(str(goodUseAmount), userSteamId, str(int(float(goodUseAmount) * goodIntRatio)))
                doSendGift(i, userGoodNum)


def connect_ftp():
    global ftp
    global loginFtpIsPending
    host = robotOptions["ftpIp"]
    ftpport = robotOptions["ftpPort"]
    user = robotOptions["ftpUser"]
    pwd = robotOptions["ftpPwd"]
    printToLog("登陆日志连接状态")
    try:
        ftp.pwd()
    except Exception:
        printToLog("正在连接FTP服务器....")
        ftp = FTP()
        try:
            ftp.connect(host, ftpport)
            ftp.login(user, pwd)
            ftp.voidcmd("PASV")
            ftp.set_pasv(True)
            printToLog("连接FTP服务器成功！！！")
        except Exception as e:
            try:
                printToLog("FTP服务器连接失败：")
                printToLog(e)
                ftp.close()
            finally:
                e = None
                del e

    loginFtpIsPending = False
    return ftp


killftp = None

def connect_kill_ftp():
    global killFtpIsPending
    global killftp
    host = robotOptions["ftpIp"]
    ftpport = robotOptions["ftpPort"]
    user = robotOptions["ftpUser"]
    pwd = robotOptions["ftpPwd"]
    try:
        killftp.pwd()
    except Exception:
        printToLog("正在连接FTP服务器....")
        killftp = FTP()
        try:
            killftp.connect(host, ftpport)
            killftp.login(user, pwd)
            killftp.voidcmd("PASV")
            killftp.set_pasv(True)
            printToLog("连接FTP服务器成功！！！")
        except Exception as e:
            try:
                printToLog("FTP服务器连接失败：")
                printToLog(e)
                killftp.close()
            finally:
                e = None
                del e

    killFtpIsPending = False
    return killftp


def connect_sftp():
    global loginFtpIsPending
    global sftp
    host = robotOptions["ftpIp"]
    ftpport = robotOptions["ftpPort"]
    user = robotOptions["ftpUser"]
    pwd = robotOptions["ftpPwd"]
    try:
        printToLog("尝试读取目录")
        sftp.listdir()
    except Exception:
        printToLog("连接ftp服务器中...")
        t = paramiko.Transport((host, ftpport))
        try:
            t.connect(username=user, password=pwd)
            sftp = paramiko.SFTPClient.from_transport(t)
            print(sftp.listdir())
            printToLog("连接ftp服务器成功！！！")
        except Exception as e:
            try:
                printToLog("FTP服务器连接失败：")
                printToLog(e)
                t.close()
            finally:
                e = None
                del e

    loginFtpIsPending = False
    return sftp


totalUserList = []
totalAllUserList = []
getUIBySIDFromTotalNum = 0

def getUserInfoBySteamidFromTotal(id):
    global getUIBySIDFromTotalNum
    global totalAllUserList
    uuser = []
    for item in totalAllUserList:
        name1 = item[1].split("(")[-1].split(")")[0]
        if name1 == id:
            uuser = item

    if len(uuser) == 0:
        getUserInfo("11")
        if getUIBySIDFromTotalNum < 3:
            getUIBySIDFromTotalNum = getUIBySIDFromTotalNum + 1
            uuser = getUserInfoBySteamidFromTotal(id)
        getUIBySIDFromTotalNum = 0
        return uuser


getUIByNameFromTotalNum = 0

def getUserInfoByNameFromTotal(name, word=''):
    global getUIByNameFromTotalNum
    uuser = []
    for item in totalAllUserList:
        name1 = item[0].split(". ")[1]
        name2 = item[6]
        if not not name1 == name:
            if name2 == "/" + name:
                pass
            uuser = item

    if len(uuser) == 0:
        getUserInfo("11")
        if getUIByNameFromTotalNum < 3:
            getUIByNameFromTotalNum = getUIByNameFromTotalNum + 1
            uuser = getUserInfoByNameFromTotal(name)
        getUIByNameFromTotalNum = 0
        return uuser


def getUserInfo(name, word=''):
    global totalAllUserList
    global totalUserList
    totalAllUserList = []
    totalUserList = []
    try:
        inputSimpleText("#ListPlayers true")
        time.sleep(0.1)
        havNum = 0
        havData = False
        userListSp = []
        while havData == False:
            userData = pyperclip.paste()
            if "\n" in userData:
                userListSp = userData.split("\n")
                if len(userListSp) > 0:
                    havData = True
                havNum = havNum + 1
                if havNum > 30:
                    havData = True
                    printToLog("未找到发言玩家，跳过本轮")
            if "slowGetPlayerWaitTime" in robotOptions:
                if robotOptions["slowGetPlayerWaitTime"] != "0":
                    time.sleep(float(robotOptions["slowGetPlayerWaitTime"]))

        userListSp.pop(0)
        userList = []
        chUs = []
        index = 0
        for item in userListSp:
            if index % 6 == 0:
                if index == 0:
                    chUs.append(item)
                else:
                    chUs.append(item)
                    userList.append(chUs)
                    chUs = []
                    index = -1
            else:
                chUs.append(item)
            index = index + 1

        userArr = []
        orderUserName = name
        uuser = []
        totalAllUserList = userList
        for u in userList:
            name1 = u[0].split(". ")[1]
            name2 = u[6]
            if not not name1 == orderUserName:
                if name2 == "/" + orderUserName:
                    pass
                totalUserList.append(u)

        if len(totalUserList) > 1:
            printToLog("发现重名玩家，跳过发货")
            inputSimpleText("【" + name + "】发现多个重名玩家，跳过本次发货，请联系管理员改名~")
            return False
        if len(totalUserList) == 1:
            uuser = totalUserList[0]
        ui.press("enter")
        return uuser
    except Exception as e:
        try:
            inputSimpleText("南极熊机器人提示：未正常获取到在线列表，请管理员适当调整【基本设置】中【获取在线列表延时】，原因：【电脑卡了】")
            return False
        finally:
            e = None
            del e


def sendQA(giftArr):
    for i in giftArr:
        codeArr = str(i["data"]["code"]).split(",")
        for j in codeArr:
            inputSimpleText(j)
            time.sleep(0.5)


def formatServerTimeToStemp(val):
    day = val.split("-")[0].replace(".", "-", 10)
    time2 = val.split("-")[1].split(":")[0].replace(".", ":", 10)
    timeVal = day + " " + time2
    timestempObj = datetime.strptime(timeVal, "%Y-%m-%d %H:%M:%S")
    timeStempVal = int(time.mktime(timestempObj.timetuple()))
    return timeStempVal


def sendTrans(giftArr):
    for i in giftArr:
        userInfo = getUserInfoByNameFromTotal(i["inserStr"].split("&&&&&")[3], i["inserStr"].split("&&&&&")[2])
        orderUserName = "【" + i["inserStr"].split("&&&&&")[3] + "】"
        if userInfo == False or len(userInfo) == 0:
            inputSimpleText("未找到玩家【" + orderUserName + "】的信息，请尝试重新发送指令~")
            return False
        userSteamId = userInfo[1].split("(")[-1].split(")")[0]
        balance = userInfo[3].split("Account balance: ")[1]
        isInWaitTime = False
        try:
            if "transWaitTime" in i["data"]:
                if float(i["data"]["transWaitTime"]) > 0:
                    keyword = i["inserStr"].split("&&&&&")[2]
                    serverTime = i["inserStr"].split("&&&&&")[5]
                    localTime = i["inserStr"].split("&&&&&")[1]
                    giftList = getUserGiftLogsByKey(keyword, userSteamId, localTime)
                    print(giftList)
                    if giftList != None:
                        if len(giftList) > 0:
                            preServerTime = formatServerTimeToStemp(giftList[-1][1])
                            currentTime = formatServerTimeToStemp(serverTime)
                            diffTime = currentTime - preServerTime
                            waitTime = float(i["data"]["transWaitTime"]) * 60
                            if diffTime < waitTime:
                                inputSimpleText(orderUserName + "的传送正在冷却中...冷却时间为【" + str(i["data"]["transWaitTime"]) + "】分钟")
                                isInWaitTime = True
        except Exception as e:
            try:
                print(e)
                logging.error(str(datetime.now()))
                logging.error(traceback.format_exc())
                isInWaitTime = False
            finally:
                e = None
                del e

        if isInWaitTime == True:
            return False
        regUser(i["inserStr"].split("&&&&&")[3], userSteamId)
        userDataInfo = fatchUser(userSteamId)
        useXiongb = False
        if "amountType" in i["data"]:
            if i["data"]["amountType"] == 1:
                useXiongb = True
                balance = userDataInfo[0][3]
        vipIsOnline = checkUserVipIsOnline(userSteamId)
        if userDataInfo[0][7] != "0":
            if vipIsOnline == True:
                vipLevelArr = totalRobotOptions["vipLevel"]
                orderUserName = "尊贵的【" + i["inserStr"].split("&&&&&")[3] + "】"
            if i["data"]["isCheckBalance"] == 0:
                doSendTrans(i, userSteamId)
            elif int(balance) < i["data"]["amount"]:
                if useXiongb == True:
                    inputSimpleText(orderUserName + "购买" + i["data"]["showName"] + "南极熊币余额不足")
                else:
                    inputSimpleText(orderUserName + "购买" + i["data"]["showName"] + "余额不足")
            else:
                goodIntRatio = 1
                if useXiongb == True:
                    try:
                        if "inteGoodVip" in totalRobotOptions["options"]:
                            goodIntRatio = float(totalRobotOptions["options"]["inteGoodVip"])
                    except Exception:
                        goodIntRatio = 1

                    reduceUserAmount(i["data"]["amount"], userSteamId, str(int(float(i["data"]["amount"]) * goodIntRatio)))
                else:
                    inputSimpleText("#ChangeCurrencyBalance Normal -" + str(i["data"]["amount"]) + " " + userSteamId)
                    try:
                        if "inteGoodNormal" in totalRobotOptions["options"]:
                            goodIntRatio = float(totalRobotOptions["options"]["inteGoodNormal"])
                    except Exception:
                        goodIntRatio = 1

                    updateUserNormalInt(str(i["data"]["amount"]), userSteamId, str(int(float(i["data"]["amount"]) * goodIntRatio)))
                doSendTrans(i, userSteamId)
            time.sleep(1)


def checkGiftHistory(instr):
    userSteamId = instr.split("&&&&&")[4]
    if len(notAllowGetGiftIds) > 0:
        if userSteamId in notAllowGetGiftIds:
            return True
        return False


def inputSimpleText(val):
    doInputAndEnter(val)


setAdminIsReading = False

def setAdminUser(banId, type, timeMin, timeStr, oldObj):
    global localFileDir
    global needSendSetAdminArr
    global setAdminIsReading
    setAdminIsReading = True
    host = robotOptions["ftpIp"]
    ftpport = str(robotOptions["ftpPort"])
    user = robotOptions["ftpUser"]
    pwd = robotOptions["ftpPwd"]
    ftpType = robotOptions["ftpType"]
    scpDir = localFileDir + "/Plugin/"
    ftpFileType = "sftp"
    ftpFilePath = "/SCUM/Saved/Config/WindowsServer/"
    if "ftpGetType" in robotOptions:
        if robotOptions["ftpGetType"] == "1":
            host = bjxHost
            ftpport = bjxFtpport
            user = bjxUser
            pwd = bjxPwd
            ftpType = bjxFtpType
            ftpFileType = "ftp"
            ftpFilePath = "/" + robotOptions["secertKey"] + "----" + str(robotOptions["ftpType"]) + "/"
    try:
        lastKillFileArr = [
         "AdminUsers.ini"]
        if "ftpGetType" in robotOptions and robotOptions["ftpGetType"] == "1":
            subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "get ' + ftpFilePath + "AdminUsers.ini " + localFileDir + '\\Logs\\AdminUsers.ini" "exit"'), startupinfo=startupinfo)
            lastKillFileArr = ["AdminUsers.ini"]
        else:
            if ftpType == 1:
                ftpFileType = "ftp"
            if ftpType == 2:
                result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "ls" "exit"'), startupinfo=startupinfo)
                arr = result.decode("utf-8")
                arr = arr.split("\r\n")
                arrList = []
                for i in arr:
                    if host + "_" in i:
                        arrList.append(i.split(" ")[-1])

                menuWord = arrList[0]
                ftpFilePath = "/" + menuWord + "/Config/WindowsServer/"
            if ftpType == 3:
                result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "ls" "exit"'), startupinfo=startupinfo)
                arr = result.decode("utf-8")
                arr = arr.split("\r\n")
                arrList = []
                for i in arr:
                    if host + "_" in i:
                        arrList.append(i.split(" ")[-1])

                menuWord = arrList[0]
                ftpFilePath = "/" + menuWord + "/Configs/"
            result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "cd ' + ftpFilePath + '" "ls" "exit"'), startupinfo=startupinfo)
            arr = result.decode("utf-8")
            arr = arr.split("\r\n")
            killList = []
            for i in arr:
                if "AdminUsers.ini" in i:
                    if "ServerSettingsAdminUsers.ini" not in i:
                        killList.append(i.split(" ")[-1])

            lastKillFileArr = killList[-1:]
            for i in lastKillFileArr:
                result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "get ' + ftpFilePath + i + " " + localFileDir + "\\Logs\\" + i + '" "exit"'), startupinfo=startupinfo)

        file_content = ""
        with open((directory + "/Logs/" + lastKillFileArr[0]), "r", encoding="UTF-8") as file:
            fileData = file.read()
            file_content = fileData.split("\n")
        if file_content != "":
            lastLoginLogArr = file_content
            newAdminIni = []
            oldData = ""
            adminObj = {'host':robotOptions["ftpIp"], 
             'ftpport':str(robotOptions["ftpPort"]), 
             'user':robotOptions["ftpUser"], 
             'pwd':robotOptions["ftpPwd"], 
             'ftpType':robotOptions["ftpType"]}
            if type == 1:
                for lastLoginLog in lastLoginLogArr:
                    if banId not in lastLoginLog:
                        newAdminIni.append(lastLoginLog)

                with open((directory + "/Logs/" + lastKillFileArr[0]), "w", encoding="UTF-8") as f:
                    f.write("\n".join(newAdminIni))
                if "ftpGetType" in robotOptions and robotOptions["ftpGetType"] == "1":
                    adminObj["contStr"] = "\n".join(newAdminIni)
                    contObjStr = json.dumps(adminObj, ensure_ascii=False)
                    data = {'secert':robotOptions["secertKey"], 
                     'status':"0", 
                     'content':contObjStr}
                    response2 = requests.post(url=(serverRoot + "updatePlayerGameAdminData?secert=" + robotOptions["secertKey"] + "&status=0&content=" + contObjStr), data=data)
                    result2 = json.loads(response2.text)
                    IsUping = True
                    while IsUping == True:
                        response2 = requests.get(url=(serverRoot + "getSecPlayerGameAdminList?secert=" + robotOptions["secertKey"]))
                        result2 = json.loads(response2.text)
                        if "code" in result2:
                            if result2["code"] == 2:
                                reducePlayerAdmin(["", banId])
                                endMonitorPlayerAdmin(["", banId])
                                printToLog("更新权限文件成功...")
                                IsUping = False

                else:
                    for i in lastKillFileArr:
                        result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "put ' + localFileDir + "\\Logs\\" + i + " " + ftpFilePath + i + '" "exit"'), startupinfo=startupinfo)

                    reducePlayerAdmin(["", banId])
                    endMonitorPlayerAdmin(["", banId])
                    printToLog("更新权限文件成功...")
            elif type == 2:
                lastLoginLogArr.append(banId + "[godmode]")
                with open((directory + "/Logs/" + lastKillFileArr[0]), "w", encoding="UTF-8") as f:
                    f.write("\n".join(lastLoginLogArr))
                if "ftpGetType" in robotOptions and robotOptions["ftpGetType"] == "1":
                    adminObj["contStr"] = "\n".join(lastLoginLogArr)
                    contObjStr = json.dumps(adminObj, ensure_ascii=False)
                    data = {'secert':robotOptions["secertKey"], 
                     'status':"0", 
                     'content':contObjStr}
                    response2 = requests.post(url=(serverRoot + "updatePlayerGameAdminData?secert=" + robotOptions["secertKey"] + "&status=0&content=" + contObjStr), data=data)
                    result2 = json.loads(response2.text)
                    IsUping = True
                    while IsUping == True:
                        response2 = requests.get(url=(serverRoot + "getSecPlayerGameAdminList?secert=" + robotOptions["secertKey"]))
                        result2 = json.loads(response2.text)
                        if "code" in result2:
                            if result2["code"] == 2:
                                printToLog("更新权限文件成功...")
                                with open((directory + "/adminUserList.txt"), "w", encoding="UTF-8") as f:
                                    f.write(json.dumps(oldObj, ensure_ascii=False))
                                sendObj = {'steamid':banId,  'timeMin':timeMin, 
                                 'timeStr':timeStr}
                                startMonitorPlayerAdmin(["", banId])
                                needSendSetAdminArr.append(sendObj)
                                IsUping = False

                else:
                    for i in lastKillFileArr:
                        result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "put ' + localFileDir + "\\Logs\\" + i + " " + ftpFilePath + i + '" "exit"'), startupinfo=startupinfo)

                    printToLog("更新权限文件成功...")
                    with open((directory + "/adminUserList.txt"), "w", encoding="UTF-8") as f:
                        f.write(json.dumps(oldObj, ensure_ascii=False))
                    sendObj = {'steamid':banId,  'timeMin':timeMin, 
                     'timeStr':timeStr}
                    startMonitorPlayerAdmin(["", banId])
                    needSendSetAdminArr.append(sendObj)
        setAdminIsReading = False
    except Exception as e:
        try:
            setAdminIsReading = False
            printToLog("更新权限文件失败...")
            printToLog(e)
            print(e)
        finally:
            e = None
            del e


def checkSetAdminIsNeedReduce():
    with open((directory + "/adminUserList.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    if oldData == "" or oldData == None:
        oldObj = []
    else:
        stream = io.StringIO(oldData)
        oldObj = json.load(stream)
    if len(oldObj) > 0:
        currentTimeStamp = datetime.timestamp(datetime.now())
        for item in oldObj:
            itemEndtamp = datetime.timestamp(datetime.strptime(item["endTime"], "%Y-%m-%d %H:%M:%S"))
            if currentTimeStamp > itemEndtamp:
                if setAdminIsReading == False:
                    threading.Thread(target=setAdminUser, args=(item["steamid"], 1, "", "", []), daemon=True).start()


def fatchAllPlayerAdmin():
    with open((directory + "/adminUserList.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    if oldData == "" or oldData == None:
        oldObj = []
    else:
        stream = io.StringIO(oldData)
        oldObj = json.load(stream)
    if len(oldObj) > 0:
        currentTimeStamp = datetime.timestamp(datetime.now())
        for item in oldObj:
            itemEndtamp = datetime.timestamp(datetime.strptime(item["endTime"], "%Y-%m-%d %H:%M:%S"))
            diffTime = (itemEndtamp - currentTimeStamp) / 60
            inputSimpleText("玩家【" + item["steamid"] + "】剩余建家权限时长：【" + str(int(diffTime)) + "】分钟")


def fatchSinglePlayerAdmin(cmdArr):
    if len(cmdArr) != 2:
        inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
    else:
        playerId = cmdArr[1]
        with open((directory + "/adminUserList.txt"), "r", encoding="UTF-8") as file:
            oldData = file.read()
        if oldData == "" or oldData == None:
            oldObj = []
        else:
            stream = io.StringIO(oldData)
            oldObj = json.load(stream)
        havePlayer = False
        if len(oldObj) > 0:
            currentTimeStamp = datetime.timestamp(datetime.now())
            for item in oldObj:
                if item["steamid"] == playerId:
                    havePlayer = True
                    itemEndtamp = datetime.timestamp(datetime.strptime(item["endTime"], "%Y-%m-%d %H:%M:%S"))
                    diffTime = (itemEndtamp - currentTimeStamp) / 60
                    inputSimpleText("玩家【" + item["steamid"] + "】剩余建家权限时长：【" + str(int(diffTime)) + "】分钟")

        if havePlayer == False:
            inputSimpleText("未找到玩家【" + playerId + "】的权限信息，请检查玩家id是否正确")


def fatchUserPersonSkillData(inserStr):
    userInfo = getUserInfo(inserStr.split("&&&&&")[3], inserStr.split("&&&&&")[2])
    if userInfo == False or len(userInfo) == 0:
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    regUser(inserStr.split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    if len(userDataInfo) == 1:
        orderUserName = "【" + inserStr.split("&&&&&")[3] + "】"
        playerPGCardData = getUserPersonSkillData(userSteamId)
        if playerPGCardData:
            inputSimpleText("玩家" + orderUserName + "拥有的职业技能如下：")
            for item in playerPGCardData:
                giftEndTime = int(datetime.strptime(str(playerPGCardData[item]["end_time"]), "%Y-%m-%d %H:%M:%S").timestamp())
                nowTime = datetime.timestamp(datetime.now())
                if nowTime < giftEndTime:
                    leftHour = int((giftEndTime - nowTime) / 60 / 60)
                    if leftHour < 24:
                        inputSimpleText("玩家" + orderUserName + "的 技能【" + item + " " + str(playerPGCardData[item]["level"]) + "级】，有效期剩余【" + str(leftHour) + "】小时")
                    else:
                        leftDay = int(leftHour / 24)
                        inputSimpleText("玩家" + orderUserName + "的 技能【" + item + "】，有效期剩余【" + str(leftDay) + "】天")

        else:
            inputSimpleText("玩家" + orderUserName + "没有正在生效中的技能")


def fatchUserPersonGiftCard(inserStr):
    userInfo = getUserInfo(inserStr.split("&&&&&")[3], inserStr.split("&&&&&")[2])
    if userInfo == False or len(userInfo) == 0:
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    regUser(inserStr.split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    if len(userDataInfo) == 1:
        orderUserName = "【" + inserStr.split("&&&&&")[3] + "】"
        playerPGCardData = getUserPersonGiftCard(userSteamId)
        if playerPGCardData:
            inputSimpleText("玩家" + orderUserName + "正在生效中的装备卡如下：")
            for item in playerPGCardData:
                giftEndTime = int(datetime.strptime(str(playerPGCardData[item]["end_time"]), "%Y-%m-%d %H:%M:%S").timestamp())
                nowTime = datetime.timestamp(datetime.now())
                if nowTime < giftEndTime:
                    leftHour = int((giftEndTime - nowTime) / 60 / 60)
                    if leftHour < 24:
                        inputSimpleText("玩家" + orderUserName + "的 装备卡【" + item + "】，有效期剩余【" + str(leftHour) + "】小时")
                    else:
                        leftDay = int(leftHour / 24)
                        inputSimpleText("玩家" + orderUserName + "的 装备卡【" + item + "】，有效期剩余【" + str(leftDay) + "】天")

        else:
            inputSimpleText("玩家" + orderUserName + "没有正在生效中的装备卡")


def doPlayerStudySkill(inserStr):
    userInfo = getUserInfo(inserStr.split("&&&&&")[3], inserStr.split("&&&&&")[2])
    userMessage = inserStr.split("&&&&&")[2]
    if userInfo == False or len(userInfo) == 0:
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    regUser(inserStr.split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    try:
        if len(userDataInfo) == 1:
            orderUserName = "【" + inserStr.split("&&&&&")[3] + "】"
            playerPGCardData = getUserPersonSkillData(userSteamId)
            keywordMsgArr = inserStr.split("&&&&&")[2].split(" ")
            if len(keywordMsgArr) != 2:
                inputSimpleText(orderUserName + "的技能指令不正确，请检查指令~")
            else:
                skillName = keywordMsgArr[1]
                canStudySkill = False
                if skillName in playerPGCardData:
                    playerPerGiftObj = playerPGCardData[skillName]
                    endInsurTime = int(datetime.strptime(str(playerPerGiftObj["end_time"]), "%Y-%m-%d %H:%M:%S").timestamp())
                    nowTime = datetime.timestamp(datetime.now())
                    if nowTime > endInsurTime:
                        canStudySkill = True
                    else:
                        canStudySkill = False
                        inputSimpleText(orderUserName + "已习得技能【" + skillName + "】，无法再次学习~")
                else:
                    canStudySkill = True
                if canStudySkill == True:
                    skillOptions = robotOptions["skillOptions"]
                    skillList = robotOptions["skillObjs"]
                    skillHave = False
                    skillObj = {}
                    for item in skillList:
                        if item["keyword"] == skillName:
                            skillObj = item
                            skillHave = True

                    if skillHave == False:
                        inputSimpleText(orderUserName + "学习的技能【" + skillName + "】不存在，请检查技能名~")
                    elif "isAllowStudy" not in skillObj or skillObj["isAllowStudy"] == "0":
                        inputSimpleText(orderUserName + "学习的技能【" + skillName + "】不支持自主学习，请联系管理员获得技能~")
                    else:
                        studyDayLong = skillOptions["studyDaysLong"]
                        isCanUpdateSkill = False
                        if skillName in playerPGCardData:
                            playerPGCardData[skillName]["level"] = 1
                            playerPGCardData[skillName]["end_time"] = datetime.fromtimestamp(datetime.timestamp(datetime.now()) + int(studyDayLong) * 24 * 60 * 60).strftime("%Y-%m-%d %H:%M:%S")
                            isCanUpdateSkill = True
                        elif len(playerPGCardData) > 0 and skillOptions["isAllowChange"] == "0" and skillOptions["isAllowMuti"] == "0":
                            inputSimpleText(orderUserName + "存在已习得的职业技能，不支持转职业，请联系管理员获得多技能~")
                        elif len(playerPGCardData) > 0 and skillOptions["isAllowMuti"] == "0":
                            inputSimpleText(orderUserName + "存在已习得的技能，不支持学习多个技能，请联系管理员获得多技能~")
                        else:
                            playerPGCardData[skillName] = {'name':skillName, 
                             'level':1, 
                             'start_time':(datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime)("%Y-%m-%d %H:%M:%S"), 
                             'end_time':(datetime.fromtimestamp(datetime.timestamp(datetime.now()) + int(studyDayLong) * 24 * 60 * 60).strftime)("%Y-%m-%d %H:%M:%S")}
                            isCanUpdateSkill = True
                        if isCanUpdateSkill == True:
                            if len(skillObj["list"]) == 0:
                                inputSimpleText(orderUserName + "学习的技能数据存在错误，请联系管理员修复~")
                            else:
                                skillLevelObj = skillObj["list"][0]
                                useAmountType = ""
                                useAmountValue = ""
                                hasNoFullAmount = False
                                if skillLevelObj["upLevelAmountType"] != "":
                                    useAmountType = skillLevelObj["upLevelAmountType"]
                                    useAmountValue = int(float(skillLevelObj["useAmount"]))
                                if useAmountType == "1":
                                    userBalance = userInfo[3].split("Account balance: ")[1]
                                    if int(userBalance) < int(useAmountValue):
                                        hasNoFullAmount = True
                                elif useAmountType == "2":
                                    userBalance = userDataInfo[0][3]
                                    if int(userBalance) < int(useAmountValue):
                                        hasNoFullAmount = True
                                if hasNoFullAmount == True:
                                    inputSimpleText(orderUserName + "的余额不足，无法学习技能哦~")
                                else:
                                    if useAmountType == "1":
                                        inputSimpleText("#ChangeCurrencyBalance Normal -" + str(useAmountValue) + " " + userSteamId)
                                    elif useAmountType == "2":
                                        reduceUserAmount(str(useAmountValue), userSteamId, 0)
                                    updateUserPersonSkillData(userSteamId, playerPGCardData)
                                    inputSimpleText("#Announce 恭喜玩家" + orderUserName + "习得【" + skillName + "】技能！！！")
    except Exception as e:
        try:
            printToLog(e)
        finally:
            e = None
            del e


def cancelPlayerSkill(cmdArr):
    if len(cmdArr) != 3:
        inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
    else:
        try:
            cmdStmid = cmdArr[1]
            skillName = cmdArr[2]
            playerPGCardData = getUserPersonSkillData(cmdStmid)
            if skillName not in playerPGCardData:
                inputSimpleText("南极熊机器人管理命令提示：该玩家未习得【" + skillName + "】技能，无法取消~")
            else:
                del playerPGCardData[skillName]
                updateUserPersonSkillData(cmdStmid, playerPGCardData)
                inputSimpleText("南极熊机器人管理命令提示：已取消该玩家的【" + skillName + "】技能~")
        except Exception as e:
            try:
                inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
                printToLog(e)
                printToLog("错误发生行号：" + traceback.format_exc())
                printToLog("获取数据出错，机器人重启中，如长时间未能恢复，请联系管理员协助解决")
                logging.error(str(datetime.now()))
                logging.error(traceback.format_exc())
            finally:
                e = None
                del e


def doPlayerUpSkill(inserStr):
    userInfo = getUserInfo(inserStr.split("&&&&&")[3], inserStr.split("&&&&&")[2])
    userMessage = inserStr.split("&&&&&")[2]
    if userInfo == False or len(userInfo) == 0:
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    regUser(inserStr.split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    hasSuccessSendSkill = False
    useAmountType = ""
    useAmountValue = 0
    try:
        if len(userDataInfo) == 1:
            orderUserName = "【" + inserStr.split("&&&&&")[3] + "】"
            playerPGCardData = getUserPersonSkillData(userSteamId)
            keywordMsgArr = inserStr.split("&&&&&")[2].split(" ")
            if len(keywordMsgArr) < 2:
                inputSimpleText(orderUserName + "的技能指令不正确，请检查指令~")
            else:
                skillName = keywordMsgArr[1]
                if skillName not in playerPGCardData:
                    inputSimpleText(orderUserName + "的未学习该技能，无法升级~")
                else:
                    newInserStrArr = inserStr.split("&&&&&")
                    newInserStrArr[2] = newInserStrArr[2].split(" ")
                    newInserStrArr[2] = newInserStrArr[2][0] + newInserStrArr[2][1]
                    newInserStrArr = "&&&&&".join(newInserStrArr)
                    if skillName in playerPGCardData and skillName != "":
                        playerPerGiftObj = playerPGCardData[skillName]
                        skillLevel = playerPerGiftObj["level"]
                        nextSkillLevel = int(skillLevel) + 1
                    if playerPerGiftObj:
                        endInsurTime = int(datetime.strptime(str(playerPerGiftObj["end_time"]), "%Y-%m-%d %H:%M:%S").timestamp())
                        nowTime = datetime.timestamp(datetime.now())
                        if nowTime > endInsurTime:
                            inputSimpleText(orderUserName + "的职业技能已过期，请重新学习，或呼叫管理员获得技能~")
                        else:
                            skillList = robotOptions["skillObjs"]
                            skillHave = False
                            skillObj = {}
                            for item in skillList:
                                if item["keyword"] == skillName:
                                    skillObj = item
                                    skillHave = True

                            if skillHave == True:
                                if nextSkillLevel > len(skillObj["list"]):
                                    inputSimpleText(orderUserName + "的【" + skillName + "】技能已是最高等级，无法继续升级哦~")
                                else:
                                    index = 1
                                    skillLevelObj = {}
                                    for leItem in skillObj["list"]:
                                        if index == nextSkillLevel:
                                            skillLevelObj = leItem
                                        index = index + 1

                                    hasNoFullAmount = False
                                    if skillLevelObj["upLevelAmountType"] != "":
                                        useAmountType = skillLevelObj["upLevelAmountType"]
                                        useAmountValue = int(float(skillLevelObj["upLevelPrice"]))
                                    if useAmountType == "1":
                                        userBalance = userInfo[3].split("Account balance: ")[1]
                                        if int(userBalance) < int(useAmountValue):
                                            hasNoFullAmount = True
                                    elif useAmountType == "2":
                                        userBalance = userDataInfo[0][3]
                                        if int(userBalance) < int(useAmountValue):
                                            hasNoFullAmount = True
                                    if hasNoFullAmount == True:
                                        inputSimpleText(orderUserName + "的余额不足，无法使用技能哦~")
                                    else:
                                        playerPGCardData[skillName]["level"] = str(nextSkillLevel)
                                        hasSuccessSendSkill = True
                                        inputSimpleText(orderUserName + "的【" + skillName + "】技能成功升至【" + skillLevelObj["keyword"] + "】！！！")
                                        updateUserPersonSkillData(userSteamId, playerPGCardData)
                        if hasSuccessSendSkill == True:
                            if useAmountType == "1":
                                inputSimpleText("#ChangeCurrencyBalance Normal -" + str(useAmountValue) + " " + userSteamId)
                            elif useAmountType == "2":
                                reduceUserAmount(str(useAmountValue), userSteamId, 0)
                            insertDataIntoSendedGift(newInserStrArr + "&&&&&" + userSteamId)
                            insertToSendedGiftData(newInserStrArr)
    except Exception as e:
        try:
            inputSimpleText("南极熊机器人命令提示：您的指令格式有误，请联系管理员协助解决")
            printToLog(e)
            printToLog("错误发生行号：" + traceback.format_exc())
            printToLog("获取数据出错，机器人重启中，如长时间未能恢复，请联系管理员协助解决")
            logging.error(str(datetime.now()))
            logging.error(traceback.format_exc())
        finally:
            e = None
            del e


def doPlayerUseSkill(inserStr):
    global lastLogsName
    userInfo = getUserInfo(inserStr.split("&&&&&")[3], inserStr.split("&&&&&")[2])
    userMessage = inserStr.split("&&&&&")[2]
    if userInfo == False or len(userInfo) == 0:
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    regUser(inserStr.split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    hasSuccessSendSkill = False
    useAmountType = ""
    useAmountValue = 0
    try:
        if len(userDataInfo) == 1:
            orderUserName = "【" + inserStr.split("&&&&&")[3] + "】"
            playerPGCardData = getUserPersonSkillData(userSteamId)
            keywordMsgArr = inserStr.split("&&&&&")[2].split(" ")
            if len(keywordMsgArr) < 2:
                inputSimpleText(orderUserName + "的技能指令不正确，请检查指令~")
            else:
                skillName = keywordMsgArr[1]
                if skillName not in playerPGCardData:
                    inputSimpleText(orderUserName + "的未学习该技能，无法使用~")
                else:
                    newInserStrArr = inserStr.split("&&&&&")
                    newInserStrArr[2] = newInserStrArr[2].split(" ")
                    newInserStrArr[2] = newInserStrArr[2][0] + newInserStrArr[2][1]
                    newInserStrArr = "&&&&&".join(newInserStrArr)
                    if skillName in playerPGCardData:
                        if skillName != "":
                            playerPerGiftObj = playerPGCardData[skillName]
                            skillLevel = playerPerGiftObj["level"]
                            if playerPerGiftObj:
                                endInsurTime = int(datetime.strptime(str(playerPerGiftObj["end_time"]), "%Y-%m-%d %H:%M:%S").timestamp())
                                nowTime = datetime.timestamp(datetime.now())
                                if nowTime > endInsurTime:
                                    inputSimpleText(orderUserName + "的职业技能已过期，请重新学习，或呼叫管理员获得技能~")
                                else:
                                    skillList = robotOptions["skillObjs"]
                                    skillHave = False
                                    skillObj = {}
                                    for item in skillList:
                                        if item["keyword"] == skillName:
                                            skillObj = item
                                            skillHave = True

                                    if skillHave == True:
                                        skillLevelObj = {}
                                        skillLevelHave = False
                                        index = 1
                                        for litem in skillObj["list"]:
                                            if index == int(skillLevel):
                                                skillLevelObj = litem
                                                skillLevelHave = True
                                            index = index + 1

                                        if skillLevelHave == True:
                                            hasNoFullAmount = False
                                            giftList = getUserGetedGiftDay(newInserStrArr, "")
                                            timeLen = len(giftList)
                                            isInMin = False
                                            if timeLen > int(skillLevelObj["dayMaxTime"]):
                                                inputSimpleText(orderUserName + "的职业技能今日使用已达最大次数，无法继续使用哦~")
                                                return False
                                            serverTime = inserStr.split("&&&&&")[5]
                                            localTime = inserStr.split("&&&&&")[1]
                                            if skillLevelObj["useAmountType"] != "":
                                                useAmountType = skillLevelObj["useAmountType"]
                                                useAmountValue = int(float(skillLevelObj["useAmount"]))
                                            if useAmountType == "1":
                                                userBalance = userInfo[3].split("Account balance: ")[1]
                                                if int(userBalance) < int(useAmountValue):
                                                    hasNoFullAmount = True
                                            elif useAmountType == "2":
                                                userBalance = userDataInfo[0][3]
                                                if int(userBalance) < int(useAmountValue):
                                                    hasNoFullAmount = True
                                            if hasNoFullAmount == True:
                                                inputSimpleText(orderUserName + "的余额不足，无法使用技能哦~")
                                            else:
                                                if giftList != None:
                                                    if len(giftList) > 0:
                                                        preServerTime = formatServerTimeToStemp(giftList[-1][1])
                                                        currentTime = formatServerTimeToStemp(serverTime)
                                                        diffTime = currentTime - preServerTime
                                                        waitTime = float(skillObj["coolTime"])
                                                        if diffTime < waitTime:
                                                            isInMin = True
                                                if isInMin == True:
                                                    inputSimpleText(orderUserName + "的职业技能冷却中，将于【" + str(diffTime) + "】秒后可再次使用~")
                                                elif skillObj["skillType"] == "1":
                                                    spStr = ""
                                                    spNum = int(skillLevelObj["itemNum"] or 1)
                                                    spLocations = []
                                                    spFX = ""
                                                    spDict = skillObj["maxDisct"]
                                                    if len(keywordMsgArr) > 2:
                                                        if keywordMsgArr[2]:
                                                            spFX = keywordMsgArr[2]
                                                        if len(keywordMsgArr) > 3:
                                                            if keywordMsgArr[3]:
                                                                spDict = keywordMsgArr[3]
                                                    if skillObj["maxDisct"] != "" and float(spDict) > float(skillObj["maxDisct"]):
                                                        inputSimpleText(orderUserName + "的技能施放距离超出最大距离，最大距离为【" + skillObj["maxDisct"] + "】米~")
                                                    elif skillObj["minDisct"] != "" and float(spDict) < float(skillObj["minDisct"]):
                                                        inputSimpleText(orderUserName + "的技能施放距离超出最小距离，最小距离为【" + skillObj["minDisct"] + "】米~")
                                                    elif spFX not in ('W', 'w', 'E',
                                                                      'e', 'N', 'n',
                                                                      'S', 's'):
                                                        inputSimpleText(orderUserName + "的技能施放方向参数不正确，请检查指令~")
                                                    else:
                                                        if skillObj["itemType"] == "1":
                                                            spStr = "#spawnzombie"
                                                        elif skillObj["itemType"] == "2":
                                                            spStr = "#spawnanimal"
                                                        if skillLevelObj["itemCode"] != "":
                                                            spStr = spStr + " " + skillLevelObj["itemCode"]
                                                        playerCurrentLoc = getPlayerCurrentLocation(userSteamId)
                                                        spHeight = ""
                                                        try:
                                                            if "spItemHeight" in skillObj:
                                                                if skillObj["spItemHeight"] != "":
                                                                    spHeight = int(skillObj["spItemHeight"])
                                                        except Exception as e:
                                                            try:
                                                                spHeight = ""
                                                            finally:
                                                                e = None
                                                                del e

                                                        spLocations = getSpItemPYLocs(playerCurrentLoc, spFX, spNum, spDict, spHeight)
                                                        if len(spLocations) > 0:
                                                            inputSimpleText("#Announce 玩家" + orderUserName + "发动【" + skillName + "】技能！！！")
                                                            for spItem in spLocations:
                                                                newStr = spStr + ' 1 Location "' + " ".join(spItem) + '"'
                                                                inputSimpleText(newStr)

                                                            hasSuccessSendSkill = True
                                                elif skillObj["skillType"] == "2":
                                                    sqId = findSquadMemberNo(userSteamId)
                                                    targetName = ""
                                                    targetSteamId = ""
                                                    if len(keywordMsgArr) > 2:
                                                        if keywordMsgArr[2]:
                                                            targetName = keywordMsgArr[2]
                                                    if targetName == "":
                                                        inputSimpleText(orderUserName + "的技能参数缺少目标，请检查指令~")
                                                    else:
                                                        isSameSquad = False
                                                        if sqId != "":
                                                            sqList = findSquadMemberList(sqId)
                                                            isSameSquad = False
                                                            if len(sqList) > 0:
                                                                for sqitem in sqList:
                                                                    itemData = sqitem.split(" ")
                                                                    if targetName in itemData:
                                                                        isSameSquad = True
                                                                        for sqPItem in itemData:
                                                                            if "7656" in sqPItem:
                                                                                targetSteamId = sqPItem

                                                        if isSameSquad == True:
                                                            inputSimpleText("#Announce 玩家" + orderUserName + "发动【" + skillName + "】技能！！！")
                                                            inputSimpleText("#TeleportTo " + userSteamId + " " + targetSteamId)
                                                            hasSuccessSendSkill = True
                                                elif skillObj["skillType"] == "3":
                                                    file_content2 = []
                                                    hasAvenger = False
                                                    avengerTargetId = ""
                                                    if lastLogsName["kill"]:
                                                        with open((directory + "/Logs/" + lastLogsName["kill"]), "r", encoding="UTF-16 LE") as file:
                                                            fileData = file.read()
                                                            file_content2 = fileData.split("\n")
                                                    for fiItem in file_content2:
                                                        if fiItem != "":
                                                            if '{"Killer"' in fiItem:
                                                                fiObj = fiItem.split(": ")
                                                                fiTime = fiObj[0]
                                                                fiObj.pop(0)
                                                                fiObj = ": ".join(fiObj)
                                                                fiObj = json.loads(fiObj)
                                                                if "Victim" in fiObj:
                                                                    if fiObj["Victim"]["UserId"] == userSteamId:
                                                                        preServerTime = formatServerTimeToStemp(fiTime)
                                                                        currentTime = formatServerTimeToStemp(serverTime)
                                                                        if currentTime - preServerTime < 180:
                                                                            hasAvenger = True
                                                                            avengerTargetId = fiObj["Killer"]["UserId"]

                                                    if hasAvenger == False:
                                                        inputSimpleText("未查询到" + orderUserName + "的3分钟内被击杀记录，请稍后再试~")
                                                    else:
                                                        inputSimpleText("#Announce 玩家" + orderUserName + "发动【" + skillName + "】技能！！！")
                                                        inputSimpleText("#teleport  -723704.250 210814.297 44028.504 " + avengerTargetId)
                                                        hasSuccessSendSkill = True
                                                elif skillObj["skillType"] == "4":
                                                    targetName = ""
                                                    targetSteamId = ""
                                                    if len(keywordMsgArr) > 2:
                                                        if keywordMsgArr[2]:
                                                            targetName = keywordMsgArr[2]
                                                    if targetName == "":
                                                        inputSimpleText(orderUserName + "的技能参数缺少目标，请检查指令~")
                                                    else:
                                                        inputSimpleText("#Announce 玩家" + orderUserName + "发动【" + skillName + "】技能！！！")
                                                        targetInfo = getUserInfoByNameFromTotal(targetName)
                                                        targetId = targetInfo[1].split("(")[-1].split(")")[0]
                                                        targetPlayerLoc = getUserLocation(targetId)
                                                        targetIsOffline = False
                                                        if targetPlayerLoc == "no find player":
                                                            targetIsOffline = True
                                                        if targetIsOffline == True:
                                                            inputSimpleText("玩家" + orderUserName + "的目标不在线~")
                                                        else:
                                                            curPDist = getPlayerDisFubenDist(userSteamId, targetPlayerLoc)
                                                            inputSimpleText("玩家" + orderUserName + "与目标的距离为：【" + str(curPDist) + "】米！！！")
                                                            hasSuccessSendSkill = True
                                                elif skillObj["skillType"] == "5":
                                                    inMinList = []
                                                    allPlayerList = getAllPlayerList()
                                                    curPlayerLoc = getUserLocation(userSteamId)
                                                    for apItem in allPlayerList:
                                                        if apItem["steamid"] != userSteamId:
                                                            apLoc = apItem["location"]
                                                            apDist = calPlayerToPlayerDist(curPlayerLoc, apLoc)
                                                            if apDist < 200:
                                                                inMinList.append(apItem["steamid"])

                                                    inputSimpleText("#Announce 玩家" + orderUserName + "发动【" + skillName + "】技能！！！")
                                                    inputSimpleText("玩家" + orderUserName + "附近200米范围内存在玩家数量为【" + str(len(inMinList)) + "】人！！！")
                                                    hasSuccessSendSkill = True
                if hasSuccessSendSkill == True:
                    if useAmountType == "1":
                        inputSimpleText("#ChangeCurrencyBalance Normal -" + str(useAmountValue) + " " + userSteamId)
                    elif useAmountType == "2":
                        reduceUserAmount(str(useAmountValue), userSteamId, 0)
                    insertDataIntoSendedGift(newInserStrArr + "&&&&&" + userSteamId)
                    insertToSendedGiftData(newInserStrArr)
    except Exception as e:
        try:
            inputSimpleText("南极熊机器人命令提示：您的指令格式有误，请联系管理员协助解决")
            printToLog(e)
            printToLog("错误发生行号：" + traceback.format_exc())
            printToLog("获取数据出错，机器人重启中，如长时间未能恢复，请联系管理员协助解决")
            logging.error(str(datetime.now()))
            logging.error(traceback.format_exc())
        finally:
            e = None
            del e


def getSpItemPYLocs(center, spType, num, dist, spHeight):
    result = []
    locX = float(center[0])
    locY = float(center[1])
    locZ = float(center[2])
    dist = int(dist)
    pyDist = -500
    if spHeight == "":
        locZ = locZ + 1000
    else:
        locZ = locZ + int(spHeight) * 100
    if spType == "W" or spType == "w":
        locX = locX + dist * 100
    if spType == "E" or spType == "e":
        locX = locX - dist * 100
    if spType == "S" or spType == "s":
        locY = locY - dist * 100
    if spType == "N" or spType == "n":
        locY = locY + dist * 100
    for i in range(int(num)):
        if i == 0:
            result.append([str(locX), str(locY), str(locZ)])
        if not not spType == "W":
            if not not spType == "w":
                if spType == "E" or spType == "e":
                    newY = locY + pyDist
                    result.append([str(locX), str(newY), str(locZ)])
                if not not spType == "S":
                    if not not spType == "s":
                        if spType == "N" or spType == "n":
                            newX = locX + pyDist
                            result.append([str(newX), str(locY), str(locZ)])
                        pyDist = pyDist - 500
                        if pyDist < -1000:
                            pyDist = 1000

    return result


def getPlayerCurrentLocation(steamid):
    result = []
    curPlayerLoc = getUserLocation(steamid)
    if curPlayerLoc == "no find player":
        return curPlayerLoc
    curObj = curPlayerLoc.split(" ")
    curX = curObj[0]
    if "=" in curX:
        curX = curX.split("=")[1]
    curY = curObj[1]
    if "=" in curY:
        curY = curY.split("=")[1]
    curZ = curObj[2]
    if "=" in curZ:
        curZ = curZ.split("=")[1]
    result = [
     curX, curY, curZ]
    return result


def sendUserPersonGiftCard(inserStr):
    userInfo = getUserInfo(inserStr.split("&&&&&")[3], inserStr.split("&&&&&")[2])
    userMessage = inserStr.split("&&&&&")[2]
    if userInfo == False or len(userInfo) == 0:
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    regUser(inserStr.split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    try:
        if len(userDataInfo) == 1:
            orderUserName = "【" + inserStr.split("&&&&&")[3] + "】"
            playerPGCardData = getUserPersonGiftCard(userSteamId)
            if userMessage in playerPGCardData:
                playerPerGiftObj = playerPGCardData[userMessage]
                if playerPGCardData:
                    endInsurTime = int(datetime.strptime(str(playerPerGiftObj["end_time"]), "%Y-%m-%d %H:%M:%S").timestamp())
                    nowTime = datetime.timestamp(datetime.now())
                    if nowTime > endInsurTime:
                        inputSimpleText(orderUserName + "的装备卡已过期")
                    else:
                        keywordMsgArr = inserStr.split("&&&&&")[2].split("/")
                        mainName = keywordMsgArr[0]
                        childName = keywordMsgArr[1]
                        childObj = {}
                        for item in totalRobotOptions["vipgifts"]:
                            if item == mainName:
                                if totalRobotOptions["vipgifts"][item]["giftType"] == "2":
                                    childList = totalRobotOptions["vipgifts"][item]["gifts"]
                                    for citem in childList:
                                        if citem == childName:
                                            childObj = childList[citem]

                        if childObj:
                            currentDayUserGetCount = 0
                            currentUserGetedCount = 0
                            oldArr = getUserGetedGiftTotal(inserStr, userMessage)
                            if oldArr:
                                currentUserGetedCount = len(oldArr)
                            oldArr = getUserGetedGiftDay(inserStr, userMessage)
                            if oldArr:
                                currentDayUserGetCount = len(oldArr)
                            dayMax = childObj["dayMaxCount"]
                            totalMax = childObj["totalMaxCount"]
                            if dayMax != -1 and currentDayUserGetCount > dayMax:
                                inputSimpleText(orderUserName + "的装备卡今日领取次数已用完")
                            elif totalMax != -1 and currentUserGetedCount > totalMax:
                                inputSimpleText(orderUserName + "的装备卡总领取次数已用完")
                            else:
                                sendObj = {'inserStr':inserStr, 
                                 'data':childObj}
                                doSendGift(sendObj)
    except Exception as e:
        try:
            printToLog(e)
        finally:
            e = None
            del e


def fatchUserPlayerAdmin(inserStr):
    userInfo = getUserInfo(inserStr.split("&&&&&")[3], inserStr.split("&&&&&")[2])
    if userInfo == False or len(userInfo) == 0:
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    regUser(inserStr.split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    if len(userDataInfo) == 1:
        orderUserName = "【" + inserStr.split("&&&&&")[3] + "】"
        with open((directory + "/adminUserList.txt"), "r", encoding="UTF-8") as file:
            oldData = file.read()
        if oldData == "" or oldData == None:
            oldObj = []
        else:
            stream = io.StringIO(oldData)
            oldObj = json.load(stream)
        havePlayer = False
        if len(oldObj) > 0:
            currentTimeStamp = datetime.timestamp(datetime.now())
            for item in oldObj:
                if item["steamid"] == userSteamId:
                    havePlayer = True
                    itemEndtamp = datetime.timestamp(datetime.strptime(item["endTime"], "%Y-%m-%d %H:%M:%S"))
                    diffTime = (itemEndtamp - currentTimeStamp) / 60
                    inputSimpleText("玩家" + orderUserName + "剩余建家权限时长：【" + str(int(diffTime)) + "】分钟")
                    if "godAdminInfo" in robotOptions:
                        if robotOptions["godAdminInfo"] != "":
                            inputSimpleText(robotOptions["godAdminInfo"])

        if havePlayer == False:
            inputSimpleText("未找到玩家" + orderUserName + "的权限信息，请检查玩家id是否正确")


def doResetPlayerLevelInfo(cmdArr, valType=0):
    if valType == 0:
        return False
    results = []
    datatableConnectLocal = sqlite3.connect("beijixiong.db")
    cursor = datatableConnectLocal.cursor()
    if valType == 1 or valType == 3:
        cursor.execute("SELECT * FROM user_list")
    else:
        if valType == 2 or valType == 4:
            if len(cmdArr) != 2:
                inputSimpleText("南极熊管理命令提示：您的命令格式有误")
                return False
            steamid = cmdArr[1]
            cursor.execute("SELECT * FROM user_list WHERE steam_id = ?", (steamid,))
    inputSimpleText("南极熊管理命令提示：重置玩家数据中...")
    results = cursor.fetchall()
    cursor.close()
    datatableConnectLocal.close()
    for item in results:
        if len(item) > 10:
            obj = {"steam_id": (item[10])}
            if not not valType == 1 or valType == 2:
                obj["normal_integral"] = int(0)
                obj["normal_vip_level"] = int(0)
        if not not valType == 3:
            if valType == 4:
                obj["integral"] = int(0)
                obj["vip_level"] = int(0)
            updateDataToUser(obj)
            normalVipLevel = getUserNormalVipLevel(item[10]) or "0"
            vipLevel = getUserVipLevel(item[10]) or "0"
            customTitle = getUserCustomTitle(item[10]) or ""
            updata = {'steam_id':item[10], 
             'normal_vip_level':normalVipLevel, 
             'vip_level':vipLevel, 
             'custom_title':customTitle}
            updateDataToUser(updata)

    if valType == 2 or valType == 4:
        uperName = ""
        uperInfo = getUserInfoBySteamidFromTotal(item[10])
        if uperInfo and len(uperInfo) > 0:
            uperNameArr = uperInfo[0].split(". ")
            uperNameArr.pop(0)
            uperName = ". ".join(uperNameArr)
            if uperName:
                resetPlayerName(uperName, updata, "init")
    else:
        updateAllPlayerName()
    inputSimpleText("南极熊管理命令提示：已成功重置玩家数据！！！")


needSendSetAdminArr = []

def doAdminCmd(val, inserStr):
    userInfo = getUserInfo(inserStr.split("&&&&&")[3], inserStr.split("&&&&&")[2])
    if userInfo == False or len(userInfo) == 0:
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    if userSteamId not in robotOptions["adminSteamid"]:
        ui.press("enter")
        return False
    adminGiveSkillKeyword = ""
    adminCancelSkillKeyword = ""
    if "skillOptions" in robotOptions:
        skillOptions = robotOptions["skillOptions"]
        if "adminGiveSkillKeyword" in skillOptions:
            if skillOptions["adminGiveSkillKeyword"] != "":
                adminGiveSkillKeyword = skillOptions["adminGiveSkillKeyword"]
            if "adminCancelSkillKeyword" in skillOptions:
                if skillOptions["adminCancelSkillKeyword"] != "":
                    adminCancelSkillKeyword = skillOptions["adminCancelSkillKeyword"]
    cmdArr = val.split("LogSCUM: Message: ")[1].split(": ")[1].split(" ")
    if cmdArr[0] == "@初始化称号":
        printToLog("收到初始化称号命令")
        updateAllPlayerName()
        inputSimpleText("南极熊机器人管理命令提示：在线玩家称号初始化完成")
    elif cmdArr[0] == adminGiveSkillKeyword and adminGiveSkillKeyword != "":
        givePlayerSkill(cmdArr)
    elif cmdArr[0] == adminCancelSkillKeyword and adminCancelSkillKeyword != "":
        cancelPlayerSkill(cmdArr)
    elif cmdArr[0] == "@重置称号":
        doResetPlayerLevelInfo(cmdArr, 2)
    elif cmdArr[0] == "@重置所有人称号":
        doResetPlayerLevelInfo(cmdArr, 1)
    elif cmdArr[0] == "@重置VIP":
        doResetPlayerLevelInfo(cmdArr, 4)
    elif cmdArr[0] == "@重置所有人VIP":
        doResetPlayerLevelInfo(cmdArr, 3)
    elif cmdArr[0] == "@更新联办":
        fatchBanListAndBan()
    elif cmdArr[0] == "@授予装备卡":
        givePlayerPersonGiftCard(cmdArr)
    elif cmdArr[0] == "@取消装备卡":
        ungivePlayerPersonGiftCard(cmdArr)
    elif cmdArr[0] == "@授予权限":
        givePlayerAdmin(cmdArr)
    elif cmdArr[0] == "@查询所有权限":
        fatchAllPlayerAdmin()
    elif cmdArr[0] == "@查询指定权限":
        fatchSinglePlayerAdmin(cmdArr)
    elif cmdArr[0] == "@取消权限":
        giveupPlayerAdmin(cmdArr)
    elif cmdArr[0] == "@权限监控":
        startMonitorPlayerAdmin(cmdArr)
    elif cmdArr[0] == "@取消监控":
        endMonitorPlayerAdmin(cmdArr)
    elif cmdArr[0] == "@重置红包":
        resetHBData()
        inputSimpleText("南极熊机器人管理命令提示：红包系统重置成功")
    elif cmdArr[0] == "@清理垃圾":
        doCleanLaJi()
    elif cmdArr[0] == "@重启机器人":
        adminRestartRobot()
    elif "carInsurAdminKeyword" in robotOptions and cmdArr[0] == robotOptions["carInsurAdminKeyword"]:
        adminGiveCarInsurToPlayer(cmdArr)
    elif len(cmdArr) != 3:
        try:
            cmdName = cmdArr[0]
            cmdStmid = cmdArr[1]
            if len(cmdArr) == 2 and cmdName == "@取消自定义称号":
                currentNormalVipLevel = str(getUserNormalVipLevel(cmdStmid))
                currentVipLevel = str(getUserVipLevel(cmdStmid))
                updateUserData = {
                  'steam_id': cmdStmid,
                  'vip_level': currentVipLevel,
                  'normal_vip_level': currentNormalVipLevel,
                  'custom_title': ""}
                updateDataToUser(updateUserData)
                inputSimpleText("南极熊机器人管理命令提示：玩家称号等级修改成功")
                uperInfo = getUserInfoBySteamidFromTotal(cmdStmid)
                if uperInfo and len(uperInfo) > 0:
                    uperNameArr = uperInfo[0].split(". ")
                    uperNameArr.pop(0)
                    uperName = ". ".join(uperNameArr)
                    resetPlayerName(uperName, updateUserData, "custom")
                else:
                    inputSimpleText("未找到玩家【" + cmdStmid + "】的信息，玩家可能不在线，跳过本次任务")
            else:
                printToLog("管理命令错误")
                inputSimpleText("南极熊机器人管理命令提示：机器人管理命令错误")
        except Exception as e:
            try:
                printToLog("管理命令错误")
                inputSimpleText("南极熊机器人管理命令提示：机器人管理命令错误")
            finally:
                e = None
                del e

    else:
        cmdName = cmdArr[0]
        cmdStmid = cmdArr[1]
        cmdVal = cmdArr[2]
        userDataInfo = fatchUser(cmdStmid)
        if len(userDataInfo) == 0:
            printToLog("未找到管理员命令所属玩家")
            inputSimpleText("南极熊机器人管理命令提示：未找到管理员命令所属玩家，请检查玩家steamid")
        elif len(userDataInfo) > 1:
            printToLog("查询到多个玩家数据")
            inputSimpleText("南极熊机器人管理命令提示：查询到多个玩家数据，请确认数据正确性")
        else:
            if cmdName == "@设置自定义称号":
                currentNormalVipLevel = str(getUserNormalVipLevel(cmdStmid))
                currentVipLevel = str(getUserVipLevel(cmdStmid))
                updateUserData = {
                  'steam_id': cmdStmid,
                  'vip_level': currentVipLevel,
                  'normal_vip_level': currentNormalVipLevel,
                  'custom_title': cmdVal}
                updateDataToUser(updateUserData)
                inputSimpleText("南极熊机器人管理命令提示：玩家称号等级修改成功")
                uperInfo = getUserInfoBySteamidFromTotal(cmdStmid)
                if uperInfo and len(uperInfo) > 0:
                    uperNameArr = uperInfo[0].split(". ")
                    uperNameArr.pop(0)
                    uperName = ". ".join(uperNameArr)
                    resetPlayerName(uperName, updateUserData, "custom")
                else:
                    inputSimpleText("未找到玩家【" + cmdStmid + "】的信息，玩家可能不在线，跳过本次任务")
            if cmdName == "@重置记录":
                resetObj = {'steamid':cmdStmid,  'keyword':cmdVal}
                adminResetUserKeyword(resetObj)
                inputSimpleText("南极熊机器人管理命令提示：玩家领取记录重置成功")
            if cmdName == "@修改称号等级":
                currentInt = "0"
                currentVipLevel = str(getUserVipLevel(cmdStmid))
                currentNormalVipLevel = str(getUserNormalVipLevel(cmdStmid))
                customTitle = getUserCustomTitle(cmdStmid)
                if "normalVipLevel" in totalRobotOptions:
                    vipLevelArrs = totalRobotOptions["normalVipLevel"]
                    for vipKey in vipLevelArrs:
                        if str(vipLevelArrs[vipKey]["keyword"]) == str(cmdVal):
                            currentNormalVipLevel = str(int(vipLevelArrs[vipKey]["upAmount"]) + 1)

                updateUserData = {
                  'steam_id': cmdStmid,
                  'vip_level': currentVipLevel,
                  'normal_vip_level': cmdVal,
                  'normal_integral': currentNormalVipLevel,
                  'custom_title': customTitle}
                updateDataToUser(updateUserData)
                inputSimpleText("南极熊机器人管理命令提示：玩家称号等级修改成功")
                uperInfo = getUserInfoBySteamidFromTotal(cmdStmid)
                if uperInfo and len(uperInfo) > 0:
                    uperNameArr = uperInfo[0].split(". ")
                    uperNameArr.pop(0)
                    uperName = ". ".join(uperNameArr)
                    resetPlayerName(uperName, updateUserData, "normal")
                else:
                    inputSimpleText("未找到玩家【" + cmdStmid + "】的信息，玩家可能不在线，跳过本次任务")
            if cmdName == "@修改vip等级":
                currentInt = str(getUserJifen(cmdStmid))
                currentNormalVipLevel = str(getUserNormalVipLevel(cmdStmid))
                customTitle = getUserCustomTitle(cmdStmid)
                if "vipLevel" in totalRobotOptions:
                    vipLevelArrs = totalRobotOptions["vipLevel"]
                    for vipKey in vipLevelArrs:
                        if str(vipLevelArrs[vipKey]["keyword"]) == str(cmdVal):
                            currentInt = str(int(vipLevelArrs[vipKey]["upAmount"]) + 1)

                updateUserData = {
                  'steam_id': cmdStmid,
                  'vip_level': cmdVal,
                  'normal_vip_level': currentNormalVipLevel,
                  'integral': currentInt,
                  'custom_title': customTitle}
                updateDataToUser(updateUserData)
                inputSimpleText("南极熊机器人管理命令提示：玩家VIP等级修改成功")
                uperInfo = getUserInfoBySteamidFromTotal(cmdStmid)
                if uperInfo and len(uperInfo) > 0:
                    uperNameArr = uperInfo[0].split(". ")
                    uperNameArr.pop(0)
                    uperName = ". ".join(uperNameArr)
                    resetPlayerName(uperName, updateUserData, "vip")
                else:
                    inputSimpleText("未找到玩家【" + cmdStmid + "】的信息，玩家可能不在线，跳过本次任务")
            if cmdName == "@修改vip到期时间":
                updateUserData = {'steam_id':cmdStmid,  'vip_end_time':cmdVal}
                updateDataToUser(updateUserData)
                inputSimpleText("南极熊机器人管理命令提示：玩家VIP到期时间修改成功")
            if cmdName == "@充值熊币":
                preAmount = userDataInfo[0][3]
                newAmount = int(preAmount) + int(cmdVal)
                updateUserData = {'steam_id':cmdStmid, 
                 'amount':newAmount}
                updateDataToUser(updateUserData)
                inputSimpleText("南极熊机器人管理命令提示：玩家熊币充值成功")
            if cmdName == "@扣除熊币":
                preAmount = userDataInfo[0][3]
                newAmount = int(preAmount) - int(cmdVal)
                updateUserData = {'steam_id':cmdStmid, 
                 'amount':newAmount}
                updateDataToUser(updateUserData)
                inputSimpleText("南极熊机器人管理命令提示：玩家熊币扣除成功")


def fatchBanListAndBan():
    directory = os.getcwd()
    oldArr = []
    printToLog("开始更新联办名单")
    inputSimpleText("南极熊机器人管理命令提示： 开始更新联办名单！！！")
    try:
        with open((directory + "/banData.txt"), "r", encoding="UTF-8") as file:
            printToLog("读取文件中")
            oldData = file.read()
            if oldData:
                oldArr = oldData.split("\n")
        response = requests.get(url="https://server.vipscum.cn/public/index.php/index/index/getBanList")
        result = json.loads(response.text)
        if result["code"] == 0:
            listData = result["data"]
            needBanList = []
            for item in listData:
                if item["steamid"] not in oldArr:
                    oldArr.append(item["steamid"])
                    needBanList.append(item["steamid"])

            for nitem in needBanList:
                inputSimpleText("#ban " + nitem)

            with open((directory + "/banData.txt"), "w", encoding="UTF-8") as f:
                f.write("\n".join(oldArr))
    except Exception as e:
        try:
            printToLog(e)
            printToLog("错误发生行号：" + traceback.format_exc())
            printToLog("获取数据出错，机器人重启中，如长时间未能恢复，请联系管理员协助解决")
            logging.error(str(datetime.now()))
            logging.error(traceback.format_exc())
        finally:
            e = None
            del e

    inputSimpleText("南极熊机器人管理命令提示： 更新联办名单完成！！！")
    printToLog("更新联办名单完成")


def reducePlayerAdmin(cmdArr):
    with open((directory + "/adminUserList.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    if oldData == "" or oldData == None:
        oldObj = []
    else:
        stream = io.StringIO(oldData)
        oldObj = json.load(stream)
    isHave = False
    newList = []
    for item in oldObj:
        if item["steamid"] != cmdArr[1]:
            newList.append(item)

    with open((directory + "/adminUserList.txt"), "w", encoding="UTF-8") as f:
        f.write(json.dumps(newList, ensure_ascii=False))


def giveupPlayerAdmin(cmdArr):
    if len(cmdArr) != 2:
        inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
    else:
        try:
            cmdName = cmdArr[0]
            cmdStmid = cmdArr[1]
            if setAdminIsReading == True:
                inputSimpleText("南极熊机器人管理命令提示：正在进行其他权限授予任务，请稍候再试......")
            else:
                if "showAdminUserId" in robotOptions and robotOptions["showAdminUserId"] == "1":
                    inputSimpleText("南极熊机器人管理命令提示：正在取消玩家【" + cmdStmid + "】权限中，请稍候......")
                else:
                    inputSimpleText("南极熊机器人管理命令提示：正在取消玩家权限中，请稍候......")
                threading.Thread(target=setAdminUser, args=(cmdStmid, 1, "", "", []), daemon=True).start()
        except Exception as e:
            try:
                inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
            finally:
                e = None
                del e


def ungivePlayerPersonGiftCard(cmdArr):
    if len(cmdArr) != 3:
        inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
    else:
        try:
            cmdName = cmdArr[0]
            cmdStmid = cmdArr[1]
            cmdGiftName = cmdArr[2]
            cmdGiftMainName = cmdArr[2].split("/")[0]
            cmdGiftChildName = cmdArr[2].split("/")[1]
            if cmdGiftMainName:
                if cmdGiftChildName:
                    userPersonGiftObj = getUserPersonGiftCard(cmdStmid)
                    if cmdGiftName in userPersonGiftObj:
                        newObj = {}
                        for item in userPersonGiftObj:
                            if item != cmdGiftName:
                                newObj[item] = userPersonGiftObj[item]

                        updateUserPersonGiftCard(cmdStmid, newObj)
                        inputSimpleText("南极熊机器人管理命令提示：装备卡取消成功")
        except Exception as e:
            try:
                inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
                printToLog(e)
                printToLog("错误发生行号：" + traceback.format_exc())
                printToLog("获取数据出错，机器人重启中，如长时间未能恢复，请联系管理员协助解决")
                logging.error(str(datetime.now()))
                logging.error(traceback.format_exc())
            finally:
                e = None
                del e


def givePlayerSkill(cmdArr):
    if len(cmdArr) != 5:
        inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
    else:
        try:
            cmdName = cmdArr[0]
            cmdStmid = cmdArr[1]
            cmdSkillName = cmdArr[2]
            cmdSkillLevel = cmdArr[3]
            cmdGiftDayLong = cmdArr[4]
            if cmdSkillName and cmdSkillLevel:
                giftsList = robotOptions["skillObjs"]
                userPerSkillObj = {
                  'name': "",
                  'level': 1,
                  'start_time': "",
                  'end_time': ""}
                for item in giftsList:
                    childObj = item
                    if "keyword" in childObj:
                        if childObj["keyword"] != "":
                            if cmdSkillName == childObj["keyword"]:
                                childGiftList = childObj["list"]
                                if int(cmdSkillLevel) <= len(childGiftList):
                                    userPerSkillObj["name"] = cmdSkillName
                                    userPerSkillObj["level"] = int(cmdSkillLevel)

                if "name" in userPerSkillObj and userPerSkillObj["name"] != "":
                    userPersonGiftObj = getUserPersonSkillData(cmdStmid)
                    userPerGiftName = userPerSkillObj["name"]
                    if userPerGiftName in userPersonGiftObj:
                        giftSendObj = userPersonGiftObj[userPerGiftName]
                        giftEndTime = int(datetime.strptime(str(giftSendObj["end_time"]), "%Y-%m-%d %H:%M:%S").timestamp())
                        nowTime = datetime.timestamp(datetime.now())
                        if nowTime > giftEndTime:
                            giftSendObj["end_time"] = datetime.fromtimestamp(datetime.timestamp(datetime.now()) + int(cmdGiftDayLong) * 24 * 60 * 60).strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            giftSendObj["end_time"] = datetime.fromtimestamp(int(datetime.strptime(str(giftSendObj["end_time"]), "%Y-%m-%d %H:%M:%S").timestamp()) + int(cmdGiftDayLong) * 24 * 60 * 60).strftime("%Y-%m-%d %H:%M:%S")
                        userPersonGiftObj[userPerGiftName] = giftSendObj
                    else:
                        userPerSkillObj["start_time"] = datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime("%Y-%m-%d %H:%M:%S")
                        userPerSkillObj["end_time"] = datetime.fromtimestamp(datetime.timestamp(datetime.now()) + int(cmdGiftDayLong) * 24 * 60 * 60).strftime("%Y-%m-%d %H:%M:%S")
                        userPersonGiftObj[userPerGiftName] = userPerSkillObj
                    updateUserPersonSkillData(cmdStmid, userPersonGiftObj)
                    inputSimpleText("南极熊机器人管理命令提示：职业技能授予成功，玩家可发送【@查询技能】查询本人拥有的职业技能")
                else:
                    inputSimpleText("南极熊机器人管理命令提示：没有找到技能或等级，无法授予，请检查技能和等级")
            else:
                inputSimpleText("南极熊机器人管理命令提示：没有找到技能或等级，无法授予，请检查技能和等级")
        except Exception as e:
            try:
                inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
                printToLog(e)
                printToLog("错误发生行号：" + traceback.format_exc())
                printToLog("获取数据出错，机器人重启中，如长时间未能恢复，请联系管理员协助解决")
                logging.error(str(datetime.now()))
                logging.error(traceback.format_exc())
            finally:
                e = None
                del e


def givePlayerPersonGiftCard(cmdArr):
    if len(cmdArr) != 4:
        inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
    else:
        try:
            cmdName = cmdArr[0]
            cmdStmid = cmdArr[1]
            cmdGiftName = cmdArr[2]
            cmdGiftMainName = cmdArr[2].split("/")[0]
            cmdGiftChildName = cmdArr[2].split("/")[1]
            cmdGiftDayLong = cmdArr[3]
            if cmdGiftMainName and cmdGiftChildName:
                giftsList = totalRobotOptions["vipgifts"]
                childGiftObj = {}
                userPerGiftName = ""
                for item in giftsList:
                    childObj = giftsList[item]
                    childMainName = ""
                    if "cardMainKeyword" in childObj:
                        childMainName = childObj["cardMainKeyword"]
                        childGiftList = childObj["gifts"]
                        for chItem in childGiftList:
                            childChildName = chItem
                            if childMainName == cmdGiftMainName:
                                if childChildName == cmdGiftChildName:
                                    childGiftObj = childGiftList[chItem]
                                    userPerGiftName = childObj["keyword"] + "/" + chItem

                if "showName" in childGiftObj:
                    userPersonGiftObj = getUserPersonGiftCard(cmdStmid)
                    if userPerGiftName == "":
                        inputSimpleText("南极熊机器人管理命令提示：没有找到礼包，无法授予，请检查礼包名")
                    else:
                        if userPerGiftName in userPersonGiftObj:
                            giftSendObj = userPersonGiftObj[userPerGiftName]
                            giftEndTime = int(datetime.strptime(str(giftSendObj["end_time"]), "%Y-%m-%d %H:%M:%S").timestamp())
                            nowTime = datetime.timestamp(datetime.now())
                            if nowTime > giftEndTime:
                                giftSendObj["end_time"] = datetime.fromtimestamp(datetime.timestamp(datetime.now()) + int(cmdGiftDayLong) * 24 * 60 * 60).strftime("%Y-%m-%d %H:%M:%S")
                            else:
                                giftSendObj["end_time"] = datetime.fromtimestamp(int(datetime.strptime(str(giftSendObj["end_time"]), "%Y-%m-%d %H:%M:%S").timestamp()) + int(cmdGiftDayLong) * 24 * 60 * 60).strftime("%Y-%m-%d %H:%M:%S")
                            userPersonGiftObj[userPerGiftName] = giftSendObj
                        else:
                            giftSendObj = {'start_time':(datetime.fromtimestamp(datetime.timestamp(datetime.now())).strftime)("%Y-%m-%d %H:%M:%S"), 
                             'end_time':(datetime.fromtimestamp(datetime.timestamp(datetime.now()) + int(cmdGiftDayLong) * 24 * 60 * 60).strftime)("%Y-%m-%d %H:%M:%S")}
                            userPersonGiftObj[userPerGiftName] = giftSendObj
                        updateUserPersonGiftCard(cmdStmid, userPersonGiftObj)
                        inputSimpleText("南极熊机器人管理命令提示：装备卡授予成功，玩家可发送【@查询装备卡】查询本人拥有的装备卡")
                else:
                    inputSimpleText("南极熊机器人管理命令提示：没有找到礼包，无法授予，请检查礼包名")
            else:
                inputSimpleText("南极熊机器人管理命令提示：没有找到礼包，无法授予，请检查礼包名")
        except Exception as e:
            try:
                inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
                printToLog(e)
                printToLog("错误发生行号：" + traceback.format_exc())
                printToLog("获取数据出错，机器人重启中，如长时间未能恢复，请联系管理员协助解决")
                logging.error(str(datetime.now()))
                logging.error(traceback.format_exc())
            finally:
                e = None
                del e


def givePlayerAdmin(cmdArr):
    if len(cmdArr) != 3:
        inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
    else:
        try:
            cmdName = cmdArr[0]
            cmdStmid = cmdArr[1]
            cmdVal = cmdArr[2]
            oldData = ""
            with open((directory + "/adminUserList.txt"), "r", encoding="UTF-8") as file:
                oldData = file.read()
            if oldData == "" or oldData == None:
                oldObj = []
            else:
                stream = io.StringIO(oldData)
                oldObj = json.load(stream)
            isHave = False
            for item in oldObj:
                if item["steamid"] == cmdArr[1]:
                    isHave = True
                    inputSimpleText("南极熊机器人管理命令提示：该玩家已被授予权限...")

            if isHave == False:
                endTimeStr = datetime.fromtimestamp(datetime.timestamp(datetime.now()) + int(cmdVal) * 60).strftime("%Y-%m-%d %H:%M:%S")
                newObj = {'steamid':cmdArr[1], 
                 'endTime':endTimeStr}
                oldObj.append(newObj)
                if setAdminIsReading == True:
                    inputSimpleText("南极熊机器人管理命令提示：正在授予其他玩家权限中，请稍候再试......")
                else:
                    if "showAdminUserId" in robotOptions and robotOptions["showAdminUserId"] == "1":
                        inputSimpleText("南极熊机器人管理命令提示：正在授予玩家【" + cmdStmid + "】权限中，请稍候大约【1】分钟...")
                    else:
                        inputSimpleText("南极熊机器人管理命令提示：正在授予玩家权限中，请稍候大约【1】分钟...")
                    threading.Thread(target=setAdminUser, args=(cmdStmid, 2, cmdVal, endTimeStr, oldObj), daemon=True).start()
        except Exception as e:
            try:
                inputSimpleText("南极熊机器人管理命令提示：您的指令格式有误")
            finally:
                e = None
                del e


needSendStartMonitorAnnou = []

def startMonitorPlayerAdmin(cmdArr):
    global needSendStartMonitorAnnou
    oldData = ""
    with open((directory + "/monitorAdmin.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    if oldData == "" or oldData == None:
        oldObj = []
    else:
        stream = io.StringIO(oldData)
        oldObj = json.load(stream)
    isHave = False
    for item in oldObj:
        if item["steamid"] == cmdArr[1]:
            isHave = True
            if "showAdminUserId" in robotOptions:
                if robotOptions["showAdminUserId"] == "1":
                    needSendStartMonitorAnnou.append("南极熊机器人管理命令提示：玩家【" + cmdArr[1] + "】正在权限监控中...")
                needSendStartMonitorAnnou.append("南极熊机器人管理命令提示：玩家正在权限监控中...")

    if isHave == False:
        newObj = {'steamid':cmdArr[1],  'cmds':[]}
        oldObj.append(newObj)
        with open((directory + "/monitorAdmin.txt"), "w", encoding="UTF-8") as f:
            f.write(json.dumps(oldObj, ensure_ascii=False))
        if "showAdminUserId" in robotOptions and robotOptions["showAdminUserId"] == "1":
            needSendStartMonitorAnnou.append("南极熊机器人管理命令提示：玩家【" + cmdArr[1] + "】正在权限监控中...")
        else:
            needSendStartMonitorAnnou.append("南极熊机器人管理命令提示：玩家正在权限监控中...")


def sendStartMonitorAnnou():
    for item in needSendStartMonitorAnnou:
        inputSimpleText(item)


def adminRestartRobot():
    restartRobot()


def restartRobot():
    inputSimpleText("南极熊机器人管理命令提示： 机器人重启中....")
    printToLog("机器人重启中...")
    restartReadOptions()


def endMonitorPlayerAdmin(cmdArr):
    oldData = ""
    with open((directory + "/monitorAdmin.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    if oldData == "" or oldData == None:
        oldObj = []
    else:
        stream = io.StringIO(oldData)
        oldObj = json.load(stream)
    isHave = False
    newArr = []
    for item in oldObj:
        if item["steamid"] == cmdArr[1]:
            isHave = True
        else:
            newArr.append(item)

    if isHave == True:
        with open((directory + "/monitorAdmin.txt"), "w", encoding="UTF-8") as f:
            f.write(json.dumps(newArr, ensure_ascii=False))
        if "showAdminUserId" in robotOptions and robotOptions["showAdminUserId"] == "1":
            needSendStartMonitorAnnou.append("南极熊机器人管理命令提示：已取消对玩家【" + cmdArr[1] + "】的权限监控！")
        else:
            needSendStartMonitorAnnou.append("南极熊机器人管理命令提示：已取消对玩家的权限监控！")
    elif "showAdminUserId" in robotOptions and robotOptions["showAdminUserId"] == "1":
        needSendStartMonitorAnnou.append("南极熊机器人管理命令提示：未找到玩家【" + cmdArr[1] + "】，请核对id是否正确")
    else:
        needSendStartMonitorAnnou.append("南极熊机器人管理命令提示：未找到玩家，请核对id是否正确")


def checkUserVipIsOnline(steamid):
    vipIsOutTime = True
    userInfo = fatchUser(steamid)
    current = int(datetime.strptime(str(datetime.now()).split(" ")[0], "%Y-%m-%d").timestamp())
    vipenddate = "0"
    try:
        vipenddate = userInfo[0][8] or "0"
    except Exception as e:
        try:
            vipenddate = "0"
        finally:
            e = None
            del e

    if len(vipenddate) < 2:
        vipIsOutTime = False
    else:
        vipend = int(datetime.strptime(str(vipenddate), "%Y-%m-%d").timestamp())
        if current > vipend:
            vipIsOutTime = False
    return vipIsOutTime


def getSignDays(totalList):
    days = 0
    listArr = []
    isLine = True
    for i in totalList:
        listArr.append(i[3])

    printToLog(str(listArr))
    diffDay = 1
    while isLine == True:
        diffDayVal = (datetime.now() - timedelta(days=diffDay)).strftime("%Y-%m-%d")
        printToLog(diffDayVal)
        if diffDayVal in listArr:
            diffDay = diffDay + 1
        else:
            isLine = False

    return diffDay


def playerSignInDo(inserStr):
    userInfo = getUserInfo(inserStr.split("&&&&&")[3], inserStr.split("&&&&&")[2])
    if userInfo == False or len(userInfo) == 0:
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    orderUserName = inserStr.split("&&&&&")[3]
    regUser(inserStr.split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    curObj = str(datetime.now()).split(".")[0]
    curDate = curObj.split(" ")[0]
    curMonth = curObj.split("-")[0] + "-" + curObj.split("-")[1]
    curTime = curObj.split(" ")[1]
    if len(userDataInfo) == 1:
        logs = getSigninLogBySteamidAndDate(userSteamId, curDate)
        if logs and len(logs) > 0:
            inputSimpleText("玩家【" + orderUserName + "】今日已签到，无法再次签到")
        else:
            rewardNameStr = ""
            signObj = [orderUserName, userSteamId, curDate, curTime]
            createSigninLog(signObj)
            totalLogs = getSigninLogBySteamid(userSteamId)
            curMons = []
            for item in totalLogs:
                if curMonth in item[3]:
                    curMons.append(item)

            curSignTimes = len(curMons)
            signGiftObj = {}
            lineDays = 0
            reLens = 0
            reIndex = 0
            if "signInType" in robotOptions and robotOptions["signInType"] == "0" or "signInType" not in robotOptions:
                if "signRewardList" in robotOptions:
                    if len(robotOptions["signRewardList"]) > 0:
                        if curSignTimes >= len(robotOptions["signRewardList"]):
                            signGiftObj = robotOptions["signRewardList"][-1]
                        else:
                            signGiftObj = robotOptions["signRewardList"][curSignTimes - 1]
                    if "signInType" in robotOptions and robotOptions["signInType"] == "1":
                        if "signRewardList" in robotOptions and len(robotOptions["signRewardList"]) > 0:
                            lineDays = getSignDays(totalLogs)
                            reLens = len(robotOptions["signRewardList"])
                            reIndex = lineDays % reLens
                            if reIndex == 0:
                                if lineDays != 0:
                                    reIndex = len(robotOptions["signRewardList"])
                                signGiftObj = robotOptions["signRewardList"][reIndex - 1]
                            if "signInType" in robotOptions and robotOptions["signInType"] == "2" or "signInType" not in robotOptions:
                                if "signRewardList" in robotOptions and len(robotOptions["signRewardList"]) > 0:
                                    reLens = len(robotOptions["signRewardList"])
                                    reIndex = len(totalLogs) % reLens
                                    if reIndex == 0:
                                        if len(totalLogs) != 0:
                                            reIndex = len(robotOptions["signRewardList"])
                                        signGiftObj = robotOptions["signRewardList"][reIndex - 1]
                                    inputSimpleText("玩家【" + orderUserName + "】签到成功，签到奖励即将开始发货~")
                                    if "amount" in signGiftObj:
                                        if signGiftObj["amount"] != "":
                                            inputSimpleText("#ChangeCurrencyBalance Normal " + str(signGiftObj["amount"]) + " " + userSteamId)
                                            rewardNameStr = rewardNameStr + str(signGiftObj["amount"]) + "美金，"
                                        if "gold" in signGiftObj:
                                            if signGiftObj["gold"] != "":
                                                inputSimpleText("#ChangeCurrencyBalance gold " + str(signGiftObj["gold"]) + " " + userSteamId)
                                                rewardNameStr = rewardNameStr + str(signGiftObj["gold"]) + "金条，"
                                        if "xiongb" in signGiftObj and signGiftObj["xiongb"] != "":
                                            try:
                                                if signGiftObj["xiongb"] != "0":
                                                    preAmount = userDataInfo[0][3]
                                                    newAmount = int(preAmount) + int(int(float(signGiftObj["xiongb"])))
                                                    updateUserData = {'steam_id':userSteamId, 
                                                     'amount':newAmount}
                                                    updateDataToUser(updateUserData)
                                                    rewardNameStr = rewardNameStr + str(int(float(signGiftObj["xiongb"]))) + "熊币，"
                                            except Exception:
                                                pass

                                            if "fame" in signGiftObj:
                                                if signGiftObj["fame"] != "":
                                                    try:
                                                        if signGiftObj["fame"] != "0":
                                                            oldFame = int(userInfo[2].replace(" ", "", 50).split(":")[1])
                                                            goodFame = int(int(float(signGiftObj["fame"])))
                                                            newFame = str(oldFame + goodFame)
                                                            inputSimpleText("#SetFamePoints " + newFame + " " + userSteamId)
                                                            rewardNameStr = rewardNameStr + str(goodFame) + "声望，"
                                                    except Exception:
                                                        pass

            if "item" in signGiftObj and signGiftObj["item"] != "":
                try:
                    if signGiftObj["item"] != "":
                        rewardCodes = signGiftObj["item"].split(",")
                        for i in rewardCodes:
                            inputSimpleText(i + " Location " + userSteamId)

                        rewardNameStr = rewardNameStr + "许多物品装备，"
                except Exception:
                    pass

                if "signInType" in robotOptions and robotOptions["signInType"] == "1":
                    inputSimpleText("玩家【" + orderUserName + "】签到成功，获得签到奖励【" + rewardNameStr + "】，奖励已成功发放，当前连续签到次数为【" + str(reIndex) + "/" + str(reLens) + "】，已连续签到【" + str(lineDays) + "】天，本月已签到【" + str(len(curMons)) + "】天，共累计签到【" + str(len(totalLogs)) + "】天~祝您玩的开心~玩的愉快~")
                elif "signInType" in robotOptions and robotOptions["signInType"] == "2":
                    inputSimpleText("玩家【" + orderUserName + "】签到成功，获得签到奖励【" + rewardNameStr + "】，奖励已成功发放，本轮连续签到次数为【" + str(reIndex) + "/" + str(reLens) + "】，共累计签到【" + str(len(totalLogs)) + "】天~祝您玩的开心~玩的愉快~")
                else:
                    inputSimpleText("玩家【" + orderUserName + "】签到成功，获得签到奖励【" + rewardNameStr + "】，奖励已成功发放，本月已签到【" + str(len(curMons)) + "】天，共累计签到【" + str(len(totalLogs)) + "】天~祝您玩的开心~玩的愉快~")


def doFatchUserNormalInit(inserStr):
    userInfo = getUserInfo(inserStr.split("&&&&&")[3], inserStr.split("&&&&&")[2])
    if userInfo == False or len(userInfo) == 0:
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    regUser(inserStr.split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    if len(userDataInfo) == 1:
        amount = userDataInfo[0][3]
        orderUserName = "【" + inserStr.split("&&&&&")[3] + "】"
        vipLevelArr = totalRobotOptions["normalVipLevel"]
        vipName = "无"
        if userDataInfo[0][12] != "0":
            if userDataInfo[0][12] != None:
                vipName = vipLevelArr[userDataInfo[0][12]]["name"]
            vipEndTime = "无"
            vipIsOnline = checkUserVipIsOnline(userSteamId)
            outStr = orderUserName + "，您当前的称号等级为：【" + vipName + "】"
            curVipLevel = int(userDataInfo[0][12])
            curPoint = int(float(userDataInfo[0][11]))
            nextVipLevel = str(curVipLevel + 1)
            nextNeedPoint = 0
            if nextVipLevel in vipLevelArr:
                nextPoint = int(vipLevelArr[nextVipLevel]["upAmount"])
                nextNeedPoint = str(nextPoint - curPoint)
        outStr = outStr + "，当前积分为：【" + str(userDataInfo[0][11]) + "】，距离称号升下一级还需要【" + str(nextNeedPoint) + "】积分"
        inputSimpleText(outStr)


def doFatchUserAmount(inserStr):
    userInfo = getUserInfo(inserStr.split("&&&&&")[3], inserStr.split("&&&&&")[2])
    if userInfo == False or len(userInfo) == 0:
        return False
    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
    regUser(inserStr.split("&&&&&")[3], userSteamId)
    userDataInfo = fatchUser(userSteamId)
    if len(userDataInfo) == 1:
        amount = userDataInfo[0][3]
        orderUserName = "【" + inserStr.split("&&&&&")[3] + "】"
        vipLevelArr = totalRobotOptions["vipLevel"]
        vipName = "无"
        if userDataInfo[0][7] != "0":
            vipName = vipLevelArr[userDataInfo[0][7]]["name"]
        vipEndTime = "无"
        try:
            if userDataInfo[0][8]:
                if len(userDataInfo[0][8]) > 0:
                    vipEndTime = userDataInfo[0][8]
        except Exception as e:
            try:
                vipEndTime = "无"
            finally:
                e = None
                del e

        vipIsOnline = checkUserVipIsOnline(userSteamId)
        if userDataInfo[0][7] != "0":
            if vipIsOnline == True:
                orderUserName = "尊贵的【" + vipName + "-" + inserStr.split("&&&&&")[3] + "】"
            vipIsOnline = checkUserVipIsOnline(userSteamId)
            outStr = ""
            if vipIsOnline == True:
                outStr = orderUserName + "，您当前的南极熊币余额为：【" + amount + "】，VIP等级为：【" + vipName + "】，VIP到期时间为：【" + vipEndTime + "】"
            else:
                outStr = orderUserName + "，您当前的南极熊币余额为：【" + amount + "】，VIP等级为：【" + vipName + "】，VIP到期时间为：【" + vipEndTime + "】VIP已过期"
            if "isAllowVipAutoUp" in robotOptions:
                if robotOptions["isAllowVipAutoUp"] == 1:
                    curVipLevel = int(userDataInfo[0][7])
                    curPoint = int(float(userDataInfo[0][9]))
                    nextVipLevel = str(curVipLevel + 1)
                    nextNeedPoint = 0
                    if nextVipLevel in vipLevelArr:
                        nextPoint = int(vipLevelArr[nextVipLevel]["upAmount"])
                        nextNeedPoint = str(nextPoint - curPoint)
                    outStr = outStr + "，当前积分为：【" + str(userDataInfo[0][9]) + "】，距离VIP升下一级还需要【" + str(nextNeedPoint) + "】积分"
        inputSimpleText(outStr)


def checkArrIsHave(arr, instr):
    result = False
    for item in arr:
        if item["inserStr"] == instr:
            result = True

    return result


def checkMsgIsRepet(arr, name, keyword):
    result = False
    for item in arr:
        if name in item["inserStr"]:
            if keyword in item["inserStr"]:
                result = True

    return result


def checkGoodCustomNum(message):
    msg = message
    result = False
    try:
        if "*" in message:
            msg = message.split("*")[0]
            num = int(message.split("*")[1])
        if msg in goodsKeys:
            result = True
        return result
    except Exception:
        return False


def checkIsPersonGiftKeyword(message):
    msg = message
    result = False
    try:
        if "/" in message:
            msg = message.split("/")[0]
        if msg in vipGiftsKeys:
            result = True
        return result
    except Exception:
        return False


def checkForbiddenKeyword(val, inserStr):
    keywords = []
    hasForb = False
    forTime = 60
    if "forbiddenKeywords" in robotOptions:
        if robotOptions["forbiddenKeywords"] != "":
            keywords = robotOptions["forbiddenKeywords"].split("、")
            for item in keywords:
                if item != "":
                    message = val.split("LogSCUM: Message: ")[1].split(": ")[1]
                    if item in message:
                        hasForb = True

        if "forbiddenTime" in robotOptions and robotOptions["forbiddenTime"] != "":
            try:
                forTime = int(float(robotOptions["forbiddenTime"]))
            except Exception as e:
                try:
                    forTime = 60
                finally:
                    e = None
                    del e

            if hasForb == True:
                userInfo = getUserInfo(inserStr.split("&&&&&")[3], inserStr.split("&&&&&")[2])
                if userInfo == False or len(userInfo) == 0:
                    return False
                userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                preData = ""
                with open((directory + "/forbiddenPlayers.txt"), "r", encoding="UTF-8") as file:
                    preData = file.read()
                if userSteamId not in robotOptions["adminSteamid"]:
                    if userSteamId not in preData:
                        userName = inserStr.split("&&&&&")[3]
                        inputSimpleText("玩家【" + userName + "】触发了禁言词汇处罚，已被禁言【" + str(forTime) + "】分钟！！！")
                        inputSimpleText("#Silence " + userSteamId)
                        oldData = ""
                        oldObj = []
                        with open((directory + "/forbiddenPlayers.txt"), "r", encoding="UTF-8") as file:
                            oldData = file.read()
                        if oldData == "" or oldData == None:
                            oldObj = []
                        else:
                            stream = io.StringIO(oldData)
                            oldObj = json.load(stream)
                        forData = {'steamid':userSteamId,  'playerName':userName, 
                         'endTime':(datetime.fromtimestamp(datetime.timestamp(datetime.now()) + int(forTime * 60)).strftime)("%Y-%m-%d %H:%M:%S")}
                        oldObj.append(forData)
                        with open((directory + "/forbiddenPlayers.txt"), "w", encoding="UTF-8") as f:
                            f.write(json.dumps(oldObj, ensure_ascii=False))
                        if len(lastVIPGiftChatArr) > 50:
                            lastVIPGiftChatArr.pop(0)
                        if val in lastVIPGiftChatArr:
                            pass
                        else:
                            lastVIPGiftChatArr.append(val)
                        with open((directory + "/lastChatData.txt"), "w", encoding="UTF-8") as f:
                            f.write("\n".join(lastVIPGiftChatArr))
                        time.sleep(0.2)


def checkUnmutePlayer():
    oldData = ""
    oldObj = []
    with open((directory + "/forbiddenPlayers.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    if oldData == "" or oldData == None:
        oldObj = []
    else:
        stream = io.StringIO(oldData)
        oldObj = json.load(stream)
    currentTimeStamp = datetime.timestamp(datetime.now())
    newObj = []
    hasReduMute = False
    for item in oldObj:
        itemEndtamp = datetime.timestamp(datetime.strptime(item["endTime"], "%Y-%m-%d %H:%M:%S"))
        if currentTimeStamp > itemEndtamp:
            inputSimpleText("玩家【" + item["playerName"] + "】禁言时间已到，已解除禁言！！！")
            inputSimpleText("#Unsilence " + item["steamid"])
            hasReduMute = True
        else:
            newObj.append(item)

    if hasReduMute == True:
        with open((directory + "/forbiddenPlayers.txt"), "w", encoding="UTF-8") as f:
            f.write(json.dumps(newObj, ensure_ascii=False))


justUpNormalLevelWordKey = "@升级称号"

def getLocalLog():
    global adminKyes
    global initChoujiangKey
    global justUpNormalLevelWordKey
    timeCheckWaitTransData()
    localappdata = os.getenv("LOCALAPPDATA")
    f = open((localappdata + "/SCUM/Saved/Logs/SCUM.log"), encoding="utf-8")
    cont = f.read()
    f.close()
    contList = cont.split("\n")
    chatArrs = []
    for i in contList:
        if i.find("LogSCUM: Message: ") != -1:
            chatArrs.append(i)

    chatArrs.reverse()
    newChatArrs = []
    nameArrs = []
    for ci in chatArrs:
        if ci.find("LogSCUM: Message: ") != -1:
            ciName = ci.split("LogSCUM: Message: ")[1].split(": ")[0]
            if ciName not in nameArrs:
                if ci not in newChatArrs:
                    nameArrs.append(ciName)
                    newChatArrs.append(ci)

    shortChatArrs = newChatArrs[:3]
    key = 0
    needToSendNewGift = []
    needToSendFreeNewGift = []
    needToSendGood = []
    needToSendQA = []
    needToSendTrans = []
    needToSendDayGift = []
    zjLonghdUserPlayKeyword = "@龙虎斗/"
    tikaUserKeyword = "@提卡/"
    fhbUserKeyword = "@发红包/"
    recoveUserKeyword = "@回收/"
    squardTransKeyword = "@队友传送ded/"
    fubenUserKeyword = "@挑战/"
    if "qhbMainPlayerKeyword" in robotOptions:
        if robotOptions["qhbMainPlayerKeyword"] != "":
            fhbUserKeyword = robotOptions["qhbMainPlayerKeyword"] + "/"
        if "recoveKeyword" in robotOptions:
            if robotOptions["recoveKeyword"] != "":
                recoveUserKeyword = robotOptions["recoveKeyword"] + "/"
            if "requestSquardTransKeyword" in robotOptions:
                if robotOptions["requestSquardTransKeyword"] != "":
                    squardTransKeyword = robotOptions["requestSquardTransKeyword"] + "/"
                if "fubenMainKeyword" in robotOptions:
                    if robotOptions["fubenMainKeyword"] != "":
                        fubenUserKeyword = robotOptions["fubenMainKeyword"] + "/"
                    otherKeys = ["@查询在线","@查询熊币","@查询积分","@查询建家时长","@查询装备卡","@查询技能"]
                    carInsurKeys = []
                    if "singleKey" not in totalRobotOptions["choujiang"]:
                        if initChoujiangKey not in otherKeys:
                            otherKeys.append(initChoujiangKey)
                    otherKeys = otherKeys + adminKyes
                    if "longhudou" in totalRobotOptions:
                        if totalRobotOptions["longhudou"]["adminKeyword"] not in otherKeys:
                            otherKeys.append(totalRobotOptions["longhudou"]["adminKeyword"])
                        if "closeAdminKeyword" in totalRobotOptions["longhudou"]:
                            if totalRobotOptions["longhudou"]["closeAdminKeyword"] not in otherKeys:
                                otherKeys.append(totalRobotOptions["longhudou"]["closeAdminKeyword"])
                        if totalRobotOptions["longhudou"]["playerKeyword"] not in otherKeys:
                            otherKeys.append(totalRobotOptions["longhudou"]["playerKeyword"])
                if "zjLonghd" in totalRobotOptions:
                    zjLonghdUserPlayKeyword = totalRobotOptions["zjLonghd"]["userPlayKeyword"]
            if "justUpNormalLevelWord" in totalRobotOptions["options"]:
                if totalRobotOptions["options"]["justUpNormalLevelWord"] not in otherKeys:
                    otherKeys.append(totalRobotOptions["options"]["justUpNormalLevelWord"])
                    justUpNormalLevelWordKey = totalRobotOptions["options"]["justUpNormalLevelWord"]
        if "carInsurPlayerKeyword" in robotOptions and robotOptions["carInsurPlayerKeyword"] != "":
            if robotOptions["carInsurPlayerKeyword"] not in otherKeys:
                otherKeys.append(robotOptions["carInsurPlayerKeyword"])
                carInsurKeys.append(robotOptions["carInsurPlayerKeyword"])
            if "carInsurGetPlayerKeyword" in robotOptions and robotOptions["carInsurGetPlayerKeyword"] != "":
                if robotOptions["carInsurGetPlayerKeyword"] not in otherKeys:
                    otherKeys.append(robotOptions["carInsurGetPlayerKeyword"])
                    carInsurKeys.append(robotOptions["carInsurGetPlayerKeyword"])
                if "carInsurGetHideTimeKeyword" in robotOptions and robotOptions["carInsurGetHideTimeKeyword"] != "":
                    if robotOptions["carInsurGetHideTimeKeyword"] not in otherKeys:
                        otherKeys.append(robotOptions["carInsurGetHideTimeKeyword"])
                        carInsurKeys.append(robotOptions["carInsurGetHideTimeKeyword"])
                    if "requestSquardTransKeyword" in robotOptions and robotOptions["requestSquardTransKeyword"] != "":
                        if robotOptions["requestSquardTransKeyword"] not in otherKeys:
                            otherKeys.append(robotOptions["requestSquardTransKeyword"])
                        if "agreeSquardTransKeyword" in robotOptions and robotOptions["agreeSquardTransKeyword"] != "":
                            if robotOptions["agreeSquardTransKeyword"] not in otherKeys:
                                otherKeys.append(robotOptions["agreeSquardTransKeyword"])
                            if "playerSignInKeyword" in robotOptions and robotOptions["playerSignInKeyword"] != "":
                                if robotOptions["playerSignInKeyword"] not in otherKeys:
                                    otherKeys.append(robotOptions["playerSignInKeyword"])
                                if "playerBuyAdminKeyword" in robotOptions and robotOptions["playerBuyAdminKeyword"] != "":
                                    if robotOptions["playerBuyAdminKeyword"] not in otherKeys:
                                        otherKeys.append(robotOptions["playerBuyAdminKeyword"])
                                    if "recoveKeyword" in robotOptions and robotOptions["recoveKeyword"] != "":
                                        if robotOptions["recoveKeyword"] not in otherKeys:
                                            otherKeys.append(robotOptions["recoveKeyword"])
                                        if "fubenMainKeyword" in robotOptions and robotOptions["fubenMainKeyword"] != "":
                                            if robotOptions["fubenMainKeyword"] not in otherKeys:
                                                otherKeys.append(robotOptions["fubenMainKeyword"])
                                            if "callDropKeyword" in robotOptions and robotOptions["callDropKeyword"] != "":
                                                if robotOptions["callDropKeyword"] not in otherKeys:
                                                    otherKeys.append(robotOptions["callDropKeyword"])
                                                if "checkCarInsurPlayerKeyword" in robotOptions and robotOptions["checkCarInsurPlayerKeyword"] != "":
                                                    if robotOptions["checkCarInsurPlayerKeyword"] not in otherKeys:
                                                        otherKeys.append(robotOptions["checkCarInsurPlayerKeyword"])
                                                        carInsurKeys.append(robotOptions["checkCarInsurPlayerKeyword"])
                                                    if "qhbMainPlayerKeyword" in robotOptions and robotOptions["qhbMainPlayerKeyword"] != "":
                                                        if robotOptions["qhbMainPlayerKeyword"] not in otherKeys:
                                                            otherKeys.append(robotOptions["qhbMainPlayerKeyword"])
                                                        if "qhbJoinPlayerKeyword" in robotOptions and robotOptions["qhbJoinPlayerKeyword"] != "":
                                                            if robotOptions["qhbJoinPlayerKeyword"] not in otherKeys:
                                                                otherKeys.append(robotOptions["qhbJoinPlayerKeyword"])
                                                            if "JCLHDMutiKeyword" in robotOptions and robotOptions["JCLHDMutiKeyword"] != "":
                                                                if robotOptions["JCLHDMutiKeyword"] not in otherKeys:
                                                                    otherKeys.append(robotOptions["JCLHDMutiKeyword"])
                                                                if "carInsurAdminKeyword" in robotOptions and robotOptions["carInsurAdminKeyword"] != "":
                                                                    if robotOptions["carInsurAdminKeyword"] not in adminKyes:
                                                                        adminKyes.append(robotOptions["carInsurAdminKeyword"])
                                                                    if "skillOptions" in robotOptions:
                                                                        skillOptions = robotOptions["skillOptions"]
                                                                        if "adminGiveSkillKeyword" in skillOptions:
                                                                            if skillOptions["adminGiveSkillKeyword"] != "":
                                                                                adminKyes.append(skillOptions["adminGiveSkillKeyword"])
                                                                            if "adminCancelSkillKeyword" in skillOptions:
                                                                                if skillOptions["adminCancelSkillKeyword"] != "":
                                                                                    adminKyes.append(skillOptions["adminCancelSkillKeyword"])
                                                                                if "studyKeyword" in skillOptions:
                                                                                    if skillOptions["studyKeyword"] != "":
                                                                                        otherKeys.append(skillOptions["studyKeyword"])
                                                                                    if "useKeyword" in skillOptions:
                                                                                        if skillOptions["useKeyword"] != "":
                                                                                            otherKeys.append(skillOptions["useKeyword"])
                                                                                        if "upLevelKeyword" in skillOptions:
                                                                                            if skillOptions["upLevelKeyword"] != "":
                                                                                                otherKeys.append(skillOptions["upLevelKeyword"])
                                                                                        for i in shortChatArrs:
                                                                                            message = ""
                                                                                            if "LogSCUM: Message:" in i:
                                                                                                if len(i.split("LogSCUM: Message: ")) > 0:
                                                                                                    message = i.split("LogSCUM: Message: ")[1].split(": ")[1].split(" ")[0]
                                                                                                if message != "":
                                                                                                    gk = message
                                                                                                    userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                    userCode = "abcdefg"
                                                                                                    userCodeArr = i.split(" ")
                                                                                                    leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                    inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                    if i not in lastVIPGiftChatArr:
                                                                                                        checkForbiddenKeyword(i, inserStr)
                                                                                                    if checkIsPersonGiftKeyword(message) == False:
                                                                                                        if checkGoodCustomNum(message) == False:
                                                                                                            if fhbUserKeyword not in message:
                                                                                                                if fubenUserKeyword not in message:
                                                                                                                    if recoveUserKeyword not in message:
                                                                                                                        if squardTransKeyword not in message:
                                                                                                                            if tikaUserKeyword not in message:
                                                                                                                                if zjLonghdUserPlayKeyword not in message:
                                                                                                                                    if message not in zjLonghdKeys:
                                                                                                                                        if message not in qaKeys:
                                                                                                                                            if message not in goodsKeys:
                                                                                                                                                if message not in transKeys:
                                                                                                                                                    if message not in giftsKeys:
                                                                                                                                                        if message not in vipGiftsKeys:
                                                                                                                                                            if message not in otherKeys:
                                                                                                                                                                if message not in choujiangKeys:
                                                                                                                                                                    continue
                                                                                                                                                                if i in lastVIPGiftChatArr:
                                                                                                                                                                    continue
                                                                                                                                                                if checkIsPersonGiftKeyword(message) == False:
                                                                                                                                                                    if checkGoodCustomNum(message) == False:
                                                                                                                                                                        if fhbUserKeyword not in message:
                                                                                                                                                                            if fubenUserKeyword not in message:
                                                                                                                                                                                if recoveUserKeyword not in message:
                                                                                                                                                                                    if squardTransKeyword not in message:
                                                                                                                                                                                        if tikaUserKeyword not in message:
                                                                                                                                                                                            if zjLonghdUserPlayKeyword not in message:
                                                                                                                                                                                                if message not in zjLonghdKeys:
                                                                                                                                                                                                    if message not in qaKeys:
                                                                                                                                                                                                        if message not in goodsKeys:
                                                                                                                                                                                                            if message not in transKeys:
                                                                                                                                                                                                                if message not in giftsKeys:
                                                                                                                                                                                                                    if message not in vipGiftsKeys:
                                                                                                                                                                                                                        if message not in choujiangKeys if message not in otherKeys else len(lastVIPGiftChatArr) > 50:
                                                                                                                                                                                                                            lastVIPGiftChatArr.pop(0)
                                                                                                                                                                                                                        if i in lastVIPGiftChatArr:
                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                            lastVIPGiftChatArr.append(i)
                                                                                                                                                                                                                        with open((directory + "/lastChatData.txt"), "w", encoding="UTF-8") as f:
                                                                                                                                                                                                                            f.write("\n".join(lastVIPGiftChatArr))
                                                                                                                                                                                                                        time.sleep(0.2)
                                                                                                                                                                                                                    userCodeArr = i.split(" ")
                                                                                                                                                                                                                    if message in adminKyes:
                                                                                                                                                                                                                        gk = message
                                                                                                                                                                                                                        userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                        userCode = "abcdefg"
                                                                                                                                                                                                                        leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                        inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                        doAdminCmd(i, inserStr)
                                                                                                                                                                                                                    if "@提卡/" in message:
                                                                                                                                                                                                                        if message.split("@提卡/")[0] == "":
                                                                                                                                                                                                                            gk = message
                                                                                                                                                                                                                            userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                            userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                            if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                return False
                                                                                                                                                                                                                            userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                            userCode = userSteamId
                                                                                                                                                                                                                            leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                            inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                            obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                             'data':{}}
                                                                                                                                                                                                                            doTiKa(obj)
                                                                                                                                                                                                                        if message in giftsKeys:
                                                                                                                                                                                                                            for gk in giftsKeys:
                                                                                                                                                                                                                                if gk in i:
                                                                                                                                                                                                                                    if "LogSCUM: Message: " in i:
                                                                                                                                                                                                                                        message = i.split("LogSCUM: Message: ")[1].split(": ")[1]
                                                                                                                                                                                                                                        if message == gk:
                                                                                                                                                                                                                                            gkObj = giftsObjs[gk]
                                                                                                                                                                                                                                            userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                                            repResult = checkMsgIsRepet(needToSendFreeNewGift, userName, gk)
                                                                                                                                                                                                                                        if repResult == True:
                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                            userInfo = getUserInfo(userName, gk)
                                                                                                                                                                                                                                            if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                return False
                                                                                                                                                                                                                                            userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                            userCode = userSteamId
                                                                                                                                                                                                                                            leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                            inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                            currentUserGetedCount = -1
                                                                                                                                                                                                                                            currentDayUserGetCount = -1
                                                                                                                                                                                                                                            totalHave = False
                                                                                                                                                                                                                                        if totalHave == False and "isCheckHistory" in gkObj:
                                                                                                                                                                                                                                            if gkObj["isCheckHistory"] == 1:
                                                                                                                                                                                                                                                if checkGiftHistory(inserStr) == True:
                                                                                                                                                                                                                                                    totalHave = True
                                                                                                                                                                                                                                                    inputSimpleText("【" + userName + "】为老玩家，不允许领取【" + gkObj["showName"] + "】")
                                                                                                                                                                                                                                            if totalHave == False:
                                                                                                                                                                                                                                                if gkObj["totalMaxCount"] != -1:
                                                                                                                                                                                                                                                    currentUserGetedCount = 0
                                                                                                                                                                                                                                                    oldArr = getUserGetedGiftTotal(inserStr, gk)
                                                                                                                                                                                                                                                    currentUserGetedCount = len(oldArr)
                                                                                                                                                                                                                                                    if currentUserGetedCount < gkObj["totalMaxCount"]:
                                                                                                                                                                                                                                                        if gkObj["dayMaxCount"] != -1:
                                                                                                                                                                                                                                                            currentDayUserGetCount = 0
                                                                                                                                                                                                                                                            oldArr = getUserGetedGiftDay(inserStr, gk)
                                                                                                                                                                                                                                                            currentDayUserGetCount = len(oldArr)
                                                                                                                                                                                                                                                            if currentDayUserGetCount < gkObj["dayMaxCount"]:
                                                                                                                                                                                                                                                                obj = {'inserStr':inserStr,  'data':gkObj}
                                                                                                                                                                                                                                                                have = False
                                                                                                                                                                                                                                                                for giftItem in needToSendFreeNewGift:
                                                                                                                                                                                                                                                                    if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                                        have = True

                                                                                                                                                                                                                                                                if have == False:
                                                                                                                                                                                                                                                                    result = checkArrIsHave(needToSendFreeNewGift, inserStr)
                                                                                                                                                                                                                                                                    if result == False:
                                                                                                                                                                                                                                                                        needToSendFreeNewGift.append(obj)
                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                inputSimpleText("【" + userName + "】的【" + gkObj["showName"] + "】今日领取次数已用完")
                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                            obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                             'data':gkObj}
                                                                                                                                                                                                                                                            have = False
                                                                                                                                                                                                                                                            for giftItem in needToSendFreeNewGift:
                                                                                                                                                                                                                                                                if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                                    have = True

                                                                                                                                                                                                                                                            if have == False:
                                                                                                                                                                                                                                                                result = checkArrIsHave(needToSendFreeNewGift, inserStr)
                                                                                                                                                                                                                                                                if result == False:
                                                                                                                                                                                                                                                                    needToSendFreeNewGift.append(obj)
                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                        inputSimpleText("【" + userName + "】的【" + gkObj["showName"] + "】领取次数已用完")
                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                            if gkObj["dayMaxCount"] != -1:
                                                                                                                                                                                                                                                currentDayUserGetCount = 0
                                                                                                                                                                                                                                                oldArr = getUserGetedGiftDay(inserStr, gk)
                                                                                                                                                                                                                                                currentDayUserGetCount = len(oldArr)
                                                                                                                                                                                                                                                if currentDayUserGetCount < gkObj["dayMaxCount"]:
                                                                                                                                                                                                                                                    obj = {'inserStr':inserStr,  'data':gkObj}
                                                                                                                                                                                                                                                    have = False
                                                                                                                                                                                                                                                    for giftItem in needToSendFreeNewGift:
                                                                                                                                                                                                                                                        if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                            have = True

                                                                                                                                                                                                                                                    if have == False:
                                                                                                                                                                                                                                                        result = checkArrIsHave(needToSendFreeNewGift, inserStr)
                                                                                                                                                                                                                                                        if result == False:
                                                                                                                                                                                                                                                            needToSendFreeNewGift.append(obj)
                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                    inputSimpleText("【" + userName + "】的【" + gkObj["showName"] + "】今日领取次数已用完")
                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                 'data':gkObj}
                                                                                                                                                                                                                                                have = False
                                                                                                                                                                                                                                                for giftItem in needToSendFreeNewGift:
                                                                                                                                                                                                                                                    if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                        have = True

                                                                                                                                                                                                                                            if have == False:
                                                                                                                                                                                                                                                result = checkArrIsHave(needToSendFreeNewGift, inserStr)
                                                                                                                                                                                                                                                if result == False:
                                                                                                                                                                                                                                                    needToSendFreeNewGift.append(obj)

                                                                                                                                                                                                                        if " @查询在线" in i:
                                                                                                                                                                                                                            inserStr = i
                                                                                                                                                                                                                            obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                             'data':{}}
                                                                                                                                                                                                                            doSendOnlineNum()
                                                                                                                                                                                                                        if message == "@查询熊币":
                                                                                                                                                                                                                            gk = "@查询熊币"
                                                                                                                                                                                                                            userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                            userCode = "abcdefg"
                                                                                                                                                                                                                            leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                            inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                            doFatchUserAmount(inserStr)
                                                                                                                                                                                                                        if message == "@查询积分":
                                                                                                                                                                                                                            gk = "@查询积分"
                                                                                                                                                                                                                            userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                            userCode = "abcdefg"
                                                                                                                                                                                                                            leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                            inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                            doFatchUserNormalInit(inserStr)
                                                                                                                                                                                                                        if message == "@查询建家时长":
                                                                                                                                                                                                                            gk = "@查询建家时长"
                                                                                                                                                                                                                            userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                            userCode = "abcdefg"
                                                                                                                                                                                                                            leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                            inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                            fatchUserPlayerAdmin(inserStr)
                                                                                                                                                                                                                        if message == "@查询装备卡":
                                                                                                                                                                                                                            gk = "@查询装备卡"
                                                                                                                                                                                                                            userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                            userCode = "abcdefg"
                                                                                                                                                                                                                            leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                            inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                            fatchUserPersonGiftCard(inserStr)
                                                                                                                                                                                                                        if message == "@查询技能":
                                                                                                                                                                                                                            gk = "@查询技能"
                                                                                                                                                                                                                            userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                            userCode = "abcdefg"
                                                                                                                                                                                                                            leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                            inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                            fatchUserPersonSkillData(inserStr)
                                                                                                                                                                                                                        if message in carInsurKeys:
                                                                                                                                                                                                                            gk = message
                                                                                                                                                                                                                            userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                            userCode = "abcdefg"
                                                                                                                                                                                                                            leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                            inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                            carInsurPlayerWordAct(i, inserStr)
                                                                                                                                                                                                                        if isOnlyGift == False:
                                                                                                                                                                                                                            if message in qaKeys:
                                                                                                                                                                                                                                for gk in qaKeys:
                                                                                                                                                                                                                                    if gk in i:
                                                                                                                                                                                                                                        if "LogSCUM: Message: " in i:
                                                                                                                                                                                                                                            message = i.split("LogSCUM: Message: ")[1].split(": ")[1]
                                                                                                                                                                                                                                            if message == gk:
                                                                                                                                                                                                                                                gkObj = qaObjs[gk]
                                                                                                                                                                                                                                                userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                                                userCode = "abcedfg"
                                                                                                                                                                                                                                                leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                currentUserGetedCount = -1
                                                                                                                                                                                                                                                currentDayUserGetCount = -1
                                                                                                                                                                                                                                                totalHave = False
                                                                                                                                                                                                                                                obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                 'data':gkObj}
                                                                                                                                                                                                                                                have = False
                                                                                                                                                                                                                                                for giftItem in needToSendQA:
                                                                                                                                                                                                                                                    if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                        have = True

                                                                                                                                                                                                                                                if have == False:
                                                                                                                                                                                                                                                    needToSendQA.append(obj)

                                                                                                                                                                                                                            if checkGoodCustomNum(message):
                                                                                                                                                                                                                                for gk in goodsKeys:
                                                                                                                                                                                                                                    if gk in i:
                                                                                                                                                                                                                                        if "LogSCUM: Message: " in i:
                                                                                                                                                                                                                                            message = i.split("LogSCUM: Message: ")[1].split(": ")[1]
                                                                                                                                                                                                                                            if not not message == gk:
                                                                                                                                                                                                                                                if "*" in message:
                                                                                                                                                                                                                                                    if gk == message.split("*")[0]:
                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                    gkObj = goodsObjs[gk]
                                                                                                                                                                                                                                                    userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                                                    userInfo = getUserInfo(userName, gk)
                                                                                                                                                                                                                                            if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                return False
                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                userCode = userSteamId
                                                                                                                                                                                                                                                leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                            if "*" in message:
                                                                                                                                                                                                                                                if gk == message.split("*")[0]:
                                                                                                                                                                                                                                                    inserStr = inserStr + "&&&&&" + message
                                                                                                                                                                                                                                                currentUserGetedCount = -1
                                                                                                                                                                                                                                                currentDayUserGetCount = -1
                                                                                                                                                                                                                                                totalHave = False
                                                                                                                                                                                                                                                if gkObj["totalMaxCount"] != -1:
                                                                                                                                                                                                                                                    currentUserGetedCount = 0
                                                                                                                                                                                                                                                    oldArr = getUserGetedGiftTotal(inserStr, gk)
                                                                                                                                                                                                                                                    currentUserGetedCount = len(oldArr)
                                                                                                                                                                                                                                                    if currentUserGetedCount < gkObj["totalMaxCount"]:
                                                                                                                                                                                                                                                        if gkObj["dayMaxCount"] != -1:
                                                                                                                                                                                                                                                            currentDayUserGetCount = 0
                                                                                                                                                                                                                                                            oldArr = getUserGetedGiftDay(inserStr, gk)
                                                                                                                                                                                                                                                            currentDayUserGetCount = len(oldArr)
                                                                                                                                                                                                                                                            if currentDayUserGetCount < gkObj["dayMaxCount"]:
                                                                                                                                                                                                                                                                obj = {'inserStr':inserStr,  'data':gkObj}
                                                                                                                                                                                                                                                                have = False
                                                                                                                                                                                                                                                                for giftItem in needToSendGood:
                                                                                                                                                                                                                                                                    if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                                        have = True

                                                                                                                                                                                                                                                                if have == False:
                                                                                                                                                                                                                                                                    needToSendGood.append(obj)
                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                inputSimpleText("【" + userName + "】的【" + gkObj["showName"] + "】今日购买次数已用完")
                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                            obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                             'data':gkObj}
                                                                                                                                                                                                                                                            have = False
                                                                                                                                                                                                                                                            for giftItem in needToSendGood:
                                                                                                                                                                                                                                                                if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                                    have = True

                                                                                                                                                                                                                                                            if have == False:
                                                                                                                                                                                                                                                                needToSendGood.append(obj)
                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                        inputSimpleText("【" + userName + "】的【" + gkObj["showName"] + "】总购买次数已用完")
                                                                                                                                                                                                                                                elif gkObj["dayMaxCount"] != -1:
                                                                                                                                                                                                                                                    currentDayUserGetCount = 0
                                                                                                                                                                                                                                                    oldArr = getUserGetedGiftDay(inserStr, gk)
                                                                                                                                                                                                                                                    currentDayUserGetCount = len(oldArr)
                                                                                                                                                                                                                                                    if currentDayUserGetCount < gkObj["dayMaxCount"]:
                                                                                                                                                                                                                                                        obj = {'inserStr':inserStr,  'data':gkObj}
                                                                                                                                                                                                                                                        have = False
                                                                                                                                                                                                                                                        for giftItem in needToSendGood:
                                                                                                                                                                                                                                                            if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                                have = True

                                                                                                                                                                                                                                                        if have == False:
                                                                                                                                                                                                                                                            needToSendGood.append(obj)
                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                        inputSimpleText("【" + userName + "】的【" + gkObj["showName"] + "】今日购买次数已用完")
                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                    obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                     'data':gkObj}
                                                                                                                                                                                                                                                    have = False
                                                                                                                                                                                                                                                    for giftItem in needToSendGood:
                                                                                                                                                                                                                                                        if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                            have = True

                                                                                                                                                                                                                                                if have == False:
                                                                                                                                                                                                                                                    needToSendGood.append(obj)

                                                                                                                                                                                                                            if message in transKeys:
                                                                                                                                                                                                                                for gk in transKeys:
                                                                                                                                                                                                                                    if gk in i:
                                                                                                                                                                                                                                        if "LogSCUM: Message: " in i:
                                                                                                                                                                                                                                            message = i.split("LogSCUM: Message: ")[1].split(": ")[1]
                                                                                                                                                                                                                                    if message == gk:
                                                                                                                                                                                                                                        gkObj = transObjs[gk]
                                                                                                                                                                                                                                        userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                                        userInfo = getUserInfo(userName, gk)
                                                                                                                                                                                                                                        serverTime = i.split("]")[0].split("[")[1]
                                                                                                                                                                                                                                        if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                            return False
                                                                                                                                                                                                                                        userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                        userCode = userSteamId
                                                                                                                                                                                                                                        leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                        inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode + "&&&&&" + serverTime
                                                                                                                                                                                                                                        currentUserGetedCount = -1
                                                                                                                                                                                                                                        currentDayUserGetCount = -1
                                                                                                                                                                                                                                        totalHave = False
                                                                                                                                                                                                                                        if gkObj["totalMaxCount"] != -1:
                                                                                                                                                                                                                                            currentUserGetedCount = 0
                                                                                                                                                                                                                                            oldArr = getUserGetedGiftTotal(inserStr, gk)
                                                                                                                                                                                                                                            currentUserGetedCount = len(oldArr)
                                                                                                                                                                                                                                            if currentUserGetedCount < gkObj["totalMaxCount"]:
                                                                                                                                                                                                                                                if gkObj["dayMaxCount"] != -1:
                                                                                                                                                                                                                                                    currentDayUserGetCount = 0
                                                                                                                                                                                                                                                    oldArr = getUserGetedGiftDay(inserStr, gk)
                                                                                                                                                                                                                                                    currentDayUserGetCount = len(oldArr)
                                                                                                                                                                                                                                                    if currentDayUserGetCount < gkObj["dayMaxCount"]:
                                                                                                                                                                                                                                                        obj = {'inserStr':inserStr,  'data':gkObj}
                                                                                                                                                                                                                                                        have = False
                                                                                                                                                                                                                                                        for giftItem in needToSendTrans:
                                                                                                                                                                                                                                                            if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                                have = True

                                                                                                                                                                                                                                                        if have == False:
                                                                                                                                                                                                                                                            needToSendTrans.append(obj)
                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                        inputSimpleText("【" + userName + "】的【" + gkObj["showName"] + "】今日购买次数已用完")
                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                    obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                     'data':gkObj}
                                                                                                                                                                                                                                                    have = False
                                                                                                                                                                                                                                                    for giftItem in needToSendTrans:
                                                                                                                                                                                                                                                        if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                            have = True

                                                                                                                                                                                                                                                    if have == False:
                                                                                                                                                                                                                                                        needToSendTrans.append(obj)
                                                                                                                                                                                                                                        elif gkObj["dayMaxCount"] != -1:
                                                                                                                                                                                                                                            currentDayUserGetCount = 0
                                                                                                                                                                                                                                            oldArr = getUserGetedGiftDay(inserStr, gk)
                                                                                                                                                                                                                                            currentDayUserGetCount = len(oldArr)
                                                                                                                                                                                                                                            if currentDayUserGetCount < gkObj["dayMaxCount"]:
                                                                                                                                                                                                                                                obj = {'inserStr':inserStr,  'data':gkObj}
                                                                                                                                                                                                                                                have = False
                                                                                                                                                                                                                                                for giftItem in needToSendTrans:
                                                                                                                                                                                                                                                    if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                        have = True

                                                                                                                                                                                                                                                if have == False:
                                                                                                                                                                                                                                                    needToSendTrans.append(obj)
                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                inputSimpleText("【" + userName + "】的【" + gkObj["showName"] + "】今日购买次数已用完")
                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                            obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                             'data':gkObj}
                                                                                                                                                                                                                                            have = False
                                                                                                                                                                                                                                            for giftItem in needToSendTrans:
                                                                                                                                                                                                                                                if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                    have = True

                                                                                                                                                                                                                                            if have == False:
                                                                                                                                                                                                                                                needToSendTrans.append(obj)

                                                                                                                                                                                                                            if message in choujiangKeys or "singleKey" not in totalRobotOptions["choujiang"] and message == initChoujiangKey:
                                                                                                                                                                                                                                userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                                userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                    return False
                                                                                                                                                                                                                                userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                userCode = userSteamId
                                                                                                                                                                                                                                leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                 'data':{}}
                                                                                                                                                                                                                                if "singleKey" not in totalRobotOptions["choujiang"]:
                                                                                                                                                                                                                                    if message == initChoujiangKey:
                                                                                                                                                                                                                                        doLottery(obj, 0)
                                                                                                                                                                                                                                    if "singleKey" in totalRobotOptions["choujiang"]:
                                                                                                                                                                                                                                        if message == totalRobotOptions["choujiang"]["singleKey"]:
                                                                                                                                                                                                                                            doLottery(obj, 0)
                                                                                                                                                                                                                                        if "mutiKey" in totalRobotOptions["choujiang"]:
                                                                                                                                                                                                                                            if message == totalRobotOptions["choujiang"]["mutiKey"]:
                                                                                                                                                                                                                                                doLottery(obj, 1)
                                                                                                                                                                                                                                            lhdAdminKeyword = [
                                                                                                                                                                                                                                             totalRobotOptions["longhudou"]["adminKeyword"]]
                                                                                                                                                                                                                                            if "closeAdminKeyword" in totalRobotOptions["longhudou"]:
                                                                                                                                                                                                                                                lhdAdminKeyword.append(totalRobotOptions["longhudou"]["closeAdminKeyword"])
                                                                                                                                                                                                                                            if "longhudou" in totalRobotOptions:
                                                                                                                                                                                                                                                if message in lhdAdminKeyword:
                                                                                                                                                                                                                                                    userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                                                    userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                                    if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                        return False
                                                                                                                                                                                                                                                    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                    userCode = userSteamId
                                                                                                                                                                                                                                                    leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                    inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                    obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                     'data':{}}
                                                                                                                                                                                                                                                    doLHDAdmin(obj)
                                                                                                                                                                                                                                                if "longhudou" in totalRobotOptions:
                                                                                                                                                                                                                                                    if totalRobotOptions["longhudou"]["playerKeyword"] == message:
                                                                                                                                                                                                                                                        userName = i.split("LogSCUM: Message: ")[1].split(": " + totalRobotOptions["longhudou"]["playerKeyword"])[0]
                                                                                                                                                                                                                                                        userInfo = getUserInfo(userName, totalRobotOptions["longhudou"]["playerKeyword"])
                                                                                                                                                                                                                                                        if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                            return False
                                                                                                                                                                                                                                                        userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                        userCode = userSteamId
                                                                                                                                                                                                                                                        leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                        inserStr = leftTime + "&&&&&" + totalRobotOptions["longhudou"]["playerKeyword"] + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                        obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                         'data':{}}
                                                                                                                                                                                                                                                        doLHDUser(obj)
                                                                                                                                                                                                                                                    if "JCLHDMutiKeyword" in robotOptions:
                                                                                                                                                                                                                                                        if robotOptions["JCLHDMutiKeyword"] == message:
                                                                                                                                                                                                                                                            userName = i.split("LogSCUM: Message: ")[1].split(": " + robotOptions["JCLHDMutiKeyword"])[0]
                                                                                                                                                                                                                                                            userInfo = getUserInfo(userName, robotOptions["JCLHDMutiKeyword"])
                                                                                                                                                                                                                                                            if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                                return False
                                                                                                                                                                                                                                                            userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                            userCode = userSteamId
                                                                                                                                                                                                                                                            leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                            inserStr = leftTime + "&&&&&" + robotOptions["JCLHDMutiKeyword"] + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                            obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                             'data':{}}
                                                                                                                                                                                                                                                            doLHDUser(obj, 1)
                                                                                                                                                                                                                                                if message == justUpNormalLevelWordKey:
                                                                                                                                                                                                                                                    userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                                                    userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                                    if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                        return False
                                                                                                                                                                                                                                                    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                    userCode = userSteamId
                                                                                                                                                                                                                                                    leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                    inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                    obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                     'data':{}}
                                                                                                                                                                                                                                                    justUpNormalLevelFun(obj)
                                                                                                                                                                                                                                            if showZJLHD == True:
                                                                                                                                                                                                                                                if "zjLonghd" in totalRobotOptions and message in zjLonghdKeys or totalRobotOptions["zjLonghd"]["userPlayKeyword"] + "/" in message:
                                                                                                                                                                                                                                                    userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                                                    userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                                    if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                        return False
                                                                                                                                                                                                                                                    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                    userCode = userSteamId
                                                                                                                                                                                                                                                    leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                    inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                    obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                     'data':{}}
                                                                                                                                                                                                                                                    if message == totalRobotOptions["zjLonghd"]["userUpKeyword"]:
                                                                                                                                                                                                                                                        userUpZjLhd(obj)
                                                                                                                                                                                                                                                    if message == totalRobotOptions["zjLonghd"]["userDownKeyword"]:
                                                                                                                                                                                                                                                        userDownZjLhd(obj)
                                                                                                                                                                                                                                                    if message == totalRobotOptions["zjLonghd"]["adminDownKeyword"]:
                                                                                                                                                                                                                                                        if userSteamId in totalRobotOptions["options"]["adminSteamid"]:
                                                                                                                                                                                                                                                            adminDownZjLhd(obj)
                                                                                                                                                                                                                                                    if totalRobotOptions["zjLonghd"]["userPlayKeyword"] + "/" in message:
                                                                                                                                                                                                                                                        playZjLhd(obj)
                                                                                                                                                                                                                                    if checkIsPersonGiftKeyword(message) and "/" in message:
                                                                                                                                                                                                                                        if message.split("/")[0] in vipGiftsKeys:
                                                                                                                                                                                                                                            gk = message
                                                                                                                                                                                                                                            userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                                            userInfo = getUserInfo(userName, gk)
                                                                                                                                                                                                                                            userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                            leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                            inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userSteamId
                                                                                                                                                                                                                                            sendUserPersonGiftCard(inserStr)
                                                                                                                                                                                                                                        if message in vipGiftsKeys:
                                                                                                                                                                                                                                            for gk in vipGiftsKeys:
                                                                                                                                                                                                                                                if gk in i:
                                                                                                                                                                                                                                                    if "LogSCUM: Message: " in i:
                                                                                                                                                                                                                                                        message = i.split("LogSCUM: Message: ")[1].split(": ")[1]
                                                                                                                                                                                                                                                        if not not message == gk:
                                                                                                                                                                                                                                                            if gk in message:
                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                            gkObj = vipGiftsObjs[gk]["gifts"]
                                                                                                                                                                                                                                                            if "giftType" in vipGiftsObjs[gk]:
                                                                                                                                                                                                                                                                if vipGiftsObjs[gk]["giftType"] == 2:
                                                                                                                                                                                                                                                                    return False
                                                                                                                                                                                                                                                                userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                                                                serverTime = i.split("]")[0].split("[")[1]
                                                                                                                                                                                                                                                                repResult = checkMsgIsRepet(needToSendNewGift, userName, gk)
                                                                                                                                                                                                                                                        if repResult == True:
                                                                                                                                                                                                                                                            break
                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                            userInfo = getUserInfo(userName, gk)
                                                                                                                                                                                                                                                            if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                                return False
                                                                                                                                                                                                                                                            userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                            userCode = userSteamId
                                                                                                                                                                                                                                                            leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                            inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode + "&&&&&" + serverTime
                                                                                                                                                                                                                                                            currentUserGetedCount = -1
                                                                                                                                                                                                                                                            currentDayUserGetCount = -1
                                                                                                                                                                                                                                                            totalHave = False
                                                                                                                                                                                                                                                            isHaveVipGift = False
                                                                                                                                                                                                                                                            isAllowGiftVipLevel = False
                                                                                                                                                                                                                                                            isAllowNormalVipLevel = False
                                                                                                                                                                                                                                                            vipGiftObj = {}
                                                                                                                                                                                                                                                            userDataInfo = fatchUser(userSteamId)
                                                                                                                                                                                                                                                            if userSteamId != "":
                                                                                                                                                                                                                                                                for gf in gkObj:
                                                                                                                                                                                                                                                                    if userSteamId in gkObj[gf]["vipIds"]:
                                                                                                                                                                                                                                                                        isHaveVipGift = True
                                                                                                                                                                                                                                                                        vipGiftObj = gkObj[gf]

                                                                                                                                                                                                                                                            vipIsOutTime = False
                                                                                                                                                                                                                                                            current = int(datetime.strptime(str(datetime.now()).split(" ")[0], "%Y-%m-%d").timestamp())
                                                                                                                                                                                                                                                            vipenddate = ""
                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                vipenddate = userDataInfo[0][8]
                                                                                                                                                                                                                                                            except Exception as e:
                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                    vipenddate = ""
                                                                                                                                                                                                                                                                finally:
                                                                                                                                                                                                                                                                    e = None
                                                                                                                                                                                                                                                                    del e

                                                                                                                                                                                                                                                            normalVipLevel = ""
                                                                                                                                                                                                                                                        if isHaveVipGift == False:
                                                                                                                                                                                                                                                            if vipenddate == None or len(vipenddate) < 2:
                                                                                                                                                                                                                                                                vipIsOutTime = True
                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                vipend = int(datetime.strptime(str(vipenddate), "%Y-%m-%d").timestamp())
                                                                                                                                                                                                                                                                if current > vipend:
                                                                                                                                                                                                                                                                    vipIsOutTime = True
                                                                                                                                                                                                                                                                if len(userDataInfo) > 0:
                                                                                                                                                                                                                                                                    userVipLevel = userDataInfo[0][7]
                                                                                                                                                                                                                                                                    for gf in gkObj:
                                                                                                                                                                                                                                                                        if gkObj[gf]["vipLevel"] != "0":
                                                                                                                                                                                                                                                                            if "vipLevel" in gkObj[gf]:
                                                                                                                                                                                                                                                                                if userVipLevel == gkObj[gf]["vipLevel"]:
                                                                                                                                                                                                                                                                                    isAllowGiftVipLevel = True
                                                                                                                                                                                                                                                                                    vipGiftObj = gkObj[gf]

                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                    normalVipLevel = userDataInfo[0][12]
                                                                                                                                                                                                                                                                    for gf in gkObj:
                                                                                                                                                                                                                                                                        if gkObj[gf]["vipIds"] == "":
                                                                                                                                                                                                                                                                            if isHaveVipGift == False:
                                                                                                                                                                                                                                                                                if gkObj[gf]["vipLevel"] == "0":
                                                                                                                                                                                                                                                                                    if isAllowGiftVipLevel == False:
                                                                                                                                                                                                                                                                                        if "normalVipLevel" in gkObj[gf]:
                                                                                                                                                                                                                                                                                            if gkObj[gf]["normalVipLevel"] == normalVipLevel:
                                                                                                                                                                                                                                                                                                isAllowNormalVipLevel = True
                                                                                                                                                                                                                                                                                                vipGiftObj = gkObj[gf]

                                                                                                                                                                                                                                                                except IndexError:
                                                                                                                                                                                                                                                                    normalVipLevel = ""
                                                                                                                                                                                                                                                                    isAllowNormalVipLevel = False

                                                                                                                                                                                                                                                                if not not isHaveVipGift == True:
                                                                                                                                                                                                                                                                    if not not isAllowGiftVipLevel == True:
                                                                                                                                                                                                                                                                        if isAllowNormalVipLevel == True:
                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                        gkObj = vipGiftObj
                                                                                                                                                                                                                                                        if isAllowGiftVipLevel == True and vipIsOutTime == True:
                                                                                                                                                                                                                                                            inputSimpleText("【" + userName + "】您的VIP已过期")
                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                            if gkObj["totalMaxCount"] != -1:
                                                                                                                                                                                                                                                                currentUserGetedCount = 0
                                                                                                                                                                                                                                                                oldArr = getUserGetedGiftTotal(inserStr, gk)
                                                                                                                                                                                                                                                                currentUserGetedCount = len(oldArr)
                                                                                                                                                                                                                                                                if currentUserGetedCount < gkObj["totalMaxCount"]:
                                                                                                                                                                                                                                                                    if gkObj["dayMaxCount"] != -1:
                                                                                                                                                                                                                                                                        currentDayUserGetCount = 0
                                                                                                                                                                                                                                                                        oldArr = getUserGetedGiftDay(inserStr, gk)
                                                                                                                                                                                                                                                                        currentDayUserGetCount = len(oldArr)
                                                                                                                                                                                                                                                                        if currentDayUserGetCount < gkObj["dayMaxCount"]:
                                                                                                                                                                                                                                                                            obj = {'inserStr':inserStr,  'data':gkObj}
                                                                                                                                                                                                                                                                            have = False
                                                                                                                                                                                                                                                                            for giftItem in needToSendNewGift:
                                                                                                                                                                                                                                                                                if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                                                    have = True

                                                                                                                                                                                                                                                                            if have == False:
                                                                                                                                                                                                                                                                                result = checkArrIsHave(needToSendNewGift, inserStr)
                                                                                                                                                                                                                                                                                if result == False:
                                                                                                                                                                                                                                                                                    needToSendNewGift.append(obj)
                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                            inputSimpleText("【" + userName + "】的【" + gkObj["showName"] + "】今日领取次数已用完")
                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                        obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                                         'data':gkObj}
                                                                                                                                                                                                                                                                        have = False
                                                                                                                                                                                                                                                                        for giftItem in needToSendNewGift:
                                                                                                                                                                                                                                                                            if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                                                have = True

                                                                                                                                                                                                                                                                        if have == False:
                                                                                                                                                                                                                                                                            result = checkArrIsHave(needToSendNewGift, inserStr)
                                                                                                                                                                                                                                                                            if result == False:
                                                                                                                                                                                                                                                                                needToSendNewGift.append(obj)
                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                    inputSimpleText("【" + userName + "】的【" + gkObj["showName"] + "】领取次数已用完")
                                                                                                                                                                                                                                                            elif gkObj["dayMaxCount"] != -1:
                                                                                                                                                                                                                                                                currentDayUserGetCount = 0
                                                                                                                                                                                                                                                                oldArr = getUserGetedGiftDay(inserStr, gk)
                                                                                                                                                                                                                                                                currentDayUserGetCount = len(oldArr)
                                                                                                                                                                                                                                                                if currentDayUserGetCount < gkObj["dayMaxCount"]:
                                                                                                                                                                                                                                                                    obj = {'inserStr':inserStr,  'data':gkObj}
                                                                                                                                                                                                                                                                    have = False
                                                                                                                                                                                                                                                                    for giftItem in needToSendNewGift:
                                                                                                                                                                                                                                                                        if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                                            have = True

                                                                                                                                                                                                                                                                    if have == False:
                                                                                                                                                                                                                                                                        result = checkArrIsHave(needToSendNewGift, inserStr)
                                                                                                                                                                                                                                                                        if result == False:
                                                                                                                                                                                                                                                                            needToSendNewGift.append(obj)
                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                    inputSimpleText("【" + userName + "】的【" + gkObj["showName"] + "】今日领取次数已用完")
                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                                 'data':gkObj}
                                                                                                                                                                                                                                                                have = False
                                                                                                                                                                                                                                                                for giftItem in needToSendNewGift:
                                                                                                                                                                                                                                                                    if giftItem["inserStr"].find(inserStr) != -1:
                                                                                                                                                                                                                                                                        have = True

                                                                                                                                                                                                                                                            if have == False:
                                                                                                                                                                                                                                                                result = checkArrIsHave(needToSendNewGift, inserStr)
                                                                                                                                                                                                                                                                if result == False:
                                                                                                                                                                                                                                                                    needToSendNewGift.append(obj)

                                                                                                                                                                                                                                        if "qhbMainPlayerKeyword" in robotOptions and robotOptions["qhbMainPlayerKeyword"] != "":
                                                                                                                                                                                                                                            if robotOptions["qhbMainPlayerKeyword"] + "/" in message:
                                                                                                                                                                                                                                                if message.index(robotOptions["qhbMainPlayerKeyword"] + "/") == 0:
                                                                                                                                                                                                                                                    userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                                                    userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                                    if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                        return False
                                                                                                                                                                                                                                                    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                    userCode = userSteamId
                                                                                                                                                                                                                                                    leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                    inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                    doMainPlayerSendHb(inserStr)
                                                                                                                                                                                                                                            if "skillOptions" in robotOptions and robotOptions["skillOptions"] != "":
                                                                                                                                                                                                                                                if robotOptions["skillOptions"]["useKeyword"] != "" and robotOptions["skillOptions"]["useKeyword"] in message:
                                                                                                                                                                                                                                                    if message.index(robotOptions["skillOptions"]["useKeyword"]) == 0:
                                                                                                                                                                                                                                                        userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                                                        userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                                        if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                            return False
                                                                                                                                                                                                                                                        userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                        userCode = userSteamId
                                                                                                                                                                                                                                                        leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                        message = i.split("LogSCUM: Message: ")[1].split(": ")[1]
                                                                                                                                                                                                                                                        serverTime = i.split("]")[0].split("[")[1]
                                                                                                                                                                                                                                                        inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode + "&&&&&" + serverTime
                                                                                                                                                                                                                                                        doPlayerUseSkill(inserStr)
                                                                                                                                                                                                                                                    if "skillOptions" in robotOptions and robotOptions["skillOptions"] != "":
                                                                                                                                                                                                                                                        if robotOptions["skillOptions"]["upLevelKeyword"] != "" and robotOptions["skillOptions"]["upLevelKeyword"] in message:
                                                                                                                                                                                                                                                            if message.index(robotOptions["skillOptions"]["upLevelKeyword"]) == 0:
                                                                                                                                                                                                                                                                userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                                                                userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                                                if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                                    return False
                                                                                                                                                                                                                                                                userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                                userCode = userSteamId
                                                                                                                                                                                                                                                                leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                                message = i.split("LogSCUM: Message: ")[1].split(": ")[1]
                                                                                                                                                                                                                                                                inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                                doPlayerUpSkill(inserStr)
                                                                                                                                                                                                                                                            if "skillOptions" in robotOptions and robotOptions["skillOptions"] != "":
                                                                                                                                                                                                                                                                if robotOptions["skillOptions"]["studyKeyword"] != "" and robotOptions["skillOptions"]["studyKeyword"] in message:
                                                                                                                                                                                                                                                                    if message.index(robotOptions["skillOptions"]["studyKeyword"]) == 0:
                                                                                                                                                                                                                                                                        userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                                                                        userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                                                        if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                                            return False
                                                                                                                                                                                                                                                                        userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                                        userCode = userSteamId
                                                                                                                                                                                                                                                                        leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                                        message = i.split("LogSCUM: Message: ")[1].split(": ")[1]
                                                                                                                                                                                                                                                                        inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                                        doPlayerStudySkill(inserStr)
                                                                                                                                                                                                                                                                    if "qhbJoinPlayerKeyword" in robotOptions and robotOptions["qhbJoinPlayerKeyword"] != "":
                                                                                                                                                                                                                                                                        if message == robotOptions["qhbJoinPlayerKeyword"]:
                                                                                                                                                                                                                                                                            userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                                                                            userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                                                            if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                                                return False
                                                                                                                                                                                                                                                                            userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                                            userCode = userSteamId
                                                                                                                                                                                                                                                                            leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                                            inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                                            doJoinPlayerGetHB(inserStr)
                                                                                                                                                                                                                                                                        if "playerSignInKeyword" in robotOptions and message == robotOptions["playerSignInKeyword"]:
                                                                                                                                                                                                                                                                            if robotOptions["playerSignInKeyword"] != "":
                                                                                                                                                                                                                                                                                gk = robotOptions["playerSignInKeyword"]
                                                                                                                                                                                                                                                                                userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                                                                                userCode = "abcdefg"
                                                                                                                                                                                                                                                                                leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                                                inserStr = leftTime + "&&&&&" + gk + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                                                playerSignInDo(inserStr)
                                                                                                                                                                                                                                                                            if "playerBuyAdminKeyword" in robotOptions and message == robotOptions["playerBuyAdminKeyword"]:
                                                                                                                                                                                                                                                                                if robotOptions["playerBuyAdminKeyword"] != "":
                                                                                                                                                                                                                                                                                    gk = robotOptions["playerBuyAdminKeyword"]
                                                                                                                                                                                                                                                                                    userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                                                                                    userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                                                                    if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                                                        return False
                                                                                                                                                                                                                                                                                    userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                                                    userCode = userSteamId
                                                                                                                                                                                                                                                                                    leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                                                    inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                                                    obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                                                     'data':{}}
                                                                                                                                                                                                                                                                                    playerBuyAdmin(obj)
                                                                                                                                                                                                                                                                                if "requestSquardTransKeyword" in robotOptions and robotOptions["requestSquardTransKeyword"] + "/" in message:
                                                                                                                                                                                                                                                                                    if message.split(robotOptions["requestSquardTransKeyword"] + "/")[0] == "":
                                                                                                                                                                                                                                                                                        gk = message
                                                                                                                                                                                                                                                                                        userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                                                                                        userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                                                                        if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                                                            return False
                                                                                                                                                                                                                                                                                        userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                                                        userCode = userSteamId
                                                                                                                                                                                                                                                                                        leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                                                        inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                                                        obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                                                         'data':{}}
                                                                                                                                                                                                                                                                                        requestSquardPlayerTrans(obj)
                                                                                                                                                                                                                                                                                    if "agreeSquardTransKeyword" in robotOptions and message == robotOptions["agreeSquardTransKeyword"]:
                                                                                                                                                                                                                                                                                        if robotOptions["agreeSquardTransKeyword"] != "":
                                                                                                                                                                                                                                                                                            gk = robotOptions["agreeSquardTransKeyword"]
                                                                                                                                                                                                                                                                                            userName = i.split("LogSCUM: Message: ")[1].split(": " + gk)[0]
                                                                                                                                                                                                                                                                                            userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                                                                            if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                                                                return False
                                                                                                                                                                                                                                                                                            userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                                                            userCode = userSteamId
                                                                                                                                                                                                                                                                                            leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                                                            inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                                                            obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                                                             'data':{}}
                                                                                                                                                                                                                                                                                            agreeNotSquadPlayerTrans(obj)
                                                                                                                                                                                                                                                                                        if "recoveKeyword" in robotOptions and robotOptions["recoveKeyword"] + "/" in message:
                                                                                                                                                                                                                                                                                            if message.split(robotOptions["recoveKeyword"] + "/")[0] == "":
                                                                                                                                                                                                                                                                                                gk = message
                                                                                                                                                                                                                                                                                                userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                                                                                                userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                                                                                if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                                                                    return False
                                                                                                                                                                                                                                                                                                userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                                                                userCode = userSteamId
                                                                                                                                                                                                                                                                                                leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                                                                inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                                                                obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                                                                 'data':{}}
                                                                                                                                                                                                                                                                                                doRecove(obj)
                                                                                                                                                                                                                                                                                            if "fubenMainKeyword" in robotOptions:
                                                                                                                                                                                                                                                                                                if robotOptions["fubenMainKeyword"] + "/" in message:
                                                                                                                                                                                                                                                                                                    if message.split(robotOptions["fubenMainKeyword"] + "/")[0] == "":
                                                                                                                                                                                                                                                                                                        gk = message
                                                                                                                                                                                                                                                                                                        userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                                                                                                        userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                                                                                        if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                                                                                            return False
                                                                                                                                                                                                                                                                                                        userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                                                                                        userCode = userSteamId
                                                                                                                                                                                                                                                                                                        leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                                                                                        inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                                                                                        obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                                                                                         'data':{}}
                                                                                                                                                                                                                                                                                                        doFuben(obj)
                                                                                                                                                                                                                            if "callDropKeyword" in robotOptions:
                                                                                                                                                                                                                                if robotOptions["callDropKeyword"] != "":
                                                                                                                                                                                                                                    if message == robotOptions["callDropKeyword"]:
                                                                                                                                                                                                                                        gk = message
                                                                                                                                                                                                                                        userName = i.split("LogSCUM: Message: ")[1].split(": " + message)[0]
                                                                                                                                                                                                                                        userInfo = getUserInfo(userName, message)
                                                                                                                                                                                                                                        if userInfo == False or len(userInfo) == 0:
                                                                                                                                                                                                                                            return False
                                                                                                                                                                                                                                        userSteamId = userInfo[1].split("(")[-1].split(")")[0]
                                                                                                                                                                                                                                        userCode = userSteamId
                                                                                                                                                                                                                                        leftTime = userCodeArr[0].split("][")[0].split("[")[1] + "&&&&&" + str(datetime.now()).split(" ")[0]
                                                                                                                                                                                                                                        inserStr = leftTime + "&&&&&" + message + "&&&&&" + userName + "&&&&&" + userCode
                                                                                                                                                                                                                                        obj = {'inserStr':inserStr, 
                                                                                                                                                                                                                                         'data':{}}
                                                                                                                                                                                                                                        doCallDrop(obj)
                                                                                                                                                                                                                                    print(needToSendNewGift)
                                                                                                                                                                                                                                    key = key + 1

                                                                                    if len(needToSendFreeNewGift) > 0:
                                                                                        sendFreeNewGift(needToSendFreeNewGift)
                                                                                if len(needToSendNewGift) > 0:
                                                                                    sendNewGift(needToSendNewGift)
                                                                            if len(needToSendGood) > 0:
                                                                                sendGood(needToSendGood)
                                                                        if len(needToSendTrans) > 0:
                                                                            sendTrans(needToSendTrans)
                                                                    if len(needToSendQA) > 0:
                                                                        sendQA(needToSendQA)


def getUserGetedGiftTotal(inserStr, gk):
    result = []
    arr = inserStr.split("&&&&&")
    localTime = arr[1]
    keyword = arr[2]
    usercode = arr[4]
    if len(arr) > 0 and len(arr[2]) > 0:
        if len(arr[4]) > 0:
            result = fatchSendedDataByUserByTotal(arr[2], arr[4])
        printToLog(keyword)
        printToLog(result)
        return result


def getUserGetedGiftDay(inserStr, gk):
    result = []
    arr = inserStr.split("&&&&&")
    localTime = arr[1]
    keyword = arr[2]
    usercode = arr[4]
    if len(arr) > 0 and len(arr[1]) > 0:
        if len(arr[2]) > 0:
            if len(arr[4]) > 0:
                result = fatchSendedDataByUserByDay(arr[1], arr[2], arr[4])
            printToLog(keyword)
            printToLog(result)
            return result


def checkUserHave(logStr, curStr, word):
    if len(logStr) > 1 and len(curStr) > 1:
        if len(word) > 1:
            if logStr.find(word) != -1:
                if len(curStr.split("&&&&&")[4]) > 0:
                    if logStr.find(curStr.split("&&&&&")[4]) != -1:
                        return True
                    return False
            return False


def checkDayUserHave(logStr, curStr, word, time):
    if len(logStr) > 1 and len(curStr) > 1:
        if len(word) > 1 and len(time) > 1:
            if logStr.find(word) != -1:
                if len(curStr.split("&&&&&")[4]) > 0:
                    if logStr.find(curStr.split("&&&&&")[4]) != -1:
                        if logStr.find(time) != -1:
                            return True
                        return False
                return False


def moustMove():
    try:
        rect = win32gui.GetWindowRect(hwnd)
        x = rect[0]
        y = rect[1]
        width = rect[2] - x
        height = rect[3] - y
        time.sleep(0.5)
        ui.moveTo((int(x + width / 2)), (int(y + height / 2 + 30)), duration=0.3)
        time.sleep(0.5)
        ui.click(x=(int(x + width / 2)), y=(int(y + height / 2 + 30)), button="left")
        time.sleep(0.5)
        ui.moveTo((int(x + width / 2 - 500)), (int(y + height / 2 + 90)), duration=0.3)
        ui.click(x=(int(x + width / 2 - 500)), y=(int(y + height / 2 + 90)), button="left")
    except Exception as e:
        try:
            printToLog("未找到游戏窗口")
        finally:
            e = None
            del e


def clearMoto():
    global clearMotoStatus
    if clearMotoStatus == False:
        clearMotoStatus = True
        inputSimpleText("#Announce 即将开始清理【滴滴摩托车】!!!")
        inputSimpleText("#DestroyAllVehicles please " + robotOptions["ddcarName"])


offlineTimes = 0
offlineTimeout = 300

def checkLoginState():
    global mouseMoveTime
    global offlineTimeout
    global offlineTimes
    global robotIsOffline
    try:
        localappdata = os.getenv("LOCALAPPDATA")
        f = open((localappdata + "/SCUM/Saved/Logs/SCUM.log"), encoding="utf-8")
        cont = f.read()
        f.close()
        contList = cont.split("\n")
        logSCUMArr = []
        for i in contList:
            if i.find("LogLevel: WORLD TRANSLATION END") != -1 or i.find("LogSCUM: [InitialSync] Uncompressed received data") != -1:
                logSCUMArr.append(i)
            if i.find("LogLoad: Game class is 'BP_MainMenuGameMode_C'") != -1:
                logSCUMArr.append(i)

        logSCUMArr.reverse()
        newLogSCUMArr = []
        for j in logSCUMArr:
            if j.find("LogLoad: Game class is 'BP_MainMenuGameMode_C'") != -1:
                newLogSCUMArr.append(j)
            if not not j.find("LogLevel: WORLD TRANSLATION END") != -1:
                if j.find("LogSCUM: [InitialSync] Uncompressed received data") != -1:
                    pass
                newLogSCUMArr.append(j)

        checkResultState = False
        for k in newLogSCUMArr:
            if checkResultState == True:
                break
            if not not k.find("LogLevel: WORLD TRANSLATION END") != -1:
                if k.find("LogSCUM: [InitialSync] Uncompressed received data") != -1:
                    checkResultState = True
                    if robotIsOffline == True:
                        offlineTimes = 0
                        robotIsOffline = False
                        mouseMoveTime = 0
                        sleepTime = 5
                        if "reloginWaitTime" in totalRobotOptions["options"]:
                            try:
                                sleepTime = int(float(totalRobotOptions["options"]["reloginWaitTime"]))
                            except Exception:
                                sleepTime = 10

                        printToLog("检测到游戏登陆，等待" + str(sleepTime) + "秒钟后切换全球频道，可在基本设置中根据自己电脑实际情况延长或缩短重连等待时间~")
                        time.sleep(sleepTime)
                        printToLog("开始切换全球频道")
                        ui.press("t")
                        time.sleep(0.05)
                        ui.press("backspace")
                        time.sleep(0.5)
                        ui.press("tab")
                        time.sleep(0.5)
                        ui.press("enter")
                        time.sleep(1)
                        inputSimpleText("发货机器人重连成功")
                    else:
                        break
                else:
                    if k.find("LogLoad: Game class is 'BP_MainMenuGameMode_C'") != -1:
                        robotIsOffline = True
                        checkResultState = True
                        offlineTimes = offlineTimes + 15
            if "openAutoCloseGame" in robotOptions:
                if robotOptions["openAutoCloseGame"] == "1":
                    if offlineTimes > offlineTimeout:
                        offlineTimes = 0
                        killGameProcess()
                    printToLog("检测到游戏掉线，正在尝试重连...掉线计时：【" + str(offlineTimes) + "】" + str(datetime.now()))
                    moustMove()
                    time.sleep(8)
                    continue

    except Exception as e:
        try:
            printToLog(e)
            printToLog("错误发生行号：" + traceback.format_exc())
            printToLog("获取数据出错，机器人重启中，如长时间未能恢复，请联系管理员协助解决")
            logging.error(str(datetime.now()))
            logging.error(traceback.format_exc())
            time.sleep(robotOptions["checkSleepTime"])
            checkLoginState()
        finally:
            e = None
            del e


def killGameProcess():
    try:
        (thread_id, process_id) = win32process.GetWindowThreadProcessId(hwnd)
        printToLog("长时间登录无响应，结束游戏重新打开" + str(process_id))
        process = psutil.Process(process_id)
        process.kill()
        time.sleep(40)
        printToLog(f"Process with PID {hwnd} has been terminated.")
    except psutil.NoSuchProcess:
        printToLog(f"No process found with PID {hwnd}.")
    except Exception as e:
        try:
            printToLog(f"Error terminating process with PID {hwnd}: {e}")
        finally:
            e = None
            del e


def doAllRewardAmount():
    checkDayReduceInt()
    inputSimpleText("开始发放在线奖励~")
    ORList = []
    if "onlineRewardList" in robotOptions:
        ORList = robotOptions["onlineRewardList"]
    allPlayer = getAllPlayerList()
    isHave = True
    for item in allPlayer:
        userSteamid = item["steamid"]
        userFakename = item["userName"]
        if item["fakename"] != "":
            userFakename = item["fakename"]
        updateUserData = {'steam_id':userSteamid,  'normal_integral':getUserNormalJifen(userSteamid), 
         'integral':getUserJifen(userSteamid), 
         'amount':getUserAmount(userSteamid)}
        userNormalVipLevel = getUserNormalVipLevel(userSteamid)
        userVipLevel = getUserVipLevel(userSteamid)
        userCusTitle = getUserCustomTitle(userSteamid)
        ORValItem = {
          'DLAmount': "",
          'amount': "",
          'normal_integral': "",
          'integral': "",
          'code': ""}
        for orItem in ORList:
            if orItem["levelType"] == "":
                if orItem["rewardType"] == "1":
                    if orItem["rewardVal"] != "":
                        ORValItem["DLAmount"] = orItem["rewardVal"]
                    if orItem["rewardType"] == "2":
                        if orItem["rewardVal"] != "":
                            ORValItem["amount"] = orItem["rewardVal"]
                        if orItem["rewardType"] == "3":
                            if orItem["rewardVal"] != "":
                                ORValItem["normal_integral"] = orItem["rewardVal"]
                            if orItem["rewardType"] == "4":
                                if orItem["rewardVal"] != "":
                                    ORValItem["integral"] = orItem["rewardVal"]
                                if orItem["rewardType"] == "5":
                                    if orItem["rewardVal"] != "":
                                        ORValItem["code"] = orItem["rewardVal"]

        for orItem in ORList:
            if orItem["levelType"] == "1":
                if not not userNormalVipLevel == orItem["levelVal"]:
                    pass
                if orItem["levelType"] == "2":
                    if not not userVipLevel == orItem["levelVal"]:
                        pass
                    if orItem["levelType"] == "3":
                        if userCusTitle == orItem["levelVal"]:
                            pass
                        if orItem["rewardType"] == "1":
                            if orItem["rewardVal"] != "":
                                ORValItem["DLAmount"] = orItem["rewardVal"]
                            if orItem["rewardType"] == "2":
                                if orItem["rewardVal"] != "":
                                    ORValItem["amount"] = orItem["rewardVal"]
                                if orItem["rewardType"] == "3":
                                    if orItem["rewardVal"] != "":
                                        ORValItem["normal_integral"] = orItem["rewardVal"]
                                    if orItem["rewardType"] == "4":
                                        if orItem["rewardVal"] != "":
                                            ORValItem["integral"] = orItem["rewardVal"]
                                        if orItem["rewardType"] == "5":
                                            if orItem["rewardVal"] != "":
                                                ORValItem["code"] = orItem["rewardVal"]

        rewStr = ""
        if ORValItem["DLAmount"] != "":
            inputSimpleText("#ChangeCurrencyBalance Normal " + ORValItem["DLAmount"] + " " + userSteamid)
            rewStr = rewStr + "美金：【" + ORValItem["DLAmount"] + "】、"
        if ORValItem["amount"] != "":
            rewStr = rewStr + "熊币：【" + ORValItem["amount"] + "】、"
            updateUserData["amount"] = str(int(updateUserData["amount"]) + int(float(ORValItem["amount"])))
            updateDataToUser(updateUserData)
        if ORValItem["normal_integral"] != "":
            updateUserData["normal_integral"] = str(int(updateUserData["normal_integral"]) + int(float(ORValItem["normal_integral"])))
            updateDataToUser(updateUserData)
            rewStr = rewStr + "称号积分：【" + ORValItem["normal_integral"] + "】、"
        if ORValItem["integral"] != "":
            updateUserData["integral"] = str(int(updateUserData["integral"]) + int(float(ORValItem["integral"])))
            rewStr = rewStr + "VIP积分：【" + ORValItem["integral"] + "】、"
            updateDataToUser(updateUserData)
        if ORValItem["code"] != "":
            rewStr = rewStr + "一堆装备"
            coArr = ORValItem["code"].split(",")
            for coItem in coArr:
                inputSimpleText(coItem + " Location " + userSteamid)

        if "onlineAnnoType" in robotOptions:
            if robotOptions["onlineAnnoType"] == "1":
                inputSimpleText("玩家【" + userFakename + "】获得在线奖励：" + rewStr + "您的奖励已发放~")

    if "onlineAnnoType" in robotOptions:
        if robotOptions["onlineAnnoType"] == "0":
            inputSimpleText("在线奖励发放完毕~")


loginFtpIsReading = False

def getFtpLog():
    global ftp
    global isReadingLoginCount
    global loginFtpIsReading
    global needSendLoginLogArr
    global sftp
    if loginFtpIsReading:
        return False
    loginFtpIsReading = True
    host = robotOptions["ftpIp"]
    ftpport = robotOptions["ftpPort"]
    user = robotOptions["ftpUser"]
    pwd = robotOptions["ftpPwd"]
    ftpType = robotOptions["ftpType"]
    file_content = ""
    file_content2 = ""
    try:
        try:
            printToLog("开始查询登录日志...")
            if ftpType == 1:
                testList = "---"
                try:
                    ftp.voidcmd("PWD")
                except Exception:
                    ftp = connect_ftp()

                if testList == "---":
                    loginFIleList = []
                    try:
                        testList = ftp.pwd()
                    except Exception:
                        ftp = connect_ftp()

                    if testList == "---":
                        loginFtpIsPending = False
                        loginFtpIsReading = False
                        return False
                    try:
                        ftp.cwd("/")
                        ftp.cwd("/SCUM/Saved/SaveFiles/Logs")
                        file_list = []
                        loginFIleList = []
                        ftp.retrlines("LIST", file_list.append)
                        for i in file_list:
                            if "login" in i:
                                loginFIleList.append(i)

                        lastTwoFileNameArr = loginFIleList[-2:]
                        if len(lastTwoFileNameArr) > 0:
                            encoding = "utf-16 LE"
                            file_data = io.BytesIO()
                            file_data_two = io.BytesIO()
                            ftp.retrbinary("RETR " + lastTwoFileNameArr[1].split(" ")[8], file_data.write)
                            ftp.retrbinary("RETR " + lastTwoFileNameArr[0].split(" ")[8], file_data_two.write)
                            file_data.seek(0)
                            file_content = file_data.read().decode(encoding).split("\n")
                            file_content2 = file_data_two.read().decode(encoding).split("\n")
                    except Exception as e:
                        try:
                            printToLog(e)
                        finally:
                            e = None
                            del e

            if ftpType == 2 or ftpType == 3:
                testList = ""
                try:
                    testList = sftp.listdir()
                except Exception as e:
                    try:
                        sftp = connect_sftp()
                    finally:
                        e = None
                        del e

                if sftp != None:
                    loginFIleList = []
                    try:
                        printToLog("开始读目录")
                        sftp.chdir("/")
                        firstDir = sftp.listdir()
                        sftp.chdir(firstDir[0])
                        if ftpType == 2:
                            sftp.chdir("SaveFiles")
                            sftp.chdir("Logs")
                        totalList = sftp.listdir()
                        printToLog("读目录结束")
                        for i in totalList:
                            if "login" in i:
                                loginFIleList.append(i)

                        lastTwoFileNameArr = loginFIleList[-2:]
                        encoding = "utf-16 LE"
                        remote_file1 = sftp.open(lastTwoFileNameArr[1], "rb")
                        file_data_obj = io.BytesIO(remote_file1.read())
                        remote_file1.close()
                        remote_file2 = sftp.open(lastTwoFileNameArr[0], "rb")
                        file_data_obj_two = io.BytesIO(remote_file2.read())
                        remote_file2.close()
                        file_content = file_data_obj.read().decode(encoding).split("\n")
                        file_content2 = file_data_obj_two.read().decode(encoding).split("\n")
                        lastLoginLog = file_content[-1]
                    except Exception as e:
                        try:
                            loginFtpIsReading = False
                        finally:
                            e = None
                            del e

                if file_content != "" and file_content2 != "":
                    lastLoginLog = file_content[-1]
                    if lastLoginLog not in lastLoginLogArr:
                        if "logged" in lastLoginLog:
                            lastLoginLogArr.append(lastLoginLog)
                            if len(lastLoginLogArr) > 10:
                                lastLoginLogArr.pop(0)
                            if lastLoginLog not in lastLoginLogArr:
                                lastLoginLogArr.append(lastLoginLog)
                            if lastLoginLog not in needSendLoginLogArr:
                                needSendLoginLogArr = []
                                if "logged out" in lastLoginLog:
                                    file_content.reverse()
                                    file_content2.reverse()
                                    curLogArr = file_content
                                    preLogArr = file_content2
                                    isHaveCur = False
                                    lastLogedIn = ""
                                    for i in curLogArr:
                                        if i != "":
                                            usrId = i.split(" ")[2].split(":")[0]
                                            if usrId in i:
                                                if "logged in" in i:
                                                    isHaveCur = True
                                                    lastLogedIn = i
                                                    break

                                    if isHaveCur == False:
                                        for i in preLogArr:
                                            if i != "":
                                                usrId = i.split(" ")[2].split(":")[0]
                                                if usrId in i:
                                                    if "logged in" in i:
                                                        isHaveCur = True
                                                        lastLogedIn = i
                                                        break

                                    if isHaveCur == True:
                                        time = lastLogedIn.split(" ")[0].split("-")
                                        newTime = time[0].replace(".", "-", 5) + " " + time[1].split(":")[0].replace(".", ":", 5)
                                        lastTimeArr = lastLoginLog.split(" ")[0].split("-")
                                        lastTime = lastTimeArr[0].replace(".", "-", 5) + " " + lastTimeArr[1].split(":")[0].replace(".", ":", 5)
                                        time1 = datetime.strptime(newTime, "%Y-%m-%d %H:%M:%S")
                                        time2 = datetime.strptime(lastTime, "%Y-%m-%d %H:%M:%S")
                                        time_diff = int((time2 - time1).total_seconds() / 60)
                                    needSendLoginLogArr.append(lastLoginLog + "-----" + str(time_diff))
                                else:
                                    needSendLoginLogArr.append(lastLoginLog)
                            with open((directory + "/lastLoginLogData.txt"), "w", encoding="UTF-8") as f:
                                f.write("\n".join(lastLoginLogArr))
                    loginFtpIsReading = False
                    isReadingLoginCount = 0
        except Exception as e:
            try:
                printToLog(e)
                loginFtpIsReading = False
                isReadingLoginCount = 0
            finally:
                e = None
                del e

    finally:
        loginFtpIsReading = False
        isReadingLoginCount = 0


killFtpIsReading = False

def getKillFtpLog():
    global killFtpIsPending
    global killFtpIsReading
    global killftp
    global killsftp
    global needSendKillLogArr
    if killFtpIsReading:
        return False
    killFtpIsReading = True
    killFtpIsPending = True
    host = robotOptions["ftpIp"]
    ftpport = robotOptions["ftpPort"]
    user = robotOptions["ftpUser"]
    pwd = robotOptions["ftpPwd"]
    ftpType = robotOptions["ftpType"]
    file_content = ""
    try:
        if ftpType == 1:
            testList = "---"
            try:
                killftp.voidcmd("PWD")
            except Exception:
                killftp = connect_kill_ftp()

            if testList == "---":
                loginFIleList = []
                try:
                    testList = killftp.pwd()
                except Exception:
                    killftp = connect_kill_ftp()

                if testList == "---":
                    killFtpIsReading = False
                    killFtpIsPending = False
                    return False
                try:
                    killftp.cwd("/")
                    killftp.cwd("/SCUM/Saved/SaveFiles/Logs")
                    file_list = []
                    loginFIleList = []
                    killftp.retrlines("LIST", file_list.append)
                    for i in file_list:
                        if "kill" in i:
                            if "event_kill" not in i:
                                loginFIleList.append(i)

                    lastTwoFileNameArr = loginFIleList[-2:]
                    if len(lastTwoFileNameArr) > 0:
                        encoding = "utf-16 LE"
                        file_data = io.BytesIO()
                        killftp.retrbinary("RETR " + lastTwoFileNameArr[1].split(" ")[8], file_data.write)
                        file_data.seek(0)
                        file_content = file_data.read().decode(encoding).split("\n")
                except Exception as e:
                    try:
                        printToLog(e)
                    finally:
                        e = None
                        del e

        if ftpType == 2 or ftpType == 3:
            testList = ""
            try:
                testList = killsftp.listdir()
            except Exception:
                killsftp = connect_sftp()

            if killsftp != None:
                loginFIleList = []
                try:
                    testList = killsftp.listdir()
                except Exception:
                    killsftp = connect_sftp()

                curr = killsftp.getcwd()
                killsftp.chdir("/")
                firstDir = killsftp.listdir()
                killsftp.chdir(firstDir[0])
                if ftpType == 2:
                    killsftp.chdir("SaveFiles")
                    killsftp.chdir("Logs")
                totalList = killsftp.listdir()
                for i in totalList:
                    if "kill" in i:
                        if "event_kill" not in i:
                            loginFIleList.append(i)

                lastTwoFileNameArr = loginFIleList[-2:]
                encoding = "utf-16 LE"
                remote_file1 = killsftp.open(lastTwoFileNameArr[1], "rb")
                file_data_obj = io.BytesIO(remote_file1.read())
                remote_file1.close()
                file_content = file_data_obj.read().decode(encoding).split("\n")
            if file_content != "":
                lastLoginLogArr = file_content[-5:]
                for lastLoginLog in lastLoginLogArr:
                    if lastLoginLog not in lastKillLogArr:
                        if "Died" in lastLoginLog:
                            lastKillLogArr.append(lastLoginLog)
                            if len(lastKillLogArr) > 10:
                                lastKillLogArr.pop(0)
                            if lastLoginLog not in lastKillLogArr:
                                lastKillLogArr.append(lastLoginLog)
                            if lastLoginLog not in needSendKillLogArr:
                                needSendKillLogArr.append(lastLoginLog)
                            with open((directory + "/lastKillLogData.txt"), "w", encoding="UTF-8") as f:
                                f.write("\n".join(lastKillLogArr))

            killFtpIsPending = False
            killFtpIsReading = False
    except Exception as e:
        try:
            printToLog(e)
            killFtpIsPending = False
            killFtpIsReading = False
        finally:
            e = None
            del e


isReadingLoginCount = 0
loginLogThread = None
loginTimeOutState = False

def getLoginLogData():
    global isReadingLoginCount
    global loginFtpIsReading
    global loginTimeOutState
    isReadingLoginCount = isReadingLoginCount + robotOptions["checkSleepTime"]
    if isReadingLoginCount > 60:
        isReadingLoginCount = 0
        loginTimeOutState = True
        loginFtpIsReading = False
        printToLog("FTP服务器长时间无响应，即将重新连接...")
    if loginFtpIsReading == False:
        if "ftpType" in robotOptions:
            if "ftpIp" in robotOptions:
                if robotOptions["ftpIp"] != "":
                    if "ftpPort" in robotOptions:
                        if robotOptions["ftpPort"] != 0:
                            if "ftpUser" in robotOptions:
                                if robotOptions["ftpUser"] != "":
                                    if "ftpPwd" in robotOptions:
                                        if robotOptions["ftpPwd"] != "":
                                            printToLog("查询登录日志中")
                                            threading.Thread(target=getFtpLog, daemon=True).start()


scpLoginIsReading = False

def getLoginLogDataSCP():
    global scpLoginIsReading
    if scpLoginIsReading == False:
        scpLoginIsReading = True
        printToLog("查询登录日志中")
        threading.Thread(target=getSCPFtpLog, daemon=True).start()


startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
localFileDir = os.getcwd()

def getSCPFtpLog():
    global needSendLoginLogArr
    global scpLoginIsReading
    host = robotOptions["ftpIp"]
    ftpport = str(robotOptions["ftpPort"])
    user = robotOptions["ftpUser"]
    pwd = robotOptions["ftpPwd"]
    ftpType = robotOptions["ftpType"]
    ftpFileType = "sftp"
    ftpFilePath = "/SCUM/Saved/SaveFiles/Logs/"
    if "ftpGetType" in robotOptions:
        if robotOptions["ftpGetType"] == "1":
            host = bjxHost
            ftpport = bjxFtpport
            user = bjxUser
            pwd = bjxPwd
            ftpType = bjxFtpType
            ftpFileType = "ftp"
            ftpFilePath = "/" + robotOptions["secertKey"] + "----" + str(robotOptions["ftpType"]) + "/"
    scpDir = localFileDir + "/Plugin/"
    try:
        if "ftpGetType" in robotOptions and robotOptions["ftpGetType"] == "1":
            pass
        else:
            printToLog("直连ftp")
            if ftpType == 1:
                ftpFileType = "ftp"
            if ftpType == 2:
                result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "ls" "exit"'), startupinfo=startupinfo)
                arr = result.decode("utf-8")
                arr = arr.split("\r\n")
                arrList = []
                for i in arr:
                    if host + "_" in i:
                        arrList.append(i.split(" ")[-1])

                menuWord = arrList[0]
                ftpFilePath = "/" + menuWord + "/SaveFiles/Logs/"
            if ftpType == 3:
                result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "ls" "exit"'), startupinfo=startupinfo)
                arr = result.decode("utf-8")
                arr = arr.split("\r\n")
                arrList = []
                for i in arr:
                    if host + "_" in i:
                        arrList.append(i.split(" ")[-1])

                menuWord = arrList[0]
                ftpFilePath = "/" + menuWord + "/"
            print(ftpFilePath)
            result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "cd ' + ftpFilePath + '" "ls" "exit"'), startupinfo=startupinfo)
            arr = result.decode("utf-8")
            arr = arr.split("\r\n")
            arrList = []
            killList = []
            playList = []
            chatList = []
            for i in arr:
                if ".log" in i:
                    if "login_" in i:
                        arrList.append(i.split(" ")[-1])
                    if ".log" in i:
                        if "chat_" in i:
                            chatList.append(i.split(" ")[-1])
                        if ".log" in i:
                            if "gameplay_" in i:
                                playList.append(i.split(" ")[-1])
                            if ".log" in i:
                                if "kill_" in i:
                                    killList.append(i.split(" ")[-1])

            lastLoginFileArr = arrList[-2:]
            killList = killList[-1:]
            playList = playList[-1:]
            chatList = chatList[-1:]
            loginList = arrList[-1:]
            lastLogsName["chat"] = chatList[0]
            lastLogsName["gameplay"] = playList[0]
            lastLogsName["kill"] = killList[0]
            lastLogsName["login"] = loginList[0]
            downStr = scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" '
            for i in lastLoginFileArr:
                downStr = downStr + '"get ' + ftpFilePath + i + " " + localFileDir + "\\Logs\\" + i + '" '

            for i in killList:
                downStr = downStr + '"get ' + ftpFilePath + i + " " + localFileDir + "\\Logs\\" + i + '" '

            for i in playList:
                downStr = downStr + '"get ' + ftpFilePath + i + " " + localFileDir + "\\Logs\\" + i + '" '

            for i in chatList:
                downStr = downStr + '"get ' + ftpFilePath + i + " " + localFileDir + "\\Logs\\" + i + '" '

            downStr = downStr + '"exit"'
            result = subprocess.check_output(downStr, startupinfo=startupinfo)
            with open((directory + "/Logs/" + lastLoginFileArr[0]), "r", encoding="UTF-16 LE") as file:
                fileData = file.read()
                file_content2 = fileData.split("\n")
            with open((directory + "/Logs/" + lastLoginFileArr[1]), "r", encoding="UTF-16 LE") as file:
                fileData = file.read()
                file_content = fileData.split("\n")
            if isOnlyGift == False and "isOpenLoginLog" in robotOptions and robotOptions["isOpenLoginLog"] == 1 or "bossLog" in robotOptions and robotOptions["bossLog"][0]["steamid"] != "":
                if file_content != "" and file_content2 != "":
                    lastLoginLog = file_content[-1]
                    if lastLoginLog not in lastLoginLogArr:
                        if "logged" in lastLoginLog:
                            lastLoginLogArr.append(lastLoginLog)
                            if len(lastLoginLogArr) > 10:
                                lastLoginLogArr.pop(0)
                            if lastLoginLog not in lastLoginLogArr:
                                lastLoginLogArr.append(lastLoginLog)
                            if lastLoginLog not in needSendLoginLogArr:
                                needSendLoginLogArr = []
                                if "logged out" in lastLoginLog:
                                    file_content.reverse()
                                    file_content2.reverse()
                                    curLogArr = file_content
                                    preLogArr = file_content2
                                    isHaveCur = False
                                    lastLogedIn = ""
                                    for i in curLogArr:
                                        if i != "":
                                            usrId = i.split(" ")[2].split(":")[0]
                                            if usrId in i:
                                                if "logged in" in i:
                                                    isHaveCur = True
                                                    lastLogedIn = i
                                                    break

                                    if isHaveCur == False:
                                        for i in preLogArr:
                                            if i != "":
                                                usrId = i.split(" ")[2].split(":")[0]
                                                if usrId in i:
                                                    if "logged in" in i:
                                                        isHaveCur = True
                                                        lastLogedIn = i
                                                        break

                                    if isHaveCur == True:
                                        time = lastLogedIn.split(" ")[0].split("-")
                                        newTime = time[0].replace(".", "-", 5) + " " + time[1].split(":")[0].replace(".", ":", 5)
                                        lastTimeArr = lastLoginLog.split(" ")[0].split("-")
                                        lastTime = lastTimeArr[0].replace(".", "-", 5) + " " + lastTimeArr[1].split(":")[0].replace(".", ":", 5)
                                        time1 = datetime.strptime(newTime, "%Y-%m-%d %H:%M:%S")
                                        time2 = datetime.strptime(lastTime, "%Y-%m-%d %H:%M:%S")
                                        time_diff = int((time2 - time1).total_seconds() / 60)
                                    needSendLoginLogArr.append(lastLoginLog + "-----" + str(time_diff))
                                else:
                                    needSendLoginLogArr.append(lastLoginLog)
                            with open((directory + "/lastLoginLogData.txt"), "w", encoding="UTF-8") as f:
                                f.write("\n".join(lastLoginLogArr))
                    scpLoginIsReading = False
    except Exception as e:
        try:
            scpLoginIsReading = False
            printToLog("读取登陆日志失败...")
            printToLog(e)
            print(e)
        finally:
            e = None
            del e


def getChatFileLogData():
    global scpLoginIsReading
    host = robotOptions["ftpIp"]
    ftpport = str(robotOptions["ftpPort"])
    user = robotOptions["ftpUser"]
    pwd = robotOptions["ftpPwd"]
    ftpType = robotOptions["ftpType"]
    ftpFileType = "sftp"
    ftpFilePath = "/SCUM/Saved/SaveFiles/Logs/"
    host = bjxHost
    ftpport = bjxFtpport
    user = bjxUser
    pwd = bjxPwd
    ftpType = bjxFtpType
    ftpFileType = "ftp"
    ftpFilePath = "/" + robotOptions["secertKey"] + "----" + str(robotOptions["ftpType"]) + "/"
    scpDir = localFileDir + "/Plugin/"
    try:
        if "ftpGetType" in robotOptions and robotOptions["ftpGetType"] == "1":
            cmdStr = scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" '
            for i in range(2):
                cmdStr = cmdStr + '"synchronize local ' + localFileDir + "\\Logs\\" + " " + ftpFilePath + ' -filemask=*.log" '

            cmdStr = cmdStr + '"exit"'
            subprocess.check_output(cmdStr)
    except Exception as e:
        try:
            scpLoginIsReading = False
            printToLog("读取聊天日志失败...")
            printToLog(e)
            print(e)
        finally:
            e = None
            del e


isReadingKillCount = 0

def getKillLogData():
    global isReadingKillCount
    global killFtpIsPending
    isReadingKillCount = isReadingKillCount + 1
    if isReadingKillCount > 5:
        isReadingKillCount = 0
    if killFtpIsPending == False:
        if killFtpIsReading == False:
            killFtpIsPending = True
            if "ftpType" in robotOptions:
                if "ftpIp" in robotOptions:
                    if robotOptions["ftpIp"] != "":
                        if "ftpPort" in robotOptions:
                            if robotOptions["ftpPort"] != 0:
                                if "ftpUser" in robotOptions:
                                    if robotOptions["ftpUser"] != "":
                                        if "ftpPwd" in robotOptions:
                                            if robotOptions["ftpPwd"] != "":
                                                printToLog("查询击杀日志中")
                                                threading.Thread(target=getKillFtpLog).start()


scpKillIsReading = False

def getKillLogDataSCP():
    global scpKillIsReading
    if scpKillIsReading == False:
        scpKillIsReading = True
        printToLog("查询击杀日志中")
        threading.Thread(target=getKillSCPLog, daemon=True).start()


def getKillSCPLog():
    global scpKillIsReading
    host = robotOptions["ftpIp"]
    ftpport = str(robotOptions["ftpPort"])
    user = robotOptions["ftpUser"]
    pwd = robotOptions["ftpPwd"]
    ftpType = robotOptions["ftpType"]
    scpDir = localFileDir + "/Plugin/"
    ftpFileType = "sftp"
    ftpFilePath = "/SCUM/Saved/SaveFiles/Logs/"
    if "ftpGetType" in robotOptions:
        if robotOptions["ftpGetType"] == "1":
            host = bjxHost
            ftpport = bjxFtpport
            user = bjxUser
            pwd = bjxPwd
            ftpType = bjxFtpType
            ftpFileType = "ftp"
            ftpFilePath = "/" + robotOptions["secertKey"] + "----" + str(robotOptions["ftpType"]) + "/"
    try:
        if "ftpGetType" in robotOptions and robotOptions["ftpGetType"] == "1":
            pass
        else:
            if ftpType == 1:
                ftpFileType = "ftp"
            if ftpType == 2:
                result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "ls" "exit"'), startupinfo=startupinfo)
                arr = result.decode("utf-8")
                arr = arr.split("\r\n")
                arrList = []
                for i in arr:
                    if host + "_" in i:
                        arrList.append(i.split(" ")[-1])

                menuWord = arrList[0]
                ftpFilePath = "/" + menuWord + "/SaveFiles/Logs/"
            if ftpType == 3:
                result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "ls" "exit"'), startupinfo=startupinfo)
                arr = result.decode("utf-8")
                arr = arr.split("\r\n")
                arrList = []
                for i in arr:
                    if host + "_" in i:
                        arrList.append(i.split(" ")[-1])

                menuWord = arrList[0]
                ftpFilePath = "/" + menuWord + "/"
            result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "cd ' + ftpFilePath + '" "ls" "exit"'), startupinfo=startupinfo)
            arr = result.decode("utf-8")
            arr = arr.split("\r\n")
            killList = []
            for i in arr:
                if ".log" in i:
                    if "kill_" in i:
                        if "event_kill_" not in i:
                            killList.append(i.split(" ")[-1])

            lastKillFileArr = killList[-1:]
            for i in lastKillFileArr:
                result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "get ' + ftpFilePath + i + " " + localFileDir + "\\Logs\\" + i + '" "exit"'), startupinfo=startupinfo)

            file_content = ""
            with open((directory + "/Logs/" + lastKillFileArr[0]), "r", encoding="UTF-16 LE") as file:
                fileData = file.read()
                file_content = fileData.split("\n")
            if file_content != "":
                lastLoginLogArr = file_content[-5:]
                for lastLoginLog in lastLoginLogArr:
                    if lastLoginLog not in lastKillLogArr:
                        if "Died" in lastLoginLog:
                            lastKillLogArr.append(lastLoginLog)
                            if len(lastKillLogArr) > 10:
                                lastKillLogArr.pop(0)
                            if lastLoginLog not in lastKillLogArr:
                                lastKillLogArr.append(lastLoginLog)
                            if lastLoginLog not in needSendKillLogArr:
                                needSendKillLogArr.append(lastLoginLog)
                            with open((directory + "/lastKillLogData.txt"), "w", encoding="UTF-8") as f:
                                f.write("\n".join(lastKillLogArr))

            scpKillIsReading = False
    except Exception as e:
        try:
            scpKillIsReading = False
            printToLog("读取击杀日志失败...")
            printToLog(e)
            print(e)
        finally:
            e = None
            del e


scpAdminIsReading = False
needSendAdminMoniArr = []

def checkIsNeedMonitAdmin():
    global scpAdminIsReading
    oldData = ""
    with open((directory + "/monitorAdmin.txt"), "r", encoding="UTF-8") as file:
        oldData = file.read()
    if oldData == "" or oldData == None:
        oldObj = []
    else:
        try:
            stream = io.StringIO(oldData)
            oldObj = json.load(stream)
            if len(oldObj) > 0:
                if scpAdminIsReading == False:
                    printToLog("查询权限日志中...")
                    threading.Thread(target=checkMonitAdminLog, daemon=True).start()
        except Exception as e:
            try:
                listOldData = []
                with open((directory + "/monitorAdmin.txt"), "r", encoding="UTF-8") as file:
                    listOldData = file.read()
                if listOldData == "" or listOldData == None:
                    listOldData = []
                else:
                    stream = io.StringIO(listOldData)
                    listOldData = json.load(stream)
                for item in listOldData:
                    startMonitorPlayerAdmin(["", item["steamid"]])
                    time.sleep(0.5)

                inputSimpleText("南极熊机器人提示：权限监控数据错误，已重新格式化权限监控数据！")
            finally:
                e = None
                del e


def sendAdminMoniAnnou():
    global banAdminIsReading
    global needSendAdminMoniArr
    maxTimes = robotOptions["maxAdminTimes"] or "2"
    for item in needSendAdminMoniArr:
        if len(item["cmds"]) >= int(maxTimes):
            if banAdminIsReading == False:
                inputSimpleText("#Announce 警告：玩家【" + item["steamid"] + "】使用了非法权限命令，警告【" + str(len(item["cmds"])) + "】次，满【" + maxTimes + "】次将直接Ban出服务器！！！")
                printToLog("更新权限文件中...")
                threading.Thread(target=banAdminUser, args=(item["steamid"],), daemon=True).start()

    needSendAdminMoniArr = []


banAdminIsReading = False

def banAdminUser(banId):
    global banAdminIsReading
    banAdminIsReading = True
    host = robotOptions["ftpIp"]
    ftpport = str(robotOptions["ftpPort"])
    user = robotOptions["ftpUser"]
    pwd = robotOptions["ftpPwd"]
    ftpType = robotOptions["ftpType"]
    scpDir = localFileDir + "/Plugin/"
    try:
        ftpFileType = "sftp"
        ftpFilePath = "/SCUM/Saved/Config/WindowsServer/"
        if ftpType == 1:
            ftpFileType = "ftp"
        if ftpType == 2:
            result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "ls" "exit"'), startupinfo=startupinfo)
            arr = result.decode("utf-8")
            arr = arr.split("\r\n")
            arrList = []
            for i in arr:
                if host + "_" in i:
                    arrList.append(i.split(" ")[-1])

            menuWord = arrList[0]
            ftpFilePath = "/" + menuWord + "/Config/WindowsServer/"
        if ftpType == 3:
            result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "ls" "exit"'), startupinfo=startupinfo)
            arr = result.decode("utf-8")
            arr = arr.split("\r\n")
            arrList = []
            for i in arr:
                if host + "_" in i:
                    arrList.append(i.split(" ")[-1])

            menuWord = arrList[0]
            ftpFilePath = "/" + menuWord + "/Configs/"
        result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "cd ' + ftpFilePath + '" "ls" "exit"'), startupinfo=startupinfo)
        arr = result.decode("utf-8")
        arr = arr.split("\r\n")
        killList = []
        for i in arr:
            if "AdminUsers.ini" in i:
                if "ServerSettingsAdminUsers.ini" not in i:
                    killList.append(i.split(" ")[-1])

        lastKillFileArr = killList[-1:]
        for i in lastKillFileArr:
            result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "get ' + ftpFilePath + i + " " + localFileDir + "\\Logs\\" + i + '" "exit"'), startupinfo=startupinfo)

        file_content = ""
        with open((directory + "/Logs/" + lastKillFileArr[0]), "r", encoding="UTF-8") as file:
            fileData = file.read()
            file_content = fileData.split("\n")
        if file_content != "":
            lastLoginLogArr = file_content
            newAdminIni = []
            oldData = ""
            for lastLoginLog in lastLoginLogArr:
                if banId not in lastLoginLog:
                    newAdminIni.append(lastLoginLog)

            with open((directory + "/Logs/" + lastKillFileArr[0]), "w", encoding="UTF-8") as f:
                f.write("\n".join(newAdminIni))
            for i in lastKillFileArr:
                result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "put ' + localFileDir + "\\Logs\\" + i + " " + ftpFilePath + i + '" "exit"'), startupinfo=startupinfo)

            printToLog("更新权限文件成功...")
            time.sleep(30)
            inputSimpleText("#ban " + banId)
        banAdminIsReading = False
    except Exception as e:
        try:
            banAdminIsReading = False
            printToLog("更新权限文件失败...")
            printToLog(e)
            print(e)
        finally:
            e = None
            del e


def sendSetAdminAnnou():
    for item in needSendSetAdminArr:
        if "showAdminUserId" in robotOptions and robotOptions["showAdminUserId"] == "1":
            inputSimpleText("南极熊机器人管理命令提示：已成功授予玩家【" + item["steamid"] + "】权限！权限时长为：【" + item["timeMin"] + "】分钟，结束时间为：【" + item["timeStr"] + "】")
        else:
            inputSimpleText("南极熊机器人管理命令提示：已成功授予玩家权限！权限时长为：【" + item["timeMin"] + "】分钟，结束时间为：【" + item["timeStr"] + "】")
        if "godAdminInfo" in robotOptions:
            if robotOptions["godAdminInfo"] != "":
                inputSimpleText(robotOptions["godAdminInfo"])


def checkMonitAdminLog():
    global monitPlayerLoginByDroneSended
    global scpAdminIsReading
    scpAdminIsReading = True
    host = robotOptions["ftpIp"]
    ftpport = str(robotOptions["ftpPort"])
    user = robotOptions["ftpUser"]
    pwd = robotOptions["ftpPwd"]
    ftpType = robotOptions["ftpType"]
    scpDir = localFileDir + "/Plugin/"
    ftpFileType = "sftp"
    ftpFilePath = "/SCUM/Saved/SaveFiles/Logs/"
    if "ftpGetType" in robotOptions:
        if robotOptions["ftpGetType"] == "1":
            host = bjxHost
            ftpport = bjxFtpport
            user = bjxUser
            pwd = bjxPwd
            ftpType = bjxFtpType
            ftpFileType = "ftp"
            ftpFilePath = "/" + robotOptions["secertKey"] + "----" + str(robotOptions["ftpType"]) + "/"
    try:
        if "ftpGetType" in robotOptions and robotOptions["ftpGetType"] == "1":
            pass
        else:
            if ftpType == 1:
                ftpFileType = "ftp"
            if ftpType == 2:
                result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "ls" "exit"'), startupinfo=startupinfo)
                arr = result.decode("utf-8")
                arr = arr.split("\r\n")
                arrList = []
                for i in arr:
                    if host + "_" in i:
                        arrList.append(i.split(" ")[-1])

                menuWord = arrList[0]
                ftpFilePath = "/" + menuWord + "/SaveFiles/Logs/"
            if ftpType == 3:
                result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "ls" "exit"'), startupinfo=startupinfo)
                arr = result.decode("utf-8")
                arr = arr.split("\r\n")
                arrList = []
                for i in arr:
                    if host + "_" in i:
                        arrList.append(i.split(" ")[-1])

                menuWord = arrList[0]
                ftpFilePath = "/" + menuWord + "/"
            result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "cd ' + ftpFilePath + '" "ls" "exit"'), startupinfo=startupinfo)
            arr = result.decode("utf-8")
            arr = arr.split("\r\n")
            killList = []
            for i in arr:
                if ".log" in i:
                    if "admin_" in i:
                        killList.append(i.split(" ")[-1])

            lastKillFileArr = killList[-1:]
            for i in lastKillFileArr:
                result = subprocess.check_output((scpDir + 'WinSCP.com /command "open ' + ftpFileType + "://" + user + ":" + pwd + "@" + host + ":" + ftpport + ' -hostkey=*" "get ' + ftpFilePath + i + " " + localFileDir + "\\Logs\\" + i + '" "exit"'), startupinfo=startupinfo)

            file_content = ""
            with open((directory + "/Logs/" + lastKillFileArr[0]), "r", encoding="UTF-16 LE") as file:
                fileData = file.read()
                file_content = fileData.split("\n")
            if file_content != "":
                lastLoginLogArr = file_content[-80:]
                oldData = ""
                maxTimes = robotOptions["maxAdminTimes"] or "2"
                with open((directory + "/monitorAdmin.txt"), "r", encoding="UTF-8") as file:
                    oldData = file.read()
                if oldData == "" or oldData == None:
                    oldObj = []
                else:
                    stream = io.StringIO(oldData)
                    oldObj = json.load(stream)
                for lastLoginLog in lastLoginLogArr:
                    lastLoginLog = lastLoginLog.lower()
                    oldKey = 0
                    try:
                        for adminItem in oldObj:
                            if oldObj[oldKey]:
                                with open((directory + "/Logs/" + lastLogsName["login"]), "r", encoding="UTF-16 LE") as file:
                                    fileData = file.read()
                                    file_content2 = fileData.split("\n")
                                for logItem in file_content2:
                                    if oldObj[oldKey]["steamid"] in logItem:
                                        if "(as drone)" in logItem:
                                            if logItem not in monitPlayerLoginByDroneSended:
                                                userSteamId = logItem.split(" ")[2].split(":")[0]
                                                userName = logItem.split(" ")[2].split(":")[1].split("(")[0]
                                                printToLog("更新权限文件中...")
                                                threading.Thread(target=banAdminUser, args=userSteamId, daemon=True).start()
                                                inputSimpleText("#Announce 南极熊权限监控提示：发现建家人员【" + userName + "】使用无人机形态登陆游戏，即将取消其权限并BAN出服务器！如果为管理误操作，请停止对该玩家指令监控~")
                                                monitPlayerLoginByDroneSended.append(logItem)

                                idStr = ": '" + oldObj[oldKey]["steamid"] + ":"
                                if ": '" + oldObj[oldKey]["steamid"] + ":" in lastLoginLog:
                                    if lastLoginLog.find(idStr) > 0:
                                        if lastLoginLog.find(idStr) < 25:
                                            if "setgodmode" not in lastLoginLog:
                                                if "target of teleportto" not in lastLoginLog:
                                                    if lastLoginLog not in oldObj[oldKey]["cmds"]:
                                                        if len(oldObj[oldKey]["cmds"]) < int(maxTimes):
                                                            oldObj[oldKey]["cmds"].append(lastLoginLog)
                                                            needSendAdminMoniArr.append(oldObj[oldKey])
                                                        else:
                                                            nedKey = 0
                                                            nedHave = False
                                                            for nedItem in needSendAdminMoniArr:
                                                                if needSendAdminMoniArr[nedKey]["steamid"] == oldObj[oldKey]["steamid"]:
                                                                    nedHave = True
                                                                nedKey = nedKey + 1

                                                            if nedHave == False:
                                                                needSendAdminMoniArr.append(oldObj[oldKey])
                                                        print(needSendAdminMoniArr)
                                                    oldKey = oldKey + 1

                    except Exception as e:
                        try:
                            printToLog(e)
                            printToLog("13123123")
                            logging.error(str(datetime.now()))
                            logging.error(traceback.format_exc())
                        finally:
                            e = None
                            del e

                with open((directory + "/monitorAdmin.txt"), "w", encoding="UTF-8") as f:
                    f.write(json.dumps(oldObj, ensure_ascii=False))
            scpAdminIsReading = False
    except Exception as e:
        try:
            scpAdminIsReading = False
            printToLog("读取管理日志失败...")
            printToLog(e)
            print(e)
        finally:
            e = None
            del e


def on_button_click(a):
    webview.evaluate_js('getValueBB("aaa")')


def expose(window):
    window.evaluate_js("pywebview.api.on_button_click()")


def startRobotRun():
    global isReadingLoginCount
    global killFtpIsPending
    global loginFtpIsReading
    global robotIsRunning
    global robotRuningId
    global threadPool
    isReadingLoginCount = 0
    loginFtpIsReading = False
    killFtpIsPending = False
    robotIsRunning = True
    if robotRuningId == 0:
        t = threading.Thread(target=initRobot, daemon=True)
        threadPool.append(t)
        t.start()


def endRobotRun():
    global robotIsRunning
    robotIsRunning = False


def restartReadOptions():
    global newRobotaOptionsData
    with open((directory + "/options.json"), "r", encoding="utf-8") as file:
        contJson = json.load(file)
    if "secertKey" in contJson:
        if contJson["secertKey"] != "":
            data = {"secertKey": (contJson["secertKey"])}
            response = requests.get(url=("https://server.vipscum.cn/public/index.php/index/index/robotGetOptions?secert=" + data["secertKey"]), data=data)
            result = json.loads(response.text)
            if result["code"] == 0:
                newRobotaOptionsData = json.loads(result["data"])
                readOptions()
                inputSimpleText("南极熊机器人管理命令提示： 机器人重启成功！！！")
                printToLog("机器人重启成功！！")


mouseMoveTime = 0
clearMotoStatus = False
clearExtTime = 0
reLoadSecretTime = 0
restartTipStatus = False
restartTipTime = 0
onlineRewardTime = 0

def initAllFreeGiftLogs():
    for item in giftsKeys:
        sendedGiftDataObj[item] = []

    for item in vipGiftsKeys:
        sendedGiftDataObj[item] = []

    for item in transKeys:
        sendedGiftDataObj[item] = []

    for item in goodsKeys:
        sendedGiftDataObj[item] = []


fubenCheckTipTime = 0
robotRuningId = 0

def initRobot():
    global clearExtTime
    global clearMotoStatus
    global datatableConnect
    global fakeNameNeedFresh
    global fubenCheckTipTime
    global hwnd
    global mouseMoveTime
    global needSendAdminMoniArr
    global needSendKillLogArr
    global needSendLoginLogArr
    global needSendSetAdminArr
    global needSendStartMonitorAnnou
    global needTransNewPlayer
    global onlineRewardTime
    global reLoadSecretTime
    global restartTipStatus
    global restartTipTime
    global robotRuningId
    initResetAllPlayerNameStatus = False
    datatableConnect = sqlite3.connect("beijixiong.db")
    restartTipStatus = False
    runRobot()
    while robotIsRunning == True:
        robotRuningId = 1000
        try:
            if hwnd == 0:
                printToLog("未检测到游戏窗口，正在启动游戏1...")
                time.sleep(20)
                openGanme()
                time.sleep(60)
                win32gui.EnumWindows(callback, None)
                win32gui.ShowWindow(hwnd, 1)
            else:
                checkLoginState()
                now = datetime.now()
                nowTimeObj = str(datetime.now()).split(" ")[1].split(".")[0].split(":")
                nowTime = nowTimeObj[0] + ":" + nowTimeObj[1]
                if len(needSendStartMonitorAnnou) > 0:
                    sendStartMonitorAnnou()
                    needSendStartMonitorAnnou = []
                for rs in robotOptions["restart"]:
                    if rs != "":
                        if rs.find(nowTime) != -1:
                            if restartTipStatus == False:
                                restartTipTime = 0
                                inputSimpleText(robotOptions["restartMessage"])
                                restartTipStatus = True

                for rs in timeAnnKyes:
                    if rs != "":
                        if rs.find(nowTime) != -1:
                            if restartTipStatus == False:
                                try:
                                    tType = rs.split("-")[0]
                                    tDay = rs.split("-")[1]
                                    tTime = rs.split("-")[2]
                                    restartTipTime = 0
                                    if tType == "0":
                                        doTimeAnnou(timeAnnObjs[rs]["code"])
                                        restartTipStatus = True
                                    elif tType == "1":
                                        nowWeekDay = str(datetime.now().weekday())
                                        if nowWeekDay == tDay:
                                            doTimeAnnou(timeAnnObjs[rs]["code"])
                                            restartTipStatus = True
                                    elif tType == "2":
                                        nowWeekDay = str(datetime.now().day)
                                        if nowWeekDay == tDay:
                                            doTimeAnnou(timeAnnObjs[rs]["code"])
                                            restartTipStatus = True
                                except Exception as e:
                                    try:
                                        printToLog(e)
                                        if restartTipStatus == False:
                                            restartTipTime = 0
                                            doTimeAnnou(timeAnnObjs[rs]["code"])
                                            restartTipStatus = True
                                    finally:
                                        e = None
                                        del e

                if fakeNameNeedFresh == True and "isShowNormalVipName" in totalRobotOptions["options"] and totalRobotOptions["options"]["isShowNormalVipName"] == 1 or "isShowVipName" in totalRobotOptions["options"] and totalRobotOptions["options"]["isShowVipName"] == 1:
                    if initResetAllPlayerNameStatus == False:
                        printToLog("正在初始化玩家称号名称")
                        initResetAllPlayerNameStatus = True
                        fakeNameNeedFresh = False
                        updateAllPlayerName()
                    if reLoadSecretTime > 300:
                        checkPeroid(robotOptions["secertKey"])
                        if "fatchBanType" in robotOptions:
                            if robotOptions["fatchBanType"] == "0":
                                fatchBanListAndBan()
                            if not ("dayReduceVipInt" in robotOptions and robotOptions["dayReduceVipInt"] != ""):
                                if not "dayReduceNormalInt" in robotOptions or robotOptions["dayReduceNormalInt"] != "":
                                    checkDayReduceInt()
                                reLoadSecretTime = 0
                            reLoadSecretTime = reLoadSecretTime + 1
                            printToLog(reLoadSecretTime)
                            checkIsNeedMonitAdmin()
                            if len(needSendAdminMoniArr) > 0:
                                sendAdminMoniAnnou()
                                needSendAdminMoniArr = []
                            if len(needSendSetAdminArr) > 0:
                                sendSetAdminAnnou()
                                needSendSetAdminArr = []
                            checkSetAdminIsNeedReduce()
                            checkUnmutePlayer()
                            if len(needTransNewPlayer) > 0:
                                sendNewPlayerTrans()
                                needTransNewPlayer = []
                            fbCheckSleepTime = 60
                            if "fubenMainCheckTime" in robotOptions:
                                if robotOptions["fubenMainCheckTime"] != 0:
                                    fbCheckSleepTime = int(robotOptions["fubenMainCheckTime"])
                                fubenCheckTipTime = fubenCheckTipTime + robotOptions["checkSleepTime"]
                                if fubenCheckTipTime > fbCheckSleepTime:
                                    fubenCheckTipTime = 0
                                    getUserInfo("11")
                                    doCheckAllFuben()
                                restartTipTime = restartTipTime + robotOptions["checkSleepTime"]
                                if restartTipTime > 60:
                                    restartTipTime = 0
                                    restartTipStatus = False
                                    checkHBIsNeedReset()
                                    timeCheckServerIsRight()
                            if "clearTimeArr" in robotOptions and len(robotOptions["clearTimeArr"]) != 0:
                                if clearMotoStatus == False:
                                    if robotOptions["isClearDDcar"] == 1:
                                        for rs in robotOptions["clearTimeArr"]:
                                            if rs != "":
                                                if rs.find(nowTime) != -1:
                                                    restartTipTime = 0
                                                    clearMoto()
                                                    clearMotoStatus = True

                                    if clearMotoStatus == True:
                                        clearExtTime = clearExtTime + 1
                                        if clearExtTime > 60:
                                            clearMotoStatus = False
                                if "isRewardOnline" in robotOptions:
                                    if "onlineTime" in robotOptions:
                                        if robotOptions["isRewardOnline"] == 1:
                                            onlineSec = robotOptions["onlineTime"] * 60
                                            currentSec = onlineRewardTime * robotOptions["checkSleepTime"]
                                            if currentSec > onlineSec:
                                                onlineRewardTime = 0
                                                doAllRewardAmount()
                                            onlineRewardTime = onlineRewardTime + 1
                if robotIsOffline == True:
                    mouseMoveTime = mouseMoveTime + 5
                    if mouseMoveTime == 10:
                        moustMove()
                    if hwnd != win32gui.GetForegroundWindow():
                        printToLog("游戏窗口失焦，自动切换到游戏窗口")
                        hwnd = 0
                        win32gui.EnumWindows(callback, None)
                        if hwnd == 0:
                            printToLog("未检测到游戏窗口，正在启动游戏3..." + str(datetime.now()))
                            time.sleep(20)
                            openGanme()
                            time.sleep(20)
                            ui.press("enter")
                            time.sleep(60)
                        else:
                            win32gui.EnumWindows(callback, None)
                            win32gui.ShowWindow(hwnd, 1)
                            rect = win32gui.GetWindowRect(hwnd)
                            x = rect[0]
                            y = rect[1]
                            width = rect[2] - x
                            height = rect[3] - y
                            if width != 1280 or height != 720:
                                win32gui.SetWindowPos(hwnd, win32gui.GetDesktopWindow(), 0, 0, 1280, 720, win32con.SWP_NOMOVE | win32con.SWP_NOZORDER)
                            else:
                                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 1280, 720, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
                            x = rect[0]
                            y = rect[1]
                            ui.click(x=(x + 100), y=(y + 100), button="left")
                    if robotIsOffline == False:
                        getLocalLog()
                        printToLog("查询中" + str(datetime.now()))
                    if ftpHasPlugin == True:
                        getLoginLogDataSCP()
                    else:
                        getLoginLogData()
                    if len(needSendLoginLogArr) > 0:
                        doSendLoginLog(needSendLoginLogArr)
                        needSendLoginLogArr = []
                    if isOnlyGift == False:
                        if "isOpenKillLog" in robotOptions:
                            if robotOptions["isOpenKillLog"] == 1:
                                if ftpHasPlugin == True:
                                    getKillLogDataSCP()
                                else:
                                    getKillLogData()
                                if len(needSendKillLogArr) > 0:
                                    doSendKillLog(needSendKillLogArr)
                                    needSendKillLogArr = []
            time.sleep(robotOptions["checkSleepTime"])
        except Exception as e:
            try:
                print(e)
                printToLog(e)
                printToLog("获取数据出错，机器人重启中，如长时间未能恢复，请联系管理员协助解决")
                logging.error(str(datetime.now()))
                logging.error(traceback.format_exc())
                time.sleep(robotOptions["checkSleepTime"])
            finally:
                e = None
                del e

    robotRuningId = 0


class Api:

    def startRobot(self):
        global robotRunLogs
        robotRunLogs = []
        startRobotRun()
        data = {'code':0, 
         'data':"开启成功"}
        return data

    def endRobot(self):
        endRobotRun()
        data = {'code':0, 
         'data':"关闭成功"}
        return data

    def updateUserZJLhdWinRatio(self, val):
        global userZJLhdWinRatio
        directory = os.getcwd()
        userZJLhdWinRatio = val
        contJson = {}
        with open((directory + "/LHDRatio.txt"), "r", encoding="utf-8") as file:
            contJson = json.load(file)
        contJson["userZJLhdWinRatio"] = str(val)
        with open((directory + "/LHDRatio.txt"), "w", encoding="UTF-8") as f:
            f.write(json.dumps(contJson, ensure_ascii=False))

    def updateSystemZJLhdWinRatio(self, val):
        global systemZJLhdWinRatio
        directory = os.getcwd()
        systemZJLhdWinRatio = val
        contJson = {}
        with open((directory + "/LHDRatio.txt"), "r", encoding="utf-8") as file:
            contJson = json.load(file)
        contJson["systemZJLhdWinRatio"] = str(val)
        with open((directory + "/LHDRatio.txt"), "w", encoding="UTF-8") as f:
            f.write(json.dumps(contJson, ensure_ascii=False))

    def getRobotStatus(self):
        status = 0
        zjLhdData = readZjLhdData()
        if robotIsRunning == True:
            status = 1
        data = {'code':0,  'data':status, 
         'winRatio':userZJLhdWinRatio, 
         'systemWinRatio':systemZJLhdWinRatio, 
         'todayAmount':zjLhdData["todayAmount"], 
         'totalAmount':zjLhdData["totalAmount"]}
        return data

    def getRunLogs(self):
        data = {'code':0, 
         'data':robotRunLogs}
        return data

    def exportAllUngetCards(self):
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        cursor.execute("SELECT * FROM card_list WHERE card_state = '0'")
        results = cursor.fetchall()
        data = {'code':0, 
         'data':results}
        cursor.close()
        datatableConnectLocal.close()
        return data

    def getGiftCardList(self):
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        cursor.execute("SELECT * FROM card_list")
        results = cursor.fetchall()
        cursor.close()
        datatableConnectLocal.close()
        backData = {'code':0, 
         'data':results}
        return backData

    def createGiftCard(self, data):
        print(data)
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        cardsArr = []
        for i in range(data["cardNum"]):
            currentCardCode = md5_encrypt("beiJX" + str(datetime.now()) + str(i))
            cardsArr.append(currentCardCode)
            cursor.execute("INSERT INTO card_list (card_value, card_name, card_code, gold_num, amount_num, fame_num, xiong_num, card_state, create_time, admin_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (currentCardCode, data["cardName"], data["cardCode"], data["goldAmount"], data["normalAmount"], data["fameAmount"], data["xiongAmount"], "0", str(datetime.now()).split(".")[0], data["adminTime"]))

        datatableConnectLocal.commit()
        cursor.close()
        datatableConnectLocal.close()
        result = {'code':0, 
         'data':cardsArr}
        return result

    def editGiftCard(self, paData):
        data = {'code':0, 
         'message':""}
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        try:
            saveData = paData
            cursor.execute("UPDATE card_list SET card_name = ?, gold_num = ?, amount_num = ?, fame_num = ?, xiong_num = ?, card_code = ?, admin_time = ? WHERE card_id = ?", (saveData[2], saveData[4], saveData[5], saveData[6], saveData[7], saveData[3], saveData[13], saveData[0]))
            datatableConnectLocal.commit()
            data["code"] = 0
            data["message"] = "保存成功"
            cursor.close()
            datatableConnectLocal.close()
            return data
        except Exception as e:
            try:
                data["code"] = 1000
                data["message"] = "保存失败"
                cursor.close()
                datatableConnectLocal.close()
                return data
            finally:
                e = None
                del e

    def deleteAllGetedCards(self):
        data = {'code':0, 
         'message':""}
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        try:
            cursor.execute("DELETE FROM card_list WHERE card_state = ?", ('1', ))
            datatableConnectLocal.commit()
            data["code"] = 0
            data["message"] = "删除成功"
            cursor.close()
            datatableConnectLocal.close()
            return data
        except Exception as e:
            try:
                data["code"] = 1000
                data["message"] = "删除失败"
                cursor.close()
                datatableConnectLocal.close()
                return data
            finally:
                e = None
                del e

    def deleteGiftCard(self, id):
        data = {'code':0, 
         'message':""}
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        try:
            cursor.execute("DELETE FROM card_list WHERE card_id = ?", (id,))
            datatableConnectLocal.commit()
            data["code"] = 0
            data["message"] = "删除成功"
            cursor.close()
            datatableConnectLocal.close()
            return data
        except Exception as e:
            try:
                data["code"] = 1000
                data["message"] = "删除失败"
                cursor.close()
                datatableConnectLocal.close()
                return data
            finally:
                e = None
                del e

    def copyCode(self, data):
        pyperclip.copy(data)
        result = {'code':0, 
         'data':"success"}
        return result

    def getRobotIsSlowStatus(self):
        data = {'code':0, 
         'data':robotIsSlow}
        return data

    def setRobotIsSlowStatus(self, status):
        global robotIsSlow
        directory = os.getcwd()
        slowData = {"isSlow": 0}
        slowData["isSlow"] = status
        robotIsSlow = status
        print(slowData)
        print(robotIsSlow)
        data = {'code':0, 
         'message':""}
        try:
            with open((directory + "/slowOption.json"), "w", encoding="UTF-8") as f:
                f.write(json.dumps(slowData, ensure_ascii=False))
            data["code"] = 0
            data["message"] = "保存成功"
            return data
        except Exception as e:
            try:
                data["code"] = 1000
                data["message"] = "保存失败"
                return data
            finally:
                e = None
                del e

    def newRobotSaveInitSecert(self, data):
        newData = {"secertKey": data}
        directory = os.getcwd()
        with open((directory + "/options.json"), "w", encoding="UTF-8") as f:
            f.write(json.dumps(newData, ensure_ascii=False))
        data = {'code':0,  'data':"保存成功"}
        return data

    def sendNewRobotOptionsData(self, data):
        global newRobotaOptionsData
        newRobotaOptionsData = data

    def getDataFromClient(self):
        try:
            directory = os.getcwd()
            contJson = {}
            with open((directory + "/options.json"), "r", encoding="utf-8") as file:
                contJson = json.load(file)
            if "options" in contJson and "secertKey" in contJson["options"] and contJson["options"]["secertKey"] != "":
                newData = {"secertKey": (contJson["options"]["secertKey"])}
                with open((directory + "/optionsbak.json"), "w", encoding="utf-8") as f:
                    f.write(json.dumps(contJson, ensure_ascii=False))
                with open((directory + "/options.json"), "w", encoding="UTF-8") as f:
                    f.write(json.dumps(newData, ensure_ascii=False))
                data = {'code':0,  'data':newData, 
                 'oldData':contJson}
            else:
                data = {'code':0,  'data':contJson}
            return data
        except:
            return False

    def saveDataFromClient(self, paData):
        directory = os.getcwd()
        data = {'code':0, 
         'message':""}
        try:
            with open((directory + "/options.json"), "w", encoding="UTF-8") as f:
                f.write(json.dumps(paData, ensure_ascii=False))
            data["code"] = 0
            data["message"] = "保存成功"
            return data
        except Exception as e:
            try:
                data["code"] = 1000
                data["message"] = "保存失败"
                return data
            finally:
                e = None
                del e

    def deleteGetGift(self, id):
        data = {'code':0, 
         'message':""}
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        try:
            cursor.execute("DELETE FROM sended_gift WHERE id = ?", (id,))
            datatableConnectLocal.commit()
            data["code"] = 0
            data["message"] = "删除成功"
            cursor.close()
            datatableConnectLocal.close()
            initAllFreeGiftLogs()
            return data
        except Exception as e:
            try:
                data["code"] = 1000
                data["message"] = "删除失败"
                cursor.close()
                datatableConnectLocal.close()
                initAllFreeGiftLogs()
                return data
            finally:
                e = None
                del e

    def getShowZJLHD(self):
        result = 0
        if showZJLHD == True:
            result = 1
        return result

    def resetUserKeyword(self, obj):
        playerSteamid = obj["steamid"]
        keyword = obj["keyword"]
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        data = {'code':0, 
         'message':""}
        try:
            cursor.execute("DELETE FROM sended_gift WHERE steamid = ? AND keyword = ?", (playerSteamid, keyword))
            datatableConnectLocal.commit()
            data["code"] = 0
            data["message"] = "删除成功"
            cursor.close()
            datatableConnectLocal.close()
            return data
        except Exception as e:
            try:
                data["code"] = 1000
                data["message"] = "删除失败"
                cursor.close()
                datatableConnectLocal.close()
                return data
            finally:
                e = None
                del e

    def deleteUser(self, id):
        data = {'code':0, 
         'message':""}
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        try:
            cursor.execute("DELETE FROM user_list WHERE user_id = ?", (id,))
            datatableConnectLocal.commit()
            data["code"] = 0
            data["message"] = "删除成功"
            cursor.close()
            datatableConnectLocal.close()
            return data
        except Exception as e:
            try:
                data["code"] = 1000
                data["message"] = "删除失败"
                cursor.close()
                datatableConnectLocal.close()
                return data
            finally:
                e = None
                del e

    def editUserSave(self, paData):
        data = {'code':0, 
         'message':""}
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        try:
            saveData = paData
            cursor.execute("UPDATE user_list SET amount = ?, vip_level = ?, vip_end_time = ?, integral = ?, normal_integral = ?, normal_vip_level = ? WHERE user_id = ?", (saveData[3], saveData[7], saveData[8], saveData[9], saveData[11], saveData[12], saveData[0]))
            datatableConnectLocal.commit()
            data["code"] = 0
            data["message"] = "保存成功"
            cursor.close()
            datatableConnectLocal.close()
            return data
        except Exception as e:
            try:
                data["code"] = 1000
                data["message"] = "保存失败"
                cursor.close()
                datatableConnectLocal.close()
                return data
            finally:
                e = None
                del e

    def getAllUserList(self):
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        cursor.execute("SELECT * FROM user_list")
        results = cursor.fetchall()
        data = {'code':0, 
         'data':results}
        cursor.close()
        datatableConnectLocal.close()
        return data

    def checkCmdIsRight(self, name):
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        cursor.execute("SELECT * FROM sended_gift where keyword=?", (name,))
        results = cursor.fetchall()
        data = {'code':0, 
         'data':results}
        cursor.close()
        datatableConnectLocal.close()
        return data

    def deleteCmdLog(self, name):
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        cursor.execute("DELETE FROM sended_gift WHERE keyword = ?", (name,))
        datatableConnectLocal.commit()
        results = cursor.fetchall()
        data = {'code':0, 
         'data':results}
        cursor.close()
        datatableConnectLocal.close()
        return data

    def getAllGetGiftList(self):
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        cursor.execute("SELECT * FROM sended_gift")
        results = cursor.fetchall()
        data = {'code':0, 
         'data':results}
        cursor.close()
        datatableConnectLocal.close()
        return data

    def getAllLhdRankData(self, type):
        print(type)
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        if type == "1":
            cursor.execute("\n            SELECT player_name, player_steamid, SUM(win_amount) as total_win_amount\n            FROM lhd_log\n            GROUP BY player_steamid\n            ORDER BY total_win_amount\n            ")
        else:
            nowDateObj = str(datetime.now()).split(".")[0].split(" ")
            nowDateStr = nowDateObj[0]
            cursor.execute("SELECT player_name, player_steamid, SUM(win_amount) as total_win_amount FROM lhd_log WHERE date=?", (nowDateStr,))
        results = cursor.fetchall()
        data = {'code':0, 
         'data':results}
        cursor.close()
        datatableConnectLocal.close()
        return data

    def getAllCarInsurList(self):
        listArr = getCarInsurPolicyTotalList()
        data = {'code':0, 
         'data':listArr}
        return data

    def updateCarInsur(self, data):
        updateCarInsurPolicy(data)
        data = {"code": 0}
        return data

    def deleteCarInsur(self, id):
        deleteCarInsurPolicyById(id)
        data = {"code": 0}
        return data

    def getAllCarInsurGetedLogList(self):
        dataList = getCarInsurTotalGetList()
        data = {'code':0, 
         'data':dataList}
        return data

    def getAllLhdLogList(self):
        datatableConnectLocal = sqlite3.connect("beijixiong.db")
        cursor = datatableConnectLocal.cursor()
        cursor.execute("SELECT * FROM lhd_log")
        results = cursor.fetchall()
        data = {'code':0, 
         'data':results}
        cursor.close()
        datatableConnectLocal.close()
        return data

    def getServerNameForHost(self):
        result = ""
        return result

    def getServerNameForIp(self):
        global checkServerIsRight
        domain = "server.vipscum.cn"
        ip = get_ip(domain)
        result = ""
        if ip:
            result = ip
            if result == "120.53.94.209":
                checkServerIsRight = True
        else:
            checkServerIsRight = False
        return result


def on_window_close():
    print("关闭")
    os._exit(0)


def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return


def checkHeader(respon):
    pass


def timeCheckServerIsRight():
    global checkServerIsRight
    domain = "server.vipscum.cn"
    ip = get_ip(domain)
    domain2 = "120.53.94.209"
    ip2 = get_ip(domain2)
    if ip != ip2 or ip != "120.53.94.209" or ip2 != "120.53.94.209":
        checkServerIsRight = False
        os._exit(0)
    else:
        checkServerIsRight = True


timeCheckServerIsRight()

def getServerNameForIp():
    global checkServerIsRight
    domain = "server.vipscum.cn"
    ip = get_ip(domain)
    result = ""
    if ip:
        result = ip
        if result == "120.53.94.209":
            checkServerIsRight = True
    else:
        checkServerIsRight = False
    print(result)


getServerNameForIp()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False


def toggleRobot():
    global window
    window.evaluate_js("bb()")


if __name__ == "__main__" and checkServerIsRight == True:
    try:
        if is_admin():
            with open("C:/Windows/System32/drivers/etc/hosts", "r", encoding="UTF-8") as file:
                hostsData = file.read()
                if "server.vipscum.cn" in hostsData or "120.53.94.209" in hostsData:
                    ui.alert(text="当前运行环境异常，请联系管理员")
                else:
                    api = Api()
                    serverUrl = "https://scum.52ai.org/public/front/169/#/optionsJson"
                    window = webview.create_window(("南极熊-SCUM内置机器人--当前版本：V" + currentVer), serverUrl, js_api=api, width=1000, height=880, screen=None, resizable=True, fullscreen=False, min_size=(900,
                                                                                                                                                                                                                                   850))
                    window.events.closed += on_window_close
                    keyboard.add_hotkey("ctrl+end", toggleRobot)
                    webview.start(debug=False)
        else:
            ui.alert(text="请使用管理员权限打开机器人")
    except Exception as e:
        try:
            print(e)
            ui.alert(text="请使用管理员权限打开机器人")
        finally:
            e = None
            del e


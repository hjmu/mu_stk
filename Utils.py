from datetime import datetime
from inspect import getframeinfo, stack
import inspect
import matplotlib  # 注意这个也要import一次
import matplotlib.pyplot as plt

# caller = getframeinfo(stack()[1][0])


# class Utils():


# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
def pl():
    previous_frame = inspect.currentframe().f_back
    (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
    # return (filename, line_number, function_name, lines, index)
    # return (filename, line_number)
    # x= ','.join((filename, str(line_number)))
    # return '['+filename.rjust(40)+str(line_number).rjust(4)+']'
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')+'[' + filename.rjust(20) + str(line_number).rjust(5) + ']'

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    # def info(self,msg):
    #     caller = getframeinfo(stack()[1][0])
    #     print("%s %30s:%4d - %s" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),caller.filename, caller.lineno, msg))
    #     # print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')," ",caller.filename, caller.lineno,msg)




# REC_LIMIT=180
#
# OLS_SLOPE=0.1
# OLS_DIRECTION=1

# logFile="c:/mu_py/mylog.txt"

def getFont():
    myfont = matplotlib.font_manager.FontProperties(fname=r'C:/Windows/Fonts/mingliu.ttc')
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    return myfont
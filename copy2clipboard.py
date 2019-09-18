import win32clipboard as w
import win32con as wc
def copy(a):
    w.OpenClipboard()
    w.EmptyClipboard()
    w.SetClipboardData(wc.CF_UNICODETEXT,"12345")
    w.CloseClipboard()
a = "123"
cpoy(a)

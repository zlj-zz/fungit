import sys

sys.path.insert(0, ".")
from fungit.gui.utils import wrap_color_str, get_width


s = "[4;54f───────────────────────────────────────── [11;54f───────────────────────────────────────── [5;54f│                                        │[6;54f│                                        │[7;54f│                                        │[8;54f│                                        │[9;54f│                                        │[10;54f│                                        │[4;54f┌[4;95f┐[11;54f└[11;95f┘[4;56f[[1mhelp menu[22m][11;34f[1m2 of 2[22m[0m[5;55f"
chinese = "这是一段测试换行的string。金樽清酒斗十千，玉盘珍羞直万钱。(羞 同：馐；直 同：值) 停杯投箸不能食，拔剑四顾心茫然。 欲渡黄河冰塞川，将登太行雪满山。(雪满山 一作：雪暗天) 闲来垂钓碧溪上，忽复乘舟梦日边。(碧 一作：坐) 行路难，行路难，多歧路，今安在？ 长风破浪会有时，直挂云帆济沧海。"

"中国"


def test_wrap():
    resp = wrap_color_str(chinese, 40)
    for line in resp:
        print(len(line), line)

    resp = wrap_color_str(s, 40)
    for line in resp:
        print(len(line), f"'{line}'")


def test_char_width():
    for i in chinese:
        print(i, get_width(ord(i)), end=" ")

    print("\n")


if __name__ == "__main__":
    # print(s)
    test_wrap()
    test_char_width()
    # print(abc(i))

    ss = "────────────────────────────────────────"
    # print(len(ss))

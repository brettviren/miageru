from sh import Command, CommandNotFound, ErrorReturnCode
import miageru.tools.yad


def chirp(line):
    print(f'chirp: {line.strip()}')

multi_line_text = '''※ 月（つき）
1. [n] Moon
2. [n] month
3. [n] moonlight
4. [n] (a) moon; natural satellite

月（げつ）
1. [n;abbr] Monday
'''

def test_yad_lowlevel():
    yad = Command("yad")
    cmd="--always-print-result --height 500 --width 1000 --text-info".split()
    cmd+=["--button", "A:echo A", "--button", "B:4"]

    try:
        yad(*cmd, _out=chirp, _in=multi_line_text)
    except ErrorReturnCode as err:
        print(f"Command exited with exit code: {err.exit_code}")
        print(f"Stderr: {err.stderr.decode()}")
        print(f"Stdout: {err.stdout.decode()}")        

def chirp(line):
    print(f'test yad: {line=}')

def test_yad_tool():
    yad = miageru.tools.yad.Command()
    buttons = dict(A=chirp, B=42)

    rc = yad.dialog(text=multi_line_text, title="test yad", buttons=buttons)
    print(f'return code: {rc}')

if '__main__' == __name__:
    # test_yad_lowlevel()
    test_yad_tool()
    


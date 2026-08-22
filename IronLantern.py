if __name__ != "__main__":
    raise ImportError("Nahh ahhh!! I don't trust you with my code you eerie bastard!")

import hashlib
from pathlib import Path
import winreg
import os
import psutil
import subprocess
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import uuid
from argon2.low_level import hash_secret_raw, Type
import json
from cryptography.exceptions import InvalidTag
from datetime import datetime
import time

TG_FORM_URL = "https://go-ns.org.ua/wp-content/themes/go-ns/send-message-to-telegram.php"

TELEGRAM_URL = "https://t.me/s/gononstopukraine"
TIKTOK_URL = "https://www.tiktok.com/@gononstopukraine"
FACEBOOK_URL = "https://www.facebook.com/gononstopukraine"
WEB_URL = "https://go-ns.org.ua/"

TXT_PREVIEW_SIZE = 8192
TXT_PRINTABLE_THRESHOLD = 0.95
NULL_BYTE_RAT = 0.005

KEY_SOURCES: dict[str, str] = {
    "telegram": TELEGRAM_URL,
    "tik-tok": TIKTOK_URL,
    "facebook": FACEBOOK_URL,
    "web": WEB_URL,
}


PARAM_SET: dict[str, int] = {
    "YES" : 1,
    "Y" : 1,
    "yes" : 1,
    "y" : 1,
    "NO" : 0,
    "no" : 0,
    "N" : 0,
    "n" : 0,
}

NONCE_SIZE = 12
SALT_SIZE = 16
YOGI_SHA256 = "ecc42df31157857f6bb17e6fd458b8bf10047a80edff10f76a3ad7126fdc6926"

EXCLUDE_DIRS = {
    "System Volume Information",
    "Microsoft",
    "Windows Defender",
    "Program Files (x86)",
    ".nuget",
    "Windows Security",
    "DriverStore",
    "Appdata",
    "NVIDIA",
    "vendor",
    "Temporary Internet Files",
    "Application Data",
    "Microsoft.NET",
    "AMD",
    "Intel",
    "Drivers",
    "MSOCache",
    "Windows",
    "packages",
    ".git",
    "Recovery",
    "Cache",
    "Boot",
    "Temp",
    "Microsoft Help",
    "Local Settings",
    "$Recycle.Bin",
    "PerfLogs",
    "WinSxS",
    "Windows.old",
    "ProgramData",
    "node_modules",
    "All Users",
    "Program Files",
}

DORMANT_EXCLUDE_DIRS = {
    # OS / protected areas
    "Windows",
    "WinSxS",
    "System32",
    "SysWOW64",
    "System Volume Information",
    "Recovery",
    "$Recycle.Bin",

    # Installed applications
    "Program Files",
    "Program Files (x86)",

    # High-noise application/dependency directories
    "node_modules",
    "packages",
    ".git",
    ".nuget",
    "vendor",

    # Caches / temporary data
    "Cache",
    "Temporary Internet Files",

    # Hardware / driver related
    "DriverStore",
    "NVIDIA",
    "AMD",
    "Intel",
    "Drivers",
}

target_roots: dict[str, list[Path]] = {
    "USERPROFILE": [
        Path("Downloads"),
        Path("Desktop"),
        Path("Documents"),
        Path("Pictures"),
        Path("Videos"),
        Path("Music"),
        Path("OneDrive"),
        Path("Saved Games"),
    ],

    "LOCALAPPDATA": [
        Path("Temp"),
    ],

    "APPDATA": [
        Path("Microsoft") / "Crypto",
    ],

    "TEMP": [
        Path(""),
    ],
}
txt_policy = 0
Error_policy = 0
NoKey_policy = 0
Unknown_policy = 0
par_crawl_pol = 0
Combat_Mode = 0
extensiv_decrypt = 0
Quarantine_password =""
extensiv_dormant = 0
report_status = 0

report_op = None
Quar_path = None
key_dict: dict[str, bytes] = {}
suspect_path = set()

FILE_SIGNATURES = {
    ".jpg":    (b"\xFF\xD8\xFF", 0),
    ".jpeg":   (b"\xFF\xD8\xFF", 0),
    ".png":    (b"\x89PNG\r\n\x1A\n", 0),
    ".gif":    (b"GIF", 0),
    ".bmp":    (b"BM", 0),
    ".webp":   (b"RIFF", 0),

    ".pdf":    (b"%PDF-", 0),
    ".rtf":    (b"{\\rtf", 0),

    ".docx":   (b"PK\x03\x04", 0),
    ".xlsx":   (b"PK\x03\x04", 0),
    ".pptx":   (b"PK\x03\x04", 0),
    ".zip":    (b"PK\x03\x04", 0),
    ".rar":    (b"Rar!\x1A\x07", 0),
    ".7z":     (b"7z\xBC\xAF\x27\x1C", 0),
    ".gz":     (b"\x1F\x8B", 0),

    ".exe":    (b"MZ", 0),
    ".dll":    (b"MZ", 0),

    ".mp3":    (b"ID3", 0),
    ".flac":   (b"fLaC", 0),
    ".ogg":    (b"OggS", 0),
    ".wav":    (b"RIFF", 0),

    ".avi":    (b"RIFF", 0),
    ".mp4":    (b"ftyp", 4),
    ".mov":    (b"ftyp", 4),
    ".mkv":    (b"\x1A\x45\xDF\xA3", 0),

    ".sqlite": (b"SQLite format 3\x00", 0),
    ".class":  (b"\xCA\xFE\xBA\xBE", 0),
}

def Iron_Scribe_init() -> Path | str:
    global report_status
    print("[#] Initializing IronLantern report file...")
    if (os.environ.get("PUBLIC") is None) :
        print("[-] PUBLIC is unavailable, IronLantern can't create the report file.")
        report_status = 0
        return "NoReport"
    report_file = Path(os.environ.get("PUBLIC")) / "IronLantern" / "Reports"
    try:
        report_file.mkdir(parents=True, exist_ok=True)
    except OSError:
        print("[-] Couldn't create the IronLantern report directory. Running without a report.")
        return "NoReport"
    date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    report_filename = f"report_{date}.txt"
    report_file = report_file / report_filename
    print(f"[+] Report path ready at {report_file}.")
    return report_file

def Iron_Scribe(message : str) :
    if report_status == 0 :
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    if report_op is not None:
        report_op.write(line + "\n")
        report_op.flush()

def Scribe_open(rprt_path):
    global report_op, report_status
    if (isinstance(rprt_path, Path)) :
            try:
                report_op = rprt_path.open("x", encoding="utf-8")
                report_status = 1
            except OSError:
                report_status = 0

def Scribe_end(rprt_path):
    global report_op, report_status
    if report_op is None:
        report_status = 0
        return
    if not report_op.closed:
        msg = f"[#] IronLantern run finished. Closing report at {rprt_path}."
        print(msg)
        Iron_Scribe(msg)
        report_op.close()
    report_op = None
    report_status = 0

def Iron_Tearer() :
    appdata = os.environ.get("APPDATA")
    if appdata is None:
        message = "[-] Unable to access APPDATA while checking Startup persistence"
        print(message)
        Iron_Scribe(message)
        return "Critic_OS_fail"
    path = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "StartUp" #This path is recovered from the static analysis
    if path.is_dir():
        message = f"[*] Inspecting Startup persistence location at {path}"
        print(message)
        Iron_Scribe(message)
        for target in path.iterdir() :          #here we start looking inside the Startup folder which contains programs launched at startup
            if not target.is_file():            #if the element isn't a file we basically don't care
                continue
            if (target.suffix != ".exe"):       #if it's not an executable we don't care as well
                continue
            if (Iron_Hunt(target.resolve()) == "Huntdown") :    #we send our hunter to confirm that the signature matches Yogi
                suspect_path.add(target.resolve())               #and send it to a future execution (death)
                message = f"[+] Confirmed Yogi sample found in Startup folder at {target.resolve()}"
                print(message)
                Iron_Scribe(message)
        return
    else :
        message = f"[!] Expected Startup persistence location was not found at {path}"
        print(message)
        Iron_Scribe(message)
        return "NoPersist"    #just a debugging value I kept

#FUNCTION THAT REMOVES PERSISTENCE FROM HKCU REGISTRY AND %APPDATA%
def Iron_Scout():
    msg = "[#] Inspecting known registry persistence..."
    print(msg)
    Iron_Scribe(msg)
    reg_path = r"Software\Microsoft\Windows\CurrentVersion\Run" #The registry path is known from static analysis
    appdata = os.environ.get("APPDATA")
    if appdata is None:
        msg = "[-] APPDATA environment variable is unavailable; Iron_Scout cannot continue."
        print(msg)
        Iron_Scribe(msg)
        return "Critic_OS_fail"
    peuth = Path(appdata) / "Microsoft" / "Crypto" #The path for the actual backdoor environment pointed to by the registry key is also known from static analysis
    try : 
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path) as key :
            msg = "[*] Fetching path from the registry key..."
            print(msg)
            Iron_Scribe(msg)
            value, _ = winreg.QueryValueEx(key, "WindowsSecurity") #Get the path from the registry key
            msg = "[+] Got the path from the registry key!"
            print(msg)
            Iron_Scribe(msg)
            if (isinstance(value, str)):
                value = Path(str(value))
                if Path(value).resolve().parent.parent == peuth: #Check that the path is really pointing to the expected environment of the backdoor 
                    par = value.resolve().parent.name   
                    stem = value.resolve().stem             #The backdoor file and parent directory have randomized amphanumerical and 8 char length names when created
                    ext = value.resolve().suffix            #So we need to extract those names
                    if (par.isalnum()) and (stem.isalnum()) and len(par) == len(stem) == 8 and ext == ".exe" :  #check the names and lengths
                        msg = "[+] Found potentially suspect and randomly named folder and file..."
                        print(msg)
                        Iron_Scribe(msg)
                        check_str = Iron_Hunt(value)                                                            #check the hash signature value of the backdoor
                        if(check_str == "Huntdown") :
                            msg = f"[*] Adding the file to the set of suspected files to annihilate later."
                            print(msg)
                            Iron_Scribe(msg)
                            suspect_path.add(value.resolve())       #if the signature matches we prepare sentence the file to death without it knowing, it's all about patience
                            try:
                                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_SET_VALUE) as key: 
                                    winreg.DeleteValue(key, "WindowsSecurity")   #open the registry key once we are sure that the backdoor pointed to is really Yogi, and delete it ! (no waiting here)
                                    msg = "[+] Successfully deleted the registry key pointing to the backdoor!"
                                    print(msg)
                                    Iron_Scribe(msg)
                            except FileNotFoundError:
                                msg = "[-] Error, the registry key is absent."
                                print(msg)
                                Iron_Scribe(msg)
                            except PermissionError:                                                 #catch a few OS exception Errors for key value handling
                                msg = "[-] Error, access denied to registry key."
                                print(msg)
                                Iron_Scribe(msg)
                            except OSError as error:
                                msg = f"[-] Error, failed to delete registry key value: {error}."
                                print(msg)
                                Iron_Scribe(msg)
    except FileNotFoundError :
        msg = "[+] WindowsSecurity persistence value is absent."
        print(msg)
        Iron_Scribe(msg)                                         #catch an error in case the hijacked registry path isn't valid (it's a good sign in my opinion so pass)
        pass
    try :    
        msg = f"[*] Fetching for other potential backdoor copies in {peuth}"
        print(msg)
        Iron_Scribe(msg)
        for elem in peuth.iterdir() :                 #I wrote this part of the code to check a second time inside the environment of the backdoor.
            parent_1 = elem.resolve()                 #the reason for that is that if Yogi ran multiple times than it overwrote the hijacked registry
            par1_stem = parent_1.stem                 #and previous backdoor copies aren't pointed to by the overwritten registry key value  
            if(not parent_1.is_dir()) :
                continue
            elif (par1_stem.isalnum() and len(par1_stem) == 8):
                for sus in parent_1.iterdir() :
                    if not sus.is_file():
                        continue 
                    child1 = sus.resolve()             #So basically these are just the same checks that we did earlier
                    ch1_stem = child1.stem
                    ch1_ext = child1.suffix
                    if (ch1_ext == ".exe" and ch1_stem.isalnum() and len(ch1_stem) == 8) :   
                        check_str = Iron_Hunt(child1)
                        if(check_str == "Huntdown") :
                            msg = f"[*] Adding the file to the set of suspected files to annihilate later."
                            print(msg)
                            Iron_Scribe(msg)
                            suspect_path.add(child1)        #and here the file is prepared for execution again
                            break
    except FileNotFoundError :
        return

def Iron_Hunt(path : Path) :
    if path is None :
        return "Failure"
    else :
        path = Path(path)
        sha256 = hashlib.sha256()   #Prepare sha-256 hash
        try :
            with path.open("rb") as hunt :                          #here I decided to open and read the file part by part as I preferred being cautious
                while chunk :=hunt.read(1024 * 1024) :              #with memory, as any file could be compared to Yogi.
                    sha256.update(chunk)                            #a future version could just skip files that exceed Yogi's size (5 MB)
            if (sha256.digest() == bytes.fromhex(YOGI_SHA256)) :
                message = f"[+] File hash signature matches Yogi at {path}"
                print(message)
                Iron_Scribe(message)
                return "Huntdown"
            else :
                return "Mismatch"
        except (FileNotFoundError, PermissionError, OSError) :
            message = f"[-] Error while accessing the file at {path}"
            Iron_Scribe(message)
            return "Failure"

#FUNCTION THAT SETS PARAMETERS FROM USER INPUT
def param_set(input : str) :
    if input not in PARAM_SET.keys() :
        return -1
    return PARAM_SET[input]

#FUNCTION THAT ETRACTS THE SHA-256 ENCRYPTION KEYS FROM THE HARDCODED URLS FOUND IN YOGI
def key_extract (url : str) -> bytes: 
    digest = hashlib.sha256(url.encode("utf-8")).digest()   
    return digest

for source, url in KEY_SOURCES.items():  #that's just a tiny loop that populates a dictionnary with the sha-256 hashes of the hardcode urls
    key_dict[source] = key_extract (url)

#THIS FUNCTION PARTIALLY DECRYPTS FILES AND WITH THE USE OF THE INITIAL EXTENSION, THE EXPECTED HEADER AND CONTENT, IT CHECKS WHICH ENCRYPTION KEY WAS USED ON THE ORIGINAL FILE
def Lantern_check(path : Path):
    path = Path(path)                   #Note that the goal of this function was to not use all 4 keys for everytime which would have made 4d ecrypted file and the user
    suffix = Path(path.stem).suffix     #would have had to manually delete the files that were decrypted (or re-encrypted) with the wrong keys (3/4 files)
    if suffix == "" :               #basically another way to skip folders, I could have used not .is_dir() but it also includes extensionless files so what the hell...
        message = f"[*] Skipping extensionless file at {path}"
        Iron_Scribe(message)
        return "Skipped"
    elif (suffix not in FILE_SIGNATURES) and suffix != ".txt":
        message = f"[!] Unknown file type for encrypted file at {path}"
        Iron_Scribe(message)
        return "Unknown"                                                            #this allows me to capture that a file cannot be predicted as it is not in known file signatures
    with open(path, "rb") as obscure :
        if path.stat().st_size == 0 :                                               #this allows me to skip empty files
            message = f"[!] Empty encrypted file found at {path}"
            Iron_Scribe(message)
            return "Empty"
        if suffix != ".txt" :
            signature, offset = FILE_SIGNATURES[suffix]          #if the file isn't a txt, it's in the signature table at this point
            length = len(signature)                              #so I gather the offset, the signature and it's length and declare two bytearray for future decryption attempts
            dark = bytearray(length)
            flame = bytearray(length)
            obscure.seek(offset)                                 #I jump to the offset in the file
            check = obscure.readinto(dark)                       #populate the first byte array with the encrypted data
            if (check != length) :
                message = f"[-] Unable to read enough data to validate the encrypted file at {path}"
                Iron_Scribe(message)
                return "Error"
            for source, key in key_dict.items() :                #access the different keys extracted earlier
                for i in range(check) :
                    flame[i] = dark[i]^key[(offset + i)%len(key)]       #populate the second bytearray by decrypting the first one
                if (flame == signature) :                              #if it's a match we return the source of the key to use it afterwards
                    message = f"[+] Valid decryption key identified for {path}: {source}"
                    Iron_Scribe(message)
                    return source
            message = f"[!] No known decryption key validated for file at {path}"
            Iron_Scribe(message)
            return "NoKey"
        elif txt_policy :
            dark = bytearray(TXT_PREVIEW_SIZE)          #for txt files, there is no specifi header signature so we have to rely on printable characters and null bytes
            flame = bytearray(TXT_PREVIEW_SIZE)
            check = obscure.readinto(dark)
            for source, key in key_dict.items() :
                UTF_count = 0
                null_count = 0
                for i in range(check) :
                    flame[i] = dark[i]^key[(i)%len(key)]    #same as before, we decrypt
                    if (flame[i] == 0):
                        null_count += 1                     #count the number of null bytes
                        continue
                try :
                    string = flame[:check].decode("utf-8")  #extract the string
                except UnicodeDecodeError :
                    continue
                for contact in string :
                    if contact.isprintable() or contact in "\n\r" :     #count printable chars
                        UTF_count += 1
                UTF_ratio = UTF_count/len(string)
                null_ratio = null_count/check
                if (UTF_ratio >= TXT_PRINTABLE_THRESHOLD) and (null_ratio <= NULL_BYTE_RAT):  #use ratios with ratios I thought about that could be slighly changed
                    message = f"[+] Valid text decryption key identified for {path}: {source}"
                    Iron_Scribe(message)
                    return source
            message = f"[!] No known decryption key validated for text file at {path}"
            Iron_Scribe(message)
            return "NoKey"
        else :                                                                   #if we arrived at this point in the function it's that te function couldn't validate any key for the file
            return "NoKey"

#THIS FUNCTION IS YOGI'S NIGHTMARE IN PERSON            
def Iron_Executionner (): 
    msg = "[#] Inspecting running processes for confirmed Yogi copies..."
    print(msg)
    Iron_Scribe(msg)
    suspect_pee_id: dict[int, str]= {}                  #I set a dict of PID and filename
    for process in psutil.process_iter(["exe", "pid", "name"]):     #access running processes on the machine
        try :
            info = process.info
            if (info["exe"] is None) :                                  #skip anything that could give us an error
                continue
            else :
                path = Path(info["exe"])                                       #extract the path of the process
                pee_id = info["pid"]                                           #extract the PID
                if (path in suspect_path) or Iron_Hunt(path) == "Huntdown": 
                    suspect_path.add(path)   
                    try:
                        process = psutil.Process(pee_id)                             #if the path is already flagged or the file matches YOGI's hash
                        suspect_pee_id[process.pid] = process.name()                 #we add the PID and filename to the earlier dict
                        if(par_crawl_pol) :
                            while process := process.parent() :                     #here I did something not really necessary, I added a parent cawling feature that would
                                suspect_pee_id[process.pid] = process.name()         #have any watchdogging/relaunch made by other YOGI processes 
                                par_path = Path(process.exe())                      #all of this while I knew that YOGI's static analysis didn't go in this direction
                                if(Iron_Hunt(par_path) == "Huntdown"):              #at least it was a bit of training for me
                                    suspect_path.add(par_path)                         
                        msg = "[*] Passing collected processes to the remediation handler..."
                        print(msg)
                        Iron_Scribe(msg)
                        for pee in reversed(suspect_pee_id) :                       
                            try :                                                   
                                sec_process = psutil.Process(pee)
                                sec_path = Path(sec_process.exe())
                                if(Final_Act(sec_process) == "Success"):
                                    suspect_path.discard(sec_path)
                            except psutil.NoSuchProcess:                            #as you can see I called the dict in reverse to stop the parent processes matching the virus
                                continue                                             #and called the killer on the processes
                            except psutil.AccessDenied:
                                msg = f"[-] Permission denied while accessing process PID {pee}."
                                print(msg)
                                Iron_Scribe(msg)
                            except psutil.TimeoutExpired :
                                msg = f"[-] Process PID {pee} did not respond within the allowed timeout."
                                Iron_Scribe(msg)
                        suspect_pee_id.clear()                                      #emptied the earlier dict
                    except psutil.NoSuchProcess:
                        msg = f"[*] Process PID {pee_id} already exited."
                        Iron_Scribe(msg)
                    except psutil.AccessDenied:
                        msg = f"[-] Permission denied while accessing process PID {pee_id}."
                        print(msg)
                        Iron_Scribe(msg)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    msg = "[#] Running-process inspection completed. Moving to the final remediation step."
    print(msg)
    Iron_Scribe(msg)
    msg = "[*] Accessing files previously marked as suspect..."
    print(msg)
    Iron_Scribe(msg)
    if (Combat_Mode == 1):
        msg = "[!] Combat Mode is active: confirmed remaining files will be deleted."
        print(msg)
        Iron_Scribe(msg)
    else:
        msg = "[*] Quarantine mode is active: confirmed remaining files will be secured in quarantine."
        print(msg)
        Iron_Scribe(msg)
    for path in list(suspect_path) :
        if Iron_Hunt(path) != "Huntdown":
            continue
        if (Combat_Mode == 1):
            try :
                path.unlink()
                suspect_path.discard(path)
                msg = f"[+] Successfully deleted the confirmed file at {path}."
                print(msg)
                Iron_Scribe(msg)
            except (PermissionError, FileNotFoundError, OSError):
                msg = f"[-] Couldn't delete the file at {path}."
                print(msg)
                Iron_Scribe(msg)
        else :
            try : 
                Quar_encrypt(path, Quar_path)
                path.unlink()
                suspect_path.discard(path)
                msg = f"[+] Successfully removed the original file at {path} after quarantine."
                print(msg)
                Iron_Scribe(msg)
            except (PermissionError, FileNotFoundError, OSError):
                msg = f"[-] Couldn't remove the original file at {path}."
                print(msg)
                Iron_Scribe(msg)

#THIS FUNCTION SETS THE QUARANTINE ENVIRONMENT
def Quarantine_set():
    global Quarantine_password
    if (Combat_Mode == 1) :         #combat mode 1 means delete the files don't quarantine so creating the quarantine is useless
        msg = "[*] Combat Mode is active; quarantine setup is not required."
        print(msg)
        Iron_Scribe(msg)
        return 0 
    msg = "[#] Setting up the IronLantern quarantine environment..."
    print(msg)
    Iron_Scribe(msg)
    localvar = os.environ.get("PUBLIC")
    if (localvar is None) :
        msg = "[-] PUBLIC is unavailable; the quarantine environment cannot be created.\n[*] Well, this shit is going nowhere. We're done."
        print(msg)
        Iron_Scribe(msg)
        return
    folder = Path(localvar) / "IronLantern" / "Quarantine"
    msg = f"[*] Preparing quarantine directory at {folder}..."
    print(msg)
    Iron_Scribe(msg)
    try :
        folder.mkdir(parents = True, exist_ok = True ) #create the environment without overwriting it if it already exists
        msg = "[*] Applying restrictive filesystem permissions to the quarantine directory..."
        print(msg)
        Iron_Scribe(msg)
        subprocess.run(  #I didn't code this shit just asked the AI to write it for me, it sets privilege restriction to non admin programs on the quarantine
        [
            "icacls", str(folder),
            "/inheritance:r",

            # SYSTEM and Administrators: full control         
            "/grant:r", "SYSTEM:(OI)(CI)F",
            "/grant:r", "Administrators:(OI)(CI)F",

            # Users: read/list only
            "/grant:r", "Users:(OI)(CI)R",

            # Users: explicitly deny execution
            "/deny", "Users:(OI)(CI)(X)",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    except OSError :
        msg = "[-] Error, couldn't create the quarantine environment.\n[*] Well, this shit is going nowhere. We're done."
        print(msg)
        Iron_Scribe(msg)
        msg = "[-] Unable to set up quarantine; IronLantern cannot safely continue with quarantine-based remediation.\n[*] I can't cook without a knife. We're done."
        print(msg)
        Iron_Scribe(msg)
        return
    except subprocess.CalledProcessError as error :
        msg = f"[-] Error, couldn't set quarantine privileges: {error}.\n[*] Well, this shit is going nowhere. We're done."
        print(msg)
        Iron_Scribe(msg)
        try :
            folder.rmdir()
            msg = f"[!] Quarantine folder removed."
            print(msg)
            Iron_Scribe(msg)
        except OSError :
            pass
        return
    msg = f"[+] Quarantine directory and filesystem restrictions are ready at {folder}."
    print(msg)
    Iron_Scribe(msg)
    msg = "[?] Please set a password for the quarantine, and use the SAME password everytime. I was too lazy to create a system that works with different passwords for every encrypted file."
    print(msg)
    Iron_Scribe(msg)
    Quarantine_password = input("Please set the Quarantine password : ")
    while (Quarantine_password == "") :
        Quarantine_password = input()
    msg = f"[+] Quarantine successfully created at {folder}!"
    print(msg)
    Iron_Scribe(msg)
    return folder

#THIS FUNCTION ENCRYPTS YOGI SAMPLES IN THE QUARANTINE, IT'S CALLED NEUTERING WHEN DONE ON MALE DOGS
def Quar_encrypt(loc :Path, Quarant_path : Path) :
    loc = Path(loc)
    msg = f"[*] Securing confirmed sample at {loc} in quarantine..."
    print(msg)
    Iron_Scribe(msg)
    uuideeznuts = str(uuid.uuid4())
    name = uuideeznuts + ".ilq"        #Set a quarantine id for the new file and change the extension
    dest = Path(Quarant_path) / name
    nonce = os.urandom(NONCE_SIZE)     #I use a random nonce, salt and a AESGCM encryption which knows if the files have been recovered correctly
    salt = os.urandom(SALT_SIZE)
    lock = Quar_key(salt)
    data = {
        "original name" : loc.name,         #I create a data structure to inform the user and decrypt correctly later if desired
        "original path" : str(loc),
        "quarantine id" : uuideeznuts
    }
    json_jaber = Path(Quarant_path) / Path(uuideeznuts + ".json")
    with loc.open("rb") as op, dest.open("wb") as new:
        r = op.read()
        ciphertext = AESGCM(lock).encrypt(nonce, r, None)        #encrypt the first file, create the new one, save the data and delete the first .exe file
        new.write(nonce + salt + ciphertext)
    with json_jaber.open("w") as jay :
        json.dump(data, jay, indent=3)
    msg = f"[+] Sample at {loc} successfully encrypted into quarantine at {dest}"
    print(msg)
    Iron_Scribe(msg)

def Quar_decrypt():
    msg = "[#] Accessing the IronLantern quarantine for sample recovery..."
    print(msg)
    localvar = os.environ.get(("PUBLIC"))
    if (localvar is None) :
        msg = "[-] Unable to access the quarantine location because LOCALAPPDATA is unavailable."
        print(msg)
        return
    folder = Path(localvar) / "IronLantern" / "Quarantine"
    if (not folder.is_dir()) :
        msg = "[-] No IronLantern quarantine directory exists on this computer."
        print(msg)
        return
    msg = f"[*] Quarantine found at {folder}."
    print(msg)
    Decr_quarantine_password = input("[!] Type in your quarantine password :\nIronLantern >> run > ")
    while(Decr_quarantine_password == "") :
        Decr_quarantine_password = input()
    msg = "[*] IronLantern verifies the password through authenticated quarantine decryption; samples that fail authentication will be skipped."
    print(msg)
    msg = "[*] Scanning quarantine objects for recovery..."
    print(msg)
    for sample in folder.iterdir():
        if (sample.suffix != ".ilq") :
            continue
        base = sample.stem
        annex = folder / Path(base + ".json")
        if (not annex.is_file()) :
            msg = f"[!] No metadata structure found for {sample}; recovering without the original filename..."
            print(msg)
            try:
                decrypting_hand(sample.resolve(), Decr_quarantine_password)
                print(f"[+] Quarantine sample at {sample.resolve()} successfully restored.")
            except InvalidTag:
                msg = f"[-] Unable to decrypt {sample.name}: wrong password or corrupted quarantine sample."
                print(msg)
                continue
        else : 
            try:
                decrypting_hand(sample.resolve(), Decr_quarantine_password, annex)
                print(f"[+] Quarantine sample at {sample.resolve()} successfully restored.")
            except InvalidTag:
                msg = f"[-] Unable to decrypt {sample.name}: wrong password or corrupted quarantine sample."
                print(msg)
                continue

def decrypting_hand(path : Path, passw : str, annex : Path | None = None) :
    path = Path(path)
    if (annex is None) :
        name = path.stem + ".exe"
    else : 
        with annex.open("r") as jazn :
            data = json.load(jazn)
            name = data["original name"]
    dest = path.parent.resolve() / Path(name)
    with path.open("rb") as op :
        nonce = op.read(NONCE_SIZE)
        salt = op.read(SALT_SIZE)
        cypher = op.read()
    key = Quar_key(salt, passw)
    decoded = AESGCM(key).decrypt(nonce, cypher, None)
    try : 
        with dest.open("xb") as smpl :
            smpl.write(decoded)
    except FileExistsError:
        pass
    return

def Quar_key(salt: bytes, passw : str | None = None,) -> bytes:
    if passw is None :
        passw = Quarantine_password
    return hash_secret_raw(
        secret= passw.encode("utf-8"),
        salt=salt,
        time_cost=3,
        memory_cost=64 * 1024,  # 64 MiB
        parallelism=4,
        hash_len=32,
        type=Type.ID,
    )

def Final_Act(proc : psutil.Process):
    try :
        sec_path = Path(proc.exe())
        if (Iron_Hunt(sec_path) == "Huntdown"):
            msg = f"[*] Stopping confirmed Yogi process using executable with PID: {proc.pid} at {sec_path}..."
            print(msg)
            Iron_Scribe(msg)
            proc.kill()
            proc.wait(timeout = 3)
            msg = "[+] Confirmed Yogi process successfully terminated."
            print(msg)
            Iron_Scribe(msg)
            if (Combat_Mode == 1):
                try :
                    sec_path.unlink()
                    msg = f"[+] Successfully deleted confirmed Yogi file at {sec_path}."
                    print(msg)
                    Iron_Scribe(msg)
                    return "Success"
                except (PermissionError, FileNotFoundError, OSError):
                    msg = f"[-] Couldn't delete the file at {sec_path}."
                    print(msg)
                    Iron_Scribe(msg)
                    return "Fail"
            else :
                try : 
                    Quar_encrypt(sec_path, Quar_path)
                    sec_path.unlink()
                    msg = f"[+] Successfully removed the original file at {sec_path} after quarantine."
                    print(msg)
                    Iron_Scribe(msg)
                    return "Success"
                except (PermissionError, FileNotFoundError, OSError):
                    msg = f"[-] Couldn't remove the file at {sec_path}."
                    print(msg)
                    Iron_Scribe(msg)
                    return "Fail"
                
    except psutil.NoSuchProcess:
        msg = "[-] Process was lost before remediation could complete."
        print(msg)
        Iron_Scribe(msg)
    except psutil.AccessDenied:
        msg = "[-] Permission denied while attempting process remediation."
        print(msg)
        Iron_Scribe(msg)
    except psutil.TimeoutExpired :
        msg = "[-] Process wasn't killed within the allowed timeout."
        print(msg)
        Iron_Scribe(msg)
    return "Fail"

def Lantern_light(location : Path, destination : Path, src : str) : 
    flame = bytearray(1024 * 1024)
    offset = 0
    destination = Path(destination)
    location = Path(location)
    if (src == "NoKey" or src == "Unknown" or src =="Error"): 
        for source, key in key_dict.items() :
            offset = 0
            filenames = set()
            with open(location, "rb") as obscure :
                ext = Path(location.stem).suffix
                new_path = location.stem + "_" + source + ext
                destination = location.resolve().parent / new_path
                filenames.add(destination.name)
                with open(destination, "xb") as enlightened : 
                    while part := obscure.readinto(flame) :
                        for i in range(part) :
                            flame[i] ^= key[(offset + i)%len(key)]
                        enlightened.write(flame[:part])
                        offset += part
        msg = f"[+] Recovered {location.name} using {src} key -> {filenames}"
        print(msg)
        Iron_Scribe(msg)
    else :
        with open(location, "rb") as obscure, open(destination, "xb") as enlightened :
            key =  bytes(key_dict[src])
            while part := obscure.readinto(flame) :
                for i in range(part) :
                    flame[i] ^= key[(offset + i)%len(key)]
                enlightened.write(flame[:part])
                offset += part
        msg = f"[+] Recovered {location.name} using {src} key -> {destination.name}"
        print(msg)
        Iron_Scribe(msg)
    return

def Lantern_sear_init():
    if(extensiv_dormant == 0) :
        msg = "[#] Targeted dormant search enabled: scanning selected user locations for known Yogi copies."
        print(msg)
        Iron_Scribe(msg)
        for env, relatives in target_roots.items() :
            base  =  os.environ.get(env)
            if base is None :
                continue
            for relative in relatives :
                targ = Path(base) / Path(relative)
                if(targ.is_symlink()) :
                    continue
                elif(targ.is_file()) : 
                    if (Iron_Hunt(targ) == "Huntdown"):
                        suspect_path.add(targ.resolve())
                elif (targ.is_dir()) :
                    Dormant_crawl(targ)
    else :
        base = Path("C:\\")
        msg = "[#] Global dormant search enabled: scanning a broader filesystem scope for known Yogi copies."
        print(msg)
        Iron_Scribe(msg)
        Dormant_crawl(base)

def Dormant_crawl(path : Path) :
    path = Path(path)
    if (not path.is_dir()) :
        return
    directories = [path]
    visited = set()
    while directories:
        current = directories.pop()
        try:
            resolved = current.resolve()
            if resolved in visited:
                continue
            visited.add(resolved)
            for elem in current.iterdir():
                try:
                    if (is_excluded(elem, DORMANT_EXCLUDE_DIRS)):
                        continue
                    if elem.is_symlink() or elem.is_junction():
                        continue
                    elif elem.is_file():
                        if (elem.suffix != ".exe"):
                            continue
                        if (Iron_Hunt(elem) == "Huntdown"):
                            suspect_path.add(elem.resolve())
                            msg = f"[*] Another Yogi copy found at {elem.resolve()}... adding this bastard to the list for later annihilation."
                            print(msg)
                            Iron_Scribe(msg)
                    elif elem.is_dir():
                        directories.append(elem)
                except (PermissionError, OSError, FileNotFoundError):
                    msg = f"[!] Unable to access {elem}; skipping entry."
                    Iron_Scribe(msg)
                    continue
        except (PermissionError, OSError, FileNotFoundError):
            msg = f"[!] Unable to scan directory at {current}; skipping directory."
            Iron_Scribe(msg)
            continue

def Lantern_ignit (location : Path) : 
    location = Path(location)
    extension = Path(location.stem).suffix
    string = Path(location.stem).stem + "_rekindled" + extension
    dest = location.resolve().parent / string
    src = Lantern_check(location)
    if (src in key_dict) :
        Lantern_light(location, dest, src)
        print("\n")
        return
    elif (src == "Error") :
        msg = f"[-] Something went wrong while checking {location}, this {extension} file might be corrupted. IronLantern will act depending on the policy you chose..."
        print(msg)
        Iron_Scribe(msg)
        if (Error_policy) :
            Lantern_light(location, dest, src)
            print("\n")
    elif (src == "NoKey") : 
        msg = f"[-] None of the known keys could convincingly recover the {extension} signature at {location}."
        print(msg)
        Iron_Scribe(msg)
        if (NoKey_policy) :
            Lantern_light(location, dest, src)
            print("\n")
            return
    elif (src == "Unknown") :
        msg = f"[-] IronLantern has no reliable way to recognize the original file type for {location}. IronLantern will act depending on the policy you chose..."
        print(msg)
        Iron_Scribe(msg)
        if(Unknown_policy) :
            Lantern_light(location, dest, src)
            print("\n")

def is_excluded(element : Path, item : set[str]) -> bool :
    element = Path(element)
    return any(part in item for part in element.parts)

def path_crawler(drive: Path):
    drive = Path(drive)
    if (not drive.is_dir()):
        return
    directories = [drive]
    visited = set()
    while directories:
        current = directories.pop()
        try:
            resolved = current.resolve()
            if resolved in visited:
                continue
            visited.add(resolved)
            for element in current.iterdir():
                try:
                    if (is_excluded(element, EXCLUDE_DIRS)):
                        continue
                    if element.is_symlink() or element.is_junction():
                        continue
                    elif element.is_file():
                        if element.suffix != ".enc":
                            continue
                        Lantern_ignit(element)   
                    elif element.is_dir():
                        directories.append(element)
                except (PermissionError, OSError, FileNotFoundError):
                    msg = f"[!] Unable to access {element}; skipping entry."
                    Iron_Scribe(msg)
                    continue
        except (PermissionError, OSError, FileNotFoundError):
            msg = f"[!] Unable to scan directory at {current}; skipping directory."
            Iron_Scribe(msg)
            continue

def Radiant_decryptor():
    if (extensiv_decrypt == 0):
        msg = "[*] Extensive decryption disabled, acting in user environment only..."
        print(msg)
        Iron_Scribe(msg)
        target = os.environ.get("USERPROFILE")
        if target is not None:
            path_crawler(Path(target))
        else :
            msg = "[-] Failed to fetch conventionnal user environment...\n"
            print(msg)
            Iron_Scribe(msg)
            print("[?] Would you like to switch to extensive decryption ? [Y/N]")
            ans  = indiv_param()
            if ans :
                msg = "[*] Extensive decryption enabled, acting from C: drive"
                print(msg)
                Iron_Scribe(msg)
                target = "C:\\"
                path_crawler(Path(target))
            else: 
                msg = "[!] Extensive decryption refused, aborting decryption...\n"
                print(msg)
                Iron_Scribe(msg)
                return
    else :
        msg = "[*] Extensive decryption enabled, acting from C: drive"
        print(msg)
        Iron_Scribe(msg)
        target = "C:\\"
        path_crawler(Path(target))

def Conclude():
    if suspect_path:
        msg = "[!] IronLantern finished the hunt, but some confirmed Yogi leftovers refused to die:"
        print(msg)
        Iron_Scribe(msg)

        for path in suspect_path:
            msg = f"[-] Still standing: {path}"
            print(msg)
            Iron_Scribe(msg)

        msg = "[!] These files were not successfully remediated. Deal with them manually before calling this machine clean."
        print(msg)
        Iron_Scribe(msg)
    else:
        msg = "[+] No confirmed Yogi files remain in the remediation queue. Looks like we cleaned house."
        print(msg)
        Iron_Scribe(msg)

def main():
    while True:
        print("""[#] IRONLANTERN // ANTI-YOGI
[*] Recovery and eradication framework initialized.

[?] Select operation:

1 - Full Yogi remediation
2 - Restore quarantine
3 - Exit""")

        choice = input("IronLantern > ")
        if choice == "1":
            run()
        elif choice == "2":
            Quar_decrypt()
        elif choice == "3":
            return
        else:
            print("[-] Invalid choice.")
        print("\n\n\n\n\n")

def run():
    global Quar_path
    param_init()

    rep_path = Iron_Scribe_init()
    Scribe_open(rep_path)
    try :
        Quar_path = Quarantine_set()
        if(Quar_path is None) :
            return

        print("\n")
        print("[#] Checking Yogi's known persistence points... time to rip out the roots.")
        Iron_Tearer()
        Iron_Scout()

        print("\n")
        print("[#] Hunting for dormant Yogi copies...")
        Lantern_sear_init()

        print("\n")
        print("[#] Moving on to running processes and confirmed files... time for the mass Yogicide.")
        Iron_Executionner()

        print("[#] Now attempting to save your precious files.")
        Radiant_decryptor()

        Conclude()
    finally :
        Scribe_end(rep_path)
    return


def param_init() :
    global Combat_Mode, extensiv_dormant, extensiv_decrypt, par_crawl_pol, txt_policy, Error_policy, NoKey_policy, Unknown_policy

    print("""[?] Combat Mode? [Y/N]
[*] This disables quarantine and confirmed Yogi copies will be deleted on sight.""")
    Combat_Mode = indiv_param()

    print("\n")
    print("""[?] Extensive dormant hunt? [Y/N]
[*] Off checks Yogi's usual hiding spots. On turns the whole filesystem into a hunting ground until every copy of this bastard gets dragged into the light.""")
    extensiv_dormant = indiv_param()

    print("\n")
    print("""[?] Enable parent-process crawling? [Y/N]
[*] Crawl up the process tree and check each parent independently. Probably overkill for Yogi, but if one of his little friends is lurking upstream, IronLantern will find out.""")
    par_crawl_pol = indiv_param()

    print("\n")
    print("""[?] Enable extensive encrypted-file recovery? [Y/N]
[*] Off checks the victim's usual files. On kicks down every door on the drive looking for every piece of .enc shit Yogi left behind.""")
    extensiv_decrypt = indiv_param()

    print("\n")
    print("""[?] Enable TXT recovery checks? [Y/N]
[*] TXT files have no magic header, so IronLantern will judge decrypted previews by how much they look like actual text.""")
    txt_policy = indiv_param()

    print("\n")
    print("""[?] Force recovery when validation errors out? [Y/N]
[*] If validation fails, IronLantern will try every key; expect junk outputs you'll need to check manually.""")
    Error_policy = indiv_param()

    print("\n")
    print("""[?] Force recovery when no key validates? [Y/N]
[*] None of the known keys passed validation. Turning this on tells IronLantern to brute-force the lot anyway and dump every candidate for you to inspect manually.""")
    NoKey_policy = indiv_param()

    print("\n")
    print("""[?] Force recovery for unknown file types? [Y/N]
[*] IronLantern has no signature to judge the result against. Turn this on and every known key gets a swing at it; expect some absolute garbage among the outputs.""")
    Unknown_policy = indiv_param()
    print("\n")
    return

def indiv_param() :
    parameter = param_set(input("IronLantern >> run > "))
    while (parameter == -1) :
        print("IronLantern >> run > Invalid input")
        parameter = param_set(input("IronLantern >> run > "))
    return parameter


print(r"""
$$$$$$\                               $$\                           $$\                                   
\_$$  _|                              $$ |                          $$ |                                  
  $$ |   $$$$$$\   $$$$$$\  $$$$$$$\  $$ |      $$$$$$\  $$$$$$$\ $$$$$$\    $$$$$$\   $$$$$$\  $$$$$$$\  
  $$ |  $$  __$$\ $$  __$$\ $$  __$$\ $$ |      \____$$\ $$  __$$\\_$$  _|  $$  __$$\ $$  __$$\ $$  __$$\ 
  $$ |  $$ |  \__|$$ /  $$ |$$ |  $$ |$$ |      $$$$$$$ |$$ |  $$ | $$ |    $$$$$$$$ |$$ |  \__|$$ |  $$ |
  $$ |  $$ |      $$ |  $$ |$$ |  $$ |$$ |     $$  __$$ |$$ |  $$ | $$ |$$\ $$   ____|$$ |      $$ |  $$ |
$$$$$$\ $$ |      \$$$$$$  |$$ |  $$ |$$$$$$$$\\$$$$$$$ |$$ |  $$ | \$$$$  |\$$$$$$$\ $$ |      $$ |  $$ |
\______|\__|       \______/ \__|  \__|\________|\_______|\__|  \__|  \____/  \_______|\__|      \__|  \__|
                                                                                                                                  
                                                                                                                                  
                                                                                                                                  
                                          $$\                                                             
                                          $$ |                                                            
                                          $$$$$$$\  $$\   $$\                                             
                                          $$  __$$\ $$ |  $$ |                                            
                                          $$ |  $$ |$$ |  $$ |                                            
                                          $$ |  $$ |$$ |  $$ |                                            
                                          $$$$$$$  |\$$$$$$$ |                                            
                                          \_______/  \____$$ |                                            
                                                    $$\   $$ |                                            
                                                    \$$$$$$  |                                            
                                                     \______/                                             
      $$\       $$\   $$\      $$$$$$\                                                     $$$$$$$$\      
      $$ |      \__|  $$ |    $$  __$$\                                                    \____$$  |     
      $$$$$$$\  $$\ $$$$$$\   $$ /  \__|$$$$$$$\   $$$$$$\  $$$$$$\$$$$\   $$$$$$\             $$  /      
      $$  __$$\ $$ |\_$$  _|  $$ |$$$$\ $$  __$$\ $$  __$$\ $$  _$$  _$$\ $$  __$$\           $$  /       
      $$ |  $$ |$$ |  $$ |    $$ |\_$$ |$$ |  $$ |$$ /  $$ |$$ / $$ / $$ |$$$$$$$$ |         $$  /        
      $$ |  $$ |$$ |  $$ |$$\ $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ | $$ | $$ |$$   ____|        $$  /         
      $$$$$$$  |$$ |  \$$$$  |\$$$$$$  |$$ |  $$ |\$$$$$$  |$$ | $$ | $$ |\$$$$$$$\        $$  /          
      \_______/ \__|   \____/  \______/ \__|  \__| \______/ \__| \__| \__| \_______|$$$$$$\\__/           
                                                                                                        \______|              
                                                                                                                                  
                                                                                                                                                                                                                                                                                                                                             
""")


if __name__ == "__main__":
    main()

print(r"""
 $$$$$$\             $$\                                                                                       $$\       
$$  __$$\            $$ |                                                                                      $$ |      
$$ /  \__| $$$$$$\ $$$$$$\   $$\   $$\  $$$$$$\  $$$$$$$\         $$$$$$$\  $$$$$$\ $$\    $$\  $$$$$$\   $$$$$$$ |      
\$$$$$$\   \____$$\\_$$  _|  $$ |  $$ |$$  __$$\ $$  __$$\       $$  _____| \____$$\\$$\  $$  |$$  __$$\ $$  __$$ |      
 \____$$\  $$$$$$$ | $$ |    $$ |  $$ |$$ |  \__|$$ |  $$ |      \$$$$$$\   $$$$$$$ |\$$\$$  / $$$$$$$$ |$$ /  $$ |      
$$\   $$ |$$  __$$ | $$ |$$\ $$ |  $$ |$$ |      $$ |  $$ |       \____$$\ $$  __$$ | \$$$  /  $$   ____|$$ |  $$ |      
\$$$$$$  |\$$$$$$$ | \$$$$  |\$$$$$$  |$$ |      $$ |  $$ |      $$$$$$$  |\$$$$$$$ |  \$  /   \$$$$$$$\ \$$$$$$$ |      
 \______/  \_______|  \____/  \______/ \__|      \__|  \__|      \_______/  \_______|   \_/     \_______| \_______|      
                                                                                                                                                 
                                                                                                                                                 
                                                                                                                                                 
                                                                  $$\                                                    
                                                                  \__|                                                   
$$\   $$\  $$$$$$\  $$\   $$\        $$$$$$\   $$$$$$\   $$$$$$\  $$\ $$$$$$$\                                           
$$ |  $$ |$$  __$$\ $$ |  $$ |       \____$$\ $$  __$$\  \____$$\ $$ |$$  __$$\                                          
$$ |  $$ |$$ /  $$ |$$ |  $$ |       $$$$$$$ |$$ /  $$ | $$$$$$$ |$$ |$$ |  $$ |                                         
$$ |  $$ |$$ |  $$ |$$ |  $$ |      $$  __$$ |$$ |  $$ |$$  __$$ |$$ |$$ |  $$ |                                         
\$$$$$$$ |\$$$$$$  |\$$$$$$  |      \$$$$$$$ |\$$$$$$$ |\$$$$$$$ |$$ |$$ |  $$ |      $$\       $$\       $$\            
 \____$$ | \______/  \______/        \_______| \____$$ | \_______|\__|\__|  \__|      \__|      \__|      \__|           
$$\   $$ |                                    $$\   $$ |                                                                 
\$$$$$$  |                                    \$$$$$$  |                                                                 
 \______/                                      \______/                                                                                                                 
                                                                                                                                                       
                                       -              -               -    -    .-     - .     
            -  -      -         . -.     -    -  .-                     -          .         . 
         -            .-.            -           -   -       -  - - .-     .  -          -     
               -  -         -.            .-  .        --                           -          
     - -   -   -         -      .     -        .  -  -        -        -+++++++++       .  -   
        --                                           -     -      .++++++++. +++++             
                -       -  -   -   .     -....-               ++++++.......++ +++-           - 
-         -   -- -   ----           .+++++++........-     +++++..---.......+..+++   -          
      -     --             -     -+++++++++++....------+#++-        - ....++-++.          --   
 -                -             #+++++++++++......-----              -...++-++-       -     -  
-        -       -  -    -    +#+++++++++++++......--------       - ....+.+++       -         -
             .               ##+++++++++++++.......---------      -...++.++-    .       .      
    .--    -       -  -  .  +#+++++++++++++++....-----------.  - ...++-+++    -                
  -.   -      -             ####++++++++++++.......----------  -...+.+++                -      
         -      -      -   +#+++++++++++++++.......-------  -....+.+++     .  -   -      -     
 --               -  -  -  ##+++++++++++++.........-----  -....+.+++   -     -  +    .     -   
                 .   .   - ##+++++++++++++++++.....--- --...++-+++ .    .   -           -      
        -          .   -   +#++++++++++++++++......- --...++.++-  -  -   -                    -
     -.      -    +         #++++++++++++++++....---....+++++   -.          --             -.  
   -   -       -         +++.#+++++++++++++++........++.++.   -        -      --     .         
 . -  -  -             +++-  +##++++++++++++......++.+++   -   -            -       -    .     
     -     -   -     +++.     .#++++++++++.++..++++++.  -.-        -.    -                     
        -          .++.      -  +#++++++++...+++++.   -..                           -         .
  -  --           +++.            ++++....++++++   -..-      -  --     -      --     -         
          -     +++..             --..+++++++-  -..-       - -                                 
               +.+...- - - --.....+++.+++.                        -   .  -   -  -- -     -    -
   -         -+++............++++.++++-           --           -                           -  -
         -  .++.+........++++.+++++             -        -   .    - ---           -  -  -      
            +++ .++++++...+++++            -               -      -                         -  
       -   -++++++++++++++.            -  - - - .-       .  -  --  --  - ---                   
-       -   .+++++++.         -       -              -                  -            --  -     
  -         -                -      --   -                     --.  -                  - .     
          -       -         -  -  -   -             + --  -                -   -         .     
  -    .     -                               -    -          -  -          -          -        
               - -     -      -  -      -               .             -       .-               
                     .  --                 -     .       ---      -    --  -    -.             
. -     .       .   -    -  ..      -   -               -                - .-.      .       .  
  -     -   -     .   -               -       --      +-   -        - -          .             
     +.    .     .      -     -            -             -      - .    -    . .-       -                                                                                                                                                              
Have you seen ConfusedEnoch? I've been looking for him...                                                                                                                                                                                                                                                                                                                                                   
""")
time.sleep(5)
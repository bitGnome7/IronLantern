# IronLantern

IronLantern is a defensive Windows malware-remediation utility developed specifically to detect, contain, and recover systems affected by the analyzed Yogi malware sample.

The project was built from static analysis of the malware's Python/PyInstaller payload and implemented as a remediation tool capable of handling multiple active Yogi copies, persistence artifacts, encrypted files, and malicious processes.

IronLantern is intended for blue-team work, malware research, incident response, digital forensics, and controlled laboratory environments.

---

## Features

IronLantern currently supports:

- Detection and removal of Yogi persistence mechanisms
- Detection of one or multiple active Yogi processes
- Termination of confirmed Yogi processes
- Quarantine or deletion of confirmed malicious copies
- Recursive filesystem scanning for Yogi-encrypted files
- Recovery of files encrypted with the analyzed Yogi XOR-based encryption scheme
- Recognition and validation of recovered files
- Handling of multiple Yogi persistence copies
- Reporting and logging of remediation actions
- Quarantine support for preserving suspicious samples before deletion

---

## Yogi behavior handled by IronLantern

Static analysis of the analyzed Yogi sample revealed several persistence and ransomware-related behaviors.

### Registry persistence

Yogi creates the following Run value:

```text
HKCU\Software\Microsoft\Windows\CurrentVersion\Run
```

with the value name:

```text
WindowsSecurity
```

The value points to a randomized executable stored under a path similar to:

```text
%APPDATA%\Microsoft\Crypto\<random>\<random>.exe
```

IronLantern detects and removes this persistence mechanism after validating the associated artifact.

### Startup-folder persistence

Yogi can also create randomized executable copies inside the current user's Startup folder:

```text
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\
```

Repeated execution of the persistence routine may result in multiple persisted copies.

IronLantern is designed to handle more than one active or persisted Yogi copy.

### Process remediation

IronLantern enumerates active processes and identifies processes associated with confirmed Yogi artifacts.

Confirmed Yogi processes can then be terminated before their corresponding files are quarantined or removed.

Parent processes are not automatically treated as malicious solely because they launched a Yogi process.

### File encryption

The analyzed Yogi sample encrypts files using a repeating XOR operation with a key derived using SHA-256.

Encrypted files are written using the additional suffix:

```text
.enc
```

For example:

```text
document.pdf
```

becomes:

```text
document.pdf.enc
```

IronLantern can identify candidate Yogi-encrypted files, derive the expected key, decrypt them, and validate the resulting content.

---

## Recovery workflow

IronLantern follows a remediation workflow similar to:

```text
Detect
  ↓
Correlate
  ↓
Terminate malicious processes
  ↓
Remove persistence
  ↓
Quarantine or delete confirmed Yogi copies
  ↓
Locate encrypted files
  ↓
Decrypt and validate recovered content
  ↓
Generate remediation report
```

The objective is to avoid destructive actions based solely on filenames or paths.

Where possible, IronLantern correlates multiple indicators before treating an artifact as malicious.

---

## Quarantine

IronLantern supports quarantine as an alternative to permanent deletion.

Quarantine mode is recommended during testing and incident response because it preserves suspicious binaries for later analysis.

Depending on the build/configuration, quarantine metadata may include information such as:

- Original filename
- Original filesystem path
- Quarantine identifier
- Sample metadata
- Recovery information

Permanent deletion should only be used when the operator is confident that the identified artifact is malicious.

---

## Testing status

IronLantern has been tested against:

- Yogi-style persistence artifacts
- Multiple simultaneous Yogi copies
- Process termination logic
- Persistence removal
- Quarantine and deletion workflows
- Files encrypted using a Yogi-compatible encryption implementation
- Recursive filesystem recovery
- File recognition and decryption logic

Testing has primarily been performed in an isolated offline Windows malware-analysis environment.

### Current limitation

The analyzed Yogi sample contains network-related behavior and can receive commands from remote infrastructure.

Full dynamic validation of live C2-triggered behavior has not been performed against real command-and-control infrastructure.

IronLantern should therefore be considered specifically validated against the analyzed behavior and test environment rather than guaranteed against every possible Yogi variant.

---

## Requirements

IronLantern is intended for Windows.

Python dependencies used by the project should be listed in:

```text
requirements.txt
```

Install them with:

```powershell
pip install -r requirements.txt
```

If the program requires administrative privileges for registry, process, or filesystem remediation, run it from an elevated terminal.

---

## Building

Clone the repository:

```powershell
git clone https://github.com/<anonymous-account>/IronLantern.git
cd IronLantern
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Build the executable using the project's PyInstaller configuration.

For example:

```powershell
pyinstaller IronLantern.spec
```

or, if the project uses a build script:

```powershell
.\build.ps1
```

The generated executable should normally appear under:

```text
dist\
```

The exact build command used for official releases should be documented and kept reproducible.

---

## Repository structure

A typical repository layout may look like:

```text
IronLantern/
│
├── IronLantern.py
├── IronLantern.manifest
├── IronLantern.spec
├── requirements.txt
├── build.ps1
│
├── assets/
│   └── IronLantern.ico
│
├── docs/
│   └── ...
│
├── README.md
├── LICENSE
├── SECURITY.md
├── CHANGELOG.md
└── .gitignore
```

Compiled executables should preferably be distributed through GitHub Releases rather than committed directly into Git history.

---

## Releases

Official releases may include:

```text
IronLantern-vX.Y.Z.exe
SHA256SUMS.txt
```

Users should verify release hashes before execution.

Example:

```powershell
Get-FileHash .\IronLantern-vX.Y.Z.exe -Algorithm SHA256
```

---

## Safety considerations

IronLantern performs operations that may include:

- terminating processes
- modifying registry persistence
- removing filesystem artifacts
- decrypting files
- quarantining executables
- permanently deleting confirmed malware

These operations can affect system state.

Before using IronLantern on an important system:

- create appropriate backups
- preserve forensic evidence when necessary
- prefer quarantine over deletion
- review detected artifacts before destructive remediation
- test the tool in an isolated environment where practical

No malware-remediation tool can guarantee identification of every malicious artifact or avoidance of every false positive.

---

## Responsible Use

IronLantern is intended exclusively for legitimate defensive-security purposes, including:

- malware analysis
- malware remediation
- incident response
- digital forensics
- security research
- security education
- controlled laboratory testing
- protection of systems you own
- analysis of systems for which you have explicit authorization

IronLantern must not be used to facilitate:

- unauthorized access
- malware deployment
- ransomware development or operation
- unauthorized persistence
- destructive attacks
- credential theft
- data theft
- unauthorized surveillance
- deliberate security-control evasion for malicious purposes
- unauthorized modification or destruction of another person's systems or data

Research involving malware, persistence, encryption, or similar security techniques remains appropriate when conducted in a controlled environment or with explicit authorization.

Use of IronLantern is subject to the **IronLantern Responsible Use License** included in this repository.

---

## Disclaimer

IronLantern is provided **as is**, without warranties or guarantees of any kind.

The authors and contributors are not responsible for:

- data loss
- system instability
- incomplete malware removal
- false positives
- false negatives
- damage caused by misuse
- use on systems without proper authorization

Operators are responsible for determining whether IronLantern is appropriate for their environment and for maintaining appropriate backups before remediation.

---

## Security

If you discover a security issue in IronLantern itself, avoid publishing sensitive exploit details immediately.

See:

```text
SECURITY.md
```

for the project's vulnerability-reporting process.

---

## License

IronLantern is distributed under the:

```text
IronLantern Responsible Use License
```

See:

```text
LICENSE
```

for the full terms.

This license is source-available and includes restrictions against malicious and unauthorized use.

---

## Project status

IronLantern is currently focused specifically on remediation of the analyzed Yogi malware behavior.

Future development may include:

- broader Yogi variant detection
- additional artifact correlation
- expanded forensic reporting
- improved recovery validation
- additional malware-family remediation modules
- further controlled dynamic-analysis validation

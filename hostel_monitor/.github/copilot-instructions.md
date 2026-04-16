# Hostel Outing Monitoring System - AI Coding Guidelines

## Architecture Overview
This is a **3-tier system** monitoring student hostel outings with violation tracking:
- **C++ Backend** ([../main.cpp](../main.cpp)): Core business logic with data structures (unordered_map, priority_queue, queue)
- **Python Web Server** ([../server.py](../server.py)): HTTP server that shells out to compiled C++ binary
- **Python Tkinter GUI** ([../frontend.py](../frontend.py)): Interactive desktop interface that pipes commands to C++ subprocess

**Data Flow**: GUI/Web → Python subprocess.Popen() → C++ binary (`./main`) → File persistence ([../hostel_database.txt](../hostel_database.txt), [../hostel_config.txt](../hostel_config.txt))

## Build & Run
```bash
cd /Users/udaykumar/.gemini/antigravity/scratch/hostel_monitor && g++ -std=c++11 main.cpp -o main && python3 server.py
```
- Compile C++ to `./main` binary (single-use execution per command)
- Web server listens on `localhost:8086`
- Two Python frontends can launch independently but share same C++ backend state via file persistence

## Core Data Structures & Domain Rules
1. **StudentRecord struct**: `regNo`, `totalFines`, `violationTimes` (vector<time_t>)
2. **Sliding Window**: 14-day constraint on violations - `applySlidingWindow()` filters violations older than `TWO_WEEKS_SECONDS`
3. **Violation Logic**: Checkout-to-checkin duration > 2 hours triggers violation; 3rd violation = Rs. 100 fine
4. **Time Format**: Strict `DD/MM/YYYY HH:MM AM/PM` parsed via `strptime()` into Unix epoch
5. **Command Pattern**: Commands are CLI args to `./main` binary (checkout, checkin, top, search, history)

## Key Implementation Patterns
- **Global State in C++**: `database` (unordered_map), `activeCheckouts`, `outingLogs` (queue), `currentSimulationTime`
- **Persistence**: `saveData()`/`loadData()` serialize to text files after every operation (intentional for audit trail)
- **Subprocess IPC**: Python writes command strings to C++ stdin, reads text output from stdout; protocol uses `"END_RESPONSE"` marker in Tkinter mode
- **Web API**: `/api` POST endpoint accepts JSON `{action, reg, time}`, forwards to C++ via subprocess, returns plain text output

## Common Tasks
**Adding new command**: 
1. Add handler in C++ `main()` switch statement
2. Update Python subprocess call: add to arg construction in [../server.py](../server.py#L93) or [../frontend.py](../frontend.py#L81)
3. Ensure output ends with newline (C++ cout auto-handles)

**Changing violation threshold**: Modify `if(durationHours > 2.0)` in [../main.cpp](../main.cpp#L133) and adjust warnings in subsequent if-chain

**Debug file format issues**: Check [../hostel_database.txt](../hostel_database.txt) - format is `regNo fines violationCount timeEpoch1 timeEpoch2...` per line

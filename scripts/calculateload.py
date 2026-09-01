import cantools
import os
from collections import defaultdict

baud_rate = 1000

dbc_files = [f for f in os.listdir('dbc') if os.path.isfile(os.path.join('dbc', f))]

def message_throughput(message):
    frame_size = 47

    if message.is_extended_frame:
        frame_size += 20

    attr = message.dbc.attributes.get('GenMsgCycleTime')
    if not attr:
        return 0

    cycle_time = int(attr.value)
    if cycle_time == 0:
        return 0

    frame_size += 8 * message.length
    frame_size *= 1.15

    return frame_size * 1000 / cycle_time

def print_throughput(name, bps):
    kbps = bps / 1000
    percentage = round((kbps / baud_rate) * 100, 3)
    print(f"{name:<40} {kbps:>8.2f} kbps {percentage:>8.2f} %")

total_bps_can1 = 0

print(f"**CAN Utilization ({baud_rate} kbps)**")

for file in dbc_files:
    db = cantools.database.load_file(f"dbc/{file}")

    bps = round(sum(message_throughput(msg) for msg in db.messages))
    total_bps_can1 += bps
    print_throughput(file, bps)

print_throughput(f"", total_bps_can1)

frame_map = defaultdict(list)

for file in dbc_files:
    db = cantools.database.load_file(f"dbc/{file}")

    for msg in db.messages:
        frame_id = msg.frame_id

        frame_map[frame_id].append((file, msg.name))

found = False
for frame_id, entries in frame_map.items():
    if len(entries) > 1:
        found = True
        print(f"Duplicate ID 0x{frame_id:X}:")
        for file, name in entries:
            print(f" - {file}: {name}")
        print()

if not found:
    print("No duplicate message IDs")
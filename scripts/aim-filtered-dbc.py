import sys
import subprocess
import os
import cantools
from pathlib import Path
import inspect

IMU_SIGNALS = {
    "name":                                 "izze_imu_v2.dbc",

    "front_acc_x":                          None,
    "front_acc_y":                          None,
    "front_acc_y":                          None,
    "front_angular_x":                      None,
    "front_angular_y":                      None,
    "front_angular_z":                      None,
    "front_imu_temp":                       None,
    "rear_acc_x":                           None,
    "rear_acc_y":                           None,
    "rear_acc_y":                           None,
    "rear_angular_x":                       None,
    "rear_angular_y":                       None,
    "rear_angular_z":                       None,
    "rear_imu_temp":                        None,
}

DISPLAY_SIGNALS = {
    "name":                                 "display.dbc",

    "cpu_temperature":                      "display_temp",
}

MOTOR_SIGNALS = {
    "name":                                 "pm100dx.dbc",

    # TODO: Determine what will be used and what can be removed
    # https://app.box.com/s/vf9259qlaadhzxqiqrt5cco8xpsn84hk/file/27334613044
    "INV_Module_A":                         "module_a_temp",
    "INV_Module_B":                         "module_b_temp",
    "INV_Module_C":                         "module_c_temp",
    "INV_Gate_Driver_Board":                "gate_drive_temp",
    "INV_Control_Board_Temperature":        "ctrl_board_temp",
    "INV_RTD1_Temperature":                 "rtd1_temp",
    "INV_RTD2_Temperature":                 "rtd2_temp",
    "INV_RTD3_Temperature":                 "rtd3_temp",
    "INV_RTD4_Temperature":                 "coolant_temp",
    "INV_RTD5_Temperature":                 "hotspot_temp",
    "INV_Motor_Temperature":                "motor_temp",
    "INV_Torque_Shudder":                   "torque_shudder",
    "INV_Analog_Input_1":                   "analog_input_1",
    "INV_Analog_Input_2":                   "analog_input_2",
    "INV_Analog_Input_3":                   "analog_input_3",
    "INV_Analog_Input_4":                   "analog_input_4",
    "INV_Analog_Input_5":                   "analog_input_5",
    "INV_Analog_Input_6":                   "analog_input_6",
    "INV_Digital_Input_1":                  "digital_input_1",
    "INV_Digital_Input_2":                  "digital_input_2",
    "INV_Digital_Input_3":                  "digital_input_3",
    "INV_Digital_Input_4":                  "digital_input_4",
    "INV_Digital_Input_5":                  "digital_input_5",
    "INV_Digital_Input_6":                  "digital_input_6",
    "INV_Digital_Input_7":                  "digital_input_7",
    "INV_Digital_Input_8":                  "digital_input_8",
    "INV_Motor_Angle_Electrical":           "motor_angle",
    "INV_Motor_Speed":                      "motor_speed",
    "INV_Electrical_Output_Frequency":      "electric_freq",
    "INV_Phase_A_Current":                  "phase_a_current",
    "INV_Phase_B_Current":                  "phase_b_current",
    "INV_Phase_C_Current":                  "phase_c_current",
    "INV_DC_Bus_Current":                   "dc_bus_current",
    "INV_DC_Bus_Voltage":                   "dc_bus_voltage",
    "INV_Output_Voltage":                   "output_voltage",
    "INV_VAB_Vd_Voltage":                   "vab_vd_voltage",
    "INV_VBC_Vq_Voltage":                   "vbc_vq_voltage",
    "INV_Iq":                               "iq_feedback",
    "INV_Id":                               "id_feedback",
    "INV_VSM_State":                        "vsm_state",
    "INV_Inverter_State":                   "inverter_state",
    "INV_Inverter_Enable_State":            "inv_enabled",
    "INV_Inverter_Run_Mode":                "run_mode",
    "INV_Inverter_Command_Mode":            "command_mode",
    "INV_Direction_Command":                "direction",
    "INV_Inverter_Enable_Lockout":          "lockout_enabled",
    "INV_Inverter_Discharge_State":         "discharge_state",
    "INV_Relay_1_Status":                   "relay_1_status",
    "INV_Relay_2_Status":                   "relay_2_status",
    "INV_Relay_3_Status":                   "relay_3_status",
    "INV_Relay_4_Status":                   "relay_4_status",
    "INV_Relay_5_Status":                   "relay_5_status",
    "INV_Relay_6_Status":                   "relay_6_status",
    "INV_BMS_Active":                       "bms_active",
    "INV_BMS_Torque_Limiting":              "bms_trq_limit",
    "INV_Max_Speed_Limiting":               "max_spd_limit",
    "INV_Low_Speed_Limiting":               "low_spd_limit",
    "INV_PWM_Frequency":                    "pwm_frequency",
    "INV_Start_Mode_Active":                "start_mode",
    "INV_Run_Fault_Hi":                     "run_fault_hi",
    "INV_Run_Fault_Lo":                     "run_fault_lo",
    "INV_Post_Fault_Hi":                    "post_fault_hi",
    "INV_Post_Fault_Lo":                    "post_fault_lo",
    "INV_Commanded_Torque":                 "torque_cmd",
    "INV_Torque_Feedback":                  "torque_fb",
    "INV_Power_On_Timer":                   "power_on_timer",
    "INV_Modulation_Index":                 "mod_index",
    "INV_Max_Discharge_Current":            "max_dischg_curr",
    "INV_Max_Charge_Current":               "max_charge_curr",
}

SIGNALS = [IMU_SIGNALS, DISPLAY_SIGNALS, MOTOR_SIGNALS]

no_rename_over = []
renamed_over   = []

for signal_dict in SIGNALS:
    for orig, rename in signal_dict.items():
        if orig == "name":
            continue

        if rename is None and len(orig) > 16:
            no_rename_over.append((orig, len(orig)))
        elif rename is not None and len(rename) > 16:
            renamed_over.append((orig, rename, len(rename)))

if no_rename_over:
    print("No rename, original exceeds 16 chars:")
    for orig, n in no_rename_over:
        print(f"  {orig!r} ({n} chars)")

if renamed_over:
    print("Renamed, but rename still exceeds 16 chars:")
    for orig, rename, n in renamed_over:
        print(f"  {orig!r} -> {rename!r} ({n} chars)")

if not no_rename_over and not renamed_over:
    print("All signal names are 16 chars or less")

OUTPUT_DIR = Path("dbc/aim")
OUTPUT_DIR.mkdir(exist_ok=True)

def clone_signal(signal, new_name):
    return cantools.database.Signal(
        name=new_name,
        start=signal.start,
        length=signal.length,
        byte_order=signal.byte_order,
        is_signed=signal.is_signed,
        raw_initial=getattr(signal, "raw_initial", None),
        raw_invalid=getattr(signal, "raw_invalid", None),
        conversion=signal.conversion,
        minimum=signal.minimum,
        maximum=signal.maximum,
        unit=signal.unit,
        dbc_specifics=getattr(signal, "dbc_specifics", None),
        comment=signal.comment,
        receivers=getattr(signal, "nodes", None),
        is_multiplexer=signal.is_multiplexer,
        multiplexer_ids=signal.multiplexer_ids,
        multiplexer_signal=getattr(signal, "multiplexer_signal", None),
        spn=getattr(signal, "spn", None),
    )

def clone_message(message, signals):
    return cantools.database.Message(
        frame_id=message.frame_id,
        name=message.name,
        length=message.length,
        signals=signals,

        contained_messages=getattr(message, "contained_messages", None),
        header_id=getattr(message, "header_id", None),
        header_byte_order=getattr(message, "header_byte_order", "big_endian"),
        unused_bit_pattern=getattr(message, "unused_bit_pattern", 0x00),

        comment=message.comment,
        senders=message.senders,
        send_type=message.send_type,
        cycle_time=message.cycle_time,

        dbc_specifics=getattr(message, "dbc_specifics", None),
        autosar_specifics=getattr(message, "autosar_specifics", None),

        is_extended_frame=getattr(message, "is_extended_frame", False),
        is_fd=getattr(message, "is_fd", False),

        bus_name=message.bus_name,
        signal_groups=getattr(message, "signal_groups", None),

        strict=getattr(message, "strict", True),
        protocol=getattr(message, "protocol", None),

        sort_signals=getattr(message, "sort_signals", None),
    )

def filter_signals(signals, rename_map):
    """Filter and rename signals based on the rename map for this signal dict."""
    return [
        clone_signal(s, rename_map[s.name.lower()])
        for s in signals
        if rename_map.get(s.name.lower()) is not None
    ]

def merge_message(existing, incoming_signals):
    existing_names = {s.name for s in existing.signals}
    new = [s for s in incoming_signals if s.name not in existing_names]
    return clone_message(existing, existing.signals + new) if new else existing

DBC_DIR = Path("dbc")
dbc_files = sorted(DBC_DIR.glob("*.dbc"))
if not dbc_files:
    raise FileNotFoundError(f"No .dbc files found in {DBC_DIR}")

all_messages = {}
for dbc_file in dbc_files:
    db = cantools.database.load_file(str(dbc_file))
    for msg in db.messages:
        all_messages[msg.frame_id] = (
            msg if msg.frame_id not in all_messages
            else merge_message(all_messages[msg.frame_id], msg.signals)
        )

# Iterate over every DBC file
for signal_dict in SIGNALS:
    dbc_name = signal_dict["name"]
    output_file = OUTPUT_DIR / dbc_name

    rename_map = {
        orig.lower(): (rename if rename is not None else orig)
        for orig, rename in signal_dict.items()
        if orig != "name" # Skip the 'name' key
    }

    # Filter messages down to selected
    filtered_messages = {}
    for msg in all_messages.values():
        filtered_signals = filter_signals(msg.signals, rename_map)
        if filtered_signals:
            filtered_messages[msg.frame_id] = clone_message(msg, filtered_signals)

    # Save the new DBC
    if filtered_messages:
        output_db = cantools.database.Database(messages=list(filtered_messages.values()))
        cantools.database.dump_file(output_db, str(output_file))
        print(f"Saved {dbc_name}: {len(filtered_messages)} messages, {sum(len(m.signals) for m in filtered_messages.values())} signals")
    else:
        print(f"No matching signals found for {dbc_name}")

print(f"\nAll files saved to {OUTPUT_DIR}")
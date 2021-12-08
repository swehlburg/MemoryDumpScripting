"""
    Created by Stephen Wehlburg for lab project
    wehlburgsc@vcu.edu
"""

import sys
import os
import time
import subprocess

PLC_dict = {
    0: "M221",
    1: "AllenBradley"
}

Program_dict = {
    0: "Elevator",
    1: "Conveyor"
}

Attack_dict = {
    0: "N/A",
    1: "PasswordBreak"
}

M221_addresses_vec = [
    0x00000000,
    0x00020000,
    0x00080000,
    0x00100000,
    0x00108000,
    0x007F8000,
    0x007FA000,
    0x007FC000,
    0x007FC500,
    0x007FFC00,
    0x00800000,
    0x00E00000,
    0x01000000,
    0x08000000,
    0xFEFFE000,
    0xFF000000,
    0xFF7FC000,
    0xFF800000,
    0xFFE00000,
    0xFFFFFFFF
]

M22_blocks_vec = [
    "RAM",
    "Reserved_area_1",
    "Peripheral_IO_registers_1",
    "On-chip_ROM_E2_data_flash",
    "Reserved_area_2",
    "FCU-RAM",
    "Reserved_area_3",
    "Peripheral_IO_registers_2",
    "Reserved_area_4",
    "Peripheral_IO_registers_3",
    "Reserved_area_5",
    "On-chip_ROM_program_ROM",
    "External_address_space",
    "Reserved_area_6",
    "On-chip_ROM_FCU_firmware_read_only",
    "Reserved_area_7",
    "On-chip_ROM_user_boot_read_only",
    "Reserved_area_8",
    "On-chip_ROM_program_ROM_read_only"
]


def formatted_dump(name: str,
                   plc_id: int, program_id: int, plc_ip: str, num_dumps: int):
    """
        main function to gather multiple memory dumps
        name: name of person taking memory dump
        plc_id: 0 -> M221, 1 -> AllenBradley
        program_id: 0 -> Elevator, 1 -> Conveyor
        plc_ip: ip address of target PLC
        num_dumps: number of memory dumps to run on this PLC
        time_delay: the amount of seconds to wait between each memory dump
    """

    plc = PLC_dict.get(plc_id)
    program = Program_dict.get(program_id)
    time_string = time.strftime("%Y_%m_%d__%H_%M_%S", time.gmtime())

    # region Directory Setup
    if not os.path.isdir(PLC_dict.get(plc_id)):
        os.mkdir(plc)

    if not os.path.isdir(str(PLC_dict.get(plc_id) + "/" + Program_dict.get(program_id))):
        os.mkdir(str(plc + "/" + program))

    if not os.path.isdir(str(PLC_dict.get(plc_id) + "/" + Program_dict.get(program_id) + "/" + time_string)):
        os.mkdir(str(plc + "/" + program + "/" + time_string))
    else:
        sys.stderr.write("Chances two dumps taken at the exact same second is minimal, potential error")
        return
    # endregion

    filepath = str(PLC_dict.get(plc_id) + "/" + Program_dict.get(program_id) + "/" + time_string + "/")

    meta_text = [str("Name: " + name),
                 str("Control Logic: " + Program_dict[program_id]),
                 str("Number of Memory Dumps: " + str(num_dumps)),
                 str("Attack: " + Attack_dict[0]),
                 str("\tAttack Parameters: " + Attack_dict[0])
                 ]

    i = 0
    while i < num_dumps:
        print("Dump Number: " + str(i))
        meta_text.append("")
        meta_text.append(str("Memory Dump Number: " + str(i+1)))
        meta_text.append(str("Start Time: " + time.strftime("Y%Y_M%m_D%d__H%H_Min%M_S%S", time.gmtime())))
        j = 0
        os.mkdir(str(filepath) + "DumpNum" + str(i))
        while j < (len(M221_addresses_vec) - 1):
            if j != 13:
                print("Block Number: " + str(j))
                subprocess.run(["python",
                                "m221_read_mem.py",
                                str(plc_ip),
                                str(M221_addresses_vec[j]),
                                str(M221_addresses_vec[j+1] - M221_addresses_vec[j]),
                                str(filepath + "DumpNum" + str(i) + "/BlockNum" + str(j) + "_" + M22_blocks_vec[j] + ".bin")])
            j += 1
        meta_text.append(str("End Time: " + time.strftime("Y%Y_M%m_D%d__H%H_Min%M_S%S", time.gmtime())))
        time.sleep(5)
        i += 1
        print()

    write_file_vector(str(filepath) + "/meta_data.txt", meta_text)


def formatted_attack_dump(name: str,
                          plc_id: int, program_id: int, plc_ip: str, num_dumps: int,
                          attack_id: int, attack_parameters: str):
    """
        main function to gather multiple memory dumps
        name: name of person running program
        plc_id: 0 -> M221, 1 -> AllenBradley
        program_id: 0 -> Elevator, 1 -> Conveyor
        plc_ip: ip address of target PLC
        num_dumps: number of memory dumps to run on this PLC
        attack_id: 0 -> N/A,
        attack_parameters: the parameters you used/will use during the attack
    """

    plc = PLC_dict.get(plc_id)
    program = Program_dict.get(program_id)
    time_string = time.strftime("%Y_%m_%d__%H_%M_%S", time.gmtime())

    # region Directory Setup
    if not os.path.isdir(PLC_dict.get(plc_id)):
        os.mkdir(plc)

    if not os.path.isdir(str(PLC_dict.get(plc_id) + "/" + Program_dict.get(program_id))):
        os.mkdir(str(plc + "/" + program))

    if not os.path.isdir(str(PLC_dict.get(plc_id) + "/" + Program_dict.get(program_id) + "/" + time_string)):
        os.mkdir(str(plc + "/" + program + "/" + time_string))
    else:
        sys.stderr.write("Chances two dumps taken at the exact same second is minimal, potential error")
        return
    # endregion

    filepath = str(PLC_dict.get(plc_id) + "/" + Program_dict.get(program_id) + "/" + time_string + "/")

    meta_text = [str("Name: " + name),
                 str("Control Logic: " + Program_dict[program_id]),
                 str("Number of Memory Dumps: " + str(num_dumps)),
                 str("Attack: " + Attack_dict[attack_id]),
                 str("\tAttack Parameters: " + attack_parameters)
                 ]

    i = 0
    while i < num_dumps:
        print("Dump Number: " + str(i))
        meta_text.append("")
        meta_text.append(str("Memory Dump Number: " + str(i+1)))
        meta_text.append(str("Start Time: " + time.strftime("%Y_%m_%d__%H_%M_%S", time.gmtime())))
        j = 0
        os.mkdir(str(filepath) + "/" + str(i))
        while j < (len(M221_addresses_vec) - 1):
            if j != 13:
                print("Block Number: " + str(j))
                subprocess.run(["python", "m221_read_mem.py",
                                str(plc_ip),
                                str(M221_addresses_vec[j]),
                                str(M221_addresses_vec[j + 1] - M221_addresses_vec[j]),
                                str(filepath + str(i) + "/" + str(j) + "_" + M22_blocks_vec[j] + ".bin")])
            j += 1
        meta_text.append(str("End Time: " + time.strftime("Y%Y_M%m_D%d__H%H_Min%M_S%S", time.gmtime())))
        time.sleep(5)
        i += 1

    write_file_vector(str(filepath) + "/meta_data.txt", meta_text)


def write_file_vector(file_name, file_vec):
    text_file = open(file_name, 'w')
    for sent in file_vec:
        text_file.write(sent + '\n')


if __name__ == '__main__':
    if len(sys.argv) == 0:
        print("PUT MENU STUFF HERE")
    elif len(sys.argv) == 7:
        """
            Order of parameters should be: "your name", plc ID, program ID, plc IP, 
        """
        formatted_dump(sys.argv[1],
                       int(sys.argv[2]),
                       int(sys.argv[3]),
                       sys.argv[4],
                       int(sys.argv[6]))
    elif len(sys.argv) == 9:
        print(str("You're running the attack: " + Attack_dict[int(sys.argv[7])]))
        print("With parameters: " + sys.argv[8])
        formatted_attack_dump(sys.argv[1],
                              int(sys.argv[2]),
                              int(sys.argv[3]),
                              sys.argv[5],
                              int(sys.argv[6]),
                              int(sys.argv[7]),
                              sys.argv[8])


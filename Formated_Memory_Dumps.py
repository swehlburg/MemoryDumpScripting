"""
    Created by Stephen Wehlburg for lab project
    wehlburgsc@vcu.edu
"""

import sys
import os
import time
import subprocess

name = ""

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


def formatted_dump(plc_id, program_id, plc_ip, num_dumps, time_delay):
    """
        main function to gather multiple memory dumps
        plc_id: 0 -> M221, 1 -> AllenBradley
        program_id: 0 -> Elevator, 1 -> Conveyor
        plc_ip: ip address of target PLC
        num_dumps: number of memory dumps to run on this PLC
        time_delay: the amount of seconds to wait between each memory dump
    """

    PLC = PLC_dict.get(plc_id)
    program = Program_dict.get(program_id)
    time_string = time.strftime("%Y_%m_%d__%H_%M_%S", time.gmtime())

    # region Directory Setup
    if not os.path.isdir(PLC_dict.get(plc_id)):
        os.mkdir(PLC)

    if not os.path.isdir(str(PLC_dict.get(plc_id) + "/" + Program_dict.get(program_id))):
        os.mkdir(str(PLC + "/" + program))

    if not os.path.isdir(str(PLC_dict.get(plc_id) + "/" + Program_dict.get(program_id) + "/" + time_string)):
        os.mkdir(str(PLC + "/" + program + "/" + time_string))
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
        print("Dump Numer: " + str(i))
        meta_text.append("")
        meta_text.append(str("Memory Dump Number: " + str(i+1)))
        meta_text.append(str("Start Time: " + time.strftime("Y%Y_M%m_D%d__H%H_Min%M_S%S", time.gmtime())))
        j = 0
        os.mkdir(str(filepath) + "/" + str(i))
        while j < (len(M221_addresses_vec) - 1):
            if j != 13:
                print("Block Numer: " + str(j))
                subprocess.run(["python", "m221_read_mem.py",
                                   str(plc_ip),
                                   str(M221_addresses_vec[j]),
                                   str(M221_addresses_vec[j+1] - M221_addresses_vec[j]),
                                   str(filepath + str(i) + "/" + str(j) + ".bin")])
#                m221_read_mem_func.test(plc_ip,
#                                        M221_addresses_vec[j],
#                                        M221_addresses_vec[j + 1] - M221_addresses_vec[j],
#                                        str(filepath + "/" + str(i) + "/" + str(j) + ".bin"))
            j += 1
        meta_text.append(str("End Time: " + time.strftime("Y%Y_M%m_D%d__H%H_Min%M_S%S", time.gmtime())))
        time.sleep(time_delay)
        i += 1
        print()

    write_file_vector(str(filepath) + "/meta_data.txt", meta_text)


def formatted_attack_dump(plc_id, program_id, plc_ip, num_dumps, time_delay, attack_id, attack_parameters):
    """
            main function to gather multiple memory dumps
            plc_id: 0 -> M221, 1 -> AllenBradley
            program_id: 0 -> Elevator, 1 -> Conveyor
            plc_ip: ip address of target PLC
            num_dumps: number of memory dumps to run on this PLC
            time_delay: the amount of seconds to wait between each memory dump
            attack_id: 0 -> N/A,
            attack_parameters: the parameters you used/will use during the attack
        """

    PLC = PLC_dict.get(plc_id)
    program = Program_dict.get(program_id)
    time_string = time.strftime("%Y_%m_%d__%H_%M_%S", time.gmtime())

    # region Directory Setup
    if not os.path.isdir(PLC_dict.get(plc_id)):
        os.mkdir(PLC)

    if not os.path.isdir(str(PLC_dict.get(plc_id) + "/" + Program_dict.get(program_id))):
        os.mkdir(str(PLC + "/" + program))

    if not os.path.isdir(str(PLC_dict.get(plc_id) + "/" + Program_dict.get(program_id) + "/" + time_string)):
        os.mkdir(str(PLC + "/" + program + "/" + time_string))
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
        print("Dump Numer: " + str(i))
        meta_text.append("")
        meta_text.append(str("Memory Dump Number: " + str(i+1)))
        meta_text.append(str("Start Time: " + time.strftime("%Y_%m_%d__%H_%M_%S", time.gmtime())))
        j = 0
        os.mkdir(str(filepath) + "/" + str(i))
        while j < (len(M221_addresses_vec) - 1):
            if j != 13:
                print("Block Numer: " + str(j))
                subprocess.run(["python", "m221_read_mem.py",
                                str(plc_ip),
                                str(M221_addresses_vec[j]),
                                str(M221_addresses_vec[j + 1] - M221_addresses_vec[j]),
                                str(filepath + str(i) + "/" + str(j) + ".bin")])
            j += 1
        meta_text.append(str("End Time: " + time.strftime("Y%Y_M%m_D%d__H%H_Min%M_S%S", time.gmtime())))
        time.sleep(time_delay)
        i += 1

    write_file_vector(str(filepath) + "/meta_data.txt", meta_text)


def write_file_vector(file_name, file_vec):
    text_file = open(file_name, 'w')
    for sent in file_vec:
        text_file.write(sent + '\n')


if __name__ == '__main__':
    name = input("Who's running this? ")
    if len(sys.argv) == 0:
        print("PUT MENU STUFF HERE")
    elif len(sys.argv) == 6:
        formatted_dump(int(sys.argv[1]),
                       int(sys.argv[2]),
                       sys.argv[3],
                       int(sys.argv[4]),
                       int(sys.argv[5]))
    elif len(sys.argv) == 7:
        print(str("You're running the attack: " + Attack_dict[int(sys.argv[6])]))
        a_p = input("What are the parameters? ")
        formatted_attack_dump(int(sys.argv[1]),
                              int(sys.argv[2]),
                              int(sys.argv[3]),
                              sys.argv[4],
                              int(sys.argv[5]),
                              int(sys.argv[6]),
                              a_p)

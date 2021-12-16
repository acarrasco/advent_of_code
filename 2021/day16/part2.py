import sys
import re
from collections import defaultdict


hex_map = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

literal_char_width = 5


def literal(binary_body):
    i = 0
    characters = []
    while binary_body[i * literal_char_width] == '1':
        c = binary_body[i * literal_char_width + 1: (i + 1) * literal_char_width]
        characters.append(c)
        i += 1
    c = binary_body[i * literal_char_width + 1: (i + 1) * literal_char_width]
    characters.append(c)

    number = int(''.join(characters), 2)
    unconsumed = binary_body[(i+1)*literal_char_width:]
    return number, unconsumed


def op_sum(binary_body):
    sub_packets, unconsumed = operator(binary_body)
    return sum(sub_packets), unconsumed

def op_product(binary_body):
    sub_packets, unconsumed = operator(binary_body)
    res = 1
    for sp in sub_packets:
        res *= sp
    return res, unconsumed

def op_min(binary_body):
    sub_packets, unconsumed = operator(binary_body)
    return min(sub_packets), unconsumed

def op_max(binary_body):
    sub_packets, unconsumed = operator(binary_body)
    return max(sub_packets), unconsumed

def op_gt(binary_body):
    sub_packets, unconsumed = operator(binary_body)
    a, b = sub_packets
    return int(a > b), unconsumed

def op_lt(binary_body):
    sub_packets, unconsumed = operator(binary_body)
    a, b = sub_packets
    return int(a < b), unconsumed

def op_eq(binary_body):
    sub_packets, unconsumed = operator(binary_body)
    a, b = sub_packets
    return int(a == b), unconsumed


packet_types = {
    0: op_sum,
    1: op_product,
    2: op_min,
    3: op_max,
    4: literal,
    5: op_gt,
    6: op_lt,
    7: op_eq,
}


def operator(binary_body):
    length_type_id = binary_body[0]
    if length_type_id == '0':
        sub_packets_length, rest = int(binary_body[1:16], 2), binary_body[16:]

        sub_packets_bits, unconsumed = rest[:sub_packets_length], rest[sub_packets_length:]
        sub_packets = []
        while sub_packets_bits:
            sub_packet, sub_packets_bits = parse_packet(sub_packets_bits)
            sub_packets.append(sub_packet)
        return sub_packets, unconsumed
    else:
        number_of_subpackets, rest = int(binary_body[1:12],2), binary_body[12:]
        sub_packets_bits = []
        unconsumed = rest
        while number_of_subpackets:
            sub_packet, unconsumed = parse_packet(unconsumed)
            sub_packets_bits.append(sub_packet)
            number_of_subpackets -= 1
        return sub_packets_bits, unconsumed


def parse_header(header):
    version = int(header[0:3], 2)
    packet_type = int(header[3:6], 2)
    return version, packet_type


def hex_to_binary(hex_string):
    return ''.join(map(hex_map.get, hex_string))


def parse_packet(binary_packet):
    header, body = binary_packet[0:6], binary_packet[6:]
    version, packet_type = parse_header(header)
    versions.append(version)
    parser = packet_types.get(packet_type, operator)
    return parser(body)


input = sys.stdin.read().strip()
bin_packet = hex_to_binary(input)

versions = []
print(parse_packet(bin_packet)[0])

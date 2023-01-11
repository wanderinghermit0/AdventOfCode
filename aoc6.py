def distinct_char_index(message, distinct_num):
    char_count = distinct_num
    header = message[:char_count]
    for _ in message:
        header_set = set(header)
        if len(header_set) == distinct_num:
            break
        header = header[1:]
        char_count += 1
        header = header + message[char_count]

    return char_count


f = open("input6.txt")
message = f.read()
packet_start = distinct_char_index(message, 4)
message_start = distinct_char_index(message, 14)

print(packet_start + 1)
print(message_start + 1)
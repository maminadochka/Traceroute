# Checksum Calculation (https://tools.ietf.org/html/rfc1071)
def calc_checksum(header):
    # Initialise checksum and overflow
    checksum = 0
    overflow = 0

    # For every word (16-bits)
    for i in range(0, len(header), 2):
        word = header[i] + (header[i + 1] << 8)

        # Add the current word to the checksum
        checksum = checksum + word
        # Separate the overflow
        overflow = checksum >> 16
        # While there is an overflow
        while overflow > 0:
            # Remove the overflow bits
            checksum = checksum & 0xFFFF
            # Add the overflow bits
            checksum = checksum + overflow
            # Calculate the overflow again
            overflow = checksum >> 16

    # There's always a chance that after calculating the checksum
    # across the header, ther is *still* an overflow, so need to
    # check for that
    overflow = checksum >> 16
    while overflow > 0:
        checksum = checksum & 0xFFFF
        checksum = checksum + overflow
        overflow = checksum >> 16

    # Ones-compliment and return
    checksum = ~checksum
    checksum = checksum & 0xFFFF

    return checksum

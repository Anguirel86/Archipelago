import hashlib
import io


class JPRom():
    """
    Class to manage the Jurassic Park ROM data.
    """

    JPUSA_MD5_HASH = "bb9c2f667ced16a2e605b385c041c744"

    _ROM_SIZE = 0x30_0000

    def __init__(self, rom: bytes | str):
        if isinstance(rom, str):
            with open(rom, "rb") as file:
                self._rom_buf = io.BytesIO(file.read())
        elif isinstance(rom, bytes):
            self._rom_buf = io.BytesIO(rom)
        else:
            raise Exception("Invalid ROM source")

        rommd5 = hashlib.md5()
        rommd5.update(self._rom_buf.getbuffer())

        if rommd5.hexdigest() != self.JPUSA_MD5_HASH:
            raise Exception("Invalid hash. Please use a Jurassic Park USA ROM")

        self.next_free_addr = -1
        self.expand_rom()

    def expand_rom(self):
        """
        Expand the Jurassic Park ROM data to 3MB
        and update the SNES headers appropriately.
        """

        # Update ROM max size from 2MB to 4MB
        self._rom_buf.seek(0x7FD7)
        self._rom_buf.write(bytes([0x0C]))

        # Update with a temp checksum
        self._rom_buf.seek(0x7FDC)
        self._rom_buf.write(bytes([0x00, 0x00, 0xFF, 0xFF]))

        # Expand the ROM to 3MB
        # Could go to 4MB, but 1MB should be mnore than enough space
        self._rom_buf.seek(0, io.SEEK_END)
        self._rom_buf.write(bytes([0] * 0x100000))

        # Set the next free address to the beginning of the first new bank (C0)
        self.next_free_addr = 0x20_0000

    @staticmethod
    def to_cpu_addr(rom_addr: int) -> int:
        """
        Convert a ROM address to a CPU address for branches/jumps

        Jurassic Park is a LoROM game, meaning it only uses 32k of each bank,
        specifically, the upper half (0x8000-0xFFFF)
        Program memory is mapped starting at 0x80_0000
        """
        # Divide by 32k to get the bank offset
        bank = 0x80 + (rom_addr >> 15)

        # shift remaining addr into upper half of the bank
        addr = 0x8000 + (rom_addr & 0x7FFF)

        # Combine the bank and address
        return (bank << 16) | addr

    def write(self, addr: int, data: bytes):
        """
        Write the given data starting at the given address.
        """
        end = addr + len(data)
        if end > self._ROM_SIZE:
            raise Exception(f"Attempt to write beyond the ROM bounds: {end}")

        self._rom_buf.seek(addr)
        self._rom_buf.write(data)

    def write_patch_with_padding(self, addr: int, end_addr: int, data: bytes):
        """
        Write to the ROM and pad out any extra bytes with NOP instructions.
        """
        total_bytes = end_addr - addr
        if total_bytes < len(data):
            raise Exception("Data overlaps end address")

        self.write(addr, data)
        pad_bytes = total_bytes - len(data)
        # TODO: This could be smarter for big gaps with a jump or branch
        #       instead of a long string of NOPs.
        nops = bytes([0xEA] * pad_bytes)
        self._rom_buf.seek(addr + len(data))
        self._rom_buf.write(nops)

    def reserve(self, requested_size: int) -> int:
        """
        Get the next free address to store data to the ROM.
        This is a ROM (file) address, not a CPU address.
        Requested_size is the size of the requested free space in bytes.
        The requested space will be reserved.

        Rudimentary free space management:
        With the ROM expansion, there is 1MB of free space starting
        at bank 0xC0.  Keep a counter of used bytes starting here and
        return the next free address.

        This routine does not honor bank boundaries.
        """
        if self.next_free_addr == -1:
            raise Exception("ROM hasn't been expanded. Free space unknown")
        addr = self.next_free_addr
        self.next_free_addr = self.next_free_addr + requested_size
        return addr

    def get_buffer(self) -> bytes:
        """
        Return the raw bytes buffer of this ROM.
        """
        return self._rom_buf.getbuffer()

    def write_to_file(self, file_name: str):
        """
        Update the SNES header checksum and write the ROM to file
        """
        # Calculate the ROM checksum and complement and write them
        # to the SNES header.
        checksum = sum(self._rom_buf.getbuffer()) & 0xFFFF
        complement = checksum ^ 0xFFFF

        self.write(0x7FDE, checksum.to_bytes(
            2, byteorder="little", signed=False))
        self.write(0x7FDC, complement.to_bytes(
            2, byteorder="little", signed=False))

        # Write file
        with open(file_name, 'wb') as f:
            f.write(self._rom_buf.getbuffer())

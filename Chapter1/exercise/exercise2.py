# class that inherits/wraps the int type
class BitStr(int):
    def __init__(self) -> None:
        # start with sentinel
        self.bit_str = 1

    def shift_left(self, places: int):
        self.bit_str <<= places

    def change_last_bits(self, bits: int):
        self.bit_str |= bits

    def __iter__(self):
        self.index = 0  # restart index for iterator
        return self

    def __next__(self):
        if self.index < self.bit_str.bit_length() - 1:
            bits: int = self.bit_str >> self.index & 0b11  # get just 2 relevant bit
            self.index += 2
            return bits
        raise StopIteration


class CompressedGene:
    def __init__(self, gene: str) -> None:
        self._compress(gene)

    def _compress(self, gene: str) -> None:
        # start with sentinel ('flag value', just for declaration?)
        self.bit_string: BitStr = BitStr()

        for nucleotide in gene.upper():
            # shift left two bits (and adds two 00s on the right)
            self.bit_string.shift_left(2)
            if nucleotide == "A":  # change last two bits to 00
                # 0b tells python it is a base 2 number
                self.bit_string.change_last_bits(0b00)
            elif nucleotide == "C":  # change last two bits to 01
                self.bit_string.change_last_bits(0b01)
            elif nucleotide == "G":  # change last two bits to 10
                self.bit_string.change_last_bits(0b10)
            elif nucleotide == "T":  # change last two bits to 11
                self.bit_string.change_last_bits(0b11)
            else:
                raise ValueError("Invalid Nucleotide:{}".format(nucleotide))

    def decompress(self) -> str:
        gene: str = ""
        for bits in self.bit_string:  # - 1 to exclude sentinel
            if bits == 0b00:  # A
                gene += "A"
            elif bits == 0b01:  # C
                gene += "C"
            elif bits == 0b10:  # G
                gene += "G"
            elif bits == 0b11:  # T
                gene += "T"
            else:
                raise ValueError("Invalid bits:{}".format(bits))
        return gene[::-1]  # [::-1] reverses string by slicing backwards

    def __str__(self) -> str:  # string representation for pretty printing
        return self.decompress()


if __name__ == "__main__":
    from sys import getsizeof
    original: str = "TAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATATAGGGATTAACCGTTATATATATATAGCCATGGATCGATTATA" * 100
    print("original is {} bytes".format(getsizeof(original)))
    compressed: CompressedGene = CompressedGene(original)  # compress
    print("compressed is {} bytes".format(getsizeof(compressed.bit_string)))
    print(compressed)
    print("original and decompressed are the same: {}".format(
        original == compressed.decompress()))

def lzv_compress(inputt):
    """Сжимает строку с использованием алгоритма LZV"""
    dictionary = {chr(i): i for i in range(256)}
    dict_size = len(dictionary.keys())
    current_string = ""
    compressed_data = []

    for symbol in inputt:
        combined_string = current_string + symbol
        if combined_string in dictionary:
            current_string = combined_string
        else:
            compressed_data.append(dictionary[current_string])
            dictionary[combined_string] = dict_size
            dict_size += 1
            current_string = symbol

    if current_string:
        compressed_data.append(dictionary[current_string])

    return compressed_data


def lzv_decompress(compressed_data):
    """Распаковывает данные, сжатые с использованием алгоритма LZV."""
    dictionary = {i: chr(i) for i in range(256)}  # Инициализация словаря ASCII символами
    dict_size = 256
    current_string = chr(compressed_data[0])
    decompressed_data = current_string

    for code in compressed_data[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            entry = current_string + current_string[0]
        else:
            raise ValueError("Некорректный код в сжатых данных")

        decompressed_data += entry
        dictionary[dict_size] = current_string + entry[0]
        dict_size += 1
        current_string = entry

    return decompressed_data


# Пример использования
if __name__ == "__main__":
    text = "TOBEORNOTTOBEORTOBEORNOT"
    print("Исходный текст:", text)

    compressed = lzv_compress(text)
    print("Сжатые данные:", compressed)

    decompressed = lzv_decompress(compressed)
    print("Распакованный текст:", decompressed)
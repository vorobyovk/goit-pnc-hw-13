def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def vigenere_cipher(text, key, mode='encrypt'):    
    result = []
    key_len = len(key)
    for i, char in enumerate(text):
        if char == ' ':
            result.append(' ')  # Keep spaces as they are
            continue

        key_char = key[i % key_len]
        key_shift = ord(key_char.lower()) - ord('a')

        if 'encrypt' == mode:
            shifted_char = chr(((ord(char.lower()) - ord('a') + key_shift) % 26) + ord('a'))
        elif 'decrypt' == mode:
            shifted_char = chr(((ord(char.lower()) - ord('a') - key_shift + 26) % 26) + ord('a'))
        else:
            raise ValueError("Invalid mode. Choose 'encrypt' or 'decrypt'.")
        
        # Keep the original case
        if char.isupper():
            shifted_char = shifted_char.upper()
        
        result.append(shifted_char)
    return ''.join(result)

def kasiski_examination(ciphertext):
    # 1. Find repeated sequences in the ciphertext
    sequence_lengths = range(3, 6)  # Consider sequences of length 3 to 5
    sequence_occurrences = {}

    for seq_len in sequence_lengths:
        for i in range(len(ciphertext) - seq_len + 1):
            sequence = ciphertext[i:i + seq_len]
            occurrences = [j for j in range(len(ciphertext)) if ciphertext.startswith(sequence, j)]
            if len(occurrences) > 1:
                sequence_occurrences[sequence] = occurrences

    # 2. Calculate distances between repeated sequences
    distances = []
    for sequence, occurrences in sequence_occurrences.items():
        for i in range(len(occurrences) - 1):
            distances.append(occurrences[i+1] - occurrences[i])

    # 3. Find the most frequent factors of the distances
    factors = []
    for distance in distances:
        for i in range(2, distance + 1):  # Check factors from 2 to distance
            if distance % i == 0:
                factors.append(i)

    # Count frequency of each factor
    factor_counts = {}
    for factor in factors:
        if factor in factor_counts:
            factor_counts[factor] += 1
        else:
            factor_counts[factor] = 1

    # Sort factors by frequency
    sorted_factors = sorted(factor_counts.items(), key=lambda x: x[1], reverse=True)

    # Return a list of possible key lengths (factors), sorted by frequency
    possible_key_lengths = [factor for factor, count in sorted_factors]
    return possible_key_lengths


def main():    
    text_file_path = "text.txt"
    config_file_path = "config.txt"

    text = read_file_content(text_file_path)
    if text is None:
        return

    config_content = read_file_content(config_file_path)
    if config_content is None:
        return

    # Extract key from config content
    key_prefix = "KEY-VEGINER = \""
    if key_prefix in config_content:
        key_start_index = config_content.find(key_prefix) + len(key_prefix)
        key_end_index = config_content.find("\"", key_start_index)
        if key_end_index != -1:
            key = config_content[key_start_index:key_end_index]
        else:
            print("Error: Key value not properly formatted in config file.")
            return
    else:
        print("Error: KEY-VEGINER not found in config file.")
        return
    
    # Encrypt the text
    encrypted_text = vigenere_cipher(text, key, 'encrypt')
    print("Encrypted text:", encrypted_text)
    print("Length of encrypted text:", len(encrypted_text))
    print("---------------------------------------------------------")
    # Decrypt the text
    decrypted_text = vigenere_cipher(encrypted_text, key, 'decrypt')
    print("Decrypted text:", decrypted_text)
    print("Length of decrypted text:", len(decrypted_text))
    print("---------------------------------------------------------")
    # Perform Kasiski examination to find possible key lengths
    possible_key_lengths = kasiski_examination(encrypted_text)
    if possible_key_lengths:
        print("\nPossible key lengths (Kasiski examination):", possible_key_lengths)
    else:
        print("\nNo repeated sequences found. Kasiski examination could not determine key length.")

if __name__ == "__main__":
    main()

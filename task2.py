import collections
import math
import config

# The most frequent letter in English is 'e'.
ENGLISH_MOST_FREQUENT_CHAR = 'e'

def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def vigenere_cipher(text, key, mode='encrypt'):
    """Encrypts or decrypts text using the Vigenere cipher."""
    key = key.lower()
    key_len = len(key)
    if key_len == 0:
        return text
    result = []
    key_index = 0
    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            shift = ord(key[key_index % key_len]) - start
            if mode == 'encrypt':
                shifted_char_code = (ord(char) - start + shift) % 26 + start
            else:  # decrypt
                shifted_char_code = (ord(char) - start - shift + 26) % 26 + start
            result.append(chr(shifted_char_code))
            key_index += 1
        elif 'A' <= char <= 'Z':
            start = ord('A')
            shift = ord(key[key_index % key_len]) - start
            if mode == 'encrypt':
                shifted_char_code = (ord(char) - start + shift) % 26 + start
            else:  # decrypt
                shifted_char_code = (ord(char) - start - shift + 26) % 26 + start
            result.append(chr(shifted_char_code))
            key_index += 1
        else:
            result.append(char)
    return "".join(result)

def frequency_analysis(text):
    """Counts the frequency of each letter in the text."""
    text = text.lower()
    frequencies = collections.Counter(c for c in text if 'a' <= c <= 'z')
    return frequencies

def find_repeated_sequences_distances(text, min_len=3, max_len=5):
    """Finds distances between repeated sequences."""
    distances = []
    for seq_len in range(min_len, max_len + 1):
        sequences = {}
        for i in range(len(text) - seq_len):
            sequence = text[i:i + seq_len]
            if sequence not in sequences:
                sequences[sequence] = []
            sequences[sequence].append(i)
        
        for sequence, positions in sequences.items():
            if len(positions) > 1:
                for i in range(len(positions) - 1):
                    distances.append(positions[i+1] - positions[i])
    return distances 

def get_factors(n):
    """Returns all factors of a number n."""
    factors = set()
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            factors.add(i)
            factors.add(n // i)
    if n > 1:
        factors.add(n)
    return list(factors)

def kasiski_examination(ciphertext):
    """Estimates Vigenere cipher key length using Kasiski examination."""
    print("Performing Kasiski examination to find key length...")
    distances = find_repeated_sequences_distances(ciphertext)
    if not distances:
        print("No repeated sequences found. Kasiski examination failed.")
        return 0
    print(f"Found distances between repeated sequences: {distances}")
    all_factors = []
    for dist in distances:
        all_factors.extend(get_factors(dist))

    factor_counts = collections.Counter(all_factors)
    
    # We are interested in key lengths in a reasonable range, e.g., 3 to 20
    most_likely_lengths = [length for length, count in factor_counts.most_common(10) if 3 <= length <= 20]

    if not most_likely_lengths:
        print("Could not determine a likely key length from factors.")
        return 0
    
    key_length = most_likely_lengths[0]
    print(f"Most common factors (potential key lengths): {factor_counts.most_common(5)}")
    print(f"Estimated key length: {key_length}")
    return key_length

def find_key_char(column):
    """Finds the most likely key character for a given column of text."""
    frequencies = frequency_analysis(column)
    if not frequencies:
        return 'a'  # Default to 'a' if no letters are in the column

    most_frequent_char = frequencies.most_common(1)[0][0]
    
    # Shift is the difference between the most frequent char and 'e'
    shift = (ord(most_frequent_char) - ord(ENGLISH_MOST_FREQUENT_CHAR)) % 26
    return chr(ord('a') + shift)

def crack_vigenere(ciphertext):
    """Cracks a Vigenere cipher."""
    key_length = kasiski_examination(ciphertext)
    if key_length == 0:
        print("Could not determine key length. Aborting crack attempt.")
        return "", "", 0

    # Split ciphertext into columns based on key length
    # Only consider alphabetic characters for splitting
    only_letters = "".join(filter(str.isalpha, ciphertext))
    columns = [only_letters[i::key_length] for i in range(key_length)]

    # Find the key
    found_key = ""
    for i, column in enumerate(columns):
        print(f"\n--- Analyzing Column {i+1} (len={len(column)}) ---")
        key_char = find_key_char(column)
        found_key += key_char
        print(f"Frequency analysis for column {i+1}: {frequency_analysis(column).most_common(3)}")
        print(f"Most frequent char: '{frequency_analysis(column).most_common(1)[0][0]}'. Assuming it was '{ENGLISH_MOST_FREQUENT_CHAR}'.")
        print(f"Deduced key character: '{key_char}'")

    print("\n---------------------------------------------------------\n")
    print(f"Found key: '{found_key}'")

    # Decrypt the text with the found key
    decrypted_text = vigenere_cipher(ciphertext, found_key, 'decrypt')
    
    return decrypted_text, found_key, key_length
    
def main():
    text_file_path = "text2.txt"
    original_key = config.KEY

    original_text = read_file_content(text_file_path)
    if original_text is None:
        return
    
    print("Original text:")
    print(original_text)
    print("\n---------------------------------------------------------\n")

    # 1. Encrypt the text using Vigenere cipher
    print(f"1. Encrypting text with Vigenere cipher (key = '{original_key}')...")
    encrypted_text = vigenere_cipher(original_text, original_key, 'encrypt')
    print("Encrypted text:")
    print(encrypted_text)
    print("\n---------------------------------------------------------\n")

    # 2. Perform frequency analysis on the encrypted text
    print("2. Performing frequency analysis on encrypted text...")
    letter_frequencies = frequency_analysis(encrypted_text)
    sorted_frequencies = sorted(letter_frequencies.items(), key=lambda item: item[1], reverse=True)
    print("Letter frequencies (most common first):")
    print(sorted_frequencies)
    print("\n---------------------------------------------------------\n")

    # 3. & 4. Determine key length, decrypt the text, and recover the key
    print("3. & 4. Decrypting text using frequency analysis (Kasiski method)...")
    decrypted_text, found_key, found_key_length = crack_vigenere(encrypted_text)
    
    print(f"\nCalculated key length: {found_key_length}")
    print(f"Calculated key: '{found_key}'")
    print("Decrypted text:")
    print(decrypted_text)
    print("\n---------------------------------------------------------\n")

    # 5. Check if the decrypted text matches the original
    print("5. Verifying decryption...")
    if found_key.lower() == original_key.lower():
        print(f"SUCCESS: The calculated key ('{found_key}') matches the original key ('{original_key}').")
    else:
        print(f"FAILURE: The calculated key ('{found_key}') does not match the original key ('{original_key}').")
    # Using strip() to handle potential trailing whitespace differences
    if original_text.strip().lower() == decrypted_text.strip().lower():
         print("SUCCESS: The decrypted text matches the original text.")
    else: 
         print("FAILURE: The decrypted text does not match the original text.")
         print("This can happen if the key was not found correctly, or if the text is too short or has an unusual letter distribution.")

if __name__ == "__main__":
    main()

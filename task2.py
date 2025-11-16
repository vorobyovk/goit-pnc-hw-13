import collections
import math
import config

# The most frequent letter in English is 'e'.
ENGLISH_MOST_FREQUENT_CHAR = 'e'

# NEW: Standard English letter frequencies for Chi-squared test
ENGLISH_FREQUENCIES = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253,
    'e': 0.12702, 'f': 0.02228, 'g': 0.02015, 'h': 0.06094,
    'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
    'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929,
    'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150,
    'y': 0.01974, 'z': 0.00074
}


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
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            shift = ord(key[key_index % key_len]) - ord('a')

            if 'a' <= char <= 'z':
                start = ord('a')
            else:
                start = ord('A')
            
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
    alpha_text = "".join(filter(str.isalpha, ciphertext)).lower()
    distances = find_repeated_sequences_distances(alpha_text)
    
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

# --- REPLACED FUNCTION ---
# This is the new, more robust function to find the key character.
def find_key_char_chi_squared(column):
    """
    Finds the most likely key character for a column using Chi-squared test.
    It tests all 26 possible shifts and picks the one that results in a
    letter frequency distribution closest to standard English.
    """
    if not column:
        return 'a'

    column_len = len(column)
    best_shift = 0
    min_chi_sq = float('inf')

    for shift in range(26):
        # Calculate the Chi-squared statistic for this potential shift
        chi_sq = 0.0
        
        # Decrypt the column with the current hypothetical shift
        decrypted_column = vigenere_cipher(column, chr(ord('a') + shift), 'decrypt')
        
        # Get the frequency distribution of the hypothetically decrypted column
        observed_counts = frequency_analysis(decrypted_column)

        for i in range(26):
            char = chr(ord('a') + i)
            
            # Observed count of this character
            observed = observed_counts.get(char, 0)
            
            # Expected count based on standard English frequencies
            expected = column_len * ENGLISH_FREQUENCIES[char]
            
            # Chi-squared formula component
            if expected == 0:
                # Avoid division by zero, though unlikely with our frequencies
                difference = observed
            else:
                difference = observed - expected
            
            chi_sq += (difference ** 2) / (expected + 1e-9) # Add 1e-9 to avoid div by zero

        # If this shift gives a distribution closer to English, save it
        if chi_sq < min_chi_sq:
            min_chi_sq = chi_sq
            best_shift = shift

    return chr(ord('a') + best_shift)

# --- END OF REPLACED FUNCTION ---

def crack_vigenere(ciphertext):
    """Cracks a Vigenere cipher."""
    key_length = kasiski_examination(ciphertext)
    if key_length == 0:
        print("Could not determine key length. Aborting crack attempt.")
        return "", "", 0
    
    # Split ciphertext into columns based on key length
    only_letters = "".join(filter(str.isalpha, ciphertext)).lower()
    columns = [only_letters[i::key_length] for i in range(key_length)]
    
    # Find the key
    found_key = ""
    for i, column in enumerate(columns):
        print(f"\n--- Analyzing Column {i+1} (len={len(column)}) ---")
        
        # --- MODIFIED CALL ---
        # We now call the new, robust function
        key_char = find_key_char_chi_squared(column)
        # --- END OF MODIFIED CALL ---
        
        found_key += key_char
        print(f"Deduced key character using Chi-squared: '{key_char}'")
        
    print("\n---------------------------------------------------------\n")
    print(f"Found key: '{found_key}'")
    
    # Decrypt the text with the found key
    decrypted_text = vigenere_cipher(ciphertext, found_key, 'decrypt')
    
    return decrypted_text, found_key, key_length
    
def main():
    text_file_path = "text.txt"
    original_key = config.KEY

    original_text = read_file_content(text_file_path)
    if original_text is None:
        return
    
    # Use a larger text if possible. For demonstration, we can use a known text.
    # If text is too short, Kasiski and Chi-squared might still fail.
    # Let's add a check for short text.
    if len("".join(filter(str.isalpha, original_text))) < 500:
        print("WARNING: The input text is very short.")
        print("Frequency analysis and Kasiski examination are unreliable on short texts.")
        print("The crack is likely to fail or produce an incorrect key.")
        print("Please use a much larger 'text.txt' file (e.g., several pages of a book) for reliable results.")

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
    print("3. & 4. Decrypting text using frequency analysis (Kasiski + Chi-squared)...")
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
    
    # 6. Decrypt the text using the known key for comparison
    print("\n6. Decrypting text using the known key for comparison...")
    known_decrypted_text = vigenere_cipher(encrypted_text, original_key, 'decrypt')
    print("Decrypted text using known key:")
    print(known_decrypted_text)

if __name__ == "__main__":
    main()
import collections
import config

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

def caesar_cipher(text, shift, mode='encrypt'):
    result = []
    for char in text:
        if 'a' <= char <= 'z':
            start = ord('a')
            if mode == 'encrypt':
                shifted_char_code = (ord(char) - start + shift) % 26 + start
            else:  # decrypt
                shifted_char_code = (ord(char) - start - shift + 26) % 26 + start
            result.append(chr(shifted_char_code))
        elif 'A' <= char <= 'Z':
            start = ord('A')
            if mode == 'encrypt':
                shifted_char_code = (ord(char) - start + shift) % 26 + start
            else:  # decrypt
                shifted_char_code = (ord(char) - start - shift + 26) % 26 + start
            result.append(chr(shifted_char_code))
        else:
            result.append(char)
    return "".join(result)

def frequency_analysis(text):
    """Counts the frequency of each letter in the text."""
    text = text.lower()
    frequencies = collections.Counter(c for c in text if 'a' <= c <= 'z')
    return frequencies

def decrypt_with_frequency_analysis(ciphertext):
    """
    Decrypts a Caesar-ciphered text using frequency analysis.
    Returns the decrypted text and the found shift.
    """
    frequencies = frequency_analysis(ciphertext)
    if not frequencies:
        print("No letters found in the ciphertext for frequency analysis.")
        return "", 0
    # The most frequent letter in English is 'e'.
    # Find the most frequent letter in the ciphertext.
    most_frequent_char = frequencies.most_common(1)[0][0]
    print(f"Most frequent character in ciphertext: '{most_frequent_char}'")
    print("Assuming it corresponds to 'e' in plaintext...")
    # Calculate the shift by assuming the most frequent character in the ciphertext
    # corresponds to 'e' in the plaintext.
    shift = (ord(most_frequent_char) - ord('e')) % 26
    # Decrypt the text using the found shift
    decrypted_text = caesar_cipher(ciphertext, shift, 'decrypt')
    return decrypted_text, shift

def main():
    """Main function to run the Caesar cipher analysis."""
    text_file_path = "text.txt"
    original_text = read_file_content(text_file_path)
    if original_text is None:
        return
    
    print("Original text:")
    print(original_text)
    print("\n---------------------------------------------------------\n")
    # 1. Encrypt the text using Caesar cipher with a shift of 3
    print(f"1. Encrypting text with Caesar cipher (shift = {config.ENCRYPTION_SHIFT})...")
    encrypted_text = caesar_cipher(original_text, config.ENCRYPTION_SHIFT, 'encrypt')
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
    # 3. Decrypt the text using frequency analysis
    print("3. Decrypting text using frequency analysis...")
    decrypted_text, found_shift = decrypt_with_frequency_analysis(encrypted_text)
    print(f"\nCalculated shift based on frequency analysis: {found_shift}")
    print("Decrypted text:")
    print(decrypted_text)
    print("\n---------------------------------------------------------\n")
    # 4. Check if the decrypted text matches the original
    print("4. Verifying decryption...")
    if found_shift == config.ENCRYPTION_SHIFT:
        print(f"SUCCESS: The calculated shift ({found_shift}) matches the original encryption shift ({config.ENCRYPTION_SHIFT}).")
        # Using strip() to handle potential trailing whitespace differences
        if original_text.strip() == decrypted_text.strip():
             print("SUCCESS: The decrypted text matches the original text.")
        else:
             print("NOTE: The decrypted text does not perfectly match the original. This could be due to whitespace or other minor differences.")
    else:
        print(f"FAILURE: The calculated shift ({found_shift}) does not match the original encryption shift ({config.ENCRYPTION_SHIFT}).")
        print("This can happen if the text is too short or has an unusual letter distribution where 'e' is not the most frequent letter in the original text.")
    # 5. Decrypt the text using the known shift for comparison
    print("\n5. Decrypting text using the known shift for comparison...")
    known_decrypted_text = caesar_cipher(encrypted_text, config.ENCRYPTION_SHIFT, 'decrypt')
    print("Decrypted text using known shift:")
    print(known_decrypted_text)
    
if __name__ == "__main__":
    main()

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

def permutation_cipher(text, key, mode='encrypt'):
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    num_columns = len(key)
    num_rows = (len(text) + num_columns - 1) // num_columns

    # Pad the text
    padding_len = num_rows * num_columns - len(text)
    text += ' ' * padding_len

    # Create matrix
    matrix = [list(text[i * num_columns:(i + 1) * num_columns]) for i in range(num_rows)]

    # Perform permutation
    if mode == 'encrypt':
        result = [''.join(matrix[i][j] for i in range(num_rows)) for j in key_order]
        return ''.join(result)
    elif mode == 'decrypt':
        # Create reverse key order
        reverse_key_order = sorted(range(len(key)), key=lambda k: key_order[k])

        # Create matrix from encrypted text
        encrypted_matrix = [list(text[i * num_rows:(i + 1) * num_rows]) for i in range(num_columns)]

        # Perform reverse permutation
        result = [''.join(encrypted_matrix[i][j] for i in reverse_key_order) for j in range(num_rows)]
        return ''.join(result)
    else:
        raise ValueError("Invalid mode. Choose 'encrypt' or 'decrypt'.")

def double_permutation_cipher(text, key1, key2, mode='encrypt'):    
    if mode == 'encrypt':
        # First permutation
        intermediate_text = permutation_cipher(text, key1, 'encrypt')
        # Second permutation
        return permutation_cipher(intermediate_text, key2, 'encrypt')
    elif mode == 'decrypt':
        # First reverse permutation
        intermediate_text = permutation_cipher(text, key2, 'decrypt')
        # Second reverse permutation
        return permutation_cipher(intermediate_text, key1, 'decrypt')


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
    key_prefix = "PERMUTATION_KEY = \""
    if key_prefix in config_content:
        key_start_index = config_content.find(key_prefix) + len(key_prefix)
        key_end_index = config_content.find("\"", key_start_index)
        if key_end_index != -1:
            key = config_content[key_start_index:key_end_index]
        else:
            print("Error: Key value not properly formatted in config file.")
            return
    else:
        print("Error: PERMUTATION_KEY not found in config file.")
        return
    permutation_key = key
    # Encrypt the text with permutation cipher    
    encrypted_text = permutation_cipher(text, permutation_key, 'encrypt')
    print("Encrypted text:", encrypted_text)
    print("Length of encrypted text:", len(encrypted_text))
    print("--------------------------------------------------------")
    # Decrypt the text
    decrypted_text = permutation_cipher(encrypted_text, permutation_key, 'decrypt')
    print("Decrypted text:", decrypted_text)
    print("Length of decrypted text:", len(decrypted_text))
    print("---------------------------------------------------------") 

    key_prefix = "PERMUTATION_KEY2 = \""
    if key_prefix in config_content:
        key_start_index = config_content.find(key_prefix) + len(key_prefix)
        key_end_index = config_content.find("\"", key_start_index)
        if key_end_index != -1:
            key = config_content[key_start_index:key_end_index]
        else:
            print("Error: Key value not properly formatted in config file.")
            return
    else:
        print("Error: PERMUTATION_KEY not found in config file.")
        return
    permutation_key2 = key
    # Encrypt the text with double permutation cipher    
    encrypted_text = double_permutation_cipher(text, permutation_key, permutation_key2, 'encrypt')
    print("Encrypted text with double permutation cipher:", encrypted_text)
    print("Length of encrypted text:", len(encrypted_text))
    print("--------------------------------------------------------")
    # Decrypt the text
    decrypted_text = double_permutation_cipher(encrypted_text, permutation_key, permutation_key2, 'decrypt')
    print("Decrypted text:", decrypted_text)
    print("Length of decrypted text:", len(decrypted_text))
    print("---------------------------------------------------------") 

if __name__ == "__main__":
    main()

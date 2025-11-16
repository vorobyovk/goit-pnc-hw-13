import task1

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

def table_cipher(text, key, mode='encrypt'):
    key = key.upper()
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    num_columns = len(key)

    if mode == 'encrypt':
        # Step 1: Prepare the text and table dimensions
        #text = text.upper().replace(" ", "")
        text = "".join(char for char in text.upper() if char.isalnum() or char.isspace())
        num_rows = (len(text) + num_columns - 1) // num_columns
        padding_len = num_rows * num_columns - len(text)
        text += 'X' * padding_len

        # Step 2: Fill the table
        matrix = [list(text[i * num_columns:(i + 1) * num_columns]) for i in range(num_rows)]

        # Step 3: Read the ciphertext
        encrypted_text = ""
        for col_index in key_order:
            for row in range(num_rows):
                encrypted_text += matrix[row][col_index]
        return encrypted_text

    elif mode == 'decrypt':
        # Step 1: Determine table dimensions
        #num_rows = len(text) // num_columns
        num_rows = (len(text) + num_columns - 1) // num_columns

        # Step 2: Prepare the table
        matrix = [['' for _ in range(num_columns)] for _ in range(num_rows)]
        
        # Step 3: Fill the table column by column based on the key order
        index = 0
        for col_index in key_order:
            for row in range(num_rows):
                matrix[row][col_index] = text[index]
                index += 1

        # Step 4: Read the original text
        decrypted_text = ""
        for row in range(num_rows):
            decrypted_text += "".join(matrix[row])

        # Step 5: Remove padding
        decrypted_text = decrypted_text.rstrip('X')
        return decrypted_text
    else:
        raise ValueError("Invalid mode. Choose 'encrypt' or 'decrypt'.")
        
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
    key_prefix = "TABLE_KEY = \""
    if key_prefix in config_content:
        key_start_index = config_content.find(key_prefix) + len(key_prefix)
        key_end_index = config_content.find("\"", key_start_index)
        if key_end_index != -1:
            key = config_content[key_start_index:key_end_index]
        else:
            print("Error: Key value not properly formatted in config file.")
            return
    else:
        print("Error: TABLE-KEY not found in config file.")
        return    
    table_key = key
    
    # Extract key from config content
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
        print("Error: TABLE-KEY not found in config file.")
        return    
    table_key2 = key

    # Encrypt the text
    encrypted_text = table_cipher(text, table_key, 'encrypt')
    print("Encrypted text:", encrypted_text)
    print("Length of encrypted text:", len(encrypted_text))
    print("---------------------------------------------------------")
    # Decrypt the text      
    decrypted_text = table_cipher(encrypted_text, table_key, 'decrypt')
    print("Decrypted text:", decrypted_text)
    print("Length of decrypted text:", len(decrypted_text))
    print("---------------------------------------------------------")
    # Encrypt the text with double cipher (Vigenere + Table)
    veginer_text= task1.vigenere_cipher(text, table_key, 'encrypt')
    double_encrypted_text = table_cipher(veginer_text, table_key2, 'encrypt')
    print("Double Encrypted text:", double_encrypted_text)
    print("Length of double encrypted text:", len(double_encrypted_text))
    print("---------------------------------------------------------")
    # Decrypt the text with double cipher (Table + Vigenere)
    table_decrypted_text = table_cipher(double_encrypted_text, table_key2, 'decrypt')
    double_decrypted_text = task1.vigenere_cipher(table_decrypted_text, table_key, 'decrypt')
    print("Double Decrypted text:", double_decrypted_text)
    print("Length of double decrypted text:", len(double_decrypted_text))
    

if __name__ == "__main__":
    main()
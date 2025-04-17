import math
import os
import sys
import hashlib

def encode_file_to_ppm(input_path):
    with open(input_path, "rb") as f:
        data = f.read()

    nb_pixels = math.ceil(len(data) / 3)
    size = math.ceil(math.sqrt(nb_pixels))
    width, height = size, size

    header = f"P6\n{width} {height}\n255\n".encode()

    pixels = bytearray()
    i = 0
    for _ in range(width * height):
        r = data[i] if i < len(data) else 0
        g = data[i+1] if i+1 < len(data) else 0
        b = data[i+2] if i+2 < len(data) else 0
        pixels.extend([r, g, b])
        i += 3

    output_filename = os.path.splitext(input_path)[0] + "_encoded.ppm"
    with open(output_filename, "wb") as f:
        f.write(header)
        f.write(pixels)

    print(f"[+] Fichier encodé en image : {output_filename}")
    return output_filename

def decode_ppm_to_file(ppm_path, original_filename):
    with open(ppm_path, "rb") as f:
        content = f.read()

    header_end = content.find(b'\n', content.find(b'\n', content.find(b'\n') + 1) + 1) + 1
    pixel_data = content[header_end:]

    original_data = bytearray(pixel_data).rstrip(b'\x00')

    reconstructed_path = os.path.splitext(original_filename)[0] + "_reconstructed" + os.path.splitext(original_filename)[1]
    with open(reconstructed_path, "wb") as f:
        f.write(original_data)

    print(f"[+] Fichier reconstruit : {reconstructed_path}")
    return reconstructed_path

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def compare_files(path1, path2):
    hash1 = file_hash(path1)
    hash2 = file_hash(path2)

    print(f"Hash original      : {hash1}")
    print(f"Hash reconstruit   : {hash2}")

    if hash1 == hash2:
        print("[✔] Vérification réussie : les fichiers sont identiques.")
        return True
    else:
        print("[✘] Échec : les fichiers sont différents.")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage : python encode_decode_ppm.py <fichier_à_encoder>")
        sys.exit(1)

    original_file = sys.argv[1]

    # Étape 1 : encodage
    ppm_file = encode_file_to_ppm(original_file)

    # Étape 2 : décodage
    reconstructed_file = decode_ppm_to_file(ppm_file, original_file)

    # Étape 3 : vérification
    compare_files(original_file, reconstructed_file)

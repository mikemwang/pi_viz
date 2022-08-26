import lut

with open("rotation_matrix.py", 'w') as f:
    for value in lut.ROTATION_MATRIX:
        f.write(f"{value},")
from ansys.mapdl import core as pymapdl
from pathlib import Path


input_script_lgw = Path("C:/00_biaxial_buckling_analysys/PythonFURG/Projeto_Final_Python/flambagem_placa.lgw")

output_converted_dirty_script = Path("C:/00_biaxial_buckling_analysys/PythonFURG/Projeto_Final_Python/flambagem_placa_dirty.py")
output_converted_cleaned_script = Path("C:/00_biaxial_buckling_analysys/PythonFURG/Projeto_Final_Python/flambagem_placa_cleaned.py")

converte_lgw_pymapdl = pymapdl.convert_script(input_script_lgw, f'{output_converted_dirty_script}')

cds = open(output_converted_dirty_script)
for line in cds:
    if line.startswith("#") or line.strip() == '':
        continue
    else:
        cleaned_script = open(file=output_converted_cleaned_script, mode='a')
        cleaned_script.write(line)
        cleaned_script.close()

cds.close()

from ansys.mapdl.core import launch_mapdl
from pathlib import Path

a = 2000  # mm
b = 1000  # mm
t = 20  # mm
E = 200000  # N/mm²
poisson = 0.3
tensao_escoamento = 355  # N/mm²
carga_escoamento = tensao_escoamento * t

carga_x = 1   # N/mm
carga_y = 1   # N/mm


def mesh_convergency_test(mesh_size):
    mapdl = launch_mapdl(loglevel="WARNING", print_com=True)
    mapdl.run("WPSTYLE,,,,,,,,0")
    mapdl.title(f'teste_convergencia_malha_{mesh_size}mm')
    mapdl.prep7()
    mapdl._run("/NOPR")
    mapdl.keyw("PR_SET", 1)
    mapdl.keyw("PR_STRUC", 1)
    mapdl.keyw("PR_THERM", 0)
    mapdl.keyw("PR_FLUID", 0)
    mapdl.keyw("PR_ELMAG", 0)
    mapdl.keyw("MAGNOD", 0)
    mapdl.keyw("MAGEDG", 0)
    mapdl.keyw("MAGHFE", 0)
    mapdl.keyw("MAGELC", 0)
    mapdl.keyw("PR_MULTI", 0)
    mapdl.run("/GO")
    mapdl.et(1, "SHELL281")
    mapdl.mptemp("", "", "")
    mapdl.mptemp(1, 0)
    mapdl.mpdata("EX", 1, "", f'{E}')
    mapdl.mpdata("PRXY", 1, "", f'{poisson}')
    mapdl.run("sect,1,shell")
    mapdl.secdata(f'{t}', 1, 0.0, 3)
    mapdl.secoffset("MID")
    mapdl.seccontrol("", "", "", "", "", "")
    mapdl.rectng(0, f'{a}', 0, f'{b}')
    mapdl.run("/UI,MESH,OFF")
    mapdl.aesize("ALL", f'{mesh_size}')
    mapdl.mshape(0, "2D")
    mapdl.mshkey(0)
    mapdl.cm("_Y", "AREA")
    mapdl.asel("", "", "", 1)
    mapdl.cm("_Y1", "AREA")
    mapdl.chkmsh("AREA")
    mapdl.cmsel("S", "_Y")
    mapdl.amesh("_Y1")
    mapdl.cmdele("_Y")
    mapdl.cmdele("_Y1")
    mapdl.cmdele("_Y2")
    mapdl.finish()
    mapdl.run("/SOL")
    mapdl.pstres(1)
    mapdl.flst(2, 4, 4, "ORDE", 2)
    mapdl.fitem(2, 1)
    mapdl.fitem(2, -4)
    mapdl.run("/GO")
    mapdl.dl("P51X", "", "UZ", 0)
    mapdl.flst(2, 1, 3, "ORDE", 1)
    mapdl.fitem(2, 1)
    mapdl.run("/GO")
    mapdl.dk("P51X", "", 0, "", 0, "UX", "UY", "", "", "")
    mapdl.flst(2, 1, 3, "ORDE", 1)
    mapdl.fitem(2, 2)
    mapdl.run("/GO")
    mapdl.dk("P51X", "", 0, "", 0, "UY", "", "", "", "")
    # Carga paralela a x
    mapdl.flst(2, 2, 4, "ORDE", 2)
    mapdl.fitem(2, 2)
    mapdl.fitem(2, 4)
    mapdl.run("/GO")
    mapdl.sfl("P51X", "PRES", f'{carga_x}')
    # Carga paralela a y - DESLIGADO PARA COMPARAR
    mapdl.flst(2, 2, 4, "ORDE", 2)
    mapdl.fitem(2, 1)
    mapdl.fitem(2, 3)
    mapdl.run("/GO")
    mapdl.sfl("P51X", "PRES", f'{carga_y}')
    mapdl.solve()
    mapdl.finish()
    mapdl.run("/SOLU")
    mapdl.run("ANTYPE,1")
    mapdl.bucopt("LANB", 1, 0, 0, "CENTER")
    mapdl.mxpand(1, 0, 0, 0, 0.001)
    print(mapdl.solve())
    mapdl.finish()
    mapdl.run("/POST1")
    mapdl.set("LIST", 999)
    mapdl.set("", "", "", "", "", "", 1)
    print(f'Tamanho de malha: {mesh_size} mm')
    print(mapdl.run('*GET, E_COUNT, ELEM,,COUNT'))
    output = "C:/00_biaxial_buckling_analysys/PythonFURG/Projeto_Final_Python/arquivos_simulacoes"
    if Path.is_dir(Path(output)):
        pass
    else:
        Path.mkdir(Path(output))
    pasta_resultados = Path(output)
    mapdl.save(fname=f'{pasta_resultados}/teste_convergencia_malha_{mesh_size}mm', ext='DB', slab='ALL') 
    mapdl.exit()


tam_malha = [200, 100, 50, 20, 17.5, 15]

for tm in tam_malha:
    mesh_convergency_test(tm)

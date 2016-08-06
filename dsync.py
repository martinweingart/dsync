#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import stat, remove, walk, path, listdir, rmdir, makedirs
from shutil import copy2
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Sincroniza dos carpetas')
    parser.add_argument('fuente', metavar='src',
                        help='Carpeta fuente')
    parser.add_argument('destino', metavar='dest',
                        help='Carpeta destino')
    parser.add_argument("-v", "--verbose", help="Ver detalles de acciones",
                        action="store_true")
    parser.add_argument("-a", "--add", help="Agregar archivos que faltan",
                        action="store_true")
    parser.add_argument("-u", "--update", help="Actualizar archivos modificados",
                        action="store_true")
    parser.add_argument("-f", "--force", help="Eliminar archivos en la carpeta destino que no están en carpeta fuente",
                        action="store_true")
    args = parser.parse_args()

    # the two directories to sync
    srcDir = args.fuente
    destDir = args.destino


    if (not(args.add or args.force or args.update) or args.add or args.update):
        #Copio archivos que no existen en destino y actualizo si son diferentes
        for root, dirs, files in walk(srcDir):
            for file in files:
                pathFileSrc = path.join(path.abspath(root), file)
                pathFileDest = path.join(path.abspath(root.replace(srcDir,destDir)), file)
                if not path.isfile(pathFileDest):
                    if (args.add or not (args.force or args.update)):
                        if args.verbose:
                            print "Copiando archivo " + pathFileSrc + "..."
                        if not path.exists(path.abspath(root.replace(srcDir,destDir))):
                            makedirs(path.abspath(root.replace(srcDir,destDir)))
                        copy2(pathFileSrc, pathFileDest)
                else:
                    if (args.update or not (args.force or args.add)):
                        if (str(stat(pathFileSrc).st_mtime) <> str(stat(pathFileDest).st_mtime)):
                            if args.verbose:
                                print "Actualizando archivo " + pathFileDest + "..."
                            copy2(pathFileSrc, pathFileDest)


    if (args.force or not (args.update or args.add)):
        #Elimino archivos que no existen en fuente
        for root, dirs, files in walk(destDir):
            for file in files:
                pathFileSrc = path.join(path.abspath(root), file)
                pathFileDest = path.join(path.abspath(root.replace(destDir,srcDir)), file)
                if not path.isfile(pathFileDest):
                    if args.verbose:
                        print "Eliminando archivo " + pathFileSrc + "..."
                    remove(pathFileSrc)

        #Elimino carpetas vacias en destino
        dirDeleted = True
        #Si borro aguna carpeta vuelvo a repetir por si hay una nueva carpeta vacía
        while(dirDeleted):
            dirDeleted = False
            for root, dirs, files in walk(destDir):
                for dir in dirs:
                    pathDirSrc = path.join(path.abspath(root), dir)
                    if not listdir(pathDirSrc):
                        if args.verbose:
                            print "Eliminando carpeta vacía " + pathDirSrc + "..."
                        rmdir(pathDirSrc)
                        dirDeleted = True

    print "Sincronización finalizada!"

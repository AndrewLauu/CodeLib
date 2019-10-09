# -*- coding: UTF-8 -*-
import os
import shutil
import sys
import time

import openpyxl as pyxl
import progressbar as p
import xlrd
from progressbar import Bar


def main():
    srcDir = input("Insert path where the excel files to be merged exist: ")
    if not os.path.isdir(srcDir):
        raise FileNotFoundError('Not a valid path', srcDir)
    dstFile = input("Insert path where to put the dst file, or where the dst file is: ")
    pattern = input(
        'Insert nHead lines and nFoot lines lines with comma as delimiter("2,2" or "2," or ",2"): ').replace('，', ',')
    # print(f'{pattern=}')
    nHead, nFoot = [int(i) if i else 0 for i in pattern.split(',')] if pattern else (0, 0)
    merge(srcDir=srcDir, dstDir=dstFile, nHead=nHead, nFoot=nFoot)


def merge(srcDir: str = None, dstDir: str = 'merge.xlsx', nHead: int =1, nFoot: int = 0, extraArea: str = None,
          minCol: int = None, maxCol: int = None, rename: bool = False):
    """
    :param srcDir: Path where the excel files to be merged exist.
    :param dstDir: Path where to put the dst file, or where the dst file is
    :param nHead: Head line number
    :param nFoot: nFoot line number
    :param extraArea: Additional area in nHead, nFooter or content to give extra information with comma as delimiter.
    Use *name for filename.
    :parm minCol: start column to merge, from 1 insteading of 0
    :parm maxCol: end column to merge, from 1
    :parm rename: Whether to rename the file merged
    """

    # loop dir
    xlFiles = []
    nPass = 0
    for root, dirs, files in os.walk(srcDir):
        for f in files:
            # EXT = f.split('.')[-1].lower()
            # path = os.path.join(root, f)
            if "xls" in f.split('.')[-1].lower():
                xlFiles.append(os.path.join(root, f))
            else:
                nPass += 1

    if xlFiles:
        nXlFiles = len(xlFiles)
        maxDirLen = len(max(xlFiles, key=len))
        print(f'Establish dir tree, found {nXlFiles} files to be merged and {nPass} non-Excel files passed.')
    else:
        raise FileNotFoundError(srcDir, 'has no file.')

    # open dst Excel
    # Got a dir, copy the last src file to there as a dst
    # Got nothing, copy the last src file to *desktop* as a dst
    
    if not os.path.isfile(dstDir):
        testFile = xlFiles.pop()
        if os.path.isdir(dstDir):
            dstDir = os.path.join(dstDir, 'mergedExcel.xlsx')
        else:
            dstDir = os.path.join('./',dstDir
                    )
        try:
            shutil.copy2(testFile, dstDir)
        except shutil.SameFileError:
            os.remove(dstDir)
            shutil.copy2(testFile, dstDir)
        print(f'No dst file specified, copied an existing file: {testFile} to {dstDir} as a dst file.')
    

    # Load dst workbook.
    print('Loading dst workbook...')
    dstBook = pyxl.load_workbook(dstDir)
    dstSheet = dstBook.active
    nTargetRow = dstSheet.max_row
    # Copy nFoot line and paste when all src files were merged.
    if nFoot:
        footContent = dstSheet.iter_rows(min_row=nTargetRow - nFoot + 1, values_only=True)
        dstSheet.delete_rows(nTargetRow - nFoot + 1, amount=nFoot)
    else:
        footContent = []

    # loop src Excel
    w = [
        p.Percentage(), ' ', p.Counter(), f'/{nXlFiles}',
        Bar(left=" |", right='| ', marker=">", fill="-"),
        p.ETA(), ' ', p.Variable('Progressing', width=maxDirLen, precision=maxDirLen)
        ]
    # if extraArea != '*name':
    #     # noinspection PyUnresolvedReferences
    #     extraArea = xl.utils.range_to_tuple('sheet1!' + extraArea)[:1]

    with p.ProgressBar(widgets=w, max_value=nXlFiles, redirect_stdout=True) as bar:
        for xl in xlFiles:
            bar.update(value=xlFiles.index(xl), Progressing=xl)

            if xl.split('.')[-1] == 'xls':
                newRow = xlsRD(xl, minCol=minCol, maxCol=maxCol, nHead=nHead, nFoot=nFoot)
            else:
                newRow = xlsxRD(xl, minCol=minCol, maxCol=maxCol, nHead=nHead, nFoot=nFoot)
            for row in newRow:
                # newRow = [cell.value for cell in row]
                dstSheet.append(row)
            if rename:
                os.rename(xl, xl.replace('.xls', '-done.xls'))

    for row in footContent:
        dstSheet.append(row)
    # time.sleep(0.2)
    # sys.stdout.flush()
    print(f'Finished all src files; saving to {dstDir}...')
    dstBook.save(dstDir)


def xlsRD(srcFp, nHead, nFoot, minCol=None, maxCol=None):
    minCol = minCol - 1 if minCol else None
    maxCol = maxCol - 1 if maxCol else None

    srcBook = xlrd.open_workbook(srcFp)
    srcSheet = srcBook.sheet_by_index(0)
    nSrcRow = srcSheet.nrows
    content = [
        srcSheet.row_values(rowx=i, start_colx=minCol, end_colx=maxCol)
        for i in range(nHead, nSrcRow - nFoot)
        ]
    return content


def xlsxRD(srcFp, nHead, nFoot, minCol=None, maxCol=None):
    srcBook = pyxl.load_workbook(srcFp, read_only=True)
    srcSheet = srcBook.active
    nSrcRow = srcSheet.max_row
    content = srcSheet.iter_rows(min_row=nHead + 1, max_row=nSrcRow - nFoot, values_only=True,
                                 min_col=minCol, max_col=maxCol)
    return content


if __name__ == '__main__':
    main()

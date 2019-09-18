import os
import shutil

import openpyxl as xl
import progressbar as p
from progressbar import Bar


def main():
    originDir = input("Insert path where the excel files to be merged exist: ")
    if not os.path.isdir(originDir):
        raise FileNotFoundError('Not a valid path', originDir)
    targetFile = input("Insert path where to put the target file, or where the target file is: ")
    format = input('Insert header lines and foot lines lines with comma as delimiter("2,2" or "2," or ",2"): ')
    header, foot = [int(i) if i else 0 for i in format.split(',')]
    merge(originDir=originDir, targetDir=targetFile, header=header, foot=foot)


def merge(originDir: str = None, targetDir: str = None, header: int = 2, foot: int = None):
    """
    :param originDir: Path where the excel files to be merged exist.
    :param targetDir: Path where to put the target file, or where the target file is
    :param header: Head line number
    :param foot: Foot line number
    """
    # Get origin files in all folders.
    xlsxFiles = []
    xlsFile=[]
    passed=[]

        footContent = []

    # loop dir
    for root, dirs, files in os.walk(originDir):
        for f in files:
            EXT=os.path.splitext(f).lower()
            if EXT == 'xlsx':
                #mergeXlsx(path,targetWS)
                xlsxFiles.append(os.path.join(root, f))
            elif EXT== 'xls':
                # xls use xlrd
                # FIXME
                xlsFiles.append(os.path.join(root, f))
                pass
            else:
                passed.append(os.path.join(root, f))

    if xlsxFiles or xlsFiles:
        nFiles = len(xlsxFiles)+len(xlsFiles)
        print(f'Establish dir tree, found {nFiles} files to be merged')
        if passed:
            print('Pass following file(s) for not being Excel file:\n','\n'.join(passed))
        if xlsFiles:
            import xlrd
    else:
        raise FileNotFoundError(originDir, 'has no file.')

    # Got a dir, copy the last origin file to there as a target
    # Got nothing, copy the last origin file to desktop as a target
    if not os.path.isfile(targetDir):
        testFile = xlsxFiles.pop()
        if os.path.isdir(targetDir):
            targetDir = os.path.join(targetDir, os.path.basename(testFile))
        else:
            targetDir = os.path.join('D:\\Desktop', os.path.basename(testFile))
        shutil.copy2(testFile, targetDir)
        print(f'No target file specified, moved an existing file: {testFile} to {targetDir} as a target file.')

    # Load target workbook.
    print('Loading target workbook...')
    targetWB = xl.load_workbook(targetDir)
    targetWS = targetWB.active
    nTargetRow = targetWS.max_row
    ## Copy foot line and paste when all origin files were merged.
    if foot:
        footContent = targetWS.iter_rows(min_row=nTargetRow - foot + 1)
        targetWS.delete_rows(nTargetRow - foot + 1, amount=foot)
    else:

    maxDirLen = len(max(xlsxFiles, key=len))
    w = [
        p.Percentage(), ' ', p.Counter(), f'/{nFiles}',
        Bar(left=" |", right='| ', marker=">", fill="-"),
        p.ETA(), ' ', p.DynamicMessage('Progressing', width=maxDirLen, precision=maxDirLen)
    ]
    with p.ProgressBar(widgets=w, max_value=nFiles) as bar:
        # Deal with *.xlsx
        for xlsxFile in xlsxFiles:
            bar.update(value=xlsxFiles.index(xlsxFile), Progressing=xlsxFile)
            originWB = xl.load_workbook(xlsxFile, read_only=True)
            originWS = originWB.active
            nOriginRow = originWS.max_row
            content = originWS.iter_rows(min_row=header + 1, max_row=nOriginRow - foot)
            # rawContent = [[cell.value for cell in row] for row in content]
            for row in content:
                newRow = [cell.value for cell in row]
                targetWS.append(newRow)

        # Deal with *.xls
        for xlsFile in xlsFiles 

    for row in footContent:
        footRow = [cell.value for cell in row]
        targetWS.append(footRow)
    print(f'Finished all files; saving to {targetDir}...')
    targetWB.save(targetDir)


if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-import os
import os
import winreg

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.pdf import PageObject

import logging
import sys

fileHandler = logging.FileHandler('PDFModifier.log', encoding='utf8')
fileHandler.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setLevel(logging.INFO)

# init root logger by setting basicConfig
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(module)s.%(funcName)s [%(levelname)s]: %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    handlers=[fileHandler, consoleHandler],
    encoding='utf8'
)

# Global logger for this module
logger: logging.Logger = logging.getLogger(__name__)


def callback_func(exc_type, exc_value, exc_traceback):
    logger.error('', exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = callback_func


def __split(pdfFile: PdfFileReader, interval: int, pageFrom: int = None, pageTo: int = None) -> list[PdfFileWriter]:
    """
    first page is 1
    :param pdfFile:
    :param interval:
    :param pageFrom:
    :param pageTo:
    :return:
    """
    nPdfPage: int = pdfFile.getNumPages()

    # check args
    if not pageFrom:
        pageFrom = 1
    if not pageTo:
        pageTo = nPdfPage
    nPage: int = pageTo - pageFrom + 1

    if not interval:
        interval = nPage
    elif interval >= nPage or interval <= 0:
        raise ValueError(f'Original PDF page {pageFrom} to {pageTo} has {nPdfPage} page(s), '
                         f'unable to split every {interval} pages.')

    if pageFrom > pageTo or pageTo > nPdfPage or pageFrom > nPdfPage:
        raise ValueError(f'Original PDF has {nPdfPage} page(s), unable to locate page {pageFrom} to {pageTo}.')

    part: int = (nPage - 1) // interval + 1

    pages: list = []
    # first page is 0
    for i in range(part):
        newPdfPart: PdfFileWriter = PdfFileWriter()

        nStart: int = i * interval + pageFrom - 1
        if i != part - 1:
            nStop: int = (i + 1) * interval + pageFrom - 1
        else:
            nStop = pageTo

        logger.info(f'( {i + 1} / {part}) Page {nStart + 1} - {nStop} -> file {i + 1}...')
        for pn in range(nStart, nStop):
            logger.debug(f'( {pn - pageFrom + 2} / {nPage}) Page {pn + 1} -> file {i + 1}...')
            newPdfPart.addPage(pdfFile.getPage(pn))

        pages.append(newPdfPart)
    return pages


def __writePdf(pdfPages: list[PdfFileWriter], saveDir: str = None, saveNames: list[str] = None, autoName: bool = True,
               baseName: str = 'result.pdf'):
    """
        Write pdf pages in *one* pdf file. Wrapped PyPdf2.PdfFileWriter

    :param pdfPages:
    :param saveDir:
    :param saveNames:
    :param autoName:
    :param baseName:
    :return:
    """

    if isinstance(pdfPages, list):
        pages: list = pdfPages
    elif isinstance(pdfPages, PageObject):
        pages = [pdfPages]
    else:
        raise TypeError(f'arg `pdfPage` expects PageObject or list[PageObject], {type(pdfPages)} was given')
    nFiles = len(pdfPages)

    saveDir = saveDir.strip('"\'') or desktopDir
    resultDir = os.path.join(saveDir, 'result')

    try:
        os.makedirs(resultDir)
    except FileExistsError:
        pass
        # following is original method to change auto increase save dir when exists. Bug difficult to fix
        # cnt: int = 1
        # while os.path.exists(resultDir):
        #     resultDir = os.path.join(saveDir, f'result_{cnt}')
        #     logger.debug(f'try to make {resultDir}')
        #     cnt += 1
        # logger.info(f'Not given save path or is inaccessible or is unable to make. '
        #             f'Save to {resultDir}.')
        # os.mkdir(resultDir)

    if saveNames and isinstance(saveNames, list):
        if len(saveNames) != nFiles:
            raise ValueError(f'{nFiles} files, but {len(saveNames)} names given.')
    elif autoName:
        saveNames = [f'{i}_{baseName}' for i in range(1, nFiles + 1)]
    else:
        raise ValueError('Arg `saveNames` not given or not list, however `autoName` was turn off.')

    cnt = 1
    for p, n in zip(pages, saveNames, strict=True):
        dstName = os.path.join(resultDir, n.lower().replace('.pdf', '') + '.pdf')
        logger.info(f'({cnt} / {nFiles}) Writing {n}...')
        with open(dstName, 'wb') as f:
            p.write(f)
        cnt += 1


def splitByInterval(filename: str, interval: int, saveDir: str = None) -> None:
    checkPath(filename, '.pdf')
    pdf: PdfFileReader = PdfFileReader(filename)
    basename: str = os.path.basename(filename)

    logger.info(f'Processing {basename}, splitting {interval} page(s) into each file...')
    group = __split(pdf, interval=interval)
    __writePdf(group, saveDir=saveDir, autoName=True, baseName=basename)


def splitByIntervalWithNames(filename: str, names: list[str], interval: int = 1, saveDir: str = ''):
    checkPath(filename, '.pdf')

    pdf = PdfFileReader(filename)
    basename: str = os.path.basename(filename)
    logger.info(f'Processing {basename}, splitting {interval} page(s) into each file...')

    group = __split(pdf, interval=interval)
    __writePdf(group, saveDir=saveDir, saveNames=names)


def splitByCsvWithConfig(csvPath: str, saveDir: str = None, strict=False):
    # csv format first page is 1
    # pdfPath pageFrom pageTo interval saveName
    #   /        1      100     20         /
    #   /        20      30     10         /
    # way 1 one pdf split into many:
    # way 2 many pdf to many each specify [auto name]:
    # way3 many pdf to many specify interval -> splitByCsv
    checkPath(csvPath, '.csv')

    csvRaw: str = open(csvPath, 'r', encoding='utf-8', errors='replace').read().strip('\ufeff').strip()
    csvLine: list[str] = csvRaw.split('\n')
    # remove header and sort by pdf path
    csvLine.pop(0)
    csvLine.sort()

    splitConfigDict: dict[str:list[dict[str:str]]] = {}
    failedRow: list[str] = []

    # csv -> dict
    for line in csvLine:
        rows: list = line.split(',')
        path = rows[0].strip().strip('"\'')
        if not checkPath(path, '.pdf', raiseErr=strict):
            errInfo = f'{csvLine.index(line)}, {line}'
            failedRow.append(errInfo)
            continue

        inner: dict = dict(zip(csvHeader[1:], rows[1:]))
        if path in splitConfigDict:
            splitConfigDict[path].append(inner)
        else:
            splitConfigDict[path] = [inner]

    logger.debug(f'Trans {len(csvLine)} csv lines to dict')

    if failedRow:
        logger.warning(f'{len(failedRow)} row(s) in csv failed to handle, '
                       f'infos are as follow:\n' + ';\n'.join(failedRow))

    # iter src PDF
    for pdfPath, config in splitConfigDict.items():
        basename: str = os.path.basename(pdfPath)
        fname: str = os.path.splitext(basename)[0]
        nConfig: int = len(config)
        names: list[str] = []
        if nConfig == 1:
            autoName: bool = True
        else:
            autoName = False
            names = [f'{i + 1}_{basename}' for i in range(nConfig)]
        logger.info(f'Processing {basename}, {nConfig} configs to it, {autoName=}, {names=}...')

        pdf = PdfFileReader(pdfPath)
        # iter split PDF
        for con in config:
            nFrom: int = int(con['pageFrom']) if con['pageFrom'] else None
            nTo: int = int(con['pageTo']) if con['pageTo'] else None
            interval: int = int(con['interval']) if con['interval'] else None

            saveDir = saveDir or con['savePath'].strip().strip('"\'') or desktopDir
            resultDir = os.path.join(saveDir, fname)

            logger.info(f'Processing page {nFrom}->{nTo} in {basename}, '
                        f'splitting {interval} page(s) into each file...')

            resultWriter: list[PdfFileWriter] = __split(pdf, interval=interval, pageFrom=nFrom, pageTo=nTo)
            __writePdf(resultWriter, saveDir=resultDir, autoName=autoName, baseName=basename,
                       saveNames=None if autoName else [names.pop(0)])


def checkPath(path: str | os.PathLike, ext: str, raiseErr=True) -> bool | None:
    check: bool = True
    ext = '.' + ext.lstrip('.').lower()
    path = path.strip().strip('"\'')

    if path.startswith('"') or path.startswith("'"):
        logger.warning(f'{path=} is wrapper in quoters.')

    if not os.path.isfile(path):
        msg = f'{path} do not exist!'
        if raiseErr:
            raise FileNotFoundError(msg)
        check = False
        logger.warning(msg)

    if os.path.splitext(path)[-1].lower() != ext:
        msg = f'{path} is not a *{ext} file!'
        if raiseErr:
            raise ValueError(msg)
        check = False
        logger.warning(msg)

    logger.debug(f'{path=}, {ext=}, {raiseErr=}, check pass.')
    return check


def rotate(dirOrPath: str | list[str], angle: int = 90, saveDir: str = ''):
    # accept one filename or dir or list of names
    # dirOrPath = list[filename | dir] | filename | dir
    # todo ? keep original file structure
    testPath: list[str] = []
    # testPath = [filename... | dir...]
    if isinstance(dirOrPath, list):
        # list of names
        testPath += dirOrPath
    elif isinstance(dirOrPath, str):
        # name or dir
        testPath.append(dirOrPath)
    else:
        raise TypeError(f'arg `filenames` expects filename(s) or dir path, {type(dirOrPath)} was given')
    logger.debug(f'Rotate {len(testPath)} file(s) or dir(s), {angle=}, {saveDir=}')

    filenames: list[str] = []
    for p in testPath:
        if os.path.isdir(p):
            for root, _, files in os.walk(p):
                if files:
                    filenames += [os.path.join(root, f) for f in files
                                  if os.path.splitext(f)[-1].lower() == '.pdf']
        elif os.path.isfile(p):
            filenames.append(p)
    if not filenames:
        raise FileNotFoundError('Files not given')

    dstPDFs: list[PdfFileWriter] = []
    saveNames: list[str] = []
    for f in filenames:
        basename = os.path.basename(f)
        logger.info(f'( {len(dstPDFs) + 1} / {len(filenames)}) Processing {basename}...')
        srcPDF = PdfFileReader(f)
        n = srcPDF.getNumPages()

        dstPDF = PdfFileWriter()
        saveNames.append(f'rotate_{basename}')

        for i in range(n):
            logger.info(f'Rotating {basename}, page {i + 1} / {n}...')
            p = srcPDF.getPage(i).rotateClockwise(int(angle))
            dstPDF.addPage(p)
        dstPDFs.append(dstPDF)
    __writePdf(dstPDFs, saveDir, saveNames, autoName=False)


def main():
    banner: list[str] = [
        '=' * 30,
        'PDF Split Tool',
        'Support following methods:',
        '-' * 20,
        '[1] Split every given interval number of page(s) into new pdf file',
        '     e.g. 1,2 // 3,4 // 5,6 ... ;',
        '[2] Split by csv file (only names) and name each pdf file by corresponding csv row;',
        '[3] Split by csv file, advanced method;',
        '[4] Rotate pdf pages;',
        '[5] Split every given interval number of page(s) into new pdf file, with name given',
        '=' * 30
    ]
    print('\n'.join(banner))

    # define vars
    pdfPath, csvPath, interval, saveDir, names = '', '', 0, '', []

    mode: str = input('Choose method no, e.g. 1: ').strip().strip('[]')
    logger.debug(f'User input {mode=}')
    if mode not in ['1', '2', '3', '4', '5']:
        raise ValueError(f'Mode {mode} is not supported.')

    if mode in ['1', '2', '5']:
        pdfPath: str = input('Input original PDF file path: ').strip().strip('"\'')
        logger.debug(f'User input {pdfPath=}')

        # check pdf file exists
        checkPath(pdfPath, '.pdf', raiseErr=True)

        path = os.path.dirname(pdfPath)
        os.chdir(path)
        logger.debug(f'Now cwd at {os.getcwd()}')

        interval: int = int(input('Input interval, every () page(s) in new pdf file: ').strip())
        logger.debug(f'User input {interval=}')

    if mode == '2':
        csvPath: str = input('Input csv file path, do not include title in csv file : '
                             ).strip().strip('"\'')
        logger.debug(f'User input {csvPath=}')

    if mode in ['4', '5']:
        stopWord = ''
        print('input names each in a line, press enter to stop: ')
        for line in iter(input, stopWord):
            names += line.strip().split('\n')
        names = [name.strip('"\'') for name in names]

    saveDir: str = input(f'Input destination dir, press enter to save at desktop: ').strip().strip('"\'')
    logger.debug(f'User input {saveDir=}')

    match mode:
        case '1':
            splitByInterval(pdfPath, interval, saveDir)
        case '2':
            checkPath(csvPath, '.csv')
            names: list[str] = open(csvPath, 'r', encoding='utf-8',
                                    errors='replace').read().strip().strip('\ufeff').split('\n')
            splitByIntervalWithNames(pdfPath, names, interval, saveDir)
        case '3':
            export = input('Export csv template? Y/n')
            logger.debug(f'User input {export=}')

            if export in 'Yy':
                templatePath = os.path.join(desktopDir, 'template.csv')
                with open(templatePath, 'w') as f:
                    f.write(','.join(csvHeader) + '\n')
                    f.write(','.join([
                        '"Path to pdf file"',
                        '"Starting page index, default as the first page when omitted"',
                        '"End page index, default as the last page when omitted"',
                        '"Every () page(s) in new pdf file'
                        'default as PageTo-pageFrom+1 when omitted"',
                        '"Save path, omissible when input in cmd, '
                        'fallback to desktop when both cmd and csv are omitted"'
                    ]))
                logger.info(f'Template export to {templatePath}.')
            csvPath: str = input('Input csv file path, include title in csv file : ').strip().strip('"\'')
            logger.debug(f'User input {csvPath=}')
            checkPath(csvPath, '.csv')
            splitByCsvWithConfig(csvPath=csvPath, saveDir=saveDir)

        case '4':
            logger.debug(f'User input {names=}')
            angle: int = int(input('Input rotate angle, 90 or +90 for clockwise 90°, '
                                   '-90 for counterclockwise 90° ').strip() or 90)
            logger.debug(f'User input {angle=}')
            rotate(names, angle, saveDir)

        case '5':
            logger.debug(f'User input {names=}')
            splitByIntervalWithNames(pdfPath, names, interval, saveDir)


# global var
csvHeader = ['pdfPath', 'pageFrom', 'pageTo', 'interval', 'savePath']
regKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                        'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
desktopDir = winreg.QueryValueEx(regKey, "Desktop")[0]

if __name__ == '__main__':
    logger.debug('init from __main__')
    main()
    logger.info('Finished.')

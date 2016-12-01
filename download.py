#!/usr/bin/env python
# coding:utf-8

import os
import json
import datetime
import time
import multiprocessing
import subprocess
import sys
import logging

# set logging
logfile = os.path.join(os.path.dirname(__file__), 'log.log')
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M',
    filename=logfile,
    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s: %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
FTPloger = logging.getLogger('FTPDownload')
NAVloger = logging.getLogger('NAVDownload')


def date2doy():
    now = datetime.datetime.now()
    return now.year, now.timetuple().tm_yday


class FTP(object):
    def __init__(self, ftp, filename, storepath):
        self.ftp = ftp
        self.filename = filename
        self.storepath = storepath

    def download(self):
        if not os.path.exists(self.storepath):
            FTPloger.warning('Not find storpath:%s' % self.storepath)
            try:
                os.makedirs(self.storepath)
                FTPloger.info('Make %s successfully!' % self.storepath)
            except:
                FTPloger.error('Can not make %s' % self.storepath)
                logging.info('Script exited!')
                sys.exit()
        filepath = os.path.join(self.storepath, self.filename)
        wgetlog = os.path.join(os.path.dirname(__file__), 'wget.log')
        try:
            args = [
                'wget', '-c', '-t', '3', '-a', wgetlog, '-O', filepath,
                self.ftp
            ]
            p = subprocess.Popen(
                args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.communicate()
            FTPloger.info('Download %s successfully!' % self.filename)
            return 1
        except:
            FTPloger.warning('Download %s failed!' % self.filename)
            return 0


class Download(object):
    """Downlaod class."""

    def __init__(self):
        self.cfg = self._readcfg()

    def _readcfg(self):
        """Read confiugration file."""
        cfgpath = os.path.join(os.path.dirname(__file__), 'configure.json')
        try:
            with open(cfgpath) as f:
                cfg = json.load(f)
        except:
            logging.error('Read %s failed!' % cfgpath)
            logging.info('Script exited!')
            sys.exit()

        return cfg

    def download(self):
        # download nav
        for cfg in self.cfg['NAV'].values():
            p = multiprocessing.Process(target=self._downloadNav, args=(cfg, ))
            p.start()

    def _downloadNav(self, cfg):
        interval = cfg['interval']
        storepath = cfg['path']
        if not storepath or not interval:
            return
        while True:
            for ftp, yearflag, doyflag, navflag, zipflag in zip(
                    cfg['ftp'], cfg['year'], cfg['doy'], cfg['nav'],
                    cfg['zip']):

                year, doy = date2doy()
                brdcfile = 'brdc%03d0.%sn' % (doy, str(year)[-2:])
                if zipflag:
                    brdcfile += '.Z'
                ftp.rstrip('/')
                if yearflag:
                    ftp += '/' + str(year)
                if doyflag:
                    ftp += '/' + '%03d' % doy
                if navflag:
                    ftp += '/' + '%sn' % str(year)[-2:]
                ftp += '/' + brdcfile
                ftpsever = FTP(ftp, brdcfile, storepath)
                if not ftpsever.download():
                    continue
                brdcpath = os.path.join(storepath, brdcfile)
                if zipflag:
                    try:
                        subprocess.call(['gzip', brdcpath, '-d', '-f'])
                        NAVloger.info('Uncompress %s successfully!' % brdcfile)
                    except:
                        NAVloger.erro('Uncompress %s failed!' % brdcfile)
                        continue
                    brdcpath = brdcpath[:-2]
                if os.path.isfile(brdcpath) and os.path.getsize(brdcpath):
                    generator = cfg['generator']
                    if not os.path.exists(generator):
                        NAVloger.error('No generator!')
                        break
                    try:
                        subprocess.call(
                            [generator, storepath, str(year), str(doy)])
                    except:
                        NAVloger.error('Generator failed!')
                    break

            time.sleep(interval)


if __name__ == '__main__':
    download = Download()
    download.download()

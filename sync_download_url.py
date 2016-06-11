#!/usr/bin/env python

#http:// www.etsi.org / deliver/etsi_ts / 121100_121199 / 121101 / 11.01.00_60 / ts_121101v110100p.pdf
#http://     host     / ================================= file_path ==================================
#http://     host     / ================ version_path(_list) ===================
#http://     host     / ======== spec_number_path(_list) =========
#http://     host     / ======= series_path(_list) ======
#http://     host     / == etsi_type ==  

import time
import urllib2
import urllib
import re
import os

host = 'http://www.etsi.org/'
etsi_type_list = ('deliver/etsi_ts/', 'deliver/etsi_tr/')
series = range(21, 38)

def log(tag, data):
    if type(data) == list:
        data = '; '.join(data)

    print time.strftime('%Y-%m-%d %H:%M:%S  ', time.localtime(time.time())) + tag + '  ====  ' + data

def getHtml(url):
    # httpHandler = urllib2.HTTPHandler(debuglevel=1)
    # httpsHandler = urllib2.HTTPSHandler(debuglevel=1)
    # opener = urllib2.build_opener(httpHandler, httpsHandler)

    # urllib2.install_opener(opener)

    log('getHtml', 'open "' + url + '" start...')
    page = urllib2.urlopen(url)
    log('getHtml', 'open "' + url + '" end')

    log('getHtml', 'read "' + url + '" start...')
    html = page.read()
    log('getHtml', 'read "' + url + '" end')

    page.close()
    return html

def fetchAllFiles(etsi_type):
    # optimize: etsi_type just read once
    html = getHtml(host + etsi_type)

    for re_series_main in series:
        series_path_list = getAllSeriesList(html, etsi_type, re_series_main)
        if series_path_list == []:
            continue

        spec_number_path_list = getSpecNumListOfEachSeries(str(re_series_main), series_path_list)
        if spec_number_path_list == []:
            continue

        file_path_list = getFilePathList0fSpec(etsi_type, spec_number_path_list)

        # for file_path in file_path_list:
        #     retrieveFile(host + file_path, str(re_series_main) + '-series')

        file = open('url.txt', 'a')
        file.writelines([host+line+'\n' for line in file_path_list])
        file.close()

def getAllSeriesList(html, etsi_type, re_series_main):
    re_series_sub = '[0-9]{3}'

    re_series_full = '1' + str(re_series_main) + re_series_sub
    re_series_list = re.compile(etsi_type + re_series_full + '_' + re_series_full + '/')
    series_path_list = re.findall(re_series_list, html)
    
    #mkdir 21-series -p .ets
    if series_path_list != []:
        log('getAllSeriesList', series_path_list)
    
        if os.path.exists(str(re_series_main) + '-series') == False:
            os.mkdir(str(re_series_main) + '-series')
    else:
        #30-series is special
        log('getAllSeriesList', str(re_series_main) + '-series is None in ' + etsi_type)

    return series_path_list
    
def getSpecNumListOfEachSeries(re_series, series_path_list):
    spec_number_path_list = []

    for series_path in series_path_list:
        html = getHtml(host + series_path)
        # += include all of spec in list, because series may be deviced into serverl part
        spec_number_path_list += re.findall(series_path + '[0-9]{6,10}' + '/', html)

    if spec_number_path_list != []:
        log('getSpecNumListOfEachSeries', spec_number_path_list)
    else:
        log('getSpecNumListOfEachSeries', 'no spec in ' + re_series)

    return spec_number_path_list

def getFilePathList0fSpec(etsi_type, spec_number_path_list):
    file_path_list = []

    for spec_number_path in spec_number_path_list:
        latest_version = getLatestVersionOfSpec(spec_number_path)
        file_name = getFileNameOfLatestVersion(etsi_type, spec_number_path, latest_version)
        #virtual download indication
        #os.mknod(file_name)
        file_path = spec_number_path + latest_version + '/' + file_name
        file_path_list.append(file_path)
    
    log('getFilePathList0fSpec', file_path_list)

    return file_path_list

def getLatestVersionOfSpec(spec_number_path):
    latest_version_path = getLatestVersionPathOfSpec(spec_number_path)
    latest_version = getDirectory(spec_number_path, latest_version_path)

    log('getLatestVersionOfSpec', latest_version)

    return latest_version

def getLatestVersionPathOfSpec(spec_number_path):
    html = getHtml(host + spec_number_path)

    re_version = re.compile(spec_number_path + '[0-9]{2}\.[0-9]{2}\.[0-9]{2}_[0-9]{2}' + '/')
    version_path_list = re.findall(re_version, html)

    log('getLatestVersionPathOfSpec', max(version_path_list))

    return max(version_path_list)
    
def getDirectory(path_parent, path_sub):
    return (set(path_sub.split('/')) - set(path_parent.split('/'))).pop()

def getFileNameOfLatestVersion(etsi_type, spec_number_path, latest_version):
    spec_number = spec_number_path.split('/')[-2]
    # 121101 + 11.01.00_60 = ts_121101v110100p.pdf
    file_name = ('ts_' if etsi_type == 'deliver/etsi_ts/' else 'tr_') \
                + spec_number \
                + 'v' \
                + latest_version.replace('.', '').replace('_60', '') \
                + 'p.pdf'

    log('getFileNameOfLatestVersion', file_name)

    return file_name

def retrieveFile(file_full_path, save_to_directory):
    log('retrieveFile', 'retrieving ' + file_full_path + ' into ' + save_to_directory)

    file_local = save_to_directory + '/' + file_full_path.split('/')[-1]
    remote_file_size = get_remote_file_size(file_full_path)

    if os.path.exists(file_local) == True:
        if remote_file_size != str(os.path.getsize(file_local)):
            # if file is not downloaded 100%
            os.remove(file_local)
        else:
           log('retrieveFile', file_local + ' is already retrieved.') 
           return 
    
    urllib.urlretrieve(file_full_path, file_local)

    if remote_file_size != str(os.path.getsize(file_local)):
        log('retrieveFile', 'retrieve ' + file_full_path + ' failed!')
    else:
        log('retrieveFile', 'retrieve ' + file_full_path + ' finished!')

def get_remote_file_size(url, proxy=None):
    opener = urllib2.build_opener()

    if proxy:
        if url.lower().startswith('https://'):
            opener.add_handler(urllib2.ProxyHandler({'https' : proxy}))
        else:
            opener.add_handler(urllib2.ProxyHandler({'http' : proxy}))
    request = urllib2.Request(url)
    request.get_method = lambda: 'HEAD'
    
    try:
        response = opener.open(request)
        response.read()
    except Exception, e:
        print '%s %s' % (url, e)
    else:
        return dict(response.headers).get('content-length', 0)

def main():
    for etsi_type in etsi_type_list:
        log('main', 'Fetching ' + etsi_type + ' ...')

        fetchAllFiles(etsi_type)

    log('main', 'All is done!')

if __name__ == '__main__':
    main()

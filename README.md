# 3GPP_SPEC_DOWNLOAD

## 0. three download ways
 - sync_download.py:
Directly download the pdf file using *retrieveFile()* when get its url.
 - async_download.py:
Use ***multiprocessing*** module, call *enqueueFilePathList()* instead of *retrieveFile()* to apply async operation.
 - sync_download_url.py (recommended):
Just save all of pdf files' urls into **url.txt**, then you can download them by following steps, copying urls, opening download software tools, and making a bulk download task.

## 1. set series to download
For default setting, it will download pdf files from 21-series to 37-series:
```
series = range(21, 38)
```
Just change the series to what you want.

## 2.pdf file url schema
eg.
> 3GPP TS 21.101 version 11.1.0 Release 11
> http://www.etsi.org/deliver/etsi_ts/121100_121199/121101/11.01.00_60/ts_121101v110100p.pdf
> 
> 3GPP TR 29.998-04-1 version 9.0.0 Release 9
> http://www.etsi.org/deliver/etsi_tr/129900_129999/1299980401/11.01.00_60/tr_1299980401v090000p.pdf

 - *host*: www.etsi.org
 - *etsi_type*: deliver/etsi_ts & deliver/etsi_tr. Only two value.
 - *series*: 121100_121199, 129900_129999, etc. Single series may be deviced into serverl parts.
 - *spec_number*: 121101, 1299980401, etc. The specific spec number.
 - *version*: 11.01.00_60, etc. One spec may have serverl versions.
 - *file*: ts_121101v110100p.pdf, tr_1299980401v090000p.pdf, etc. Consist of etsi_type, spec_number and version.

note: I use *file_path* not *file* to represent the file in code, so there are some redundancy, which need to be optimized.
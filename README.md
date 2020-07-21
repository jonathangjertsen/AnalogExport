## Analog export

Saleae Logic analog measurement extension which exports analog data to "CSV", that is, one row of data per sample.
You can call `numpy.loadtxt` on the resulting file(s) to get the data out.

This provides a quick way to export short analog snippets without going through the usual export dialog box.

Since there is currently NO configurability available for analog measurements, the following behaviour is fixed:

* ALL measurements taken will be exported. If you plan on making large measurements that you do not intend to export,
  you should disable this plugin first.
* The data will exported to a subdirectory named "SaleaeAnalogExport/data" in your home directory.
* The filename will be "timestamp.txt.gz", where "timestamp" is replaced with the current Unix timestamp.
* The "exp_hint" measurement will contain the timestamp that was used to name the file.
* The "exp_status" measurement will be one of the following:
    * -2: Already exported, not re-exporting.
    * -1: The "measurement" was not requested.
    * 0: Data was successfully stored.
    * 1:  Some kind of OS error (e.g. permission denied) occurred.
    * 2:  Should not happen, indicates a silly programming error. Please save the capture and report a bug!

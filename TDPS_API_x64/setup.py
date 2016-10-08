from distutils.core      import setup
from distutils.sysconfig import get_python_lib
import sys
import os
import shutil

if __name__ == "__main__":

    destPath = os.path.normpath(get_python_lib())
    #
    # Do the distutils installation
    #
    setup(name         = "TDPS",
          version      = "1.1 (x64)",
          description  = "GTA data Interface",
          py_modules=['TDPS','Callback','DSPStruct'],
          platforms    = "Microsoft Windows",
          data_files   = [('',['lib/CompressLib.dll', 'lib/dbghelp.dll','lib/DspCurlApi.dll','lib/DSP_Util64.dll',
                            'lib/libcurl.dll', 'lib/libDspCompressorApi64.dll', 'lib/libDspProto64.dll',
                            'lib/libDspSession64.dll','lib/libeay32.dll', 'lib/libLogger64.dll', 'lib/libRedisProxy64.dll',
                            'lib/libSubManager64.dll','lib/libTDPSApi64.dll','lib/libXmlConfig64.dll', 'lib/log4cplus.dll',
                            'lib/msvcp100.dll', 'lib/msvcr100.dll','lib/NTKernel64.dll','lib/libDspRsaApi64.dll',
                            'lib/NTWrap64.dll',  'lib/ssleay32.dll', 'lib/zlibwapi.dll']),
		                  ('',['config/Tdps.xml','config/DSPSdk.xml','config/log_config_api.properties'])
                         ]
         )
#
# -------------------------------- End of file --------------------------------

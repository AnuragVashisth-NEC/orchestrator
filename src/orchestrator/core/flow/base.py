import logging

from orchestrator.core.keystone import IdMKeystoneOperations as IdMOperations
from orchestrator.core.keypass import AccCKeypassOperations as AccCOperations

logger = logging.getLogger('orchestrator_core')


class FlowBase(object):
    def __init__(self,
                 KEYSTONE_PROTOCOL,
                 KEYSTONE_HOST,
                 KEYSTONE_PORT,
                 KEYPASS_PROTOCOL=None,
                 KEYPASS_HOST=None,
                 KEYPASS_PORT=None):
        self.idm = IdMOperations(KEYSTONE_PROTOCOL, KEYSTONE_HOST, KEYSTONE_PORT)

        self.ac = AccCOperations(KEYPASS_PROTOCOL, KEYPASS_HOST, KEYPASS_PORT)


    def composeErrorCode(self, ex):
        '''
        Compose error detail and code from AssertionError exception ex
        '''
        # Get line where exception was produced
        #exc_type, exc_obj, exc_tb = sys.exc_info()
        #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        #print(exc_type, fname, exc_tb.tb_lineno)
        res = { "error": str(ex), "code": 400 }
        if isinstance(ex.message, tuple):  # Python 2.7
            res['code'] = ex.message[0]
        elif isinstance(ex.args, tuple):   # Python 2.6
            res['code'] = ex.args[0]
        return res
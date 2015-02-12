import logging

from orchestrator.core.flow.base import FlowBase

logger = logging.getLogger('orchestrator_core')


class CreateNewServiceUser(FlowBase):

    def createNewServiceUser(self,
                             SERVICE_NAME,
                             SERVICE_ID,
                             SERVICE_ADMIN_USER,
                             SERVICE_ADMIN_PASSWORD,
                             SERVICE_ADMIN_TOKEN,
                             NEW_USER_NAME,
                             NEW_USER_PASSWORD,
                             NEW_USER_EMAIL):

        '''Creates a new user Service (aka domain user keystone).

        In case of HTTP error, return HTTP error

        Params:
        - SERVICE_NAME: Service name
        - SERVICE_ADMIN_USER: Service admin username
        - SERVICE_ADMIN_PASSWORD: Service admin password
        - SERVICE_ADMIN_TOKEN: Service admin token
        - NEW_USER_NAME: New user name (required)
        - NEW_USER_PASSWORD: New user password (required)
        - NEW_USER_EMAIL: New user password (optional)
        Return:
        - id: New user Id
        '''

        logger.debug("createNewServiceUser invoked with: ")
        logger.debug("SERVICE_NAME=%s" % SERVICE_NAME)
        logger.debug("SERVICE_ID=%s" % SERVICE_ID)
        logger.debug("SERVICE_ADMIN_USER=%s" % SERVICE_ADMIN_USER)
        logger.debug("SERVICE_ADMIN_PASSWORD=%s" % SERVICE_ADMIN_PASSWORD)
        logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)
        logger.debug("NEW_USER_NAME=%s" % NEW_USER_NAME)
        logger.debug("NEW_USER_PASSWORD=%s" % NEW_USER_PASSWORD)
        logger.debug("NEW_USER_EMAIL=%s" % NEW_USER_EMAIL)


        try:
            if not SERVICE_ADMIN_TOKEN:
                SERVICE_ADMIN_TOKEN = self.idm.getToken(SERVICE_NAME,
                                                        SERVICE_ADMIN_USER,
                                                        SERVICE_ADMIN_PASSWORD)
            logger.debug("SERVICE_ADMIN_TOKEN=%s" % SERVICE_ADMIN_TOKEN)


            #
            # 1. Get service (aka domain)
            #
            if not SERVICE_ID:
                ID_DOM1 = self.idm.getDomainId(SERVICE_ADMIN_TOKEN,
                                               SERVICE_NAME)
                SERVICE_ID=ID_DOM1

            logger.debug("ID of your service %s:%s" % (SERVICE_NAME, SERVICE_ID))

            #
            # 2.  Create user
            #
            ID_USER = self.idm.createUserDomain(SERVICE_ADMIN_TOKEN,
                                                SERVICE_ID,
                                                SERVICE_NAME,
                                                NEW_USER_NAME,
                                                NEW_USER_PASSWORD,
                                                NEW_USER_EMAIL)
            logger.debug("ID of user %s: %s" % (NEW_USER_NAME, ID_USER))


        except Exception, ex:
            logger.error(ex)
            return self.composeErrorCode(ex)


        logger.info("Summary report:")
        logger.info("ID_DOM1=%s" % SERVICE_ID)
        logger.info("ID_USER=%s" % ID_USER)

        return {"id":ID_USER}




import json
import os

from orchestrator.common.util import RestOperations
from orchestrator.core import policies

# TODO: Interface (Base) + Implementations (Derived)

# class IdMOperations(object):
#     def __init__(self):
#         None

#     def createService(self):
#         None

#     def createSubService(self):
#         None


# class IdMKeystoneOperations

# class AccessControlOperations
# class AccessControlKeypassOperations


class IdMOperations(object):
    '''
       IoT IdM (keystone + keypass)
    '''

    def __init__(self,
                 KEYSTONE_PROTOCOL=None,
                 KEYSTONE_HOST=None,
                 KEYSTONE_PORT=None,
                 KEYPASS_PROTOCOL=None,
                 KEYPASS_HOST=None,
                 KEYPASS_PORT=None
             ):

        self.KEYSTONE_PROTOCOL=KEYSTONE_PROTOCOL
        self.KEYSTONE_HOST=KEYSTONE_HOST
        self.KEYSTONE_PORT=KEYSTONE_PORT
        self.KEYPASS_PROTOCOL=KEYPASS_PROTOCOL
        self.KEYPASS_HOST=KEYPASS_HOST
        self.KEYPASS_PORT=KEYPASS_PORT

        self.IdMRestOperations = RestOperations(KEYSTONE_PROTOCOL,
                                                KEYSTONE_HOST,
                                                KEYSTONE_PORT)

        self.AccessControlRestOperations = RestOperations(KEYPASS_PROTOCOL,
                                                          KEYPASS_HOST,
                                                          KEYPASS_PORT)

        self.policy_dir = os.path.dirname(policies.__file__)


    def getToken(self,
                 DOMAIN_NAME,
                 DOMAIN_ADMIN_USER,
                 DOMAIN_ADMIN_PASSWORD):

        auth_data = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": DOMAIN_ADMIN_USER,
                            "password": DOMAIN_ADMIN_PASSWORD
                        }
                    }
                }
            }
            }
                # ,
                #   "scope": {
                #       "domain": {
                #           "name": DOMAIN_NAME
                #       }
                #   }
                # }
            #}

        if DOMAIN_NAME:
            auth_data['auth']['identity']['password']['user'].update({"domain": { "name": DOMAIN_NAME}})

            scope_domain = {
                "scope": {
                    "domain": {
                        "name": DOMAIN_NAME
                    }
                }
            }
            auth_data['auth'].update(scope_domain)

        res = self.IdMRestOperations.rest_request(url='/v3/auth/tokens',
                                method='POST', data=auth_data)
        assert res.code == 201, (res.code, res.msg)
        return res.headers.get('X-Subject-Token')

    def getToken2(self,
                 DOMAIN_ID,
                 DOMAIN_ADMIN_USER,
                 DOMAIN_ADMIN_PASSWORD):
        auth_data = {
            "auth": {
                "identity": {
                    "methods": [
                        "password"
                    ],
                    "password": {
                        "user": {
                            "name": DOMAIN_ADMIN_USER,
                            "password": DOMAIN_ADMIN_PASSWORD
                        }
                    }
                }
            }
            }
                # ,
                #   "scope": {
                #       "domain": {
                #           "name": DOMAIN_NAME
                #       }
                #   }
                # }
            #}

        if DOMAIN_ID:
            auth_data['auth']['identity']['password']['user'].update({"domain": { "id": DOMAIN_ID}})

            scope_domain = {
                "scope": {
                    "domain": {
                        "id": DOMAIN_ID
                    }
                }
            }
            auth_data['auth'].update(scope_domain)

        res = self.IdMRestOperations.rest_request(url='/v3/auth/tokens',
                                method='POST', data=auth_data)
        assert res.code == 201, (res.code, res.msg)
        return res.headers.get('X-Subject-Token')

    # aka createService
    def createDomain(self,
                     CLOUD_ADMIN_TOKEN,
                     NEW_SERVICE_NAME,
                     NEW_SERVICE_DESCRIPTION):

        body_data = {
            "domain": {
                "enabled": True,
                "name": "%s" % NEW_SERVICE_NAME,
                "description": "%s" % NEW_SERVICE_DESCRIPTION
            }
        }
        res = self.IdMRestOperations.rest_request(url='/v3/domains',
                                method='POST', data=body_data,
                                auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response['domain']['id']


    def getRoleId(self,
                 CLOUD_ADMIN_TOKEN,
                 ROLE_NAME):
        res = self.IdMRestOperations.rest_request(url='/v3/roles?name=%s' % ROLE_NAME,
                                method='GET',
                                auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        # TODO ensure ADMIN_ROLE_ID?
        return json_body_response['roles'][0]['id']


    def grantDomainRole(self,
                      CLOUD_ADMIN_TOKEN,
                      ID_DOM1,
                      ID_ADM1,
                      ADMIN_ROLE_ID):
        res = self.IdMRestOperations.rest_request(url='/v3/domains/%s/users/%s/roles/%s' % (
                                ID_DOM1, ID_ADM1, ADMIN_ROLE_ID),
                                method='PUT',
                                auth_token=CLOUD_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)
        # TODO: return?

    def createDomainRole(self,
                        SERVICE_ADMIN_TOKEN,
                        SUB_SERVICE_ROLE_NAME,
                        ID_DOM1):
        body_data = {
            "schemas": ["urn:scim:schemas:extension:keystone:1.0"],
            "name": "%s" % SUB_SERVICE_ROLE_NAME,
            "domain_id": "%s" % ID_DOM1
        }
        res = self.IdMRestOperations.rest_request(url='/v3/OS-SCIM/Roles',
                                method='POST', data=body_data,
                                auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response['id']


    # TODO: move into AccessControlOperations?
    def provisionPolicy(self,
                        SERVICE_NAME,
                        SERVICE_ADMIN_TOKEN,
                        SUB_SERVICE_ROLE_ID,
                        POLICY_FILE_NAME):

        xml_data = open(self.policy_dir + '/' + POLICY_FILE_NAME)
        body_data = xml_data.read()
        xml_data.close()
        res = self.AccessControlRestOperations.rest_request(
                                url='pap/v1/subject/'+SUB_SERVICE_ROLE_ID,
                                method='POST',
                                json_data=False,
                                data=body_data,
                                auth_token=SERVICE_ADMIN_TOKEN,
                                fiware_service=SERVICE_NAME)

        assert res.code == 201, (res.code, res.msg)
        # TODO: return ?


    # aka createSubService
    def createProject(self,
                      SERVICE_ADMIN_TOKEN,
                      ID_DOM1,
                      NEW_SUBSERVICE_NAME,
                      NEW_SUBSERVICE_DESCRIPTION):

        body_data = {
            "project": {
                "enabled": True,
                "domain_id": "%s" % ID_DOM1,
                "name": "/%s" % NEW_SUBSERVICE_NAME,
                "description": "%s" % NEW_SUBSERVICE_DESCRIPTION
            }
        }
        res = self.IdMRestOperations.rest_request(url='/v3/projects',
                                method='POST', data=body_data,
                                auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response['project']['id']


    def getDomainId(self, SERVICE_ADMIN_TOKEN, DOMAIN_NAME):

        auth_data = {
        "auth": {
            "identity": {
                "methods": [
                    "token"
                ],
                "token": {
                    "id": SERVICE_ADMIN_TOKEN
                }
            },
            "scope": {
                "domain": {
                    "name": DOMAIN_NAME
                }
            }
        }
        }
        res = self.IdMRestOperations.rest_request(url='/v3/auth/tokens',
                                method='POST', data=auth_data)


        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response['token']['user']['domain']['id']

    def createUserDomain(self,
                      SERVICE_ADMIN_TOKEN,
                      ID_DOM1,
                      SERVICE_NAME,
                      NEW_USER_NAME,
                      NEW_USER_PASSWORD):

        body_data = {
            "user": {
                "description": "user of domain %s" % SERVICE_NAME,
                "enabled": True,
                "domain_id": "%s" % ID_DOM1,
                "name": "%s" % NEW_USER_NAME,
                "password": "%s" % NEW_USER_PASSWORD,
            }
        }
        res = self.IdMRestOperations.rest_request(url='/v3/users',
                                method='POST', data=body_data,
                                auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response['user']['id']


    def createRoleDomain(self,
                      SERVICE_ADMIN_TOKEN,
                      ID_DOM1,
                      NEW_ROLE_NAME):

        body_data = {
                "enabled": "\[\"urn:scim:schemas:extension:keystone:1.0\"\]",  # TODO: check this string!
                "domain_id": "%s" % ID_DOM1,
                "name": "%s" % NEW_ROLE_NAME,
        }
        res = self.IdMRestOperations.rest_request(url='/v3/OS-SCIM/Roles',
                                method='POST', data=body_data,
                                auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response['id']


    def getProjectId(self, SERVICE_ADMIN_TOKEN, DOMAIN_NAME, PROJECT_NAME):

        auth_data = {
        "auth": {
            "identity": {
                "methods": [
                    "token"
                ],
                "token": {
                    "id": SERVICE_ADMIN_TOKEN
                }
            },
            "scope": {
                "domain": {
                    "name": DOMAIN_NAME
                }
            }
        }
        }
        res = self.IdMRestOperations.rest_request(url='/v3/auth/tokens',
                                method='POST', data=auth_data)


        assert res.code == 201, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        for project in json_body_response['projects']:
            if project['name'] == PROJECT_NAME:
                return project['id']


    def getDomainRoleId(self,
                 SERVICE_ADMIN_TOKEN,
                 DOMAIN_ID,
                 ROLE_NAME):
        res = self.IdMRestOperations.rest_request(url='/v3/OS-SCIM/Roles?domain_id=%s' % DOMAIN_ID,
                                method='GET',
                                auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)

        for role in json_body_response['Resources']:
            if role['name'] == ROLE_NAME:
                return role['id']



    def getDomainUserId(self,
                 SERVICE_ADMIN_TOKEN,
                 DOMAIN_ID,
                 USER_NAME):
        res = self.IdMRestOperations.rest_request(url='/v3/OS-SCIM/Users?domain_id=%s' % DOMAIN_ID,
                                method='GET',
                                auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)

        for user in json_body_response['Resources']:
            if user['userName'] == USER_NAME:
                return user['id']

    def grantProjectRole(self,
                      SERVICE_ADMIN_TOKEN,
                      ID_PRO1,
                      ID_USER,
                      ROLE_ID):
        res = self.IdMRestOperations.rest_request(url='/v3/projects/%s/users/%s/roles/%s' % (
                                ID_PRO1, ID_USER, ROLE_ID),
                                method='PUT',
                                auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)
        # TODO: return?

    def detailUser(self,
                   SERVICE_ADMIN_TOKEN,
                   ID_USER):

        res = self.IdMRestOperations.rest_request(url='/v3/OS-SCIM/Users/%s' % ID_USER,
                                                  method='GET', data=None,
                                                  auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response

    def removeUser(self,
                   SERVICE_ADMIN_TOKEN,
                   ID_USER):

        res = self.IdMRestOperations.rest_request(url='/v3/OS-SCIM/Users/%s' % ID_USER,
                                method='DELETE', data=None,
                                auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 204, (res.code, res.msg)
        #return ?

    def updateUser(self,
                   SERVICE_ADMIN_TOKEN,
                   ID_USER,
                   USER_DATA):
        body_data = {

            "schemas": ["urn:scim:schemas:core:1.0",
                        "urn:scim:schemas:extension:keystone:1.0"],
        }
        body_data.update(USER_DATA)
        res = self.IdMRestOperations.rest_request(url='/v3/OS-SCIM/Users/%s' % ID_USER,
                                method='PATCH', data=body_data,
                                auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        #return ?
        return json_body_response

    def getDomains(self,
                   SERVICE_ADMIN_TOKEN):

        res = self.IdMRestOperations.rest_request(url='/v3/domains',
                                                  method='GET',
                                                  auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)

        domains = []
        for domain in json_body_response['domains']:
            domain_data = {
                "id": domain['id'],
                "name": domain['name'],
                "enabled": domain['enabled']
            }
            if 'description' in domain:
                domain_data.update({"description": domain['description']})
            domains.append(domain_data)

        return domains

    def getDomain(self,
                  SERVICE_ADMIN_TOKEN,
                  DOMAIN_ID):
        res = self.IdMRestOperations.rest_request(url='/v3/domains?domain_id=%s' % DOMAIN_ID,
                                                  method='GET',
                                                  auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)
        return json_body_response

    def getDomainRoles(self,
                       SERVICE_ADMIN_TOKEN,
                       DOMAIN_ID):

        res = self.IdMRestOperations.rest_request(url='/v3/OS-SCIM/Roles?domain_id=%s' % DOMAIN_ID,
                                                  method='GET',
                                                  auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)

        # Group each role by name and id
        roles = []
        for role in json_body_response['Resources']:
            role_data = {"role":
                         {
                             "name": role['name'],
                             "id": role['id']
                         }
                     }
            roles.append(role_data)

        return roles


    def getDomainUsers(self,
                       SERVICE_ADMIN_TOKEN,
                       DOMAIN_ID):

        res = self.IdMRestOperations.rest_request(url='/v3/OS-SCIM/Users?domain_id=%s' % DOMAIN_ID,
                                                  method='GET',
                                                  auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)

        # Group each role by name and id
        users = []
        for user in json_body_response['Resources']:
            users.append(
                {"name": user['userName'],
                 "id": user['id'],
                 "description": user["displayName"],
                 "domain_id": user['urn:scim:schemas:extension:keystone:1.0']['domain_id'],
                 "enabled": user['active']
             })
        return users

    def getDomainProjects(self,
                          SERVICE_ADMIN_TOKEN,
                          DOMAIN_ID):

        res = self.IdMRestOperations.rest_request(url='/v3/projects?domain_id=%s' % DOMAIN_ID,
                                                  method='GET',
                                                  auth_token=SERVICE_ADMIN_TOKEN)
        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)

        # Group each role by name and id
        projects = []
        for project in json_body_response['projects']:
            project_data = {
                "name": project['name'],
                "id": project['id'],
                "domain_id": project['domain_id']
            }
            # TODO: include domain_name into each project ?
            if 'description' in project:
                project_data.update({"description": project['description']})

            projects.append(project_data)
        return projects


    def getRoleAssignmnts(self,
                          SERVICE_ADMIN_TOKEN,
                          PROJECT_ID):

        res = self.IdMRestOperations.rest_request(url='/v3/role_assignments?scope.project.id=%s' % PROJECT_ID,
                                                  method='GET',
                                                  auth_token=SERVICE_ADMIN_TOKEN)

        assert res.code == 200, (res.code, res.msg)
        data = res.read()
        json_body_response = json.loads(data)

        # Group each role by name and id
        import pdb
        pdb.set_trace()
        return None

        # projects = {}
        # for project in json_body_response['projects']:
        #     project_data = {
        #         "name": project['name'],
        #         "id": project['id'],
        #         "domain_id": project['domain_id']
        #     }
        #     # TODO: include domain_name into each project ?
        #     if 'description' in project:
        #         project_data.update({"description": project['description']})

        #     projects.append(project_data)
        # return projects

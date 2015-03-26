#!/bin/bash

cd ../../orchestrator/commands/

python ./createNewService.py http               \
                                 localhost      \
                                 5000           \
                                 admin_domain   \
                                 cloud_admin    \
                                 password       \
                                 SmartValencia  \
                                 smartvalencia  \
                                 adm1           \
                                 password       \
                                 http           \
                                 localhost      \
                                 8080

python ./assignInheritRoleServiceUser.py http        \
                                    localhost        \
                                    5000             \
                                    SmartValencia    \
                                    adm1             \
                                    password         \
                                    adm1             \
                                    SubServiceAdmin  \
                                    http             \
                                    localhost        \
                                    8080

python ./createNewSubService.py  http                \
                                      localhost      \
                                      5000           \
                                      SmartValencia  \
                                      adm1           \
                                      password       \
                                      Electricidad   \
                                      electricidad

python ./createNewServiceUser.py  http               \
                                      localhost      \
                                      5000           \
                                      SmartValencia  \
                                      adm1           \
                                      password       \
                                      Alice          \
                                      password

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       SmartValencia  \
                                       adm1           \
                                       password       \
                                       Electricidad   \
                                       SubServiceAdmin\
                                       Alice

python ./createNewSubService.py  http                \
                                      localhost      \
                                      5000           \
                                      SmartValencia  \
                                      adm1           \
                                      password       \
                                      Basuras        \
                                      basuras

python ./createNewServiceUser.py  http                \
                                       localhost      \
                                       5000           \
                                       SmartValencia  \
                                       adm1           \
                                       password       \
                                       bob            \
                                       password

python ./assignRoleSubServiceUser.py http             \
                                       localhost      \
                                       5000           \
                                       SmartValencia  \
                                       adm1           \
                                       password       \
                                       Basuras        \
                                       SubServiceAdmin\
                                       bob

python ./createNewServiceUser.py  http               \
                                      localhost      \
                                      5000           \
                                      SmartValencia  \
                                      adm1           \
                                      password       \
                                      Carl           \
                                      password

python ./createNewServiceRole.py  http               \
                                      localhost      \
                                      5000           \
                                      SmartValencia  \
                                      adm1           \
                                      password       \
                                      ServiceCustomer\
                                      http           \
                                      localhost      \
                                      8080

python ./assignRoleServiceUser.py http                \
                                       localhost      \
                                       5000           \
                                       SmartValencia  \
                                       adm1           \
                                       password       \
                                       ServiceCustomer\
                                       Carl

python ./assignInheritRoleServiceUser.py http         \
                                    localhost         \
                                    5000              \
                                    SmartValencia     \
                                    adm1              \
                                    password          \
                                    Carl              \
                                    SubServiceCustomer\
                                    http              \
                                    localhost         \
                                    8080


cd -

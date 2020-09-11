# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/18 19:14

# 超管手机号
ADMIN_PHONE = ['输入admin的手机号', '']

DEBUG = True
PDB_DEBUG = True


# 百度ak
BD_API_MAP_PARAMS = {
    'ak': '用户自己的ak',
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'sheep',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'macbookpro2020',
        # 使用mysql的innodb引擎,MyISAM虽快但没有事务rollback
        'OPTIONS': {
            # 'init_command': 'SET default_storage_engine=INNODB;',
            'charset': 'utf8mb4', },
        "CONN_MAX_AGE": 1000,
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8_general_ci',
        }
    },
}

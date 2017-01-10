# coding:utf-8
import json
import os


class ConfigManager:
    PATH = os.path.dirname(__file__) + os.path.sep

    def __init__(self):
        self.files = []
        self.config = {}
        self.add_file('timer.conf')
        self.add_file('db.conf')
        self.add_file('log.conf')
        self.reload()

    def add_file(self, fname):
        self.files.append(ConfigManager.PATH + fname)

    def reload(self):
        for fname in self.files:
            with open(fname, 'r') as file:
                try:
                    j = json.load(file)
                    self.config.update(j)
                except ValueError:
                    print('配置文件 %s 格式错误' % fname)

    def __getitem__(self, key):
        return self.config.get(key, '不存在该配置项')

# global conf : gconf 为全局唯一的ConfigManager对象
gconf = ConfigManager()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib.request
import os, sys

url = ['http://vip-tv.xyz/playlist/zabava.m3u', 
       'http://vip-tv.xyz/playlist/koala.m3u', 
       'http://vip-tv.xyz/playlist/detskiy.m3u']

temp = '/tmp'
temp_all = 'all.m3u'
playlist = 'tv.m3u'

def download(): # Скачиваем все плейлисты каналов из массива
  for element in url: 
      filename = str(element.split("/")[-1:])[2 : -2]
      urllib.request.urlretrieve(element, temp + '/' + filename)

def merge(): # Мержим в один файл все скачаные плейлисты
  for element in url: 
      filename = element.split("/")[-1:]
      print(filename)
      with open(temp + '/' + temp_all, 'a') as outfile:
        for fname in filename:
          with open(temp + '/' + fname) as infile:
              outfile.write(infile.read())

def generate(channel_name, url): # Генерируем плейлист и сохраняем его в файл
  useragent = "User-Agent=OnlineTvAppDroid"
  f = open('./tv/' + playlist, 'a')
  if 'disney' in url or 'cartoonnetwork' in url or 'jim_jam' in url or 'nickelodeon' in url or 'karusel' in url or 'mult' in url or 'skazki' in url or 'WEB_Smilik' in url:
     f.write(channel_name + '\n' + url + '\n')
  else: 
     f.write(channel_name + '\n' + url + '|' + useragent + '\n')

def parse(): # Парсим temp_all и генерируем плейлист
  f = open(temp + '/' + temp_all)
  for line in f.readlines():
    if '#EXTINF:' in line:
      channel_name = line.rstrip()
    elif 'http://' in line or 'https://' in line:
      url = line.rstrip()
      generate(channel_name, url)
       

def clean(): # Зачищаем временные файлы
  os.system('rm ./tv/tv.m3u')
  os.system('rm /tmp/*.m3u')

def push(): # Отправляем в репозиторий готовый плейлист
  root = os.path.dirname(os.path.realpath(__file__))
  os.system('cd ' + root + '/tv && git add .')
  os.system('cd ' + root + '/tv && git commit -m \"New TV PlayList\"')
  os.system('cd ' + root + '/tv && git push')

clean()
download()
merge()
parse()
push()

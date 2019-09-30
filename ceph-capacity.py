#!/usr/bin/env python2
import subprocess, json, sys, time, os, math, getopt

input_cluster = sys.argv[1]
ceph_conf = ("ceph." + str(input_cluster) + ".conf")

def jsoncmd(command):
  with open(os.devnull, 'w') as devnull:
    out = subprocess.check_output(command.split(), stderr=devnull)
  return json.loads(out)


def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

df_data = jsoncmd("ceph -c " +  "/etc/ceph/" + str(ceph_conf) + " --id admin df -f json")
total_used_bytes=df_data['stats']['total_used_bytes']
total_bytes=df_data['stats']['total_bytes']
total_avail_bytes=df_data['stats']['total_avail_bytes']

def cluster_size_calculation():
    avail_ratiopercent = (total_avail_bytes * 30 / 100)
    return total_avail_bytes - avail_ratiopercent

real_size_bytes = cluster_size_calculation()
real_size_gigabytes = convert_size(real_size_bytes)

print(real_size_gigabytes)
print(real_size_bytes)
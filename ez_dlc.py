import os, os.path
import subprocess, sys
import errno
import shutil
import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
gen_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def safe_open_w(path):
    mkdir_p(os.path.dirname(path))
    return open(path, 'w')

try:
	contentid = sys.argv[1]
	name = sys.argv[2]
	titleid = contentid[7:16]
except:
	print("Usage: {} {} {}".format(sys.argv[0], 'DLC_CID', '\"DLC_NAME\"'))
	sys.exit(2)

if not os.path.exists('orbis-pub-cmd.exe'):
	print("File \'orbis-pub-cmd.exe\' is missing from current directory!!")
	sys.exit(2)
	
if len(contentid) is not 36:
	print("DLC CID IS TOO LONG OR TOO SHORT, IT HAS TO BE 36 CHARACTERS LONG, FOR EXAMPLE 'UP9000-CUSA00900_00-SPEXPANSIONDLC03'")
	sys.exit(2)

SFX_template = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<paramsfo>
 <param key="ATTRIBUTE">0</param>
 <param key="CATEGORY">ac</param>
 <param key="CONTENT_ID">%s</param>
 <param key="FORMAT">obs</param>
 <param key="TITLE">%s</param>
 <param key="TITLE_ID">%s</param>
 <param key="VERSION">01.00</param>
</paramsfo>)""" % (contentid, name, titleid)

GP4_template = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<psproject fmt="gp4" version="1000">
  <volume>
    <volume_type>pkg_ps4_ac_nodata</volume_type>
    <volume_id>PS4VOLUME</volume_id>
    <volume_ts>%s</volume_ts>
    <package content_id="%s" passcode="00000000000000000000000000000000"/>
  </volume>
  <files img_no="0">
	<file targ_path="sce_sys/param.sfo" orig_path="%s\\fake_dlc_temp\sce_sys\param.sfo"/>
  </files>
  <rootdir>
    <dir targ_name="sce_sys"/>
  </rootdir>
</psproject>""" % (gen_time, contentid, current_dir)

## save both files
x = safe_open_w('fake_dlc_temp/param_template.sfx')
x.write(SFX_template)
x.close()
x = safe_open_w('fake_dlc_temp/fake_dlc_project.gp4')
x.write(GP4_template)
x.close()

## Precreate some directories if needed
mkdir_p(os.path.dirname('fake_dlc_temp/sce_sys/'))
if os.path.isdir("fake_dlc_pkg"):
	pass
else:
	os.mkdir('fake_dlc_pkg')

## convert sfo template to sfo file
subprocess.check_call(['orbis-pub-cmd.exe', 'sfo_create', 'fake_dlc_temp\param_template.sfx', 'fake_dlc_temp\sce_sys\param.sfo'])

## build fpkg out of generated PG4 project file
subprocess.check_call(['orbis-pub-cmd.exe', 'img_create', '%s\\fake_dlc_temp\\fake_dlc_project.gp4' % current_dir, '%s\\fake_dlc_pkg\%s-A0000-V0100.pkg' % (current_dir, contentid)])

## be a good boy and clean up after
shutil.rmtree('fake_dlc_temp')
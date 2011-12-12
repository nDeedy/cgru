#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import af
import afcommon
import cgruutils
import services.service

def error_exit( error_str = None):
   if error_str is not None: print( error_str)
   sys.stdout.flush()
   sys.exit(1)

def usage_exit():
   print('\n\
examples:\n\
\n\
afjob path/scene.shk 1 100\n\
\n\
afjob path/scene.hip 1 100 -fpt 3 -pwd projects/test -node /out/mantra1 -take back -name my_job\n\
\n\
arguments:\n\
\n\
path/scene.shk       -   (R) Scene, which file extension determinate run command and task type\n\
1                    -   (R) First frame to render\n\
100                  -   (R) Last frame to render\n\
-by 1                -   Frames increment, default = 1\n\
-fpt 1               -   Frames per task, default = 1\n\
-pwd projects/test   -   Working directory, if not set current will be used.\n\
-name my_job         -   Job name, if not set scene name will be used.\n\
-node                -   Node to render ( houdini driver, nuke write, max camera )\n\
-type                -   Service type\n\
-take                -   Take to use ( houdini take, xsi pass, max batch )\n\
-ignoreinputs        -   not to render input nodes ( houdini ignore inputs ROP parameter )\n\
-tempscene           -   copy scene to temporary file to render\n\
-deletescene         -   delete scene when job deleted\n\
-pause               -   start job paused ( offline afanasy state )\n\
-os                  -   OS needed mask, "any" to render on any platform\n\
-hostsmask           -   job render hosts mask\n\
-hostsexcl           -   job render hosts to exclude mask\n\
-maxruntasks         -   maximum number of hosts to use\n\
-maxruntime          -   maximum run time for task in seconds\n\
-priority            -   job priority\n\
-capacity            -   tasks capacity\n\
-capmin              -   tasks minimum capacity coefficient\n\
-capmax              -   tasks maximum capacity coefficient\n\
-depmask             -   wait untill other jobs of the same user, satisfying this mask\n\
-depglbl             -   wait untill other jobs of any user, satisfying this mask\n\
-output              -   override output filename\n\
-images              -   images to preview (img.%04d.jpg)\n\
-image               -   image to preview (img.0000.jpg)\n\
-exec                -   customuze command executable.\n\
-varirender attr start step count - variate parameter\n\
-simulate            -   enable simulation\n\
(R)                  -   REQUIRED arguments\n\
\n\
')
   error_exit()

def integer( string):
   try:
      number = int( string)
   except:
      error_exit( str(sys.exc_info()[1]))
   return number
   
argsv = sys.argv
argsl = len( argsv)

if argsl < 4:
   usage_exit()

scene = argsv[1]
ext = scene.rfind('.')
if ext == -1: ext = ''
else: ext = scene[ext+1:]
name = os.path.basename(scene)

#
# initial arguments values

s = integer( argsv[2])
e = integer( argsv[3])
fpt = 1
by  = 1
pwd = os.getenv('PWD', os.getcwd())
file           = ''
node           = ''
ignoreinputs   = False
take           = ''
deletescene    = False
tempscene      = False
startpaused    = False
hostsmask      = ''
hostsexcl      = ''
maxruntime     = 0
maxruntasks    = -1
priority       = -1
capacity       = -1
capmin         = -1
capmax         = -1
dependmask     = ''
dependglobal   = ''
output         = ''
images         = ''
image          = ''
blocktype      = ''
platform       = ''
varirender     = False
simulate       = False

cmd = None
cmds = []
blocknames = []

#
# checking some critical argumens values

if s < 0:
   error_exit( 'invalid start frame')
if e < 0:
   error_exit( 'invalid end frame')

#
# getting arguments

for i in range( argsl):
   arg = argsv[i]

   if arg == '-by':
      i += 1
      if i == argsl: break
      by = integer(argsv[i])
      continue

   if arg == '-fpr':
      print('"-fpr" (frame per render) is absolete, use "-fpt" (frame per task) instead.')
      arg = '-fpt'
   if arg == '-fpt':
      i += 1
      if i == argsl: break
      fpt = integer(argsv[i])
      continue

   if arg == '-pwd':
      i += 1
      if i == argsl: break
      pwd = argsv[i]
      continue

   if arg == '-exec':
      i += 1
      if i == argsl: break
      cmd = '"%s"' % argsv[i]
      continue

   if arg == '-file':
      i += 1
      if i == argsl: break
      file = argsv[i]
      continue

   if arg == '-name':
      i += 1
      if i == argsl: break
      name = argsv[i]
      continue

   if arg == '-node':
      i += 1
      if i == argsl: break
      node = argsv[i]
      continue

   if arg == '-take':
      i += 1
      if i == argsl: break
      take = argsv[i]
      continue

   if arg == '-deletescene':
      deletescene = True
      continue

   if arg == '-tempscene':
      tempscene = True
      continue

   if arg == '-ignoreinputs':
      ignoreinputs = True
      continue

   if arg == '-pause':
      startpaused = True

   if arg == '-hostsmask':
      i += 1
      if i == argsl: break
      hostsmask = argsv[i]
      continue

   if arg == '-hostsexcl':
      i += 1
      if i == argsl: break
      hostsexcl = argsv[i]
      continue

   if arg == '-maxhosts':
      print('"-maxhosts" (maximum hosts) is absolete, use "-maxruntasks" (maximum running tasks) instead.')
      arg = '-maxruntasks'
   if arg == '-maxruntasks':
      i += 1
      if i == argsl: break
      maxruntasks = integer(argsv[i])
      continue

   if arg == '-maxruntime':
      i += 1
      if i == argsl: break
      maxruntime = integer(argsv[i])
      continue

   if arg == '-priority':
      i += 1
      if i == argsl: break
      priority =integer(argsv[i])
      continue

   if arg == '-capacity':
      i += 1
      if i == argsl: break
      capacity = int(argsv[i])
      continue

   if arg == '-capmin':
      i += 1
      if i == argsl: break
      capmin = int(argsv[i])
      continue

   if arg == '-capmax':
      i += 1
      if i == argsl: break
      capmax = int(argsv[i])
      continue

   if arg == '-depmask':
      i += 1
      if i == argsl: break
      dependmask = argsv[i]
      continue

   if arg == '-depglbl':
      i += 1
      if i == argsl: break
      dependglobal = argsv[i]
      continue

   if arg == '-images':
      i += 1
      if i == argsl: break
      images = argsv[i]
      continue

   if arg == '-output':
      i += 1
      if i == argsl: break
      output = argsv[i]
      continue

   if arg == '-image':
      i += 1
      if i == argsl: break
      image = argsv[i]
      continue

   if arg == '-type':
      i += 1
      if i == argsl: break
      blocktype = argsv[i]
      continue

   if arg == '-os':
      i += 1
      if i == argsl: break
      platform = argsv[i]
      continue

   if arg == '-varirender':
      i += 1
      if i == argsl: break
      varirender_attr = argsv[i]
      i += 1
      if i == argsl: break
      varirender_start = integer(argsv[i])
      i += 1
      if i == argsl: break
      varirender_step = integer(argsv[i])
      i += 1
      if i == argsl: break
      varirender_count = integer(argsv[i])
      varirender = True
      continue

   if arg == '-simulate':
      simulate = True
      continue
#
# command construction:
cmdextension = os.getenv('AF_CMDEXTENSION', '')

# Check some parameters:
if fpt < 1:
   print('fpt - frames per task - must be > 0 ( setting to 1)')
   fpt = 1
if by < 1:
   print('by - frames step (by frame) - must be > 0 ( setting to 1)')
   by = 1

if tempscene:
   scene = cgruutils.copyJobFile( scene, name, ext)
   if scene == '': sys.exit(1)

# Initialize general parameters:
blockname = node

# Shake:
if ext == 'shk':
   scenetype = 'shake'
   if cmd is None: cmd = 'shake' + cmdextension
   cmd += ' -exec ' + scene + ' -vv -t @#@-@#@'

# Blender:
if ext == 'blend':
   scenetype = 'blender'
   if cmd is None: cmd = 'blender' + cmdextension
   cmd += ' -b "%s"' % scene
   cmd += ' -s @#@ -e @#@ -j %d -a' % by

# Nuke:
elif ext == 'nk':
   scenetype = 'nuke'
   if cmd is None: cmd = 'nuke' + cmdextension
   cmd += ' -i'
   cmd += ' -F @#@-@#@x' + str(by)
   if capmin != -1 or capmax != -1: cmd += ' -m ' + services.service.str_capacity
   if node != '': cmd += ' -X %s' % node
   cmd += ' -x "%s"' % scene

# Houdini:
elif ext == 'hip':
   if node == '':
      error_exit( 'no houdini driver to render specified')
   scenetype = 'hbatch_mantra'
   if cmd is None: cmd = 'hrender_af' + cmdextension
   if capmin != -1 or capmax != -1: cmd += ' --numcpus '+ services.service.str_capacity
   if ignoreinputs: cmd += ' -i'
   cmd += ' -s @#@ -e @#@ --by %d' % by
   if take != '': cmd += ' -t "%s"' % take
   cmd += ' "%s" "%s"' % (scene,node)

# Mantra:
elif ext == 'ifd':
   scenetype = 'mantra'
   if cmd is None: cmd = 'mantra' + cmdextension
   if capmin != -1 or capmax != -1: cmd += ' -j '+ services.service.str_capacity
   cmd += ' -V a -f "%s"' % scene

# Maya:
elif ext == 'mb':
   scenetype = 'maya'
#   cmd = 'mayabatch' + cmdextension + ' -file "' + scene + '" -command "afanasyBatch(@#@,@#@,1,1);quit -f;"'
   if cmd is None: cmd = 'mayarender' + cmdextension
   cmd += ' -s @#@ -e @#@ -b %d' % by
   if node != '': cmd += ' -cam "%s"' % node
   if take != '': cmd += ' -rl "%s"' % take
   if output != '':
      if os.path.isdir( output):
         cmd += ' -rd "%s"' % output
      else:
         cmd += ' -rd "%s"' % os.path.dirname( output)
         im = os.path.basename( output)
         of = im[im.rfind('.')+1:]
         im = im[:im.rfind('.')]
         im = im[:im.rfind('.')]
         cmd += ' -im "%s"' % os.path.basename( im)
         cmd += ' -of "%s"' % os.path.basename( of)
      images = output
   cmd += ' -proj "%s"' % pwd
   cmd += ' "%s"' % scene

# XSI:
elif ext == 'scn':
   scenetype = 'xsi'
   xsirenderscript = os.environ['CGRU_LOCATION']
   xsirenderscript = os.path.join( xsirenderscript, 'plugins')
   xsirenderscript = os.path.join( xsirenderscript, 'xsi')
   xsirenderscript = os.path.join( xsirenderscript, 'afrender.py')
   if cmd is None: cmd = 'xsibatch' + cmdextension
   cmd += ' -script %s' % xsirenderscript
   cmd += ' -lang Python -main afRender -args'
   cmd += ' -scene "%s"' % scene
   cmd += ' -start @#@ -end @#@ -step ' + str(by)
   cmd += ' -simulate'
   if simulate:   cmd += ' 1'
   else:          cmd += ' 0'
   if take != '': cmd += ' -renderPass ' + take
   if varirender:
      cmd += ' -attr ' + varirender_attr + ' -value '
      value = varirender_start
      for i in range( 0, varirender_count):
         cmds.append( cmd + str(value))
         blocknames.append( 'variant[%d]' % value)
         value += varirender_step
      cmd = ''

# 3D MAX:
elif ext == 'max':
   scenetype = 'max'
   if cmd is None: cmd = '3dsmaxcmd' + cmdextension
   cmd += ' "' + scene + '" -start:@#@ -end:@#@ -nthFrame:' + str(by) + ' -v:5  -continueOnError -showRFW:0'
   if node != '': cmd += ' -cam:"%s"' % node
   if take != '':
      cmd += ' -batchrender'
      if take != 'all': cmd += ':"%s"' % take
      if blockname != '': blockname = take + ' ' + blockname
      else: blockname = take
   if output != '':
      cmd += ' -o:"%s"' % output
      images = output

# After FX:
elif ext == 'aep':
   scenetype = 'afterfx'
   if cmd is None: cmd = 'aerender' + cmdextension
   cmd += ' -project "%s"' % scene
   cmd += ' -mp -s @#@ -e @#@ -i %d -mp' % by
   if node != '': cmd += ' -comp "%s"' % node
   if take != '':
      cmd += ' -RStemplate "%s"' % take
   if output != '':
      output = os.path.join( os.getcwd(), output)
      cmd += ' -output "%s"' % output
      images = os.path.join( os.path.dirname( output), os.path.basename( output).replace('[','@').replace(']','@'))

# simple generic:
else:
   scenetype = 'generic'
   if cmd is None: cmd = scene
   cmd += ' @#@ @#@'

#
# Creating a Job:

# Create a Block(s) af first:
blocks = []
if blockname == '': blockname = scenetype
if blocktype == '': blocktype = scenetype
if len( cmds) == 0:
   cmds.append( cmd)
   blocknames.append( blockname)
i = 0   
for cmd in cmds:
   block = af.Block( blocknames[i], blocktype)
   block.setWorkingDirectory( pwd )
   block.setNumeric( s, e, fpt, by)
   if scenetype == 'max': block.setCommand( cmd, False, False )
   else: block.setCommand( cmd )
   block.setCapacity( capacity)
   block.setVariableCapacity( capmin, capmax)
   if maxruntime != 0: block.setTasksMaxRunTime( maxruntime)
   if images != '': block.setFiles( afcommon.patternFromDigits( afcommon.patternFromStdC( images)))
   blocks.append( block)
   i += 1

# Create a Job:
job = af.Job( name)
job.setPriority( priority)
if maxruntasks    != -1: job.setMaxRunningTasks( maxruntasks)
if hostsmask      != '': job.setHostsMask( hostsmask)
if hostsexcl      != '': job.setHostsMaskExclude( hostsexcl)
if dependmask     != '': job.setDependMask( dependmask)
if dependglobal   != '': job.setDependMaskGlobal( dependglobal)
if deletescene         : job.setCmdPost('deletefiles "%s"' % os.path.abspath(scene))
if startpaused         : job.offLine()
if platform != '':
   if platform == 'any': job.setNeedOS('')
   else: job.setNeedOS( platform)

# Add a Block to a Job:
job.blocks.extend( blocks)

# Send Job to server:
if job.send() == False: sys.exit(1)

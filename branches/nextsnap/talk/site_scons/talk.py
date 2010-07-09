# Copyright 2010 Google Inc.
# All Rights Reserved.
#
# Author: Tim Haloun (thaloun@google.com)
#         Daniel Petersson (dape@google.com)
#
import os


def Library(env, **kwargs):
  """Extends ComponentLibrary to support multiplatform builds.

  Args:
    env: The current environment.
    kwargs: The keyword arguments.
  """
  params = CombineDicts(kwargs, {'COMPONENT_STATIC': True})
  return ExtendComponent(env, env.ComponentLibrary, **params)


def DynamicLibrary(env, **kwargs):
  """Extends ComponentLibrary to support multiplatform builds
     of dynmic libraries. This use COMPONENT_STATIC = false.

  Args:
    env: The environment object.
    kwargs: The keyword arguments.

  Returns:
    See swtoolkit ComponentLibrary
  """
  params = CombineDicts(kwargs, {'COMPONENT_STATIC': False})
  return ExtendComponent(env, env.ComponentLibrary, **params)


def Object(env, **kwargs):
  return ExtendComponent(env, env.ComponentObject, **kwargs)


def Unittest(env, **kwargs):
  """Extends ComponentTestProgram to support unittest built
     for multiple platforms.

  Args:
    env: The current environment.
    kwargs: The keyword arguments.

  Returns:
    See swtoolkit ComponentProgram.
  """
  kwargs['name'] = kwargs['name'] + '_unittest'

  common_test_params = {
    'posix_cppdefines': ['GUNIT_NO_GOOGLE3', 'GTEST_HAS_RTTI=0'],
    'libs': ['unittest_main', 'gunit']
  }
  if not kwargs.has_key('explicit_libs'):
    common_test_params['win_libs'] = [
      'advapi32',
      'crypt32',
      'iphlpapi',
      'secur32',
      'shell32',
      'shlwapi',
      'user32',
      'wininet',
      'ws2_32'
    ]
    common_test_params['lin_libs'] = [
      'pthread',
      ':libssl.so.0.9.8',
      ':libcrypto.so.0.9.8',
    ]

  params = CombineDicts(kwargs, common_test_params)
  return ExtendComponent(env, env.ComponentTestProgram, **params)


def App(env, **kwargs):
  """Extends ComponentProgram to support executables with platform specific
     options.

  Args:
    env: The current environment.
    kwargs: The keyword arguments.

  Returns:
    See swtoolkit ComponentProgram.
  """
  if not kwargs.has_key('explicit_libs'):
    common_app_params = {
      'win_libs': [
        'advapi32',
        'crypt32',
        'iphlpapi',
        'secur32',
        'shell32',
        'shlwapi',
        'user32',
        'wininet',
        'ws2_32'
      ]}
    params = CombineDicts(kwargs, common_app_params)
  else:
    params = kwargs
  return ExtendComponent(env, env.ComponentProgram, **params)


def Repository(env, at, path):
  """Maps a directory external to $MAIN_DIR to the given path so that sources
     compiled from it end up in the correct place under $OBJ_DIR.  NOT required
     when only referring to header files.

  Args:
    env: The current environment object.
    at: The 'mount point' within the current directory.
    path: Path to the actual directory.
  """
  env.Dir(at).addRepository(env.Dir(path))


def Components(*paths):
  """Completes the directory paths with the correct file
     names such that the directory/directory.scons name
     convention can be used.

  Args:
    paths: The paths to complete. If it refers to an existing
           file then it is ignored.

  Returns:
    The completed lif scons files that are needed to build talk.
  """
  files = []
  for path in paths:
    if os.path.isfile(path):
      files.append(path)
    else:
      files.append(ExpandSconsPath(path))
  return files


def ExpandSconsPath(path):
  """Expands a directory path into the path to the
     scons file that our build uses.
     Ex: magiflute/plugin/common => magicflute/plugin/common/common.scons

  Args:
    path: The directory path to expand.

  Returns:
    The expanded path.
  """
  return '%s/%s.scons' % (path, os.path.basename(path))


def AddMediaLibs(env, **kwargs):
  lmi_libdir = '$GOOGLE3/third_party/lmi/files/merged/lib/'
  if env.Bit('windows'):
    if env.get('COVERAGE_ENABLED'):
      lmi_libdir += 'win32/c_only'
    else:
      lmi_libdir += 'win32/Release'
  elif env.Bit('mac'):
    lmi_libdir += 'macos'
  elif env.Bit('linux'):
    lmi_libdir += 'linux/x86'

  ipp_libdir = '$GOOGLE3/third_party/Intel_ipp/%s/ia32/lib'
  if env.Bit('windows'):
    ipp_libdir %= 'v_5_2_windows'
  elif env.Bit('mac'):
    ipp_libdir %= 'v_5_3_mac_os_x'
  elif env.Bit('linux'):
    ipp_libdir %= 'v_5_2_linux'

  AddToDict(kwargs, 'libdirs', [
    '$MAIN_DIR/third_party/gips/Libraries/',
    ipp_libdir,
    lmi_libdir,
  ])

  gips_lib = ''
  if env.Bit('windows'):
    if env.Bit('debug'):
      gips_lib = 'gipsvoiceenginelib_mtd'
    else:
      gips_lib = 'gipsvoiceenginelib_mt'
  elif env.Bit('mac'):
    gips_lib = 'VoiceEngine_mac_universal_gcc'
  elif env.Bit('linux'):
    gips_lib = 'VoiceEngine_Linux_external_gcc'

  AddToDict(kwargs, 'libs', [
    gips_lib,
    'LmiAudioCommon',
    'LmiClient',
    'LmiCmcp',
    'LmiDeviceManager',
    'LmiH263ClientPlugIn',
    'LmiH263CodecCommon',
    'LmiH263Decoder',
    'LmiH263Encoder',
    'LmiH264ClientPlugIn',
    'LmiH264CodecCommon',
    'LmiH264Common',
    'LmiH264Decoder',
    'LmiH264Encoder',
    'LmiIce',
    'LmiMediaPayload',
    'LmiOs',
    'LmiPacketCache',
    'LmiProtocolStack',
    'LmiRateShaper',
    'LmiRtp',
    'LmiSecurity',
    'LmiSignaling',
    'LmiStun',
    'LmiTransport',
    'LmiUi',
    'LmiUtils',
    'LmiVideoCommon',
    'LmiXml',
    'ippsmerged',
    'ippsemerged',
    'ippvcmerged',
    'ippvcemerged',
    'ippimerged',
    'ippiemerged',
    'ippsrmerged',
    'ippsremerged',
  ])

  if env.Bit('windows'):
    AddToDict(kwargs, 'libs', [
      'ippcorel',
      'ippscmerged',
      'ippscemerged',
      'strmiids',
      'dsound',
    ])
  else:
    AddToDict(kwargs, 'libs', [
      'ippcore',
      'ippacmerged',
      'ippacemerged',
      'ippccmerged',
      'ippccemerged',
      'ippchmerged',
      'ippchemerged',
      'ippcvmerged',
      'ippcvemerged',
      'ippdcmerged',
      'ippdcemerged',
      'ippjmerged',
      'ippjemerged',
      'ippmmerged',
      'ippmemerged',
      'ipprmerged',
      'ippremerged',
    ])

  return kwargs


def ReadVersion(filename):
  """Executes the supplied file and pulls out a version definition from it. """
  defs = {}
  execfile(str(filename), defs)
  if not defs.has_key('version'):
    return '0.0.0.0'
  version = defs['version']
  parts = version.split(',')
  build = os.environ.get('GOOGLE_VERSION_BUILDNUMBER')
  if build:
    parts[-1] = str(build)
  return '.'.join(parts)


#-------------------------------------------------------------------------------
# Helper methods for translating talk.Foo() declarations in to manipulations of
# environmuent construction variables, including parameter parsing and merging,
#
def Depends(env, name, kwargs):
  depends = GetEntry(kwargs, 'depends')
  if depends is not None:
    env.Depends(name, depends)


def GetEntry(dict, key):
  """Get the value from a dictionary by key. If the key
     isn't in the dictionary then None is returned. If it is in
     the dictionaruy the value is fetched and then is it removed
     from the dictionary.

  Args:
    key: The key to get the value for.
    kwargs: The keyword argument dictionary.
  Returns:
    The value or None if the key is missing.
  """
  value = None
  if dict.has_key(key):
    value = dict[key]
    dict.pop(key)

  return value


def MergeAndFilterByPlatform(env, params):
  """Take a dictionary of arguments to lists of values, and, depending on
     which platform we are targetting, merge the lists of associated keys.
     Merge by combining value lists like so:
       {win_foo = [a,b], lin_foo = [c,d], foo = [e], mac_bar = [f], bar = [g] }
       becomes {foo = [a,b,e], bar = [g]} on windows, and
       {foo = [e], bar = [f,g]} on mac

  Args:
    env: The hammer environment which knows which platforms are active
    params: The keyword argument dictionary.
  Returns:
    A new dictionary with the filtered and combined entries of params
  """
  platforms = {
    'linux': 'lin_',
    'mac': 'mac_',
    'posix': 'posix_',
    'windows': 'win_',
  }
  active_prefixes = [
    platforms[x] for x in iter(platforms) if env.Bit(x)
  ]
  inactive_prefixes = [
    platforms[x] for x in iter(platforms) if not env.Bit(x)
  ]

  merged = {}
  for arg, values in params.iteritems():
    inactive_platform = False

    key = arg

    for prefix in active_prefixes:
      if arg.startswith(prefix):
        key = arg[len(prefix):]

    for prefix in inactive_prefixes:
      if arg.startswith(prefix):
        inactive_platform = True

    if inactive_platform:
      continue

    AddToDict(merged, key, values)

  return merged


def ExtendComponent(env, component, **kwargs):
  # get our target identifier
  name = GetEntry(kwargs, 'name')
  log_env = GetEntry(kwargs, 'dump')

  if (kwargs.has_key('include_talk_media_libs') and
      kwargs['include_talk_media_libs']):
    kwargs = AddMediaLibs(env, **kwargs)

  # prune parameters for inactive platforms or modes
  # and combine the rest of the platforms
  params = MergeAndFilterByPlatform(env, kwargs)

  # apply any explicit dependencies
  Depends(env, name, kwargs)

  AddToDict(params, 'CPPDEFINES', env.Dictionary('CPPDEFINES'), False)
  AddToDict(params, 'CPPPATH', env.Dictionary('CPPPATH'), False)
  AddToDict(params, 'CCFLAGS', env.Dictionary('CCFLAGS'), False)
  AddToDict(params, 'LIBPATH', env.Dictionary('LIBPATH'), False)
  AddToDict(params, 'LINKFLAGS', env.Dictionary('LINKFLAGS'), False)
  if env.Bit('mac'):
    AddToDict(params, 'FRAMEWORKS', env.Dictionary('FRAMEWORKS'), False)

  RenameKey(params, 'cppdefines', 'CPPDEFINES')
  if params.has_key('prepend_includedirs'):
    RenameKey(params, 'includedirs', 'CPPPATH', False)
  else:
    RenameKey(params, 'includedirs', 'CPPPATH')
  RenameKey(params, 'ccflags', 'CCFLAGS', False)
  RenameKey(params, 'libdirs', 'LIBPATH')
  RenameKey(params, 'link_flags', 'LINKFLAGS')
  RenameKey(params, 'libs', 'LIBS')

  srcs = GetEntry(params, 'srcs')
  if srcs is None or len(srcs) == 0:
    return None

  # invoke the builder function
  return component(name, srcs, **params)


def AddToDict(dictionary, key, values, append=True):
  """Merge the given key value(s) pair into a dictionary.  If it contains an
     entry with that key already, then combine by appending or prepending the
     values as directed.  Otherwise, assign a new keyvalue pair.
  """
  if values is None:
    return

  if not dictionary.has_key(key):
    dictionary[key] = values
    return

  cur = dictionary[key]
  # TODO(dape): Make sure that there are no duplicates
  # in the list. I can't use python set for this since
  # the nodes that are returned by the SCONS builders
  # are not hashable.
  # dictionary[key] = list(set(cur).union(set(values)))
  if append:
    dictionary[key] = cur + values
  else:
    dictionary[key] = values + cur


def CombineDicts(a, b):
  """Unions two dictionaries by combining values of keys shared between them.
  """
  c = {}
  for key in a:
    if b.has_key(key):
      c[key] = a[key] + b.pop(key)
    else:
      c[key] = a[key]

  for key in b:
    c[key] = b[key]

  return c


def RenameKey(d, old, new, append=True):
  AddToDict(d, new, GetEntry(d, old), append)
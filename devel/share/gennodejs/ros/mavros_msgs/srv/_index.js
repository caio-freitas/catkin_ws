
"use strict";

let FileClose = require('./FileClose.js')
let FileList = require('./FileList.js')
let CommandHome = require('./CommandHome.js')
let WaypointPush = require('./WaypointPush.js')
let FileRemoveDir = require('./FileRemoveDir.js')
let CommandTriggerControl = require('./CommandTriggerControl.js')
let WaypointClear = require('./WaypointClear.js')
let ParamPush = require('./ParamPush.js')
let SetMode = require('./SetMode.js')
let CommandBool = require('./CommandBool.js')
let FileTruncate = require('./FileTruncate.js')
let WaypointPull = require('./WaypointPull.js')
let CommandInt = require('./CommandInt.js')
let FileChecksum = require('./FileChecksum.js')
let CommandTOL = require('./CommandTOL.js')
let WaypointSetCurrent = require('./WaypointSetCurrent.js')
let FileRename = require('./FileRename.js')
let CommandLong = require('./CommandLong.js')
let StreamRate = require('./StreamRate.js')
let FileRead = require('./FileRead.js')
let FileRemove = require('./FileRemove.js')
let ParamSet = require('./ParamSet.js')
let ParamPull = require('./ParamPull.js')
let FileWrite = require('./FileWrite.js')
let FileMakeDir = require('./FileMakeDir.js')
let FileOpen = require('./FileOpen.js')
let SetMavFrame = require('./SetMavFrame.js')
let ParamGet = require('./ParamGet.js')

module.exports = {
  FileClose: FileClose,
  FileList: FileList,
  CommandHome: CommandHome,
  WaypointPush: WaypointPush,
  FileRemoveDir: FileRemoveDir,
  CommandTriggerControl: CommandTriggerControl,
  WaypointClear: WaypointClear,
  ParamPush: ParamPush,
  SetMode: SetMode,
  CommandBool: CommandBool,
  FileTruncate: FileTruncate,
  WaypointPull: WaypointPull,
  CommandInt: CommandInt,
  FileChecksum: FileChecksum,
  CommandTOL: CommandTOL,
  WaypointSetCurrent: WaypointSetCurrent,
  FileRename: FileRename,
  CommandLong: CommandLong,
  StreamRate: StreamRate,
  FileRead: FileRead,
  FileRemove: FileRemove,
  ParamSet: ParamSet,
  ParamPull: ParamPull,
  FileWrite: FileWrite,
  FileMakeDir: FileMakeDir,
  FileOpen: FileOpen,
  SetMavFrame: SetMavFrame,
  ParamGet: ParamGet,
};


"use strict";

let FileRename = require('./FileRename.js')
let FileRemove = require('./FileRemove.js')
let FileRemoveDir = require('./FileRemoveDir.js')
let CommandHome = require('./CommandHome.js')
let FileClose = require('./FileClose.js')
let FileWrite = require('./FileWrite.js')
let SetMavFrame = require('./SetMavFrame.js')
let StreamRate = require('./StreamRate.js')
let WaypointClear = require('./WaypointClear.js')
let ParamGet = require('./ParamGet.js')
let WaypointSetCurrent = require('./WaypointSetCurrent.js')
let ParamSet = require('./ParamSet.js')
let FileChecksum = require('./FileChecksum.js')
let FileList = require('./FileList.js')
let FileOpen = require('./FileOpen.js')
let SetMode = require('./SetMode.js')
let WaypointPush = require('./WaypointPush.js')
let FileMakeDir = require('./FileMakeDir.js')
let CommandInt = require('./CommandInt.js')
let ParamPull = require('./ParamPull.js')
let CommandLong = require('./CommandLong.js')
let FileTruncate = require('./FileTruncate.js')
let WaypointPull = require('./WaypointPull.js')
let CommandBool = require('./CommandBool.js')
let FileRead = require('./FileRead.js')
let ParamPush = require('./ParamPush.js')
let CommandTOL = require('./CommandTOL.js')
let CommandTriggerControl = require('./CommandTriggerControl.js')

module.exports = {
  FileRename: FileRename,
  FileRemove: FileRemove,
  FileRemoveDir: FileRemoveDir,
  CommandHome: CommandHome,
  FileClose: FileClose,
  FileWrite: FileWrite,
  SetMavFrame: SetMavFrame,
  StreamRate: StreamRate,
  WaypointClear: WaypointClear,
  ParamGet: ParamGet,
  WaypointSetCurrent: WaypointSetCurrent,
  ParamSet: ParamSet,
  FileChecksum: FileChecksum,
  FileList: FileList,
  FileOpen: FileOpen,
  SetMode: SetMode,
  WaypointPush: WaypointPush,
  FileMakeDir: FileMakeDir,
  CommandInt: CommandInt,
  ParamPull: ParamPull,
  CommandLong: CommandLong,
  FileTruncate: FileTruncate,
  WaypointPull: WaypointPull,
  CommandBool: CommandBool,
  FileRead: FileRead,
  ParamPush: ParamPush,
  CommandTOL: CommandTOL,
  CommandTriggerControl: CommandTriggerControl,
};

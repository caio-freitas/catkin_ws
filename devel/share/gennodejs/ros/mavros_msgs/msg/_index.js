
"use strict";

let PositionTarget = require('./PositionTarget.js');
let Vibration = require('./Vibration.js');
let ParamValue = require('./ParamValue.js');
let CommandCode = require('./CommandCode.js');
let RCOut = require('./RCOut.js');
let HilGPS = require('./HilGPS.js');
let DebugValue = require('./DebugValue.js');
let OpticalFlowRad = require('./OpticalFlowRad.js');
let WaypointList = require('./WaypointList.js');
let Waypoint = require('./Waypoint.js');
let HilStateQuaternion = require('./HilStateQuaternion.js');
let Thrust = require('./Thrust.js');
let ExtendedState = require('./ExtendedState.js');
let WaypointReached = require('./WaypointReached.js');
let ActuatorControl = require('./ActuatorControl.js');
let CamIMUStamp = require('./CamIMUStamp.js');
let GlobalPositionTarget = require('./GlobalPositionTarget.js');
let BatteryStatus = require('./BatteryStatus.js');
let Altitude = require('./Altitude.js');
let FileEntry = require('./FileEntry.js');
let HilControls = require('./HilControls.js');
let RadioStatus = require('./RadioStatus.js');
let State = require('./State.js');
let HilSensor = require('./HilSensor.js');
let ManualControl = require('./ManualControl.js');
let Mavlink = require('./Mavlink.js');
let OverrideRCIn = require('./OverrideRCIn.js');
let HilActuatorControls = require('./HilActuatorControls.js');
let HomePosition = require('./HomePosition.js');
let AttitudeTarget = require('./AttitudeTarget.js');
let RCIn = require('./RCIn.js');
let VFR_HUD = require('./VFR_HUD.js');
let ADSBVehicle = require('./ADSBVehicle.js');

module.exports = {
  PositionTarget: PositionTarget,
  Vibration: Vibration,
  ParamValue: ParamValue,
  CommandCode: CommandCode,
  RCOut: RCOut,
  HilGPS: HilGPS,
  DebugValue: DebugValue,
  OpticalFlowRad: OpticalFlowRad,
  WaypointList: WaypointList,
  Waypoint: Waypoint,
  HilStateQuaternion: HilStateQuaternion,
  Thrust: Thrust,
  ExtendedState: ExtendedState,
  WaypointReached: WaypointReached,
  ActuatorControl: ActuatorControl,
  CamIMUStamp: CamIMUStamp,
  GlobalPositionTarget: GlobalPositionTarget,
  BatteryStatus: BatteryStatus,
  Altitude: Altitude,
  FileEntry: FileEntry,
  HilControls: HilControls,
  RadioStatus: RadioStatus,
  State: State,
  HilSensor: HilSensor,
  ManualControl: ManualControl,
  Mavlink: Mavlink,
  OverrideRCIn: OverrideRCIn,
  HilActuatorControls: HilActuatorControls,
  HomePosition: HomePosition,
  AttitudeTarget: AttitudeTarget,
  RCIn: RCIn,
  VFR_HUD: VFR_HUD,
  ADSBVehicle: ADSBVehicle,
};

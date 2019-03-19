
"use strict";

let ActuatorControl = require('./ActuatorControl.js');
let CommandCode = require('./CommandCode.js');
let WaypointList = require('./WaypointList.js');
let Mavlink = require('./Mavlink.js');
let OverrideRCIn = require('./OverrideRCIn.js');
let VFR_HUD = require('./VFR_HUD.js');
let FileEntry = require('./FileEntry.js');
let OpticalFlowRad = require('./OpticalFlowRad.js');
let State = require('./State.js');
let HilSensor = require('./HilSensor.js');
let WaypointReached = require('./WaypointReached.js');
let DebugValue = require('./DebugValue.js');
let HilGPS = require('./HilGPS.js');
let ManualControl = require('./ManualControl.js');
let RCIn = require('./RCIn.js');
let RadioStatus = require('./RadioStatus.js');
let RCOut = require('./RCOut.js');
let ADSBVehicle = require('./ADSBVehicle.js');
let Thrust = require('./Thrust.js');
let CamIMUStamp = require('./CamIMUStamp.js');
let BatteryStatus = require('./BatteryStatus.js');
let GlobalPositionTarget = require('./GlobalPositionTarget.js');
let HilControls = require('./HilControls.js');
let ExtendedState = require('./ExtendedState.js');
let PositionTarget = require('./PositionTarget.js');
let AttitudeTarget = require('./AttitudeTarget.js');
let Vibration = require('./Vibration.js');
let Altitude = require('./Altitude.js');
let HilStateQuaternion = require('./HilStateQuaternion.js');
let HomePosition = require('./HomePosition.js');
let Waypoint = require('./Waypoint.js');
let HilActuatorControls = require('./HilActuatorControls.js');
let ParamValue = require('./ParamValue.js');

module.exports = {
  ActuatorControl: ActuatorControl,
  CommandCode: CommandCode,
  WaypointList: WaypointList,
  Mavlink: Mavlink,
  OverrideRCIn: OverrideRCIn,
  VFR_HUD: VFR_HUD,
  FileEntry: FileEntry,
  OpticalFlowRad: OpticalFlowRad,
  State: State,
  HilSensor: HilSensor,
  WaypointReached: WaypointReached,
  DebugValue: DebugValue,
  HilGPS: HilGPS,
  ManualControl: ManualControl,
  RCIn: RCIn,
  RadioStatus: RadioStatus,
  RCOut: RCOut,
  ADSBVehicle: ADSBVehicle,
  Thrust: Thrust,
  CamIMUStamp: CamIMUStamp,
  BatteryStatus: BatteryStatus,
  GlobalPositionTarget: GlobalPositionTarget,
  HilControls: HilControls,
  ExtendedState: ExtendedState,
  PositionTarget: PositionTarget,
  AttitudeTarget: AttitudeTarget,
  Vibration: Vibration,
  Altitude: Altitude,
  HilStateQuaternion: HilStateQuaternion,
  HomePosition: HomePosition,
  Waypoint: Waypoint,
  HilActuatorControls: HilActuatorControls,
  ParamValue: ParamValue,
};

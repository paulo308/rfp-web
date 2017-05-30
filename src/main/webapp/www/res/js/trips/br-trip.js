if( typeof exports !== 'undefined' ) {
  if( typeof module !== 'undefined' && module.exports ) {
    console.log("BR Trip nodeJs");
    module.exports = RFPWBRTrip;
    var RFPWBRTripSegment = require("./br-trip-segment");
  }
}
/**
 * A trip between two points as generated by the best recommender service. The
 * trip is self sufficient and can be drawn on the map. It contains one or more
 * segments that represent its parts.
 */
function RFPWBRTrip(brTripInstance)
{
  this.uid = brTripInstance.uid;
  this.errorMsg = brTripInstance.errorMsg;
  this.segments = [];
  if (brTripInstance.segments !== null && brTripInstance.segments !== undefined)
  {
    for (var idx=0; idx<brTripInstance.segments.length; ++idx)
      this.segments.push(new RFPWBRTripSegment(brTripInstance.segments[idx]));
  }
  this.totalTime = brTripInstance.totalTime;
}

RFPWBRTrip.prototype.getUid = function() {return this.uid;}
RFPWBRTrip.prototype.setUid = function(uid) {this.uid = uid;}

RFPWBRTrip.prototype.isSuccess = function() {return this.errorMsg === null;}
RFPWBRTrip.prototype.getErrorMsg = function() {return this.errorMsg;}
RFPWBRTrip.prototype.getSegments = function() {return this.segments;}
RFPWBRTrip.prototype.getTotalTime = function() {return this.totalTimes;}
package main
//this code is to be installed in the virtual machine side (host)
import (
	"flag"
	"fmt"  //import fmt for printing
	"log"
  "os"  //importing log for logging out errors
	"encoding/csv"//"math/rand" //importing for computing mathematical computations
	"time"
	//"strconv"
  //"encoding/binary"
	"encoding/json"
	//"strings"
//	"net/http"
	"github.com/influxdata/influxdb1-client/v2"
	"github.com/scionproto/scion/go/lib/snet" //importing snet packages
	"github.com/scionproto/scion/go/lib/sciond" //importing sciond packages
)

type Message struct {
  Date string
  //Time string
  Time time.Time
  Body string
  Motion int
  Interval string
	Personcontact int
	ArrayTiming[] string
}

var (

 saddr string   //Intialising local variables
 ef error
 ser *snet.Addr
 scionconnection snet.Conn


)

const (
	// MyDB specifies name of database
	MyDB = "motiontimings6"
)

var Recmes Message

func logerror(ef error) {   //func which will be caused frequently to log out errors

if ef!=nil{

log.Println(ef)
}
}




func main() {



  flag.StringVar(&saddr, "s", "", "server addr")  // flag used to fetch value from command line
  flag.Parse()



  ser, ef = snet.AddrFromString(saddr)      // AddrFromString converts an address string of format isd-as,[ipaddr]:port
  logerror(ef)


  dpath := "/run/shm/dispatcher/default.sock"
 	snet.Init(ser.IA, sciond.GetDefaultSCIONDPath(nil), dpath)  //Init initializes the default SCION networking context.


   scionconnection, ef = snet.ListenSCION("udp4", ser) //  ListenSCION registers laddr with the dispatcher. Nil values for laddr are
                                                           // not supported yet. The returned connection's ReadFrom and WriteTo methods
                                                           // can be used to receive and send SCION packets with per-packet addressing.
                                                           // Parameter network must be "udp4".
   logerror(ef)











	//tags := map[string]string{"productView": productMeasurement["ProductName"].(string)}





	 receivePacketBuffer := make([]byte, 2500) //Intiating a dynamic array of respective size
   //sendPacketBuffer := make([]byte, 2500)
   file, ef := os.OpenFile("sensor_motion_new_values.csv", os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0644)
   logerror(ef)
   writer := csv.NewWriter(file)
   //n, ef := scionconnection.Write(sendPacketBuffer) //send response to serber
	 //logerror(ef)
  for{

		c, err := client.NewHTTPClient(client.HTTPConfig{
 		Addr: "http://localhost:8086",
 	 })
 	if err != nil {
 	 fmt.Println("Error creating InfluxDB Client: ", err.Error())
    }
    defer c.Close()




 	 bp, err := client.NewBatchPoints(client.BatchPointsConfig{
  		Database:  MyDB,
  		Precision: "s",
  	})
  	if err != nil {
  		log.Fatal(err)
  	}


	  n, _, ef := scionconnection.ReadFrom(receivePacketBuffer)  //reading response from server
			 logerror(ef)

			 ef = json.Unmarshal(receivePacketBuffer[:n], &Recmes)
			 logerror(ef)
       writer.Write([]string{string(receivePacketBuffer)})
      //var data = [][]string{{Recmes.Date,Recmes.Time,strconv.Itoa(Recmes.Motion)}}
    //  writer.Write(data)



		tags := map[string]string{"Receivedmotiontime": Recmes.Interval,"Receiveddate" : Recmes.Date}
		fields := map[string]interface{}{
							"Motion":  Recmes.Motion,
              "Receivedtime":Recmes.Time,
							"MotionTimeArray":Recmes.ArrayTiming,

					}

		//pt, err := client.NewPoint("sensormotion", tags, fields, time.Now())
    pt, err := client.NewPoint("sensormotion", tags, fields, Recmes.Time)
		if err != nil {
			log.Fatal(err)
		}
		bp.AddPoint(pt)

		// Write the batch
		if err := c.Write(bp); err != nil {
			log.Fatal(err)
		}

		// Close client resources
		if err := c.Close(); err != nil {
			log.Fatal(err)
		}

    //writer.Write([]string{string(receivePacketBuffer)})
    fmt.Print(string(receivePacketBuffer[:n]))

 }

}

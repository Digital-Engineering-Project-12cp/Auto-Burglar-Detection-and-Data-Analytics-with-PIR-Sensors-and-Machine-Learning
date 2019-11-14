package main
//this code is to be installed in the client side which is our raspberry
import (
	"flag"
	"fmt"  //import fmt for printing
	"log"  //importing log for logging out errors
	//"math/rand" //importing for computing mathematical computations
	"time"
	"encoding/json"
	//"strconv"
  //"encoding/binary"
  "github.com/stianeikeland/go-rpio"
	"github.com/scionproto/scion/go/lib/snet" //importing snet packages
	"github.com/scionproto/scion/go/lib/sciond" //importing sciond packages
	"github.com/influxdata/influxdb1-client/v2"
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

func logerror(ef error){    //func which will be caused frequently to log out errors

if ef!=nil{
 log.Println(ef)
}
}

var personpresence[] int


const (
	// MyDB specifies name of database
	MyDB = "motiontimings5"
)

func main(){

  var (

  	clientAddress string
    serverAddress string
    ef error
   client_local *snet.Addr
   server_destination *snet.Addr
   scionconnection snet.Conn
  )

  var sendData Message



  flag.StringVar(&clientAddress, "c", "", "Client SCION AS address")
  flag.StringVar(&serverAddress, "s", "", "Server SCION AS Address")
  flag.Parse()


  client_local, ef = snet.AddrFromString(clientAddress)
  logerror(ef)
  server_destination, ef = snet.AddrFromString(serverAddress)
  logerror(ef)



  dpath := "/run/shm/dispatcher/default.sock"
  snet.Init(client_local.IA, sciond.GetDefaultSCIONDPath(nil), dpath)

  scionconnection, ef = snet.DialSCION("udp4", client_local, server_destination)
  logerror(ef)


//  receivePacketBuffer := make([]byte, 2500) //Intiating a dynamic array of respective size
  sendPacketBuffer := make([]byte, 2500)

  err := rpio.Open();
  if(err!=nil){
  fmt.Println("Unable to open GPIO",err.Error())
}

Personsensorvalue := rpio.Pin(16)
Inputsensorvalue := rpio.Pin(23)
Outputled := rpio.Pin(24)
//PersonOutputled := rpio.Pin(20)



Personsensorvalue.Input()
Inputsensorvalue.Input()

Outputled.Output()
//PersonOutputled.Output()


//PersonOutputled.Low()
Outputled.Low()

for{
  //b, clientAddr, ef := scionconnection.ReadFrom(receivePacketBuffer)
   time_previous := time.Now()
   time_catch :=  time_previous.Add(time.Minute*1)
	 fmt.Println(time_catch.Format("15:04:05"))
	 i:=0
	 q:=1
   z:=0
	 totalaverage:=0

	 for time.Now().Before(time_catch){

		if(Inputsensorvalue.Read()==1){
		 Outputled.High()
   	i++
		if(Personsensorvalue.Read()==1){
		//	PersonOutputled.High()
		  personpresence = append(personpresence,1)
	  	//PersonOutputled.Low()
	  }else {
		//	PersonOutputled.Low()
		  personpresence = append(personpresence,0)
	  }

		c, err := client.NewHTTPClient(client.HTTPConfig{
		 Addr: "http://192.168.0.102:8086",
		})
	 if err != nil {
		fmt.Println("Error creating InfluxDB Client: ", err.Error())
		}
		defer c.Close()


   sendData.ArrayTiming = append(sendData.ArrayTiming, time.Now().Format("15:04:05"))

		bp, err := client.NewBatchPoints(client.BatchPointsConfig{
		 Database:  MyDB,
		 Precision: "s",
	 })
	 if err != nil {
		 log.Fatal(err)
	 }


	 tags := map[string]string{"Receiveddate" : time.Now().Format("01-02-2006")}
	 fields := map[string]interface{}{
						 "Motion":  "Motion detected",
						 "Receivedtime":time.Now(),
						 "Motionvalue":  q,

				 }

	 //pt, err := client.NewPoint("sensormotion", tags, fields, time.Now())
	 pt, err := client.NewPoint("sensormotion", tags, fields, time.Now())
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


 		Outputled.Low()
		time.Sleep(time.Second * 1)
	}else {
		c, err := client.NewHTTPClient(client.HTTPConfig{
	   Addr: "http://192.168.0.102:8086",
	  })
	  if err != nil {
	  fmt.Println("Error creating InfluxDB Client: ", err.Error())
	  }
	  defer c.Close()

		if(Personsensorvalue.Read()==1){
		//	PersonOutputled.High()
 	    personpresence = append(personpresence,1)
 		 //PersonOutputled.Low()
 	  }else {
		//	PersonOutputled.Low()
 		  personpresence = append(personpresence,0)
 	  }


	  bp, err := client.NewBatchPoints(client.BatchPointsConfig{
	   Database:  MyDB,
	   Precision: "s",
	  })
	  if err != nil {
	   log.Fatal(err)
	  }


	  tags := map[string]string{"Receiveddate" : time.Now().Format("01-02-2006")}
	  fields := map[string]interface{}{
	           "Motion":  "Motion not detected",
	           "Receivedtime":time.Now(),
	           "Motionvalue":  z,

	       }

	  //pt, err := client.NewPoint("sensormotion", tags, fields, time.Now())
	  pt, err := client.NewPoint("sensormotion", tags, fields, time.Now())
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




	}
	 }

		//var final_value string = time_catch.Format("01-02-2006") + "|" + time_catch.Format("15:04:05")+"|"+strconv.Itoa(i)
   sendData.Date = time_catch.Format("01-02-2006")
	// sendData.Time = time_catch.Format("15:04:05")
   sendData.Time = time_catch
	 sendData.Body = "Motion detected"
	 sendData.Motion = i
   sendData.Interval = time_previous.Format("15:04:05") + "-" + time_catch.Format("15:04:05")
	 for _, number := range personpresence {
  totalaverage = totalaverage + number
   }
    superaverage := (float64(totalaverage) / float64(len(personpresence)))
		truncatedsuperaverage := float64(int(superaverage * 100)) / 100

	 if (truncatedsuperaverage > float64(0.5)){
		 sendData.Personcontact = 1
	 }else{
		 sendData.Personcontact = 0
	 }


	 b, _ := json.Marshal(sendData)

		//fmt.Println(final_value)
		fmt.Println(string(b))
		//copy(sendPacketBuffer, final_value)
		copy(sendPacketBuffer, b)
		_, ef = scionconnection.Write(sendPacketBuffer[: len(b)])
		sendData.ArrayTiming = nil
		personpresence = nil
		superaverage = 0.0
		 logerror(ef)
		 time.Sleep(time.Second * 1)



















	 }

   //var sensorValues string = "Motion detected"
	 //time_recivd := time.Now()
	 //var final_value string = sensorValues + "|" + time_recivd.Format("15:04:05")
  //fmt.Println(final_value )
	//var final_value string = sensorValues + "|" + time_recivd.Format("15:04:05")

        //sending back the response to client
     //  _, ef = scionconnection.WriteTo(sendPacketBuffer[: sensorValues], clientAddr)



   //time.Sleep(time.Second * 0.5)



defer rpio.Close()



}

// Present a "Will be back soon web page", as stand-in webserver.
// 2011-01-30 <jc@wippler.nl>
//
// License: GPLv2

#include <EtherCard.h>
#include <dht11.h>
#define DHT11PIN 4
dht11 DHT11;

#define STATIC 1  // set to 1 to disable DHCP (adjust myip/gwip values below)

#if STATIC
// ethernet interface ip address
static byte myip[] = { 10,0,0,200 };
// gateway ip address
static byte gwip[] = { 10,0,0,1 };
#endif

// ethernet mac address - must be unique on your network
static byte mymac[] = { 0x74,0x69,0x69,0x2D,0x30,0x31 };

byte Ethernet::buffer[500]; // tcp/ip send and receive buffer

void setup(){
  Serial.begin(57600);
  Serial.println("\n[backSoon]");

  // Change 'SS' to your Slave Select pin, if you arn't using the default pin
  if (ether.begin(sizeof Ethernet::buffer, mymac, SS) == 0)
    Serial.println( "Failed to access Ethernet controller");
#if STATIC
  ether.staticSetup(myip, gwip);
#else
  if (!ether.dhcpSetup())
    Serial.println("DHCP failed");
#endif

  ether.printIp("IP:  ", ether.myip);
  ether.printIp("GW:  ", ether.gwip);
  ether.printIp("DNS: ", ether.dnsip);
}

void loop(){
  // wait for an incoming TCP packet, but ignore its contents
  if (ether.packetLoop(ether.packetReceive())) {
    int chk = DHT11.read(DHT11PIN);
    Serial.print("Humidity (%): ");
    Serial.println(DHT11.humidity, 2);
    Serial.print("Temperature (C): ");
    Serial.println(DHT11.temperature, 2);
    
    BufferFiller bfill;
    bfill = ether.tcpOffset();
    bfill.emit_p(PSTR(
    "HTTP/1.0 200 OK\r\n"
    "Content-Type: application/json\r\n"
    "Pragma: no-cache\r\n"
    "\r\n"
    "{\"Temperature\" : $D, \"Humidity\" : $D}"
    
   ), DHT11.temperature, DHT11.humidity);
     
    ether.httpServerReply(bfill.position());
  }
}
